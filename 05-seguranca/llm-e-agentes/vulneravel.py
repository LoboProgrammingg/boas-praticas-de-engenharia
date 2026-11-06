"""LLM05 + LLM06: a saída do modelo é executada como se fosse código confiável.

O texto gerado escolhe *qualquer* método da loja e os argumentos que quiser. Se um
documento envenenado (prompt injection) convencer o modelo, a ação acontece.
"""

import json
from dataclasses import dataclass, field


@dataclass
class Loja:
    pedidos: dict[int, str] = field(default_factory=dict)

    def consultar_pedido(self, pedido_id: int) -> str:
        return self.pedidos[pedido_id]

    def cancelar_pedido(self, pedido_id: int) -> None:
        self.pedidos[pedido_id] = "cancelado"

    def apagar_tudo(self) -> None:
        self.pedidos.clear()


def executar_saida_do_llm(loja: Loja, saida: str) -> object:
    chamada = json.loads(saida)
    return getattr(loja, chamada["ferramenta"])(**chamada.get("argumentos", {}))
