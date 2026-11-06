import pytest

from conftest import CarregarExemplo


def test_ruim_consumidor_passa_com_o_stub_antigo(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert ruim.ClienteDeCep(ruim.ProvedorStub()).descricao("40000000") == "Rua A, Salvador"


def test_ruim_o_mesmo_consumidor_quebra_com_o_provedor_real(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(KeyError, match="logradouro"):
        ruim.ClienteDeCep(ruim.ProvedorReal()).descricao("40000000")


@pytest.mark.parametrize("provedor", ["ProvedorFake", "ProvedorReal"])
def test_bom_fake_e_provedor_real_satisfazem_o_mesmo_contrato(
    exemplo: CarregarExemplo, provedor: str
) -> None:
    bom = exemplo("bom.py")

    resposta = getattr(bom, provedor)().consultar("40000000")

    assert bom.violacoes(resposta) == []


def test_bom_campos_extras_do_provedor_nao_quebram_o_contrato(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    resposta = bom.ProvedorReal().consultar("40000000")

    assert "ibge" in resposta
    assert bom.violacoes(resposta) == []


def test_bom_teste_de_contrato_detecta_provedor_que_renomeou_campos(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    resposta_nova = {"street": "Rua A", "city": "Salvador", "uf": "BA"}

    assert bom.violacoes(resposta_nova) == [
        "falta o campo 'logradouro'",
        "falta o campo 'cidade'",
    ]


def test_bom_teste_de_contrato_detecta_mudanca_de_tipo(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    resposta = {"logradouro": "Rua A", "cidade": "Salvador", "uf": 29}

    assert bom.violacoes(resposta) == ["'uf' deveria ser str"]


def test_bom_consumidor_testado_com_o_fake_funciona_com_o_real(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    com_fake = bom.ClienteDeCep(bom.ProvedorFake()).descricao("40000000")
    com_real = bom.ClienteDeCep(bom.ProvedorReal()).descricao("40000000")

    assert com_fake == com_real == "Rua A, Salvador/BA"
