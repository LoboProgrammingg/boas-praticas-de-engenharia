"""A10: falhar fechado, responder genérico e desfazer tudo.

* ``esta_autorizado``: qualquer exceção na checagem resulta em **negado** (fail closed);
* ``responder_erro``: o cliente recebe só uma mensagem genérica e um ``error_id``; o
  detalhe técnico vai para o log, com o mesmo ``error_id`` para correlação;
* ``transferir``: as duas pontas rodam numa única transação com rollback completo.
"""

import logging
import sqlite3
import uuid
from collections.abc import Callable

log = logging.getLogger("app")


def responder_erro(erro: Exception) -> tuple[int, dict[str, str]]:
    error_id = uuid.uuid4().hex
    log.error("erro não tratado", extra={"error_id": error_id}, exc_info=erro)
    return 500, {"detail": "internal error", "error_id": error_id}


def esta_autorizado(verificar: Callable[[], bool]) -> bool:
    try:
        return verificar() is True
    except Exception:
        log.exception("falha ao verificar autorização; acesso negado")
        return False


def transferir(conexao: sqlite3.Connection, origem: int, destino: int, valor: int) -> None:
    with conexao:
        conexao.execute("UPDATE contas SET saldo = saldo - ? WHERE id = ?", (valor, origem))
        creditado = conexao.execute(
            "UPDATE contas SET saldo = saldo + ? WHERE id = ?", (valor, destino)
        )
        if creditado.rowcount == 0:
            raise LookupError("conta de destino inexistente")
