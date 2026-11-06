import io
import logging
from collections.abc import Iterator

import pytest

from conftest import CarregarExemplo

CPF = "000.000.000-00"
EMAIL = "ana@exemplo.test"
SENHA = "senha-de-teste"


@pytest.fixture
def saida() -> Iterator[io.StringIO]:
    buffer = io.StringIO()
    yield buffer
    buffer.close()


def _montar_logger(saida: io.StringIO, filtro: logging.Filter | None) -> Iterator[logging.Logger]:
    log = logging.getLogger(f"lgpd.teste.{id(saida)}")
    handler = logging.StreamHandler(saida)
    if filtro is not None:
        handler.addFilter(filtro)
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False
    yield log
    log.removeHandler(handler)
    handler.close()


@pytest.fixture
def log(saida: io.StringIO) -> Iterator[logging.Logger]:
    yield from _montar_logger(saida, None)


@pytest.fixture
def log_com_filtro(saida: io.StringIO, exemplo: CarregarExemplo) -> Iterator[logging.Logger]:
    yield from _montar_logger(saida, exemplo("seguro.py").FiltroSemPii())


def test_vulneravel_grava_cpf_email_e_senha_no_log(
    exemplo: CarregarExemplo, log: logging.Logger, saida: io.StringIO
) -> None:
    vulneravel = exemplo("vulneravel.py")

    vulneravel.registrar_login(log, EMAIL, CPF, SENHA)

    gravado = saida.getvalue()
    assert CPF in gravado
    assert EMAIL in gravado
    assert SENHA in gravado


def test_seguro_registra_apenas_identificadores_internos(
    exemplo: CarregarExemplo, log: logging.Logger, saida: io.StringIO
) -> None:
    seguro = exemplo("seguro.py")

    seguro.registrar_login(log, "7f3c", "req-42")

    assert saida.getvalue().strip() == "login_succeeded user_id=7f3c request_id=req-42"


def test_filtro_redige_dado_pessoal_que_escapou_para_a_mensagem(
    log_com_filtro: logging.Logger, saida: io.StringIO
) -> None:
    log_com_filtro.info("falha para %s cpf=%s senha=%s", EMAIL, CPF, SENHA)

    gravado = saida.getvalue()
    assert CPF not in gravado
    assert EMAIL not in gravado
    assert SENHA not in gravado
    assert "[CPF]" in gravado
    assert "[EMAIL]" in gravado


@pytest.mark.parametrize("cpf", ["000.000.000-00", "00000000000", "000.000.00000"])
def test_redigir_texto_cobre_formatos_comuns_de_cpf(exemplo: CarregarExemplo, cpf: str) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.redigir_texto(f"cliente {cpf} ligou") == "cliente [CPF] ligou"


def test_redigir_texto_preserva_mensagens_sem_dado_pessoal(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.redigir_texto("pedido 123 criado") == "pedido 123 criado"
