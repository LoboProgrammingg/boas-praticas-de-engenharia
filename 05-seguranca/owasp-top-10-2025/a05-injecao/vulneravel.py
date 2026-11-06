"""A05: SQL por interpolação de string e HTML sem escape.

A entrada do usuário vira parte do código (SQL e HTML) em vez de ficar como dado.
"""

import sqlite3


def buscar_usuarios(conexao: sqlite3.Connection, nome: str) -> list[tuple[str, str]]:
    consulta = f"SELECT nome, email FROM usuarios WHERE nome = '{nome}'"
    return conexao.execute(consulta).fetchall()


def renderizar_comentario(texto: str) -> str:
    return f"<p>{texto}</p>"
