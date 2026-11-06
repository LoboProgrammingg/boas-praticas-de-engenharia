"""Degradação elegante: perder um enfeite não derruba a página.

Quando o serviço de recomendação falha de um jeito *esperado* (``DependenciaIndisponivelError``), a
página responde com a melhor alternativa disponível, nesta ordem:

1. as últimas recomendações boas daquele usuário (possivelmente defasadas);
2. uma lista genérica de itens populares.

A degradação é **explícita** (``degradada=True``) e **observável** (um log de aviso).
Qualquer outro erro, como um bug, continua subindo: degradar não é engolir exceções.
"""

import logging
from dataclasses import dataclass
from typing import Protocol

POPULARES: tuple[str, ...] = ("mais-vendido-1", "mais-vendido-2", "mais-vendido-3")


class DependenciaIndisponivelError(Exception):
    """O serviço de recomendação está indisponível, lento ou com o circuito aberto."""


class Recomendador(Protocol):
    def recomendar(self, usuario: str) -> tuple[str, ...]: ...


@dataclass(frozen=True, slots=True)
class Pagina:
    usuario: str
    recomendacoes: tuple[str, ...]
    degradada: bool


class PaginaInicial:
    def __init__(self, recomendador: Recomendador, log: logging.Logger) -> None:
        self._recomendador = recomendador
        self._log = log
        self._ultimas_boas: dict[str, tuple[str, ...]] = {}

    def montar(self, usuario: str) -> Pagina:
        try:
            recomendacoes = self._recomendador.recomendar(usuario)
        except DependenciaIndisponivelError as erro:
            alternativa = self._ultimas_boas.get(usuario, POPULARES)
            self._log.warning(
                "recomendacoes_degradadas",
                extra={"contexto": {"usuario": usuario, "motivo": str(erro)}},
            )
            return Pagina(usuario, alternativa, degradada=True)
        self._ultimas_boas[usuario] = recomendacoes
        return Pagina(usuario, recomendacoes, degradada=False)
