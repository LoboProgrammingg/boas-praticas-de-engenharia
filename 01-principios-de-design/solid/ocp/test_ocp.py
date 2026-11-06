from decimal import Decimal

import pytest

from conftest import CarregarExemplo


def test_ruim_ignora_silenciosamente_um_desconto_novo(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert ruim.preco_com_desconto("aniversario", Decimal("100")) == Decimal("100")


def test_bom_aceita_um_desconto_novo_sem_editar_codigo_existente(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    tabela = bom.TabelaDeDescontos()
    tabela.registrar("black_friday", bom.percentual("0.8"))

    tabela.registrar("aniversario", bom.percentual("0.85"))

    assert tabela.aplicar("black_friday", Decimal("100")) == Decimal("80.0")
    assert tabela.aplicar("aniversario", Decimal("100")) == Decimal("85.00")


def test_bom_falha_alto_para_desconto_desconhecido(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(ValueError, match="desconhecido"):
        bom.TabelaDeDescontos().aplicar("inexistente", Decimal("100"))
