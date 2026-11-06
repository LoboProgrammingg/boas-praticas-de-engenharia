import inspect
from decimal import Decimal

import pytest

from conftest import CarregarExemplo

PRECOS = [Decimal("0.10"), Decimal("0.20")]


def _classes_definidas(modulo: object) -> list[str]:
    return [
        nome
        for nome, objeto in vars(modulo).items()
        if inspect.isclass(objeto) and objeto.__module__ == getattr(modulo, "__name__", "")
    ]


def test_ruim_e_bom_chegam_ao_mesmo_resultado(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    bom = exemplo("bom.py")

    assert ruim.total(PRECOS) == bom.total(PRECOS) == Decimal("0.30")


def test_ruim_precisa_de_tres_classes_para_somar(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert len(_classes_definidas(ruim)) == 3


def test_bom_nao_define_nenhuma_classe(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert _classes_definidas(bom) == []


def test_ruim_erra_o_nome_da_estrategia_so_em_tempo_de_execucao(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(KeyError):
        ruim.FabricaDeEstrategias().criar("somma")


def test_simples_nao_e_ingenuo_float_acumula_erro_e_decimal_nao(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert sum([0.1, 0.2]) != 0.3
    assert bom.total(PRECOS) == Decimal("0.30")
