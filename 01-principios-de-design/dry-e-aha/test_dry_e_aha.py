import inspect
from decimal import Decimal

import pytest

from conftest import CarregarExemplo


def test_ruim_repete_a_mesma_regra_de_negocio_em_dois_lugares(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert inspect.getsource(ruim).count('Decimal("1.17")') == 2
    assert not hasattr(ruim, "ALIQUOTA_ICMS")


def test_bom_muda_a_aliquota_em_um_unico_ponto(
    exemplo: CarregarExemplo, monkeypatch: pytest.MonkeyPatch
) -> None:
    bom = exemplo("bom.py")
    monkeypatch.setattr(bom, "ALIQUOTA_ICMS", Decimal("0.18"))

    assert bom.total_do_checkout(Decimal("100")) == Decimal("118.00")
    assert bom.total_da_fatura(Decimal("100")) == Decimal("118.00")


def test_ruim_ignora_em_silencio_uma_flag_quando_outra_vence(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    usuario = ruim.Usuario("Ana", "ana@exemplo.com")

    com_compacto = ruim.renderizar(usuario, compacto=True, para_email=True)
    sem_compacto = ruim.renderizar(usuario, para_email=True)

    assert com_compacto == sem_compacto


def test_ruim_aceita_oito_combinacoes_de_flags_que_ninguem_projetou(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    usuario = ruim.Usuario("Ana", "ana@exemplo.com")
    flags = [(a, c, e) for a in (False, True) for c in (False, True) for e in (False, True)]

    saidas = {ruim.renderizar(usuario, admin=a, compacto=c, para_email=e) for a, c, e in flags}

    assert len(flags) == 8
    assert len(saidas) < len(flags)


def test_bom_mantem_duas_funcoes_que_evoluem_sem_se_afetar(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    usuario = bom.Usuario("Ana", "ana@exemplo.com")

    assert bom.renderizar_perfil(usuario) == "Ana <ana@exemplo.com>"
    assert bom.renderizar_assinatura_de_email(usuario) == "-- Ana"
