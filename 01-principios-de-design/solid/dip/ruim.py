"""DIP violado: a regra de negócio cria e conhece os detalhes concretos.

Para testar se um cupom expirou é preciso controlar o relógio do sistema.
"""

from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass
class Cupom:
    codigo: str
    expira_em: datetime

    def esta_expirado(self) -> bool:
        return datetime.now(UTC) > self.expira_em
