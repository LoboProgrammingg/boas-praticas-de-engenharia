from decimal import Decimal

import pytest

from conftest import CarregarExemplo


def test_ruim_aceita_argumentos_trocados_e_devolve_um_numero_plausivel(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    certo = ruim.calc(Decimal("1000"), Decimal("0.01"))

    trocado = ruim.calc(Decimal("0.01"), Decimal("1000"))

    assert isinstance(trocado, Decimal)
    assert trocado != certo


def test_ruim_obter_usuario_escreve_no_estado_ao_ser_chamado(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    ruim.obter_usuario(7)

    assert ruim.USUARIOS == {7: "usuario-7"}


def test_bom_calcula_o_mesmo_valor_com_parametros_que_se_explicam(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    valor = bom.valor_composto_em_um_ano(principal=Decimal("1000"), taxa_mensal=Decimal("0.01"))

    assert round(valor, 2) == Decimal("1126.83")


def test_bom_recusa_chamada_posicional_que_poderia_trocar_os_valores(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(TypeError):
        bom.valor_composto_em_um_ano(Decimal("0.01"), Decimal("1000"))


def test_bom_buscar_nao_altera_e_obter_ou_criar_avisa_no_nome(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    usuarios: dict[int, str] = {}

    assert bom.buscar_usuario(usuarios, 7) is None
    assert usuarios == {}
    assert bom.obter_ou_criar_usuario(usuarios, 7) == "usuario-7"
    assert usuarios == {7: "usuario-7"}
