"""Um único modelo para escrever e para ler.

Para listar o total gasto por cliente, o serviço carrega cada agregado ``Pedido`` completo
(com todos os itens) e soma em memória. A leitura paga o custo do modelo de escrita.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Pedido:
    id: str
    cliente: str
    itens: list[Decimal]


class ServicoDePedidos:
    def __init__(self) -> None:
        self._pedidos: dict[str, Pedido] = {}
        self.carregamentos = 0

    def fazer_pedido(self, id: str, cliente: str, itens: list[Decimal]) -> None:
        self._pedidos[id] = Pedido(id, cliente, itens)

    def _carregar(self, id: str) -> Pedido:
        self.carregamentos += 1
        return self._pedidos[id]

    def total_do_cliente(self, cliente: str) -> Decimal:
        ids = [p.id for p in self._pedidos.values() if p.cliente == cliente]
        return sum((sum(self._carregar(i).itens, Decimal("0")) for i in ids), Decimal("0"))
