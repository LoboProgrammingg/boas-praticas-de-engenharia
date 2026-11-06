"""A04: senha guardada com SHA-256 puro.

SHA-256 é um hash rápido e sem sal: a mesma senha gera sempre o mesmo valor, o que
permite tabelas pré-computadas e força bruta em bilhões de tentativas por segundo.
"""

import hashlib


def hash_senha(senha: str) -> str:
    return hashlib.sha256(senha.encode()).hexdigest()


def verificar_senha(hash_guardado: str, senha: str) -> bool:
    return hash_senha(senha) == hash_guardado
