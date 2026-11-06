"""SRP violado: a mesma classe calcula, persiste e formata e-mail.

Ela muda quando muda a regra de preço, o esquema do banco ou o texto do e-mail,
três razões diferentes, vindas de três pessoas diferentes.
"""

import sqlite3
from decimal import Decimal


class Fatura:
    def __init__(
        self, cliente: str, itens: list[tuple[str, Decimal, int]], conexao: sqlite3.Connection
    ) -> None:
        self.cliente = cliente
        self.itens = itens
        self.conexao = conexao

    def total(self) -> Decimal:
        return sum((preco * quantidade for _, preco, quantidade in self.itens), Decimal("0"))

    def salvar(self) -> None:
        self.conexao.execute(
            "INSERT INTO faturas (cliente, total) VALUES (?, ?)", (self.cliente, str(self.total()))
        )

    def como_email(self) -> str:
        return f"Olá, {self.cliente}! Sua fatura deu R$ {self.total():.2f}."
