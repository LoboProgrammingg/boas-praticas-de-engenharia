"""A10: exceções tratadas de forma a vazar informação, abrir acesso e deixar estado pela metade.

* ``responder_erro`` devolve ao cliente a mensagem interna da exceção (CWE-209);
* ``esta_autorizado`` falha **aberto**: se a checagem quebra, libera (CWE-636);
* ``transferir`` debita e confirma antes de saber se o crédito vai dar certo.
"""

import sqlite3
from collections.abc import Callable


def responder_erro(erro: Exception) -> tuple[int, dict[str, str]]:
    return 500, {"detail": str(erro)}


def esta_autorizado(verificar: Callable[[], bool]) -> bool:
    try:
        return verificar()
    except Exception:
        return True


def transferir(conexao: sqlite3.Connection, origem: int, destino: int, valor: int) -> None:
    conexao.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ?", (valor, origem))
    conexao.commit()
    creditado = conexao.execute(
        "UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, destino)
    )
    if creditado.rowcount == 0:
        raise LookupError("conta de destino inexistente")
    conexao.commit()
