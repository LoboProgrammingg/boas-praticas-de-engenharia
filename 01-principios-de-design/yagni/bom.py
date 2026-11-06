"""YAGNI aplicado: uma função concreta para o único gateway que existe.

Quando o segundo gateway for real, extrai-se a interface com dois casos de uso
na mão, e não com um palpite.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Cobranca:
    id: str
    valor_em_centavos: int


def cobrar(valor_em_centavos: int, token: str) -> Cobranca:
    if valor_em_centavos <= 0:
        raise ValueError("o valor da cobrança deve ser positivo")
    return Cobranca(f"ch_{token}", valor_em_centavos)
