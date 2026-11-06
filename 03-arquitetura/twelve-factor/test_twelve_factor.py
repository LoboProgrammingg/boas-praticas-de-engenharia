import pytest
from pydantic import ValidationError

from conftest import CarregarExemplo

AMBIENTE = {"DATABASE_URL": "postgresql://localhost/app", "API_KEY": "segredo", "PORT": "9000"}


def test_ruim_segredo_e_configuracao_estao_no_codigo_fonte(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    assert "senha-de-producao" in ruim.descrever()


def test_bom_le_a_configuracao_do_ambiente_com_tipos(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    config = bom.Config.do_ambiente(AMBIENTE)

    assert config.database_url == "postgresql://localhost/app"
    assert config.port == 9000
    assert config.api_key.get_secret_value() == "segredo"


def test_bom_mesmo_codigo_deploys_diferentes(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    homologacao = bom.Config.do_ambiente({**AMBIENTE, "DATABASE_URL": "postgresql://hml/app"})
    producao = bom.Config.do_ambiente({**AMBIENTE, "DATABASE_URL": "postgresql://prod/app"})

    assert homologacao.database_url != producao.database_url


def test_bom_falha_ao_subir_quando_falta_variavel_obrigatoria(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(ValidationError, match="database_url"):
        bom.Config.do_ambiente({"API_KEY": "segredo"})


def test_bom_porta_invalida_e_rejeitada(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(ValidationError, match="port"):
        bom.Config.do_ambiente({**AMBIENTE, "PORT": "abc"})


def test_bom_segredo_nao_vaza_na_representacao(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    config = bom.Config.do_ambiente(AMBIENTE)

    assert "segredo" not in repr(config)
    assert "segredo" not in str(config)
