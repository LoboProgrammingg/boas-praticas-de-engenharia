"""LLM05 + LLM06: a saída do modelo é entrada **não confiável**.

Controles aplicados, em camadas:

1. **allowlist de ferramentas**: só existem ``consultar_pedido`` e ``cancelar_pedido``;
2. **schema fechado** (pydantic, ``extra="forbid"``): nada de campos extras, como um
   ``usuario_id`` escolhido pelo modelo;
3. **identidade vem da sessão**, nunca do modelo: o pedido precisa ser do usuário atual;
4. **menor privilégio + humano no circuito**: a ferramenta destrutiva só roda com
   aprovação explícita de uma pessoa.
"""

from dataclasses import dataclass, field
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError


@dataclass
class Pedido:
    dono_id: str
    status: str = "aberto"


@dataclass
class Loja:
    pedidos: dict[int, Pedido] = field(default_factory=dict)


class ConsultarPedido(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    ferramenta: Literal["consultar_pedido"]
    pedido_id: int = Field(gt=0)


class CancelarPedido(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    ferramenta: Literal["cancelar_pedido"]
    pedido_id: int = Field(gt=0)


type Chamada = ConsultarPedido | CancelarPedido

_CHAMADA = TypeAdapter[Chamada](Annotated[Chamada, Field(discriminator="ferramenta")])


class SaidaInvalidaError(Exception):
    pass


class AprovacaoNecessariaError(Exception):
    pass


class PedidoNaoEncontradoError(Exception):
    pass


def _pedido_do_usuario(loja: Loja, pedido_id: int, usuario_id: str) -> Pedido:
    pedido = loja.pedidos.get(pedido_id)
    if pedido is None or pedido.dono_id != usuario_id:
        raise PedidoNaoEncontradoError(pedido_id)
    return pedido


def executar_saida_do_llm(
    loja: Loja, saida: str, usuario_id: str, *, aprovado_por_humano: bool = False
) -> str:
    try:
        chamada = _CHAMADA.validate_json(saida)
    except ValidationError as erro:
        raise SaidaInvalidaError("saída do modelo fora do contrato") from erro

    pedido = _pedido_do_usuario(loja, chamada.pedido_id, usuario_id)
    if isinstance(chamada, CancelarPedido):
        if not aprovado_por_humano:
            raise AprovacaoNecessariaError(chamada.ferramenta)
        pedido.status = "cancelado"
    return pedido.status
