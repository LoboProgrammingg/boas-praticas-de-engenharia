"""O stub do serviço de CEP envelheceu e ninguém percebeu.

O consumidor foi testado contra um stub com os campos ``logradouro`` e ``cidade``. O
serviço real passou a responder ``street`` e ``city``. Os testes do consumidor continuam
verdes; em produção, ``KeyError``.
"""

from typing import Protocol


class ProvedorDeCep(Protocol):
    def consultar(self, cep: str) -> dict[str, str]: ...


class ProvedorStub:
    """Como o serviço respondia quando o stub foi escrito."""

    def consultar(self, cep: str) -> dict[str, str]:
        return {"logradouro": "Rua A", "cidade": "Salvador"}


class ProvedorReal:
    """Como o serviço responde hoje (simulado em processo, sem rede)."""

    def consultar(self, cep: str) -> dict[str, str]:
        return {"street": "Rua A", "city": "Salvador"}


class ClienteDeCep:
    def __init__(self, provedor: ProvedorDeCep) -> None:
        self._provedor = provedor

    def descricao(self, cep: str) -> str:
        resposta = self._provedor.consultar(cep)
        return f"{resposta['logradouro']}, {resposta['cidade']}"
