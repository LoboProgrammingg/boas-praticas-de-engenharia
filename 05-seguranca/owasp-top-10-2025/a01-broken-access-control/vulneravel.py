"""A01 / API1 (BOLA): qualquer usuário autenticado lê qualquer pedido pelo ID.

A consulta confia no ID que veio da URL e esquece de perguntar *de quem* é o pedido.
"""

import sqlite3
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pedido:
    id: int
    tenant_id: int
    descricao: str


def buscar_pedido(conexao: sqlite3.Connection, pedido_id: int, tenant_id: int) -> Pedido | None:
    linha = conexao.execute(
        "SELECT id, tenant_id, descricao FROM pedidos WHERE id = ?", (pedido_id,)
    ).fetchone()
    return None if linha is None else Pedido(*linha)
