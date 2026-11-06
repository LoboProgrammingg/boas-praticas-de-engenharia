"""Dois erros opostos no mesmo arquivo.

1. DRY violado: a mesma regra de negócio (alíquota) escrita em dois lugares.
2. DRY mal aplicado: casos que só parecem iguais fundidos numa função com flags.
"""

from dataclasses import dataclass
from decimal import Decimal


def total_do_checkout(preco: Decimal) -> Decimal:
    return preco * Decimal("1.17")


def total_da_fatura(preco: Decimal) -> Decimal:
    return preco * Decimal("1.17")


@dataclass(frozen=True, slots=True)
class Usuario:
    nome: str
    email: str


def renderizar(
    usuario: Usuario, *, admin: bool = False, compacto: bool = False, para_email: bool = False
) -> str:
    if para_email:
        texto = f"-- {usuario.nome}"
    elif compacto:
        texto = usuario.nome
    else:
        texto = f"{usuario.nome} <{usuario.email}>"
    if admin:
        texto += " [admin]"
    return texto
