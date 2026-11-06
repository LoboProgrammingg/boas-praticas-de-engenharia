from decimal import Decimal

import pytest

from conftest import CarregarExemplo


def test_ruim_somar_saques_sem_checar_o_retorno_produz_total_errado(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    conta = ruim.Conta(Decimal("100"))

    total_sacado = ruim.sacar(conta, Decimal("30")) + ruim.sacar(conta, Decimal("500"))

    assert total_sacado == Decimal("29")


def test_ruim_devolve_none_e_perde_o_motivo_da_falha(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert ruim.ler_valor("12,50") is None
    assert ruim.ler_valor("abc") is None


def test_bom_interrompe_o_fluxo_e_informa_os_dados_da_falha(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    conta = bom.Conta(Decimal("100"))

    with pytest.raises(bom.SaldoInsuficienteError) as informacao:
        conta.sacar(Decimal("500"))

    assert (informacao.value.saldo, informacao.value.valor) == (Decimal("100"), Decimal("500"))
    assert conta.saldo == Decimal("100")


def test_bom_saque_valido_devolve_o_valor_e_debita_o_saldo(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    conta = bom.Conta(Decimal("100"))

    assert conta.sacar(Decimal("30")) == Decimal("30")
    assert conta.saldo == Decimal("70")


def test_bom_traduz_o_erro_tecnico_e_preserva_a_causa(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(bom.ValorInvalidoError, match="'12,50'") as informacao:
        bom.ler_valor("12,50")

    assert informacao.value.__cause__ is not None
