import inspect
from decimal import Decimal

from conftest import CarregarExemplo


def test_ruim_tem_comentario_que_afirma_um_desconto_que_o_codigo_nao_aplica(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")

    assert "10% de desconto" in inspect.getsource(ruim.valor_cobravel)
    assert ruim.valor_cobravel(Decimal("100")) == Decimal("100")


def test_ruim_guarda_codigo_morto_em_comentario(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    linhas = inspect.getsource(ruim.valor_cobravel).splitlines()

    assert any(linha.strip().startswith("# resultado =") for linha in linhas)


def test_bom_eleva_ao_minimo_do_gateway_e_nao_mexe_acima_dele(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.valor_cobravel(Decimal("2.50")) == Decimal("5.00")
    assert bom.valor_cobravel(Decimal("100")) == Decimal("100")


def test_bom_documenta_o_contrato_publico_e_a_regra_vive_numa_constante_nomeada(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    assert bom.valor_cobravel.__doc__ is not None
    minimo = bom.VALOR_MINIMO_DO_GATEWAY
    assert minimo == Decimal("5.00")
