"""Circuit breaker: fechado, aberto e meio-aberto.

* **Fechado**: chama normalmente e conta falhas consecutivas.
* **Aberto**: ao atingir ``limite_de_falhas``, rejeita sem chamar o fornecedor
  (``CircuitoAbertoError``) durante ``reabrir_apos`` segundos.
* **Meio-aberto**: passado esse tempo, deixa passar uma tentativa. Se der certo, fecha;
  se falhar, volta a abrir.

O relógio é injetado (nos testes, um relógio falso). Esta versão **não é thread-safe**; em
produção, use uma biblioteca madura ou proteja o estado com um lock.
"""

import time
from collections.abc import Callable
from typing import Literal

type Estado = Literal["fechado", "aberto", "meio-aberto"]


class CircuitoAbertoError(Exception):
    """O breaker está aberto: o fornecedor nem foi chamado."""


class CircuitBreaker:
    def __init__(
        self,
        *,
        limite_de_falhas: int = 3,
        reabrir_apos: float = 30.0,
        relogio: Callable[[], float] = time.monotonic,
        conta_como_falha: tuple[type[Exception], ...] = (Exception,),
    ) -> None:
        self._limite = limite_de_falhas
        self._reabrir_apos = reabrir_apos
        self._relogio = relogio
        self._conta_como_falha = conta_como_falha
        self._falhas = 0
        self._aberto_em: float | None = None

    @property
    def estado(self) -> Estado:
        if self._aberto_em is None:
            return "fechado"
        if self._relogio() - self._aberto_em < self._reabrir_apos:
            return "aberto"
        return "meio-aberto"

    def chamar[T](self, operacao: Callable[[], T]) -> T:
        if self.estado == "aberto":
            raise CircuitoAbertoError
        try:
            resultado = operacao()
        except self._conta_como_falha:
            self._registrar_falha()
            raise
        self._falhas = 0
        self._aberto_em = None
        return resultado

    def _registrar_falha(self) -> None:
        self._falhas += 1
        if self._falhas >= self._limite or self._aberto_em is not None:
            self._aberto_em = self._relogio()
