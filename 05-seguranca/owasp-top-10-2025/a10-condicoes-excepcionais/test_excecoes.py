import logging
import sqlite3
from collections.abc import Iterator

import pytest

from conftest import CarregarExemplo

SEGREDO_INTERNO = "connection to db-interno:5432 failed"


def _verificacao_quebrada() -> bool:
    raise RuntimeError("serviço de políticas indisponível")


@pytest.fixture
def conexao() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE contas (id INTEGER PRIMARY KEY, saldo INTEGER NOT NULL)")
    conexao.executemany("INSERT INTO contas VALUES (?, ?)", [(1, 100), (2, 0)])
    conexao.commit()
    yield conexao
    conexao.close()


def _saldo(conexao: sqlite3.Connection, conta: int) -> int:
    return int(conexao.execute("SELECT saldo FROM contas WHERE id = ?", (conta,)).fetchone()[0])


def test_vulneravel_devolve_a_mensagem_interna_ao_cliente(exemplo: CarregarExemplo) -> None:
    vulneravel = exemplo("vulneravel.py")

    _, corpo = vulneravel.responder_erro(RuntimeError(SEGREDO_INTERNO))

    assert SEGREDO_INTERNO in corpo["detail"]


def test_seguro_responde_generico_e_registra_o_detalhe_com_o_mesmo_error_id(
    exemplo: CarregarExemplo, caplog: pytest.LogCaptureFixture
) -> None:
    seguro = exemplo("seguro.py")

    with caplog.at_level(logging.ERROR, logger="app"):
        status, corpo = seguro.responder_erro(RuntimeError(SEGREDO_INTERNO))

    assert status == 500
    assert SEGREDO_INTERNO not in str(corpo)
    assert corpo["detail"] == "internal error"
    registro = caplog.records[0]
    assert registro.error_id == corpo["error_id"]  # type: ignore[attr-defined]
    assert registro.exc_info is not None
    assert SEGREDO_INTERNO in str(registro.exc_info[1])


def test_vulneravel_libera_o_acesso_quando_a_checagem_quebra(
    exemplo: CarregarExemplo,
) -> None:
    vulneravel = exemplo("vulneravel.py")

    assert vulneravel.esta_autorizado(_verificacao_quebrada) is True


def test_seguro_nega_o_acesso_quando_a_checagem_quebra(
    exemplo: CarregarExemplo, caplog: pytest.LogCaptureFixture
) -> None:
    seguro = exemplo("seguro.py")

    with caplog.at_level(logging.ERROR, logger="app"):
        assert seguro.esta_autorizado(_verificacao_quebrada) is False

    assert "acesso negado" in caplog.text


def test_seguro_so_autoriza_quando_a_checagem_devolve_true(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.esta_autorizado(lambda: True) is True
    assert seguro.esta_autorizado(lambda: False) is False


def test_vulneravel_perde_dinheiro_quando_o_credito_falha(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    vulneravel = exemplo("vulneravel.py")

    with pytest.raises(LookupError):
        vulneravel.transferir(conexao, 1, 999, 40)

    assert _saldo(conexao, 1) == 60


def test_seguro_desfaz_o_debito_quando_o_credito_falha(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(LookupError):
        seguro.transferir(conexao, 1, 999, 40)

    assert _saldo(conexao, 1) == 100


def test_seguro_confirma_as_duas_pontas_quando_tudo_da_certo(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")

    seguro.transferir(conexao, 1, 2, 40)

    assert (_saldo(conexao, 1), _saldo(conexao, 2)) == (60, 40)
