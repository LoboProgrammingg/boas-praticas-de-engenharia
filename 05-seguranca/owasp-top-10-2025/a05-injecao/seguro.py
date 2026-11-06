"""A05: consulta parametrizada para SQL e escape de saída para HTML.

* SQL: o driver envia o texto como *parâmetro*, nunca como parte do comando.
* HTML: ``html.escape`` neutraliza ``<``, ``>``, ``&`` e aspas no corpo do documento e em
  atributos entre aspas. Em app real, prefira um template engine com autoescape.
"""

import html
import sqlite3


def buscar_usuarios(conexao: sqlite3.Connection, nome: str) -> list[tuple[str, str]]:
    return conexao.execute("SELECT nome, email FROM usuarios WHERE nome = ?", (nome,)).fetchall()


def renderizar_comentario(texto: str) -> str:
    return f"<p>{html.escape(texto, quote=True)}</p>"
