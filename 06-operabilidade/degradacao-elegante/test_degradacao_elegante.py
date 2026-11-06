import logging

import pytest

from conftest import CarregarExemplo


class RecomendadorFalso:
    def __init__(self, erro: Exception | None = None) -> None:
        self.erro = erro

    def recomendar(self, usuario: str) -> tuple[str, ...]:
        if self.erro is not None:
            raise self.erro
        return ("livro-1", "livro-2")


def test_ruim_falha_da_recomendacao_derruba_a_pagina(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    with pytest.raises(TimeoutError):
        ruim.pagina_inicial(RecomendadorFalso(TimeoutError("lento")), "ana")


def test_bom_com_dependencia_saudavel_a_pagina_nao_e_degradada(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    pagina = bom.PaginaInicial(RecomendadorFalso(), logging.getLogger("teste")).montar("ana")

    assert pagina.recomendacoes == ("livro-1", "livro-2")
    assert pagina.degradada is False


def test_bom_sem_historico_cai_para_os_itens_populares(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    recomendador = RecomendadorFalso(bom.DependenciaIndisponivelError("fora do ar"))

    pagina = bom.PaginaInicial(recomendador, logging.getLogger("teste")).montar("ana")

    assert pagina.recomendacoes == bom.POPULARES
    assert pagina.degradada is True


def test_bom_com_historico_serve_as_ultimas_recomendacoes_boas(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    recomendador = RecomendadorFalso()
    pagina_inicial = bom.PaginaInicial(recomendador, logging.getLogger("teste"))
    pagina_inicial.montar("ana")
    recomendador.erro = bom.DependenciaIndisponivelError("fora do ar")

    pagina = pagina_inicial.montar("ana")

    assert pagina.recomendacoes == ("livro-1", "livro-2")
    assert pagina.degradada is True


def test_bom_a_degradacao_e_registrada_em_log(
    exemplo: CarregarExemplo, caplog: pytest.LogCaptureFixture
) -> None:
    bom = exemplo("bom.py")
    recomendador = RecomendadorFalso(bom.DependenciaIndisponivelError("circuito aberto"))

    with caplog.at_level(logging.WARNING):
        bom.PaginaInicial(recomendador, logging.getLogger("teste")).montar("ana")

    registro = caplog.records[0]
    assert registro.getMessage() == "recomendacoes_degradadas"
    assert registro.__dict__["contexto"] == {"usuario": "ana", "motivo": "circuito aberto"}


def test_bom_um_bug_nao_e_escondido_pela_degradacao(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    recomendador = RecomendadorFalso(TypeError("bug no código"))

    with pytest.raises(TypeError):
        bom.PaginaInicial(recomendador, logging.getLogger("teste")).montar("ana")
