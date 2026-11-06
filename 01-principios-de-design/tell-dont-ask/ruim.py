"""Ask: o pedido é um saco de dados e as regras vivem fora dele.

Quem usa ``ServicoDePedidos.confirmar`` respeita as regras. Quem escreve direto em
``pedido.status`` (um relatório, um script, outro serviço) cria um estado inválido.
"""

from dataclasses import dataclass, field


@dataclass
class Pedido:
    itens: list[str] = field(default_factory=list)
    status: str = "rascunho"


class ServicoDePedidos:
    def confirmar(self, pedido: Pedido) -> None:
        if pedido.status != "rascunho":
            raise ValueError("pedido já confirmado")
        if not pedido.itens:
            raise ValueError("pedido vazio")
        pedido.status = "confirmado"
