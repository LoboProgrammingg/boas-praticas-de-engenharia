"""Nomes que revelam intenção, unidade e efeito.

* O nome da função diz o que ela calcula; os parâmetros dizem o que são.
* Parâmetros nomeados e obrigatórios tornam impossível trocá-los sem perceber.
* ``buscar_*`` lê; ``obter_ou_criar_*`` avisa que pode escrever.
"""

from collections.abc import Mapping, MutableMapping
from decimal import Decimal

MESES_NO_ANO = 12


def valor_composto_em_um_ano(*, principal: Decimal, taxa_mensal: Decimal) -> Decimal:
    return principal * (1 + taxa_mensal) ** MESES_NO_ANO


def buscar_usuario(usuarios: Mapping[int, str], id_usuario: int) -> str | None:
    return usuarios.get(id_usuario)


def obter_ou_criar_usuario(usuarios: MutableMapping[int, str], id_usuario: int) -> str:
    if id_usuario not in usuarios:
        usuarios[id_usuario] = f"usuario-{id_usuario}"
    return usuarios[id_usuario]
