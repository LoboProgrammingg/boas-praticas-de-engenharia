"""Exceções tipadas, com contexto, que não deixam o erro passar em silêncio.

* ``SaldoInsuficienteError`` carrega os dados da falha e interrompe o fluxo.
* ``ler_valor`` traduz o erro técnico em um erro do domínio, preservando a causa
  (``raise ... from``).
"""

from decimal import Decimal, InvalidOperation


class SaldoInsuficienteError(Exception):
    def __init__(self, saldo: Decimal, valor: Decimal) -> None:
        super().__init__(f"saldo {saldo} insuficiente para sacar {valor}")
        self.saldo = saldo
        self.valor = valor


class ValorInvalidoError(ValueError):
    pass


class Conta:
    def __init__(self, saldo: Decimal) -> None:
        self.saldo = saldo

    def sacar(self, valor: Decimal) -> Decimal:
        if valor > self.saldo:
            raise SaldoInsuficienteError(self.saldo, valor)
        self.saldo -= valor
        return valor


def ler_valor(texto: str) -> Decimal:
    try:
        return Decimal(texto)
    except InvalidOperation as erro:
        raise ValorInvalidoError(f"valor monetário inválido: {texto!r}") from erro
