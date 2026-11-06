"""Logs soltos: quando duas requisições se intercalam, as linhas não dizem de quem são.

Não há identificador de correlação, nem duração, nem contagem. Para saber *qual* cobrança
falhou e *quanto* demorou, é preciso adivinhar lendo o arquivo.
"""

import logging

log = logging.getLogger("ruim.observabilidade")


def cobrar(valor: int, saldo: int) -> None:
    log.info("iniciando cobrança")
    if valor > saldo:
        log.error("erro ao cobrar")
        return
    log.info("cobrança concluída")
