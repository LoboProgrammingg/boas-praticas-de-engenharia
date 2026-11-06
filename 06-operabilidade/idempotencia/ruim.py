"""Criação de pagamento sem idempotência: cada reenvio cobra de novo.

O cliente enviou a requisição, o servidor cobrou, mas a resposta se perdeu (timeout).
O cliente, sem saber, repete. Resultado: o cliente é cobrado duas vezes.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Pagamento:
    id: str
    valor: int


class ServidorDePagamentos:
    def __init__(self) -> None:
        self.cobrancas: list[Pagamento] = []

    def criar_pagamento(self, valor: int) -> Pagamento:
        pagamento = Pagamento(f"pay_{len(self.cobrancas) + 1}", valor)
        self.cobrancas.append(pagamento)
        return pagamento
