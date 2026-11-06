"""Tell: o pedido protege as próprias regras.

O estado só muda por métodos que checam as invariantes. Não há como confirmar um
pedido vazio nem alterar um pedido já confirmado.
"""


class PedidoVazioError(ValueError):
    pass


class PedidoJaConfirmadoError(ValueError):
    pass


class Pedido:
    def __init__(self) -> None:
        self._itens: list[str] = []
        self._confirmado = False

    @property
    def itens(self) -> tuple[str, ...]:
        return tuple(self._itens)

    @property
    def confirmado(self) -> bool:
        return self._confirmado

    def adicionar(self, item: str) -> None:
        if self._confirmado:
            raise PedidoJaConfirmadoError
        self._itens.append(item)

    def confirmar(self) -> None:
        if self._confirmado:
            raise PedidoJaConfirmadoError
        if not self._itens:
            raise PedidoVazioError
        self._confirmado = True
