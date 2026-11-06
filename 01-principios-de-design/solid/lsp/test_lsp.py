from conftest import CarregarExemplo


def test_ruim_quadrado_nao_substitui_retangulo(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert ruim.dobrar_largura(ruim.Retangulo(2, 3)) == 12
    assert ruim.dobrar_largura(ruim.Quadrado(2)) == 16


def test_bom_toda_forma_cumpre_o_mesmo_contrato(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    assert bom.area_total([bom.Retangulo(2, 3), bom.Quadrado(2)]) == 10


def test_bom_alterar_largura_gera_novo_valor_sem_efeito_colateral(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    original = bom.Retangulo(2, 3)

    maior = original.com_largura(4)

    assert (original.area(), maior.area()) == (6, 12)
