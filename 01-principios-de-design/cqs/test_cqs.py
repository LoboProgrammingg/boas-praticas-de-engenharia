import pytest

from conftest import CarregarExemplo


def test_ruim_gasta_um_numero_a_cada_leitura(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    numerador = ruim.NumeradorDeFaturas()

    registrado_no_log = numerador.proximo_numero()
    usado_na_fatura = numerador.proximo_numero()

    assert (registrado_no_log, usado_na_fatura) == (1, 2)


@pytest.mark.parametrize("leituras", [1, 2, 10])
def test_bom_consultar_quantas_vezes_quiser_nao_muda_nada(
    exemplo: CarregarExemplo, leituras: int
) -> None:
    bom = exemplo("bom.py")
    numerador = bom.NumeradorDeFaturas()
    numerador.avancar()

    lidos = {numerador.atual() for _ in range(leituras)}

    assert lidos == {1}


def test_bom_so_o_comando_muda_o_estado(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    numerador = bom.NumeradorDeFaturas()

    resultado = numerador.avancar()

    assert resultado is None
    assert numerador.atual() == 1
