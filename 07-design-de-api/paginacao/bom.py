"""Paginação por cursor (keyset) com token opaco, ao estilo do Google AIP-158.

* ``tamanho_da_pagina`` tem padrão (50) e máximo (1000); valores maiores são reduzidos ao
  máximo, em vez de gerar erro.
* ``token`` é opaco para o cliente: aqui, a posição ``(criado_em, id)`` do último item em
  base64. Base64 só esconde o formato; em produção, assine ou criptografe o token (por
  exemplo, com HMAC) para que ninguém o forje nem dependa da sua estrutura.
* A consulta usa a posição, não um deslocamento: ``WHERE (criado_em, id) < (?, ?)``. Dados
  que entram ou saem antes do cursor não causam duplicidade nem pulo, e com um índice em
  ``(criado_em, id)`` o custo não cresce com a profundidade da página.
"""

import base64
import binascii
import json
import sqlite3
from dataclasses import dataclass

TAMANHO_PADRAO = 50
TAMANHO_MAXIMO = 1000


class TokenInvalidoError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Pagina:
    ids: list[int]
    proximo_token: str | None


def _codificar(criado_em: str, id_: int) -> str:
    return base64.urlsafe_b64encode(json.dumps([criado_em, id_]).encode()).decode()


def _decodificar(token: str) -> tuple[str, int]:
    try:
        criado_em, id_ = json.loads(base64.urlsafe_b64decode(token.encode()))
    except (binascii.Error, ValueError, TypeError) as erro:
        raise TokenInvalidoError(token) from erro
    if not isinstance(criado_em, str) or not isinstance(id_, int):
        raise TokenInvalidoError(token)
    return criado_em, id_


def listar(
    conexao: sqlite3.Connection, tamanho_da_pagina: int | None = None, token: str | None = None
) -> Pagina:
    tamanho = min(tamanho_da_pagina or TAMANHO_PADRAO, TAMANHO_MAXIMO)
    if token is None:
        linhas = conexao.execute(
            "SELECT id, criado_em FROM posts ORDER BY criado_em DESC, id DESC LIMIT ?",
            (tamanho + 1,),
        ).fetchall()
    else:
        criado_em, id_ = _decodificar(token)
        linhas = conexao.execute(
            "SELECT id, criado_em FROM posts WHERE (criado_em, id) < (?, ?) "
            "ORDER BY criado_em DESC, id DESC LIMIT ?",
            (criado_em, id_, tamanho + 1),
        ).fetchall()
    pagina = linhas[:tamanho]
    tem_mais = len(linhas) > tamanho
    proximo = _codificar(pagina[-1][1], pagina[-1][0]) if tem_mais else None
    return Pagina([linha[0] for linha in pagina], proximo)
