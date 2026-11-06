"""API3 (mass assignment): o corpo da requisição vira atributos do objeto.

O modelo aceita campos extras e a função copia *tudo* para o usuário, então o cliente
escolhe ``is_admin`` e ``tenant_id`` junto com ``display_name``.
"""

from dataclasses import dataclass

from pydantic import BaseModel, ConfigDict


@dataclass
class Usuario:
    id: int
    tenant_id: int
    display_name: str
    is_admin: bool = False
    senha_hash: str = "<hash>"


class AtualizarPerfil(BaseModel):
    model_config = ConfigDict(extra="allow")

    display_name: str


def atualizar_perfil(usuario: Usuario, corpo: dict[str, object]) -> Usuario:
    for campo, valor in AtualizarPerfil.model_validate(corpo).model_dump().items():
        setattr(usuario, campo, valor)
    return usuario


def perfil_para_resposta(usuario: Usuario) -> dict[str, object]:
    return dict(vars(usuario))
