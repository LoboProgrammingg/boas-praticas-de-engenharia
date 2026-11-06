import sqlite3
from collections.abc import Callable, Iterator
from types import ModuleType

import pytest

from conftest import CarregarExemplo


@pytest.fixture
def conexao() -> Iterator[sqlite3.Connection]:
    conexao = sqlite3.connect(":memory:")
    conexao.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, criado_em TEXT NOT NULL)")
    conexao.executemany(
        "INSERT INTO posts (id, criado_em) VALUES (?, ?)",
        [(n, f"2026-01-{n:02d}") for n in range(1, 7)],
    )
    yield conexao
    conexao.close()


def _novo_post_no_topo(conexao: sqlite3.Connection) -> None:
    conexao.execute("INSERT INTO posts (criado_em) VALUES ('2026-02-01')")


def _percorrer_com_cursor(
    bom: ModuleType, conexao: sqlite3.Connection, entre_paginas: Callable[[], object] | None = None
) -> list[int]:
    vistos: list[int] = []
    token = None
    while True:
        pagina = bom.listar(conexao, tamanho_da_pagina=2, token=token)
        vistos += pagina.ids
        token = pagina.proximo_token
        if token is None:
            return vistos
        if entre_paginas is not None:
            entre_paginas()


def test_ruim_item_novo_entre_paginas_repete_um_item(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    ruim = exemplo("ruim.py")

    pagina_1 = ruim.listar(conexao, pagina=1, tamanho=2)
    _novo_post_no_topo(conexao)
    pagina_2 = ruim.listar(conexao, pagina=2, tamanho=2)

    assert pagina_1 == [6, 5]
    assert pagina_2 == [5, 4]


def test_ruim_item_removido_entre_paginas_faz_um_item_ser_pulado(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    ruim = exemplo("ruim.py")

    pagina_1 = ruim.listar(conexao, pagina=1, tamanho=2)
    conexao.execute("DELETE FROM posts WHERE id = 6")
    pagina_2 = ruim.listar(conexao, pagina=2, tamanho=2)

    assert pagina_1 == [6, 5]
    assert pagina_2 == [3, 2]


def test_bom_percorre_tudo_sem_repetir_nem_pular(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")

    assert _percorrer_com_cursor(bom, conexao) == [6, 5, 4, 3, 2, 1]


def test_bom_item_novo_entre_paginas_nao_causa_duplicidade(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")

    vistos = _percorrer_com_cursor(bom, conexao, lambda: _novo_post_no_topo(conexao))

    assert vistos == [6, 5, 4, 3, 2, 1]


def test_bom_item_removido_entre_paginas_nao_faz_pular_ninguem(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")

    vistos = _percorrer_com_cursor(
        bom, conexao, lambda: conexao.execute("DELETE FROM posts WHERE id = 6")
    )

    assert vistos == [6, 5, 4, 3, 2, 1]


def test_bom_token_e_opaco_e_a_ultima_pagina_nao_tem_proximo(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")

    primeira = bom.listar(conexao, tamanho_da_pagina=4)
    ultima = bom.listar(conexao, tamanho_da_pagina=4, token=primeira.proximo_token)

    assert isinstance(primeira.proximo_token, str)
    assert not primeira.proximo_token.isdigit()
    assert ultima.ids == [2, 1]
    assert ultima.proximo_token is None


@pytest.mark.parametrize("token", ["isto-nao-e-base64!", "e30=", "WzEsIDJd"])
def test_bom_token_invalido_e_rejeitado(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection, token: str
) -> None:
    bom = exemplo("bom.py")

    with pytest.raises(bom.TokenInvalidoError):
        bom.listar(conexao, token=token)


def test_bom_tamanho_acima_do_maximo_e_reduzido_ao_maximo(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")
    conexao.executemany(
        "INSERT INTO posts (id, criado_em) VALUES (?, ?)",
        [(n, "2025-12-31") for n in range(100, 1200)],
    )

    pagina = bom.listar(conexao, tamanho_da_pagina=5000)

    assert len(pagina.ids) == bom.TAMANHO_MAXIMO
    assert pagina.proximo_token is not None


def test_bom_sem_tamanho_usa_o_padrao(
    exemplo: CarregarExemplo, conexao: sqlite3.Connection
) -> None:
    bom = exemplo("bom.py")

    pagina = bom.listar(conexao)

    assert len(pagina.ids) == 6
    assert bom.TAMANHO_PADRAO == 50
