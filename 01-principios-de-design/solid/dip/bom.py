"""DIP aplicado: a regra depende de uma abstração (Relogio) e o detalhe é injetado."""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


class Relogio(Protocol):
    def agora(self) -> datetime: ...


class RelogioDoSistema:
    def agora(self) -> datetime:
        return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class Cupom:
    codigo: str
    expira_em: datetime

    def esta_expirado(self, relogio: Relogio) -> bool:
        return relogio.agora() > self.expira_em
