"""Especificação OpenAPI **gerada do código**: os modelos Pydantic são a fonte única.

Os mesmos modelos validam a resposta e produzem o JSON Schema que vai para o documento
OpenAPI, então a documentação não diverge da implementação. O documento declara a versão
``3.2.0`` da OpenAPI Specification, e os erros são ``application/problem+json``.
"""

from typing import Any, Literal

from pydantic import BaseModel, Field

VERSAO_OPENAPI = "3.2.0"


class Item(BaseModel):
    sku: str
    quantidade: int = Field(ge=1)


class Pedido(BaseModel):
    id: str
    status: Literal["aberto", "pago"]
    itens: list[Item]
    total_centavos: int


class Problema(BaseModel):
    type: str = "about:blank"
    title: str
    status: int
    detail: str | None = None


def _componentes() -> dict[str, Any]:
    componentes: dict[str, Any] = {}
    for modelo in (Pedido, Problema):
        schema = modelo.model_json_schema(ref_template="#/components/schemas/{model}")
        componentes.update(schema.pop("$defs", {}))
        componentes[modelo.__name__] = schema
    return componentes


def construir_openapi() -> dict[str, Any]:
    return {
        "openapi": VERSAO_OPENAPI,
        "info": {"title": "Pedidos", "version": "1.0.0"},
        "paths": {
            "/pedidos/{pedido_id}": {
                "get": {
                    "operationId": "obterPedido",
                    "summary": "Busca um pedido pelo identificador",
                    "parameters": [
                        {
                            "name": "pedido_id",
                            "in": "path",
                            "required": True,
                            "schema": {"type": "string"},
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "O pedido",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Pedido"}
                                }
                            },
                        },
                        "404": {
                            "description": "Pedido não encontrado",
                            "content": {
                                "application/problem+json": {
                                    "schema": {"$ref": "#/components/schemas/Problema"}
                                }
                            },
                        },
                    },
                }
            }
        },
        "components": {"schemas": _componentes()},
    }


PEDIDOS = {
    "p1": Pedido(
        id="p1", status="pago", itens=[Item(sku="CAFE", quantidade=2)], total_centavos=1990
    )
}


def obter_pedido(pedido_id: str) -> tuple[int, dict[str, Any]]:
    pedido = PEDIDOS.get(pedido_id)
    if pedido is None:
        problema = Problema(title="Not Found", status=404, detail=f"Pedido {pedido_id} não existe.")
        return 404, problema.model_dump(mode="json", exclude_none=True)
    return 200, pedido.model_dump(mode="json")
