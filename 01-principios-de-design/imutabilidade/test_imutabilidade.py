import dataclasses

import pytest

from conftest import CarregarExemplo


def test_ruim_altera_o_historico_junto_com_o_carrinho(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    carrinho = ["café"]
    historico = [carrinho]

    ruim.adicionar_item(carrinho, "pão")

    assert historico == [["café", "pão"]]


def test_bom_devolve_um_valor_novo_e_preserva_o_original(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    original = bom.Carrinho(("café",))
    historico = [original]

    novo = bom.adicionar_item(original, "pão")

    assert historico == [bom.Carrinho(("café",))]
    assert novo.itens == ("café", "pão")


def test_bom_nao_aceita_atribuicao_depois_de_criado(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    carrinho = bom.Carrinho(("café",))

    with pytest.raises(dataclasses.FrozenInstanceError):
        carrinho.itens = ()


def test_bom_pode_ser_chave_de_dicionario_porque_e_hashavel(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    carrinho = bom.Carrinho(("café",))

    assert {carrinho: "pago"}[bom.Carrinho(("café",))] == "pago"
