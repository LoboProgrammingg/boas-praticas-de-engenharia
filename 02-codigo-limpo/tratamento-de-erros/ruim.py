"""Códigos de retorno e erros engolidos.

* ``sacar`` devolve ``-1`` em caso de falha. Quem esquece de checar soma ``-1``
  ao total e segue em frente com um número errado.
* ``ler_valor`` troca o erro por ``None``, perdendo o motivo da falha.
"""

from decimal import Decimal, InvalidOperation


class Conta:
    def __init__(self, saldo: Decimal) -> None:
        self.saldo = saldo


def sacar(conta: Conta, valor: Decimal) -> Decimal:
    if valor > conta.saldo:
        return Decimal(-1)
    conta.saldo -= valor
    return valor


def ler_valor(texto: str) -> Decimal | None:
    try:
        return Decimal(texto)
    except InvalidOperation:
        return None
