import pytest

from conftest import CarregarExemplo


def test_ruim_perde_centavos(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert sum(ruim.parcelar(100, 3)) == 99


def test_bom_divisao_exata_gera_parcelas_iguais(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.parcelar(90, 3) == [30, 30, 30]


def test_bom_resto_vai_para_as_primeiras_parcelas(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.parcelar(100, 3) == [34, 33, 33]


@pytest.mark.parametrize(("total", "parcelas"), [(100, 3), (1, 5), (0, 4), (999, 7)])
def test_bom_a_soma_das_parcelas_e_sempre_o_total(
    exemplo: CarregarExemplo, total: int, parcelas: int
) -> None:
    bom = exemplo("bom.py")

    assert sum(bom.parcelar(total, parcelas)) == total


def test_bom_zero_parcelas_e_rejeitado(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(ValueError, match="positivo"):
        bom.parcelar(100, 0)
