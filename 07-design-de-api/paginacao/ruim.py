"""Paginação por ``OFFSET``: instável quando os dados mudam entre uma página e outra.

``page=2`` significa "pule as primeiras 2 linhas de **agora**". Se entrou um item novo no
topo, o último da página 1 reaparece na página 2 (duplicado); se um item saiu, outro é
pulado. Além disso, o banco percorre e descarta todas as linhas puladas.
"""

import sqlite3


def listar(conexao: sqlite3.Connection, pagina: int, tamanho: int) -> list[int]:
    linhas = conexao.execute(
        "SELECT id FROM posts ORDER BY criado_em DESC, id DESC LIMIT ? OFFSET ?",
        (tamanho, (pagina - 1) * tamanho),
    ).fetchall()
    return [linha[0] for linha in linhas]
