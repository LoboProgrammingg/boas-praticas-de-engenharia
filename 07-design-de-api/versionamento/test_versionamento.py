import pytest

from conftest import CarregarExemplo


def _cliente_antigo_le_nome_e_saldo(corpo: dict[str, object]) -> tuple[object, int]:
    """Código de uma integração escrita em 2026-01, antes das mudanças."""
    nome = corpo["name"]
    saldo = corpo["balance"]
    assert isinstance(saldo, int)
    return nome, saldo + 1


def test_ruim_mudanca_no_lugar_quebra_a_integracao_existente(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(KeyError, match="name"):
        _cliente_antigo_le_nome_e_saldo(ruim.obter_cliente("c1"))


def test_bom_conta_fixada_na_versao_antiga_continua_funcionando(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    api = bom.Api()
    api.fixar_versao("integracao-antiga", "2026-01-01")

    corpo = api.obter_cliente("integracao-antiga", "c1")

    assert _cliente_antigo_le_nome_e_saldo(corpo) == ("Ana Souza", 1001)
    assert corpo == {"id": "c1", "name": "Ana Souza", "balance": 1000}


def test_bom_conta_nova_e_fixada_na_versao_mais_recente(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    api = bom.Api()

    corpo = api.obter_cliente("integracao-nova", "c1")

    assert corpo == {
        "id": "c1",
        "full_name": "Ana Souza",
        "balance": {"amount": 1000, "currency": "BRL"},
    }


def test_bom_versao_intermediaria_aplica_so_as_mudancas_posteriores(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    api = bom.Api()
    api.fixar_versao("meio", "2026-03-01")

    corpo = api.obter_cliente("meio", "c1")

    assert corpo == {"id": "c1", "full_name": "Ana Souza", "balance": 1000}


def test_bom_cabecalho_troca_a_versao_de_uma_unica_requisicao(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    api = bom.Api()
    api.obter_cliente("conta", "c1")

    com_cabecalho = api.obter_cliente("conta", "c1", versao_no_cabecalho="2026-01-01")
    sem_cabecalho = api.obter_cliente("conta", "c1")

    assert "name" in com_cabecalho
    assert "full_name" in sem_cabecalho


def test_bom_atualizar_a_versao_da_conta_e_uma_decisao_explicita(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    api = bom.Api()
    api.fixar_versao("conta", "2026-01-01")
    assert "name" in api.obter_cliente("conta", "c1")

    api.fixar_versao("conta", bom.VERSAO_ATUAL)

    assert "full_name" in api.obter_cliente("conta", "c1")


def test_bom_versao_inexistente_e_rejeitada(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(bom.VersaoDesconhecidaError):
        bom.Api().obter_cliente("conta", "c1", versao_no_cabecalho="1999-01-01")
