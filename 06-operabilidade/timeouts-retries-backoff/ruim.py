"""Retry ingênuo: tenta tudo, sem teto, sem jitter e sem timeout.

* Repete qualquer exceção, inclusive erros permanentes (bug, validação).
* Repete também operações que mudam estado, sem nenhuma proteção contra duplicidade.
* A espera ``2 ** tentativa`` é idêntica para todos os clientes: quando o servidor cai,
  todos voltam juntos, nos mesmos instantes (*thundering herd*), e o derrubam de novo.
* A operação não recebe timeout: uma chamada pendurada trava o cliente para sempre.
"""

import time
from collections.abc import Callable


def com_retry[T](
    operacao: Callable[[], T],
    tentativas: int = 5,
    dormir: Callable[[float], None] = time.sleep,
) -> T:
    for tentativa in range(tentativas - 1):
        try:
            return operacao()
        except Exception:
            dormir(2**tentativa)
    return operacao()
