"""A01 / API1 (BOLA): o escopo do tenant mora na própria consulta.

Pedido de outro tenant e pedido inexistente produzem a mesma resposta (404), então
o endpoint não revela quais IDs existem.
"""

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pedido:
    id: int
    tenant_id: int
    descricao: str


class PedidoNaoEncontradoError(Exception):
    status_http = 404


def buscar_pedido(conexao: sqlite3.Connection, pedido_id: int, tenant_id: int) -> Pedido:
    linha = conexao.execute(
        "SELECT id, tenant_id, descricao FROM pedidos WHERE id = ? AND tenant_id = ?",
        (pedido_id, tenant_id),
    ).fetchone()
    if linha is None:
        raise PedidoNaoEncontradoError(pedido_id)
    return Pedido(*linha)
