"""Policy engine mínimo: regras declaradas em um lugar só, negar por padrão.

* ``PoliticaDeAcesso.pode`` é o único ponto de decisão; endpoints só perguntam.
* O tenant é verificado **antes** de qualquer regra: nenhuma regra consegue esquecê-lo.
* Ação desconhecida, regra que lança exceção e lista de regras vazia resultam em **negado**.
* Uma ação é permitida quando *pelo menos uma* de suas regras aprova.
"""

from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Usuario:
    id: str
    tenant_id: str
    papeis: frozenset[str]


@dataclass(frozen=True, slots=True)
class Recurso:
    tipo: str
    tenant_id: str
    dono_id: str


type Regra = Callable[[Usuario, Recurso], bool]


class AcessoNegadoError(Exception):
    status_http = 404


def tem_papel(papel: str) -> Regra:
    return lambda usuario, _recurso: papel in usuario.papeis


def eh_dono(usuario: Usuario, recurso: Recurso) -> bool:
    return usuario.id == recurso.dono_id


class PoliticaDeAcesso:
    def __init__(self, regras: Mapping[str, Sequence[Regra]]) -> None:
        self._regras = dict(regras)

    def pode(self, usuario: Usuario, acao: str, recurso: Recurso) -> bool:
        if usuario.tenant_id != recurso.tenant_id:
            return False
        try:
            return any(regra(usuario, recurso) for regra in self._regras.get(acao, ()))
        except Exception:
            return False

    def exigir(self, usuario: Usuario, acao: str, recurso: Recurso) -> None:
        if not self.pode(usuario, acao, recurso):
            raise AcessoNegadoError(acao)


POLITICA_DE_FATURAS = PoliticaDeAcesso(
    {
        "fatura:ler": [eh_dono, tem_papel("financeiro")],
        "fatura:excluir": [tem_papel("admin")],
    }
)
