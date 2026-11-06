from decimal import Decimal
from types import SimpleNamespace

import pytest

from conftest import CarregarExemplo


def test_ruim_e_bom_calculam_o_mesmo_frete(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    bom = exemplo("bom.py")

    pedido_ruim = ruim.Pedido(ruim.Cliente("Ana", ruim.Endereco("Recife")))
    pedido_bom = bom.Pedido(bom.Cliente("Ana", bom.Endereco("Recife")))

    assert ruim.calcular_frete(pedido_ruim) == bom.calcular_frete(pedido_bom) == Decimal("0")


def test_ruim_exige_reproduzir_a_cadeia_inteira_ate_num_falso(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    falso = SimpleNamespace(cidade_de_entrega=lambda: "Recife")

    with pytest.raises(AttributeError):
        ruim.calcular_frete(falso)


def test_bom_depende_de_uma_unica_pergunta_e_aceita_qualquer_falso(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    entrega_em_recife = SimpleNamespace(cidade_de_entrega=lambda: "Recife")
    entrega_em_sampa = SimpleNamespace(cidade_de_entrega=lambda: "São Paulo")

    assert bom.calcular_frete(entrega_em_recife) == Decimal("0")
    assert bom.calcular_frete(entrega_em_sampa) == Decimal("25")


def test_bom_absorve_mudanca_de_estrutura_dentro_do_proprio_pedido(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    class PedidoComEnderecoDeEntregaPropria:
        def cidade_de_entrega(self) -> str:
            return "Olinda"

    assert bom.calcular_frete(PedidoComEnderecoDeEntregaPropria()) == Decimal("25")
