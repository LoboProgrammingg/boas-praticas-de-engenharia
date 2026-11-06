"""Bounded Contexts: cada contexto tem o seu modelo, na sua linguagem.

* Vendas: ``Comprador`` (quem pode pedir).
* Cobrança: ``Devedor`` (quem deve e quanto).

Os contextos só conversam por um tradutor na fronteira (Anticorruption Layer), então um
mudar de nome ou de campo não quebra o outro.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Comprador:
    """Contexto de Vendas."""

    nome: str
    email: str
    pode_comprar_a_prazo: bool


@dataclass(frozen=True, slots=True)
class Devedor:
    """Contexto de Cobrança."""

    documento_do_pagador: str
    limite_de_credito: Decimal
    dias_de_atraso: int

    def inadimplente(self) -> bool:
        return self.dias_de_atraso > 0


@dataclass(frozen=True, slots=True)
class CadastroExterno:
    """Formato que o sistema legado de cadastro entrega."""

    nome: str
    email: str
    documento: str
    limite: str
    atraso_em_dias: int


def para_cobranca(cadastro: CadastroExterno) -> Devedor:
    return Devedor(cadastro.documento, Decimal(cadastro.limite), cadastro.atraso_em_dias)


def para_vendas(cadastro: CadastroExterno) -> Comprador:
    devedor = para_cobranca(cadastro)
    a_prazo = not devedor.inadimplente() and devedor.limite_de_credito > 0
    return Comprador(cadastro.nome, cadastro.email, a_prazo)
