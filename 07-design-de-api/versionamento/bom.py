"""Versionamento por data, ao estilo do Stripe: o código fala só a versão mais nova.

* Versões são datas (``2026-09-01``) e cada uma traz poucas mudanças incompatíveis.
* A conta é **fixada** (*pinned*) na versão mais recente na primeira requisição e continua
  nela até pedir para atualizar. Um cabeçalho (``Stripe-Version`` no Stripe) troca a versão
  de uma única requisição.
* O servidor monta sempre a representação **atual** e depois "volta no tempo", aplicando as
  mudanças de versão (``MudancaDeVersao``) até chegar à versão alvo.

Acrescentar um campo opcional ou um endpoint novo é compatível e não cria versão.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import cast

type Corpo = dict[str, object]

VERSAO_ATUAL = "2026-09-01"


class VersaoDesconhecidaError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class MudancaDeVersao:
    """Descreve como desfazer, na resposta, uma mudança introduzida em ``versao``."""

    versao: str
    descricao: str
    desfazer: Callable[[Corpo], Corpo]


def _saldo_volta_a_ser_inteiro(corpo: Corpo) -> Corpo:
    saldo = cast(Corpo, corpo["balance"])
    return {**corpo, "balance": saldo["amount"]}


def _full_name_volta_a_ser_name(corpo: Corpo) -> Corpo:
    resto = {chave: valor for chave, valor in corpo.items() if chave != "full_name"}
    return {**resto, "name": corpo["full_name"]}


MUDANCAS = (
    MudancaDeVersao(
        "2026-09-01", "balance vira objeto {amount, currency}", _saldo_volta_a_ser_inteiro
    ),
    MudancaDeVersao("2026-03-01", "name vira full_name", _full_name_volta_a_ser_name),
)
VERSOES_CONHECIDAS = frozenset({"2026-01-01", *(mudanca.versao for mudanca in MUDANCAS)})


def _representacao_atual(cliente_id: str) -> Corpo:
    return {
        "id": cliente_id,
        "full_name": "Ana Souza",
        "balance": {"amount": 1000, "currency": "BRL"},
    }


class Api:
    def __init__(self) -> None:
        self._versao_da_conta: dict[str, str] = {}

    def obter_cliente(
        self, conta: str, cliente_id: str, versao_no_cabecalho: str | None = None
    ) -> Corpo:
        alvo = versao_no_cabecalho or self._versao_da_conta.setdefault(conta, VERSAO_ATUAL)
        if alvo not in VERSOES_CONHECIDAS:
            raise VersaoDesconhecidaError(alvo)
        corpo = _representacao_atual(cliente_id)
        for mudanca in MUDANCAS:
            if mudanca.versao > alvo:
                corpo = mudanca.desfazer(corpo)
        return corpo

    def fixar_versao(self, conta: str, versao: str) -> None:
        if versao not in VERSOES_CONHECIDAS:
            raise VersaoDesconhecidaError(versao)
        self._versao_da_conta[conta] = versao
