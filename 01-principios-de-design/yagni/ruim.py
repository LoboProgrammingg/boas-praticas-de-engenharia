"""YAGNI violado: suporte a "N gateways" quando só existe um.

Interface, registro e fábrica foram escritos para um segundo gateway que ninguém pediu.
O uso mais simples exige configurar o registro antes.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Cobranca:
    id: str
    valor_em_centavos: int


class GatewayDePagamento(ABC):
    @abstractmethod
    def cobrar(self, valor_em_centavos: int, token: str) -> Cobranca: ...


class GatewayStripe(GatewayDePagamento):
    def cobrar(self, valor_em_centavos: int, token: str) -> Cobranca:
        return Cobranca(f"ch_{token}", valor_em_centavos)


class FabricaDeGateways:
    _registro: dict[str, type[GatewayDePagamento]] = {}  # noqa: RUF012

    @classmethod
    def registrar(cls, nome: str, gateway: type[GatewayDePagamento]) -> None:
        cls._registro[nome] = gateway

    @classmethod
    def criar(cls, nome: str) -> GatewayDePagamento:
        return cls._registro[nome]()


def cobrar(valor_em_centavos: int, token: str, gateway: str = "stripe") -> Cobranca:
    return FabricaDeGateways.criar(gateway).cobrar(valor_em_centavos, token)
