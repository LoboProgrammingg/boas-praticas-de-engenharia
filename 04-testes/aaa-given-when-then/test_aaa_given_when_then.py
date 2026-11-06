"""Testes escritos em AAA (Arrange, Act, Assert) com nomes em Given-When-Then.

O código sob teste (``Carrinho``) fica aqui mesmo para que o arquivo seja lido de cima a
baixo. Em um projeto real ele estaria em outro módulo.
"""

from dataclasses import dataclass, field
from decimal import Decimal

import pytest


@dataclass
class Carrinho:
    itens: list[Decimal] = field(default_factory=list)
    desconto_percentual: Decimal = Decimal(0)

    def adicionar(self, preco: Decimal) -> None:
        if preco <= 0:
            raise ValueError("preço deve ser positivo")
        self.itens.append(preco)

    def aplicar_cupom(self, percentual: Decimal) -> None:
        if not Decimal(0) < percentual <= Decimal(50):
            raise ValueError("cupom entre 0 e 50 por cento")
        self.desconto_percentual = percentual

    def total(self) -> Decimal:
        bruto = sum(self.itens, Decimal(0))
        return bruto * (Decimal(100) - self.desconto_percentual) / Decimal(100)


@pytest.fixture
def carrinho_com_dois_itens() -> Carrinho:
    carrinho = Carrinho()
    carrinho.adicionar(Decimal(60))
    carrinho.adicionar(Decimal(40))
    return carrinho


def test_dado_carrinho_vazio_quando_calcula_total_entao_e_zero() -> None:
    # Arrange (Given)
    carrinho = Carrinho()

    # Act (When)
    total = carrinho.total()

    # Assert (Then)
    assert total == Decimal(0)


def test_dado_dois_itens_quando_calcula_total_entao_soma_os_precos(
    carrinho_com_dois_itens: Carrinho,
) -> None:
    total = carrinho_com_dois_itens.total()

    assert total == Decimal(100)


def test_dado_dois_itens_quando_aplica_cupom_de_10_por_cento_entao_total_cai_10_por_cento(
    carrinho_com_dois_itens: Carrinho,
) -> None:
    carrinho_com_dois_itens.aplicar_cupom(Decimal(10))

    assert carrinho_com_dois_itens.total() == Decimal(90)


@pytest.mark.parametrize("percentual", [Decimal(0), Decimal(-5), Decimal("50.01"), Decimal(100)])
def test_quando_cupom_fora_da_faixa_entao_e_rejeitado_e_o_total_nao_muda(
    carrinho_com_dois_itens: Carrinho, percentual: Decimal
) -> None:
    with pytest.raises(ValueError, match="cupom"):
        carrinho_com_dois_itens.aplicar_cupom(percentual)

    assert carrinho_com_dois_itens.total() == Decimal(100)


@pytest.mark.parametrize("preco", [Decimal(0), Decimal(-1)])
def test_quando_adiciona_item_sem_preco_positivo_entao_levanta_erro(preco: Decimal) -> None:
    carrinho = Carrinho()

    with pytest.raises(ValueError, match="preço"):
        carrinho.adicionar(preco)

    assert carrinho.itens == []
