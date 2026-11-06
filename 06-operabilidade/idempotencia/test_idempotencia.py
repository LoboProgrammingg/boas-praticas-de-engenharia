from concurrent.futures import ThreadPoolExecutor

import pytest

from conftest import CarregarExemplo


def test_ruim_reenvio_apos_resposta_perdida_cobra_duas_vezes(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    servidor = ruim.ServidorDePagamentos()

    servidor.criar_pagamento(100)  # cobrou, mas a resposta se perdeu
    servidor.criar_pagamento(100)  # o cliente repete sem saber

    assert len(servidor.cobrancas) == 2


def test_bom_reenvio_com_a_mesma_chave_devolve_o_mesmo_pagamento(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    servidor = bom.ServidorDePagamentos()

    primeiro = servidor.criar_pagamento("chave-1", 100)
    reenvio = servidor.criar_pagamento("chave-1", 100)

    assert reenvio == primeiro
    assert len(servidor.cobrancas) == 1


def test_bom_chaves_diferentes_sao_pagamentos_diferentes(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    servidor = bom.ServidorDePagamentos()

    servidor.criar_pagamento("chave-1", 100)
    servidor.criar_pagamento("chave-2", 100)

    assert len(servidor.cobrancas) == 2


def test_bom_mesma_chave_com_payload_diferente_e_rejeitada(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    servidor = bom.ServidorDePagamentos()
    servidor.criar_pagamento("chave-1", 100)

    with pytest.raises(bom.ChaveReutilizadaError):
        servidor.criar_pagamento("chave-1", 999)

    assert len(servidor.cobrancas) == 1


def test_bom_mesma_chave_enquanto_a_primeira_ainda_roda_e_conflito(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    conflitos: list[Exception] = []

    def reenvio_no_meio_da_cobranca(valor: int) -> None:
        try:
            servidor.criar_pagamento("chave-1", valor)
        except bom.EmProcessamentoError as erro:
            conflitos.append(erro)

    servidor = bom.ServidorDePagamentos(reenvio_no_meio_da_cobranca)

    servidor.criar_pagamento("chave-1", 100)

    assert len(conflitos) == 1
    assert len(servidor.cobrancas) == 1


def test_bom_falha_na_execucao_libera_a_chave_para_novo_envio(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    gateway_fora_do_ar = [True]

    def gateway(valor: int) -> None:
        if gateway_fora_do_ar[0]:
            raise ConnectionError("gateway fora")

    servidor = bom.ServidorDePagamentos(gateway)
    with pytest.raises(ConnectionError):
        servidor.criar_pagamento("chave-1", 100)
    gateway_fora_do_ar[0] = False

    pagamento = servidor.criar_pagamento("chave-1", 100)

    assert pagamento.valor == 100
    assert len(servidor.cobrancas) == 1


def test_bom_requisicoes_concorrentes_com_a_mesma_chave_cobram_uma_vez(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    servidor = bom.ServidorDePagamentos()

    def enviar(_: int) -> str:
        try:
            return str(servidor.criar_pagamento("chave-1", 100).id)
        except bom.EmProcessamentoError:
            return "conflito"

    with ThreadPoolExecutor(max_workers=8) as pool:
        resultados = list(pool.map(enviar, range(32)))

    assert len(servidor.cobrancas) == 1
    assert set(resultados) <= {"pay_1", "conflito"}
