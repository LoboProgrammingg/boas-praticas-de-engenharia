import logging
from collections.abc import Iterator
from itertools import count

import pytest

from conftest import CarregarExemplo


class Coletor(logging.Handler):
    def __init__(self) -> None:
        super().__init__()
        self.registros: list[logging.LogRecord] = []

    def emit(self, record: logging.LogRecord) -> None:
        self.registros.append(record)


@pytest.fixture
def coletor() -> Iterator[Coletor]:
    coletor = Coletor()
    raiz = logging.getLogger()
    nivel = raiz.level
    raiz.addHandler(coletor)
    raiz.setLevel(logging.INFO)
    yield coletor
    raiz.removeHandler(coletor)
    raiz.setLevel(nivel)


class RelogioFalso:
    def __init__(self) -> None:
        self.agora = 0.0

    def __call__(self) -> float:
        return self.agora


def _ids() -> Iterator[str]:
    return (f"id{n}" for n in count(1))


def test_ruim_duas_requisicoes_intercaladas_geram_linhas_indistinguiveis(
    exemplo: CarregarExemplo, coletor: Coletor
) -> None:
    ruim = exemplo("ruim.py")

    ruim.cobrar(valor=50, saldo=10)
    ruim.cobrar(valor=5, saldo=10)
    ruim.cobrar(valor=50, saldo=10)

    mensagens = [r.getMessage() for r in coletor.registros]
    assert mensagens.count("iniciando cobrança") == 3
    assert not any(hasattr(r, "trace_id") for r in coletor.registros)


def test_bom_spans_aninhados_compartilham_o_trace_e_apontam_para_o_pai(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")
    relogio, ids = RelogioFalso(), _ids()
    telemetria = bom.Telemetria(relogio, lambda: next(ids))

    with telemetria.span("POST /pedidos"):
        relogio.agora = 1.0
        with telemetria.span("cobrar"):
            relogio.agora = 3.5

    cobrar, pedido = telemetria.spans
    assert cobrar.trace_id == pedido.trace_id
    assert cobrar.pai == pedido.span_id
    assert pedido.pai is None
    assert (cobrar.duracao, pedido.duracao) == (2.5, 3.5)


def test_bom_cada_requisicao_tem_o_seu_trace(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    ids = _ids()
    telemetria = bom.Telemetria(RelogioFalso(), lambda: next(ids))

    with telemetria.span("requisicao 1"):
        pass
    with telemetria.span("requisicao 2"):
        pass

    primeira, segunda = telemetria.spans
    assert primeira.trace_id != segunda.trace_id


def test_bom_logs_carregam_o_trace_id_do_span_ativo(
    exemplo: CarregarExemplo, coletor: Coletor
) -> None:
    bom = exemplo("bom.py")
    ids = _ids()
    telemetria = bom.Telemetria(RelogioFalso(), lambda: next(ids))
    coletor.addFilter(bom.FiltroDeTrace())

    with telemetria.span("POST /pedidos"):
        logging.getLogger("teste").info("cobrança iniciada")
    logging.getLogger("teste").info("fora de qualquer requisição")

    dentro, fora = coletor.registros
    assert dentro.__dict__["trace_id"] == telemetria.spans[0].trace_id
    assert fora.__dict__["trace_id"] is None


def test_bom_metricas_contam_eventos(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    telemetria = bom.Telemetria(RelogioFalso(), lambda: "x")

    telemetria.contar("pagamento.falhou")
    telemetria.contar("pagamento.falhou")

    assert telemetria.metricas["pagamento.falhou"] == 2
