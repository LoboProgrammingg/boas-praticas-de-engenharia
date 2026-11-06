"""Retry com timeout por tentativa, backoff exponencial, full jitter e teto.

* Só repete ``FalhaTransitoriaError`` (falha parcial/temporária). Erro permanente sobe na hora.
* Só repete se o chamador declara a operação ``idempotente``; senão, uma tentativa só.
* Cada tentativa recebe um ``timeout``: nenhuma chamada fica pendurada.
* Espera = ``uniform(0, min(teto, base * 2**tentativa))`` ("full jitter", Brooker/AWS).
* ``dormir`` e ``sorteio`` são injetáveis: os testes não dormem nem dependem de sorte.
"""

import random
import time
from collections.abc import Callable
from dataclasses import dataclass


class FalhaTransitoriaError(Exception):
    """Falha que pode passar sozinha: timeout, 503, conexão recusada."""


@dataclass(frozen=True, slots=True)
class Politica:
    tentativas: int = 4
    timeout: float = 1.0
    base: float = 0.1
    teto: float = 2.0


POLITICA_PADRAO = Politica()


def calcular_espera(
    tentativa: int,
    *,
    base: float,
    teto: float,
    sorteio: Callable[[float, float], float] = random.uniform,
) -> float:
    return sorteio(0.0, min(teto, base * 2**tentativa))


def com_retry[T](
    operacao: Callable[[float], T],
    *,
    idempotente: bool,
    politica: Politica = POLITICA_PADRAO,
    dormir: Callable[[float], None] = time.sleep,
    sorteio: Callable[[float, float], float] = random.uniform,
) -> T:
    limite = politica.tentativas if idempotente else 1
    feitas = 0
    while True:
        try:
            return operacao(politica.timeout)
        except FalhaTransitoriaError:
            feitas += 1
            if feitas >= limite:
                raise
            dormir(
                calcular_espera(feitas - 1, base=politica.base, teto=politica.teto, sorteio=sorteio)
            )
