"""DRY aplicado ao conhecimento, e duplicação mantida onde ela é só acidental.

* A alíquota existe em um único lugar: mudou a regra, muda uma linha.
* Perfil na tela e assinatura de e-mail se parecem, mas evoluem por motivos
  diferentes. Duas funções pequenas custam menos do que uma abstração errada.
"""

from dataclasses import dataclass
from decimal import Decimal

ALIQUOTA_ICMS = Decimal("0.17")


def com_icms(preco: Decimal) -> Decimal:
    return preco * (1 + ALIQUOTA_ICMS)


def total_do_checkout(preco: Decimal) -> Decimal:
    return com_icms(preco)


def total_da_fatura(preco: Decimal) -> Decimal:
    return com_icms(preco)


@dataclass(frozen=True, slots=True)
class Usuario:
    nome: str
    email: str


def renderizar_perfil(usuario: Usuario) -> str:
    return f"{usuario.nome} <{usuario.email}>"


def renderizar_assinatura_de_email(usuario: Usuario) -> str:
    return f"-- {usuario.nome}"
