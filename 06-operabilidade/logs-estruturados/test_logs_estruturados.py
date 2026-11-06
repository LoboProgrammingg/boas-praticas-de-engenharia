import io
import json
import logging
from collections.abc import Iterator

import pytest

from conftest import CarregarExemplo


@pytest.fixture
def saida() -> Iterator[io.StringIO]:
    buffer = io.StringIO()
    log = logging.getLogger("teste.logs")
    manipulador = logging.StreamHandler(buffer)
    log.addHandler(manipulador)
    log.setLevel(logging.INFO)
    log.propagate = False
    yield buffer
    log.removeHandler(manipulador)


@pytest.fixture
def log(saida: io.StringIO) -> logging.Logger:
    return logging.getLogger("teste.logs")


def test_ruim_vaza_o_cpf_e_nao_e_json(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    buffer = io.StringIO()
    manipulador = logging.StreamHandler(buffer)
    ruim.log.addHandler(manipulador)
    ruim.log.propagate = False
    try:
        ruim.registrar_falha_de_pagamento("123.456.789-09", "p1", "timeout")
    finally:
        ruim.log.removeHandler(manipulador)

    linha = buffer.getvalue()
    assert "123.456.789-09" in linha
    with pytest.raises(json.JSONDecodeError):
        json.loads(linha)


def test_bom_um_evento_e_uma_linha_json_com_campos_pesquisaveis(
    exemplo: CarregarExemplo, log: logging.Logger, saida: io.StringIO
) -> None:
    bom = exemplo("bom.py")
    log.handlers[0].setFormatter(bom.FormatadorJson())

    bom.registrar_falha_de_pagamento(log, "p1", "timeout")

    linhas = saida.getvalue().splitlines()
    assert len(linhas) == 1
    evento = json.loads(linhas[0])
    assert evento["event"] == "payment_failed"
    assert evento["level"] == "ERROR"
    assert (evento["pedido_id"], evento["motivo"]) == ("p1", "timeout")
    assert evento["timestamp"].endswith("+00:00")


def test_bom_a_mensagem_e_estavel_entre_ocorrencias(
    exemplo: CarregarExemplo, log: logging.Logger, saida: io.StringIO
) -> None:
    bom = exemplo("bom.py")
    log.handlers[0].setFormatter(bom.FormatadorJson())

    bom.registrar_falha_de_pagamento(log, "p1", "timeout")
    bom.registrar_falha_de_pagamento(log, "p2", "recusado")

    eventos = [json.loads(linha) for linha in saida.getvalue().splitlines()]
    assert {evento["event"] for evento in eventos} == {"payment_failed"}


def test_bom_chaves_sensiveis_sao_mascaradas(
    exemplo: CarregarExemplo, log: logging.Logger, saida: io.StringIO
) -> None:
    bom = exemplo("bom.py")
    log.handlers[0].setFormatter(bom.FormatadorJson())

    log.info("login", extra={"contexto": {"cpf": "123.456.789-09", "token": "abc", "ok": True}})

    evento = json.loads(saida.getvalue())
    assert evento["cpf"] == evento["token"] == "[REDACTED]"
    assert evento["ok"] is True
    assert "123.456.789-09" not in saida.getvalue()


def test_bom_contexto_nao_sobrescreve_os_campos_reservados(
    exemplo: CarregarExemplo, log: logging.Logger, saida: io.StringIO
) -> None:
    bom = exemplo("bom.py")
    log.handlers[0].setFormatter(bom.FormatadorJson())

    log.info("evento_real", extra={"contexto": {"event": "forjado", "level": "DEBUG"}})

    evento = json.loads(saida.getvalue())
    assert (evento["event"], evento["level"]) == ("evento_real", "INFO")


def test_bom_excecao_vai_em_campo_proprio_e_continua_uma_linha(
    exemplo: CarregarExemplo, log: logging.Logger, saida: io.StringIO
) -> None:
    bom = exemplo("bom.py")
    log.handlers[0].setFormatter(bom.FormatadorJson())

    try:
        raise ValueError("boom")
    except ValueError:
        log.exception("job_failed")

    assert len(saida.getvalue().splitlines()) == 1
    assert "ValueError: boom" in json.loads(saida.getvalue())["exc"]
