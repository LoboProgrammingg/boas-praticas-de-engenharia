"""Log em texto livre, interpolado, que vaza dado pessoal.

O CPF vai para o log, a mensagem muda a cada ocorrência (impossível agrupar) e o motivo da
falha está misturado ao texto: só dá para encontrar com ``grep`` e adivinhação.
"""

import logging

log = logging.getLogger("ruim.logs")


def registrar_falha_de_pagamento(cpf: str, pedido_id: str, motivo: str) -> None:
    log.error(f"falha no pagamento do cliente {cpf} (pedido {pedido_id}): {motivo}")
