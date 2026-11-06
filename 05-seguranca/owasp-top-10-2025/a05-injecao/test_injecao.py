import sqlite3
from collections.abc import Iterator

import pytest
from hypothesis import given
from hypothesis import strategies as st

from conftest import CarregarExemplo

ENTRADA_MALICIOSA = "' OR '1'='1"
TEXTO_SEM_SURROGATES = st.text(alphabet=st.characters(exclude_categories=["Cs"]))


@pytest.fixture
def conexao() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE usuarios (nome TEXT, email TEXT)")
    conexao.executemany(
        "INSERT INTO usuarios VALUES (?, ?)",
        [("ana", "ana@exemplo.test"), ("bia", "bia@exemplo.test")],
    )
    yield conexao
    conexao.close()


def test_vulneravel_devolve_todos_os_usuarios_com_a_entrada_maliciosa(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    vulneravel = exemplo("vulneravel.py")

    assert len(vulneravel.buscar_usuarios(conexao, ENTRADA_MALICIOSA)) == 2


def test_seguro_trata_a_entrada_maliciosa_como_um_nome_qualquer(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.buscar_usuarios(conexao, ENTRADA_MALICIOSA) == []


def test_seguro_continua_encontrando_o_usuario_legitimo(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.buscar_usuarios(conexao, "ana") == [("ana", "ana@exemplo.test")]


def test_seguro_nunca_devolve_linha_cujo_nome_seja_diferente_da_entrada(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")

    @given(nome=TEXTO_SEM_SURROGATES)
    def propriedade(nome: str) -> None:
        assert all(linha[0] == nome for linha in seguro.buscar_usuarios(conexao, nome))

    propriedade()


def test_vulneravel_deixa_o_script_passar_para_o_html(exemplo: CarregarExemplo) -> None:
    vulneravel = exemplo("vulneravel.py")

    assert vulneravel.renderizar_comentario("<script>alert(1)</script>") == (
        "<p><script>alert(1)</script></p>"
    )


def test_seguro_escapa_o_html_da_entrada(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.renderizar_comentario("<script>alert(1)</script>") == (
        "<p>&lt;script&gt;alert(1)&lt;/script&gt;</p>"
    )


def test_seguro_escapa_aspas_para_nao_quebrar_atributos(exemplo: CarregarExemplo) -> None:
    seguro = exemplo("seguro.py")

    assert '"' not in seguro.renderizar_comentario('" onmouseover="x')
