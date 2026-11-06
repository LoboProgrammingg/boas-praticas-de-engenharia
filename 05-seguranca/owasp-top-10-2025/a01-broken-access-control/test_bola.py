import sqlite3
from collections.abc import Iterator

import pytest

from conftest import CarregarExemplo

TENANT_A = 10
TENANT_B = 20


@pytest.fixture
def conexao() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(":memory:")
    conexao.execute(
        "CREATE TABLE pedidos (id INTEGER PRIMARY KEY, tenant_id INTEGER NOT NULL, "
        "descricao TEXT NOT NULL)"
    )
    conexao.executemany(
        "INSERT INTO pedidos VALUES (?, ?, ?)",
        [(1, TENANT_A, "pedido da empresa A"), (2, TENANT_B, "pedido da empresa B")],
    )
    yield conexao
    conexao.close()


def test_vulneravel_entrega_pedido_de_outro_tenant(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    vulneravel = exemplo("vulneravel.py")

    pedido = vulneravel.buscar_pedido(conexao, 2, TENANT_A)

    assert pedido is not None
    assert pedido.descricao == "pedido da empresa B"


def test_seguro_entrega_o_proprio_pedido(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")

    assert seguro.buscar_pedido(conexao, 1, TENANT_A).descricao == "pedido da empresa A"


def test_seguro_nega_pedido_de_outro_tenant_com_404(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.PedidoNaoEncontradoError) as erro:
        seguro.buscar_pedido(conexao, 2, TENANT_A)

    assert erro.value.status_http == 404


def test_seguro_nao_distingue_pedido_alheio_de_pedido_inexistente(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    seguro = exemplo("seguro.py")
    respostas = []

    for pedido_id in (2, 999):
        with pytest.raises(seguro.PedidoNaoEncontradoError) as erro:
            seguro.buscar_pedido(conexao, pedido_id, TENANT_A)
        respostas.append(erro.value.status_http)

    assert respostas == [404, 404]
