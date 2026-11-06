"""Especificação escrita à mão, separada do código: já nasce desatualizada.

A documentação diz que a resposta tem ``valor`` (string) e ``moeda``. O código devolve
``total_centavos`` (inteiro) e não tem ``moeda``. Quem gera um cliente a partir da
especificação recebe um cliente que não funciona.
"""

from typing import Any

ESPECIFICACAO: dict[str, Any] = {
    "openapi": "3.2.0",
    "info": {"title": "Pedidos", "version": "1.0.0"},
    "paths": {
        "/pedidos/{pedido_id}": {
            "get": {
                "responses": {
                    "200": {
                        "description": "O pedido",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "required": ["id", "valor", "moeda"],
                                    "properties": {
                                        "id": {"type": "string"},
                                        "valor": {"type": "string"},
                                        "moeda": {"type": "string"},
                                    },
                                }
                            }
                        },
                    }
                }
            }
        }
    },
}


def obter_pedido(pedido_id: str) -> dict[str, object]:
    return {"id": pedido_id, "total_centavos": 1990}
