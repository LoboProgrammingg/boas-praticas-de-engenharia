"""Os três sinais da observabilidade, correlacionados por um ``trace_id``.

* **Trace**: ``Telemetria.span`` registra o caminho da requisição (spans aninhados).
* **Metric**: ``Telemetria.contar`` incrementa um contador.
* **Log**: ``FiltroDeTrace`` põe o ``trace_id`` em cada registro de log.

É um modelo mínimo, com relógio e gerador de ids injetados para ser determinístico. Em
produção use o SDK do OpenTelemetry, que implementa esses conceitos, a propagação entre
processos e os exportadores padronizados.
"""

import logging
from collections import Counter
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass

_trace_atual: ContextVar[str | None] = ContextVar("trace_atual", default=None)
_span_atual: ContextVar[str | None] = ContextVar("span_atual", default=None)


@dataclass(frozen=True, slots=True)
class Span:
    nome: str
    trace_id: str
    span_id: str
    pai: str | None
    duracao: float


class Telemetria:
    def __init__(self, relogio: Callable[[], float], gerar_id: Callable[[], str]) -> None:
        self._relogio = relogio
        self._gerar_id = gerar_id
        self.spans: list[Span] = []
        self.metricas: Counter[str] = Counter()

    @contextmanager
    def span(self, nome: str) -> Iterator[None]:
        trace_id = _trace_atual.get() or self._gerar_id()
        pai, span_id, inicio = _span_atual.get(), self._gerar_id(), self._relogio()
        token_trace, token_span = _trace_atual.set(trace_id), _span_atual.set(span_id)
        try:
            yield
        finally:
            _trace_atual.reset(token_trace)
            _span_atual.reset(token_span)
            self.spans.append(Span(nome, trace_id, span_id, pai, self._relogio() - inicio))

    def contar(self, nome: str) -> None:
        self.metricas[nome] += 1


class FiltroDeTrace(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.trace_id = _trace_atual.get()
        return True
