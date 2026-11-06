"""Nomes que não dizem nada, e um nome que mente.

* ``calc(d, r)``: calcula o quê? ``d`` e ``r`` são o quê? Os argumentos trocados de
  lugar continuam rodando e devolvem um número plausível.
* ``obter_usuario`` promete uma leitura, mas cria o usuário quando ele não existe.
"""

from decimal import Decimal

USUARIOS: dict[int, str] = {}


def calc(d: Decimal, r: Decimal) -> Decimal:
    return d * (1 + r) ** 12


def obter_usuario(id: int) -> str:
    if id not in USUARIOS:
        USUARIOS[id] = f"usuario-{id}"
    return USUARIOS[id]
