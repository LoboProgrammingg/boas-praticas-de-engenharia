from decimal import Decimal

import pytest

from conftest import CarregarExemplo

LINHAS = [["produto", "preço"], ["café", "10"]]


def test_ruim_trocar_os_booleanos_muda_a_saida_sem_nenhum_erro(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    pretendido = ruim.exportar(LINHAS, True, False)
    trocado = ruim.exportar(LINHAS, False, True)

    assert pretendido == "café,10"
    assert trocado == "produto | preço\ncafé | 10"


def test_bom_cada_formato_tem_nome_proprio_e_o_booleano_vai_nomeado(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    assert bom.exportar_csv(LINHAS, com_cabecalho=False) == "café,10"
    assert bom.exportar_tabela(LINHAS) == "produto | preço\ncafé | 10"


def test_bom_recusa_booleano_posicional(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(TypeError):
        bom.exportar_csv(LINHAS, False)


def test_ruim_destroi_os_precos_originais_do_chamador(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    precos = [Decimal("100"), Decimal("50")]

    resultado = ruim.aplicar_desconto(precos, Decimal("10"))

    assert resultado is None
    assert precos == [Decimal("90"), Decimal("45")]


def test_bom_devolve_valores_novos_e_nao_toca_na_entrada(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    precos = (Decimal("100"), Decimal("50"))

    com_desconto = bom.precos_com_desconto(precos, Decimal("10"))

    assert com_desconto == (Decimal("90"), Decimal("45"))
    assert precos == (Decimal("100"), Decimal("50"))
