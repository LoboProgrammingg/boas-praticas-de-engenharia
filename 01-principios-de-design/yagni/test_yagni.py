import pytest

from conftest import CarregarExemplo


def test_ruim_falha_se_o_registro_nao_foi_configurado_antes(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(KeyError):
        ruim.cobrar(1000, "tok_1")


def test_ruim_so_funciona_depois_de_registrar_o_unico_gateway(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    ruim.FabricaDeGateways.registrar("stripe", ruim.GatewayStripe)

    assert ruim.cobrar(1000, "tok_1").id == "ch_tok_1"


def test_bom_cobra_direto_sem_cerimonia(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    cobranca = bom.cobrar(1000, "tok_1")

    assert (cobranca.id, cobranca.valor_em_centavos) == ("ch_tok_1", 1000)


def test_bom_continua_validando_a_entrada_yagni_nao_e_desleixo(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(ValueError, match="positivo"):
        bom.cobrar(0, "tok_1")
