import pytest

from conftest import CarregarExemplo


def test_ruim_pedidos_quebra_quando_o_estoque_muda_a_sua_estrutura_interna(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    estoque = ruim.Estoque({"A": 5})
    estoque._saldos = None  # o dono do estoque "refatora" a estrutura interna

    with pytest.raises(AttributeError):
        ruim.Pedidos(estoque).fazer("A", 1)


def test_bom_pedidos_usa_so_a_api_publica_do_estoque(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    saldos = {"A": 5}

    pedidos = bom.Pedidos(bom.EstoqueLocal(saldos))

    assert pedidos.fazer("A", 3) is True
    assert pedidos.fazer("A", 3) is False
    assert saldos == {"A": 2}


def test_bom_trocar_local_por_remoto_nao_muda_o_modulo_de_pedidos(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    local = bom.EstoqueLocal({"A": 5})
    remoto = bom.EstoqueRemoto(local.reservar)

    assert bom.Pedidos(remoto).fazer("A", 2) is True


def test_bom_o_premio_da_distribuicao_falha_de_rede_aparece_so_no_adaptador_remoto(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    def rede_fora(sku: str, quantidade: int) -> bool:
        raise bom.FalhaDeRedeError(f"timeout reservando {sku} x{quantidade}")

    pedidos = bom.Pedidos(bom.EstoqueRemoto(rede_fora))

    with pytest.raises(bom.FalhaDeRedeError):
        pedidos.fazer("A", 1)
