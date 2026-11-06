import random
from types import ModuleType

import pytest

from conftest import CarregarExemplo


class OperacaoQueFalha:
    def __init__(self, falhas: int, erro: type[Exception]) -> None:
        self.falhas = falhas
        self.erro = erro
        self.chamadas = 0
        self.timeouts: list[float] = []

    def __call__(self, timeout: float = 0.0) -> str:
        self.chamadas += 1
        self.timeouts.append(timeout)
        if self.chamadas <= self.falhas:
            raise self.erro("falhou")
        return "ok"


def _esperas_de_um_cliente_ruim(ruim: ModuleType) -> list[float]:
    esperas: list[float] = []
    operacao = OperacaoQueFalha(falhas=3, erro=RuntimeError)
    ruim.com_retry(operacao, dormir=esperas.append)
    return esperas


def test_ruim_todos_os_clientes_esperam_exatamente_o_mesmo_tempo(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")

    esperas_por_cliente = [_esperas_de_um_cliente_ruim(ruim) for _ in range(100)]

    assert esperas_por_cliente[0] == [1, 2, 4]
    assert {tuple(esperas) for esperas in esperas_por_cliente} == {(1, 2, 4)}


def test_ruim_repete_ate_erro_permanente(exemplo: CarregarExemplo) -> None:
    ruim = exemplo("ruim.py")
    operacao = OperacaoQueFalha(falhas=99, erro=ValueError)

    with pytest.raises(ValueError, match="falhou"):
        ruim.com_retry(operacao, dormir=lambda _: None)

    assert operacao.chamadas == 5


def test_bom_clientes_diferentes_esperam_tempos_diferentes(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    primeiras_esperas: set[float] = set()

    for semente in range(100):
        esperas: list[float] = []
        operacao = OperacaoQueFalha(falhas=1, erro=bom.FalhaTransitoriaError)
        bom.com_retry(
            operacao,
            idempotente=True,
            dormir=esperas.append,
            sorteio=random.Random(semente).uniform,  # noqa: S311
        )
        primeiras_esperas.add(esperas[0])

    assert len(primeiras_esperas) > 90


def test_bom_espera_fica_entre_zero_e_o_teto_exponencial(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    sorteio = random.Random(1).uniform  # noqa: S311

    for tentativa in range(10):
        espera = bom.calcular_espera(tentativa, base=0.1, teto=2.0, sorteio=sorteio)
        assert 0.0 <= espera <= min(2.0, 0.1 * 2**tentativa)


def test_bom_sorteio_recebe_o_teto_que_cresce_e_para_no_limite(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    limites: list[float] = []

    def sorteio(minimo: float, maximo: float) -> float:
        limites.append(maximo)
        return maximo

    for tentativa in range(7):
        bom.calcular_espera(tentativa, base=0.1, teto=2.0, sorteio=sorteio)

    assert limites == [0.1, 0.2, 0.4, 0.8, 1.6, 2.0, 2.0]


def test_bom_recupera_apos_falhas_transitorias_e_passa_timeout_a_cada_tentativa(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    operacao = OperacaoQueFalha(falhas=2, erro=bom.FalhaTransitoriaError)
    esperas: list[float] = []

    resultado = bom.com_retry(
        operacao, idempotente=True, politica=bom.Politica(timeout=0.5), dormir=esperas.append
    )

    assert resultado == "ok"
    assert operacao.timeouts == [0.5, 0.5, 0.5]
    assert len(esperas) == 2


def test_bom_desiste_no_limite_de_tentativas_e_propaga_o_erro(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    operacao = OperacaoQueFalha(falhas=99, erro=bom.FalhaTransitoriaError)
    esperas: list[float] = []

    with pytest.raises(bom.FalhaTransitoriaError):
        bom.com_retry(
            operacao, idempotente=True, politica=bom.Politica(tentativas=4), dormir=esperas.append
        )

    assert operacao.chamadas == 4
    assert len(esperas) == 3


def test_bom_erro_permanente_nao_e_repetido(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    operacao = OperacaoQueFalha(falhas=99, erro=ValueError)

    with pytest.raises(ValueError, match="falhou"):
        bom.com_retry(operacao, idempotente=True, dormir=lambda _: None)

    assert operacao.chamadas == 1


def test_bom_operacao_nao_idempotente_nao_e_repetida(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    operacao = OperacaoQueFalha(falhas=99, erro=bom.FalhaTransitoriaError)

    with pytest.raises(bom.FalhaTransitoriaError):
        bom.com_retry(operacao, idempotente=False, dormir=lambda _: None)

    assert operacao.chamadas == 1
