import json
from typing import Any

import pytest

from conftest import CarregarExemplo

SAIDA_ENVENENADA = json.dumps({"ferramenta": "apagar_tudo"})


def test_vulneravel_executa_a_ferramenta_destrutiva_escolhida_pelo_modelo(
    exemplo: CarregarExemplo,
) -> None:
    vulneravel = exemplo("vulneravel.py")
    loja = vulneravel.Loja(pedidos={1: "aberto", 2: "aberto"})

    vulneravel.executar_saida_do_llm(loja, SAIDA_ENVENENADA)

    assert loja.pedidos == {}


@pytest.fixture
def loja(exemplo: CarregarExemplo) -> Any:
    seguro = exemplo("seguro.py")
    return seguro.Loja(pedidos={1: seguro.Pedido(dono_id="ana"), 2: seguro.Pedido(dono_id="bia")})


def test_seguro_rejeita_ferramenta_fora_da_allowlist(exemplo: CarregarExemplo, loja: Any) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.SaidaInvalidaError):
        seguro.executar_saida_do_llm(loja, SAIDA_ENVENENADA, "ana")

    assert len(loja.pedidos) == 2


@pytest.mark.parametrize(
    "saida",
    [
        "isto não é json",
        '{"ferramenta": "consultar_pedido"}',
        '{"ferramenta": "consultar_pedido", "pedido_id": "1; DROP"}',
        '{"ferramenta": "consultar_pedido", "pedido_id": -1}',
        '{"ferramenta": "consultar_pedido", "pedido_id": 1, "usuario_id": "bia"}',
    ],
)
def test_seguro_rejeita_saida_malformada_ou_com_campos_extras(
    exemplo: CarregarExemplo, loja: Any, saida: str
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.SaidaInvalidaError):
        seguro.executar_saida_do_llm(loja, saida, "ana")


def test_seguro_executa_a_consulta_valida_do_proprio_usuario(
    exemplo: CarregarExemplo, loja: Any
) -> None:
    seguro = exemplo("seguro.py")

    resultado = seguro.executar_saida_do_llm(
        loja, '{"ferramenta": "consultar_pedido", "pedido_id": 1}', "ana"
    )

    assert resultado == "aberto"


def test_seguro_nao_deixa_o_modelo_tocar_em_pedido_de_outro_usuario(
    exemplo: CarregarExemplo, loja: Any
) -> None:
    seguro = exemplo("seguro.py")

    with pytest.raises(seguro.PedidoNaoEncontradoError):
        seguro.executar_saida_do_llm(
            loja, '{"ferramenta": "consultar_pedido", "pedido_id": 2}', "ana"
        )


def test_seguro_exige_aprovacao_humana_para_cancelar(exemplo: CarregarExemplo, loja: Any) -> None:
    seguro = exemplo("seguro.py")
    saida = '{"ferramenta": "cancelar_pedido", "pedido_id": 1}'

    with pytest.raises(seguro.AprovacaoNecessariaError):
        seguro.executar_saida_do_llm(loja, saida, "ana")
    assert loja.pedidos[1].status == "aberto"

    resultado = seguro.executar_saida_do_llm(loja, saida, "ana", aprovado_por_humano=True)

    assert resultado == "cancelado"
