"""Alta coesão e baixo acoplamento: um conceito por unidade, dependências por parâmetro.

* ``Cpf``: tudo sobre documento num lugar só.
* ``TabelaDeFrete``: tudo sobre preço de entrega num lugar só.
* ``ServicoDeSms``: recebe o canal de envio (uma porta estreita), sem estado global.
"""

from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol


@dataclass(frozen=True, slots=True)
class Cpf:
    numero: str

    def __post_init__(self) -> None:
        if len(self.numero) != 11 or not self.numero.isdigit():
            raise ValueError("CPF deve ter 11 dígitos")

    def formatado(self) -> str:
        return f"{self.numero[:3]}.{self.numero[3:6]}.{self.numero[6:9]}-{self.numero[9:]}"


@dataclass(frozen=True, slots=True)
class TabelaDeFrete:
    base: Decimal = Decimal("10")
    por_km: Decimal = Decimal("0.5")

    def calcular(self, distancia_em_km: int) -> Decimal:
        return self.base + self.por_km * distancia_em_km


class CanalDeSms(Protocol):
    def enviar(self, telefone: str, mensagem: str) -> None: ...


class ServicoDeSms:
    def __init__(self, canal: CanalDeSms) -> None:
        self._canal = canal

    def avisar_entrega(self, telefone: str, pedido: str) -> None:
        self._canal.enviar(telefone, f"Seu pedido {pedido} saiu para entrega.")
