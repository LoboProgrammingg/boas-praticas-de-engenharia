"""A04: Argon2id com os parâmetros mínimos do OWASP Password Storage Cheat Sheet.

m=19456 KiB (19 MiB), t=2, p=1. O sal é aleatório por senha e vem embutido no hash,
junto dos parâmetros, o que permite aumentar o custo depois (``precisa_rehash``).
"""

from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

_HASHER = PasswordHasher(time_cost=2, memory_cost=19_456, parallelism=1)


def hash_senha(senha: str) -> str:
    return _HASHER.hash(senha)


def verificar_senha(hash_guardado: str, senha: str) -> bool:
    try:
        return _HASHER.verify(hash_guardado, senha)
    except (VerificationError, InvalidHashError):
        return False


def precisa_rehash(hash_guardado: str) -> bool:
    return _HASHER.check_needs_rehash(hash_guardado)
