from decimal import Decimal

import pytest

from conftest import CarregarExemplo


def test_ruim_listar_o_total_carrega_todos_os_agregados_do_cliente(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    servico = ruim.ServicoDePedidos()
    for numero in range(5):
        servico.fazer_pedido(f"p{numero}", "Ana", [Decimal("10")])

    total = servico.total_do_cliente("Ana")

    assert total == Decimal("50")
    assert servico.carregamentos == 5


def test_bom_consulta_le_a_projecao_sem_carregar_agregados(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    projecao = bom.TotalPorCliente()
    comando = bom.FazerPedido(projecao)
    for numero in range(5):
        comando(f"p{numero}", "Ana", (Decimal("10"),))

    assert projecao.total_do_cliente("Ana") == Decimal("50")
    assert projecao.total_do_cliente("Bia") == Decimal("0")


def test_bom_comando_ainda_protege_a_invariante_do_agregado(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    projecao = bom.TotalPorCliente()

    with pytest.raises(ValueError, match="vazio"):
        bom.FazerPedido(projecao)("p1", "Ana", ())

    assert projecao.total_do_cliente("Ana") == Decimal("0")


def test_bom_projecao_e_reconstruivel_a_partir_dos_eventos(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    eventos = [bom.PedidoFeito("Ana", Decimal("10")), bom.PedidoFeito("Ana", Decimal("5"))]
    projecao = bom.TotalPorCliente()

    for evento in eventos:
        projecao.aplicar(evento)

    assert projecao.total_do_cliente("Ana") == Decimal("15")
