"""Autorização espalhada em ``if user.role == "admin"``.

A regra fica copiada em cada endpoint, compara string solta e esquece o tenant: um admin
da empresa A apaga a fatura da empresa B.
"""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Usuario:
    id: str
    tenant_id: str
    role: str


@dataclass(frozen=True, slots=True)
class Fatura:
    id: str
    tenant_id: str
    dono_id: str


def pode_excluir_fatura(usuario: Usuario, fatura: Fatura) -> bool:
    return usuario.role == "admin"


def pode_ler_fatura(usuario: Usuario, fatura: Fatura) -> bool:
    return usuario.role == "admin" or usuario.id == fatura.dono_id
