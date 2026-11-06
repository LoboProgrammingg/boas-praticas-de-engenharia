"""Regra de negócio acoplada à infraestrutura: o "centro" conhece SQLite e SMTP.

``Pedido`` valida, grava no banco e dispara e-mail. Para testar a regra de que um pedido
não pode ser vazio é preciso um banco e um servidor de e-mail, e trocar qualquer um deles
significa mexer na regra de negócio.
"""

import sqlite3
from decimal import Decimal

CAMINHO_DO_BANCO = "pedidos.db"


class Pedido:
    def __init__(self, cliente: str, itens: list[Decimal]) -> None:
        self.cliente = cliente
        self.itens = itens

    def total(self) -> Decimal:
        return sum(self.itens, Decimal("0"))

    def confirmar(self) -> None:
        if not self.itens:
            raise ValueError("pedido vazio")
        conexao = sqlite3.connect(CAMINHO_DO_BANCO)
        conexao.execute("CREATE TABLE IF NOT EXISTS pedidos (cliente TEXT, total TEXT)")
        conexao.execute("INSERT INTO pedidos VALUES (?, ?)", (self.cliente, str(self.total())))
        conexao.commit()
        conexao.close()
        print(f"enviando e-mail para {self.cliente}")
