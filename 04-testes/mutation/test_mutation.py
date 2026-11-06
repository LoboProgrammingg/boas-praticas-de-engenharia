"""Um minúsculo "mutation testing" feito à mão.

Ferramentas como mutmut (Python) e Stryker (JavaScript/TypeScript) geram os mutantes
automaticamente; aqui eles são escritos à mão para mostrar a ideia.
"""

from collections.abc import Callable
from types import ModuleType

from conftest import CarregarExemplo

type Regra = Callable[[int], bool]

MUTANTES: dict[str, Regra] = {
    "idade >= 18  ->  idade > 18": lambda idade: idade > 18,
    "idade >= 18  ->  idade >= 19": lambda idade: idade >= 19,
    "idade >= 18  ->  idade >= 17": lambda idade: idade >= 17,
    "idade >= 18  ->  idade <= 18": lambda idade: idade <= 18,
    "retorna sempre True": lambda idade: True,
}


def _suite_passa(modulo: ModuleType, regra: Regra) -> bool:
    return all(regra(idade) is esperado for idade, esperado in modulo.CASOS)


def _sobreviventes(modulo: ModuleType) -> list[str]:
    return [nome for nome, mutante in MUTANTES.items() if _suite_passa(modulo, mutante)]


def test_a_suite_fraca_passa_contra_o_codigo_original(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert _suite_passa(ruim, ruim.pode_comprar_bebida)


def test_ruim_mutantes_de_fronteira_sobrevivem_apesar_da_cobertura_total(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")

    assert _sobreviventes(ruim) == [
        "idade >= 18  ->  idade > 18",
        "idade >= 18  ->  idade >= 19",
        "idade >= 18  ->  idade >= 17",
    ]


def test_bom_casos_de_fronteira_matam_todos_os_mutantes(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert _suite_passa(bom, bom.pode_comprar_bebida)
    assert _sobreviventes(bom) == []
