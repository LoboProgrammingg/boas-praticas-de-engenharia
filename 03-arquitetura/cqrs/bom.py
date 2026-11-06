"""CQRS mínimo: o comando altera o agregado; a consulta lê um modelo de leitura próprio.

* Comando (``FazerPedido``): passa pelo agregado ``Pedido`` e valida invariantes.
* Evento (``PedidoFeito``): avisa que algo aconteceu.
* Projeção (``TotalPorCliente``): modelo de leitura, atualizado pelo evento.
* Consulta (``total_do_cliente``): lê só a projeção, sem tocar no agregado.

Neste exemplo a projeção é atualizada na mesma chamada. Com bancos separados ela fica
*eventualmente consistente*, e esse é o custo real do padrão.
"""

from collections import defaultdict
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class PedidoFeito:
    cliente: str
    total: Decimal


@dataclass(frozen=True, slots=True)
class Pedido:
    id: str
    cliente: str
    itens: tuple[Decimal, ...]

    def __post_init__(self) -> None:
        if not self.itens:
            raise ValueError("pedido vazio")

    def total(self) -> Decimal:
        return sum(self.itens, Decimal("0"))


class TotalPorCliente:
    def __init__(self) -> None:
        self._totais: defaultdict[str, Decimal] = defaultdict(Decimal)

    def aplicar(self, evento: PedidoFeito) -> None:
        self._totais[evento.cliente] += evento.total

    def total_do_cliente(self, cliente: str) -> Decimal:
        return self._totais[cliente]


class FazerPedido:
    def __init__(self, projecao: TotalPorCliente) -> None:
        self.pedidos: dict[str, Pedido] = {}
        self._projecao = projecao

    def __call__(self, id: str, cliente: str, itens: tuple[Decimal, ...]) -> None:
        pedido = Pedido(id, cliente, itens)
        self.pedidos[id] = pedido
        self._projecao.aplicar(PedidoFeito(cliente, pedido.total()))
