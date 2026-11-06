import json
from typing import Any

from conftest import CarregarExemplo

TIPOS_JSON: dict[str, type | tuple[type, ...]] = {
    "string": str,
    "integer": int,
    "number": (int, float),
    "boolean": bool,
    "object": dict,
    "array": list,
}


def _resolver(schema: dict[str, Any], componentes: dict[str, Any]) -> dict[str, Any]:
    if "$ref" in schema:
        return componentes[schema["$ref"].rsplit("/", 1)[1]]  # type: ignore[no-any-return]
    return schema


def divergencias(
    schema: dict[str, Any], corpo: Any, componentes: dict[str, Any], caminho: str = "$"
) -> list[str]:
    """Compara um corpo real com o schema documentado (um subconjunto de JSON Schema)."""
    schema = _resolver(schema, componentes)
    tipo = schema.get("type")
    if tipo is not None and not isinstance(corpo, TIPOS_JSON[tipo]):
        return [f"{caminho}: documentado como {tipo}, recebido {type(corpo).__name__}"]
    if tipo == "array":
        return [
            problema
            for indice, elemento in enumerate(corpo)
            for problema in divergencias(
                schema["items"], elemento, componentes, f"{caminho}[{indice}]"
            )
        ]
    if tipo != "object":
        return []
    propriedades = schema.get("properties", {})
    problemas = [
        f"{caminho}.{campo}: documentado como obrigatório, ausente"
        for campo in schema.get("required", [])
        if campo not in corpo
    ]
    problemas += [
        f"{caminho}.{campo}: presente na resposta, não documentado"
        for campo in corpo
        if campo not in propriedades
    ]
    for campo, subschema in propriedades.items():
        if campo in corpo:
            problemas += divergencias(subschema, corpo[campo], componentes, f"{caminho}.{campo}")
    return problemas


def test_ruim_a_especificacao_escrita_a_mao_diverge_da_resposta_real(
    exemplo: CarregarExemplo,
) -> None:
    ruim = exemplo("ruim.py")
    schema = ruim.ESPECIFICACAO["paths"]["/pedidos/{pedido_id}"]["get"]["responses"]["200"][
        "content"
    ]["application/json"]["schema"]

    problemas = divergencias(schema, ruim.obter_pedido("p1"), {})

    assert problemas == [
        "$.valor: documentado como obrigatório, ausente",
        "$.moeda: documentado como obrigatório, ausente",
        "$.total_centavos: presente na resposta, não documentado",
    ]


def test_bom_a_resposta_real_obedece_a_especificacao_gerada(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    spec = bom.construir_openapi()
    operacao = spec["paths"]["/pedidos/{pedido_id}"]["get"]

    for pedido_id, status in (("p1", 200), ("inexistente", 404)):
        codigo, corpo = bom.obter_pedido(pedido_id)
        schema = next(iter(operacao["responses"][str(status)]["content"].values()))["schema"]
        assert codigo == status
        assert divergencias(schema, corpo, spec["components"]["schemas"]) == []


def test_bom_documento_declara_a_versao_e_a_operacao(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    spec = bom.construir_openapi()
    operacao = spec["paths"]["/pedidos/{pedido_id}"]["get"]

    assert spec["openapi"] == "3.2.0"
    assert operacao["operationId"] == "obterPedido"
    assert operacao["parameters"][0]["in"] == "path"
    assert set(operacao["responses"]) == {"200", "404"}


def test_bom_erros_sao_documentados_como_problem_json(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")

    resposta_404 = bom.construir_openapi()["paths"]["/pedidos/{pedido_id}"]["get"]["responses"][
        "404"
    ]

    assert list(resposta_404["content"]) == ["application/problem+json"]


def test_bom_todo_ref_aponta_para_um_schema_que_existe(exemplo: CarregarExemplo) -> None:
    bom = exemplo("bom.py")
    spec = bom.construir_openapi()
    texto = json.dumps(spec)
    schemas = spec["components"]["schemas"]

    referencias = {parte.split('"')[0].rsplit("/", 1)[1] for parte in texto.split('"$ref": "')[1:]}

    assert {"Pedido", "Problema", "Item"} <= set(schemas)
    assert referencias <= set(schemas)


def test_bom_schema_gerado_reflete_obrigatoriedade_e_restricoes_do_modelo(
    exemplo: CarregarExemplo,
) -> None:
    bom = exemplo("bom.py")

    schemas = bom.construir_openapi()["components"]["schemas"]

    assert set(schemas["Pedido"]["required"]) == {"id", "status", "itens", "total_centavos"}
    assert schemas["Pedido"]["properties"]["status"]["enum"] == ["aberto", "pago"]
    assert schemas["Item"]["properties"]["quantidade"]["minimum"] == 1
