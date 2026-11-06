"""API3 (mass assignment e exposição excessiva): schemas fechados na entrada e na saída.

* entrada: ``extra="forbid"`` rejeita qualquer campo que o cliente não deveria enviar;
* saída: um modelo próprio decide o que sai, em vez de serializar o objeto inteiro.
"""

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict, Field


@dataclass
class Usuario:
    id: int
    tenant_id: int
    display_name: str
    is_admin: bool = False
    senha_hash: str = "<hash>"


class AtualizarPerfil(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    display_name: str = Field(min_length=1, max_length=80)


class PerfilPublico(BaseModel):
    id: int
    display_name: str


def atualizar_perfil(usuario: Usuario, corpo: dict[str, object]) -> Usuario:
    dados = AtualizarPerfil.model_validate(corpo)
    usuario.display_name = dados.display_name
    return usuario


def perfil_para_resposta(usuario: Usuario) -> dict[str, object]:
    return PerfilPublico(id=usuario.id, display_name=usuario.display_name).model_dump()
