"""Chamada direta a um fornecedor que está falhando, sem nenhuma proteção.

Cada requisição do usuário insiste no fornecedor lento ou fora do ar. Cada uma paga o
timeout inteiro, segura recursos enquanto espera e aumenta a carga sobre quem precisa se
recuperar: a falha de um serviço vira falha em cascata.
"""

from collections.abc import Callable


def buscar_recomendacoes(fornecedor: Callable[[str], list[str]], usuario: str) -> list[str]:
    return fornecedor(usuario)
