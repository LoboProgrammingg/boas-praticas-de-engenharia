import sqlite3
from collections.abc import Iterator
from decimal import Decimal

import pytest

from conftest import CarregarExemplo


@pytest.fixture
def conexao() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE faturas (cliente TEXT, total TEXT)")
    yield conexao
    conexao.close()


def test_ruim_exige_banco_ate_para_calcular_um_total(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(TypeError):
        ruim.Fatura("Ana", [("Café", Decimal("10"), 2)])


def test_bom_calcula_sem_nenhuma_infraestrutura(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    fatura = bom.Fatura("Ana", (bom.Item("Café", Decimal("10"), 2),))

    assert fatura.total() == Decimal("20")


def test_bom_persiste_por_um_repositorio_trocavel(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")
    fatura = bom.Fatura("Ana", (bom.Item("Café", Decimal("10"), 2),))

    bom.RepositorioSqlite(conexao).salvar(fatura)

    assert conexao.execute("SELECT cliente, total FROM faturas").fetchall() == [("Ana", "20")]


def test_mudar_o_texto_do_email_nao_toca_na_regra_de_negocio(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    fatura = bom.Fatura("Ana", (bom.Item("Café", Decimal("10"), 2),))

    assert bom.formatar_email(fatura) == "Olá, Ana! Sua fatura deu R$ 20.00."
