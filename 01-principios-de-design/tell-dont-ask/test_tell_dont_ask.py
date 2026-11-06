import pytest

from conftest import CarregarExemplo


def test_ruim_protege_as_regras_so_para_quem_passa_pelo_servico(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(ValueError, match="vazio"):
        ruim.ServicoDePedidos().confirmar(ruim.Pedido())


def test_ruim_aceita_pedido_vazio_confirmado_quando_alguem_escreve_direto(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    pedido = ruim.Pedido()

    pedido.status = "confirmado"

    assert pedido.itens == []
    assert pedido.status == "confirmado"


def test_bom_recusa_confirmar_pedido_vazio(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(bom.PedidoVazioError):
        bom.Pedido().confirmar()


def test_bom_nao_deixa_ninguem_escrever_direto_no_estado(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    pedido = bom.Pedido()

    with pytest.raises(AttributeError):
        pedido.confirmado = True


def test_bom_congela_o_pedido_depois_de_confirmado(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    pedido = bom.Pedido()
    pedido.adicionar("café")
    pedido.confirmar()

    with pytest.raises(bom.PedidoJaConfirmadoError):
        pedido.adicionar("pão")
    with pytest.raises(bom.PedidoJaConfirmadoError):
        pedido.confirmar()

    assert pedido.itens == ("café",)
