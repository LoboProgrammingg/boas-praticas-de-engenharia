import pytest

from conftest import CarregarExemplo


def test_ruim_implementacao_mente_sobre_o_que_sabe_fazer(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    impressora = ruim.ImpressoraSimples()

    assert isinstance(impressora, ruim.Impressora)
    with pytest.raises(NotImplementedError):
        impressora.digitalizar("contrato")


def test_bom_cada_cliente_recebe_apenas_a_capacidade_que_precisa(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.imprimir_relatorio(bom.ImpressoraSimples(), "vendas") == "impresso: vendas"
    assert bom.arquivar(bom.Multifuncional(), "contrato") == b"contrato"
