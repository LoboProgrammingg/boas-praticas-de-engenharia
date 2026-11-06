from dataclasses import fields
from decimal import Decimal

import pytest

from conftest import CarregarExemplo


def test_ruim_um_unico_modelo_obriga_a_conhecer_os_campos_de_todos_os_contextos(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(TypeError):
        ruim.Cliente(nome="Ana", email="ana@exemplo.com")


def test_bom_cada_contexto_so_conhece_o_que_precisa(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    campos_vendas = {campo.name for campo in fields(bom.Comprador)}
    campos_cobranca = {campo.name for campo in fields(bom.Devedor)}

    assert "limite_de_credito" not in campos_vendas
    assert "email" not in campos_cobranca


def test_bom_tradutor_converte_o_cadastro_externo_para_cada_modelo(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    cadastro = bom.CadastroExterno("Ana", "ana@exemplo.com", "123", "500.00", 0)

    assert bom.para_cobranca(cadastro) == bom.Devedor("123", Decimal("500.00"), 0)
    assert bom.para_vendas(cadastro) == bom.Comprador("Ana", "ana@exemplo.com", True)


def test_bom_a_mesma_pessoa_e_inadimplente_na_cobranca_e_sem_prazo_em_vendas(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    cadastro = bom.CadastroExterno("Ana", "ana@exemplo.com", "123", "500.00", 15)

    assert bom.para_cobranca(cadastro).inadimplente()
    assert not bom.para_vendas(cadastro).pode_comprar_a_prazo
