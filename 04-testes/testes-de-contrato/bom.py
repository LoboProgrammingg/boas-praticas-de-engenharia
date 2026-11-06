"""Um contrato explícito, verificado contra o dublê **e** contra o provedor real.

``CONTRATO`` descreve o que o consumidor espera da resposta. A mesma verificação roda no
fake usado pelos testes do consumidor e no provedor real. Se o provedor mudar (ou o fake
envelhecer), o teste de contrato falha, no ritmo das mudanças do provedor, e não só
quando o consumidor quebra em produção.
"""

from typing import Protocol

CONTRATO: dict[str, type] = {"logradouro": str, "cidade": str, "uf": str}


def violacoes(resposta: dict[str, object]) -> list[str]:
    problemas = [f"falta o campo '{campo}'" for campo in CONTRATO if campo not in resposta]
    problemas += [
        f"'{campo}' deveria ser {tipo.__name__}"
        for campo, tipo in CONTRATO.items()
        if campo in resposta and not isinstance(resposta[campo], tipo)
    ]
    return problemas


class ProvedorDeCep(Protocol):
    def consultar(self, cep: str) -> dict[str, object]: ...


class ProvedorFake:
    def consultar(self, cep: str) -> dict[str, object]:
        return {"logradouro": "Rua A", "cidade": "Salvador", "uf": "BA"}


class ProvedorReal:
    """Representa o serviço de verdade; num projeto real, faria a chamada HTTP."""

    def consultar(self, cep: str) -> dict[str, object]:
        return {"logradouro": "Rua A", "cidade": "Salvador", "uf": "BA", "ibge": 2927408}


class ClienteDeCep:
    def __init__(self, provedor: ProvedorDeCep) -> None:
        self._provedor = provedor

    def descricao(self, cep: str) -> str:
        resposta = self._provedor.consultar(cep)
        return f"{resposta['logradouro']}, {resposta['cidade']}/{resposta['uf']}"
