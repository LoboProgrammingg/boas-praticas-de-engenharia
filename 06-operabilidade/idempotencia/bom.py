"""Idempotência por ``Idempotency-Key``: a mesma chave devolve o mesmo resultado.

Fluxo (inspirado no rascunho IETF do cabeçalho ``Idempotency-Key``):

1. Chave nova: registra a chave com a impressão digital (*fingerprint*) do payload, executa
   e guarda o resultado.
2. Mesma chave e mesmo payload, resultado pronto: devolve o resultado guardado, sem cobrar.
3. Mesma chave com payload diferente: ``ChaveReutilizadaError`` (o rascunho sugere HTTP 422).
4. Mesma chave enquanto a primeira requisição ainda roda: ``EmProcessamentoError`` (409).
5. Se a execução falhar, a chave é liberada para que um novo envio possa tentar.

Em produção, o registro é uma tabela com ``UNIQUE(idempotency_key)`` e expiração, gravada
na mesma transação do efeito; aqui um dicionário protegido por lock ilustra a lógica.
"""

import hashlib
import json
import threading
from collections.abc import Callable
from dataclasses import dataclass


class ChaveReutilizadaError(Exception):
    """A mesma chave chegou com um payload diferente (HTTP 422 no rascunho)."""


class EmProcessamentoError(Exception):
    """A primeira requisição com esta chave ainda não terminou (HTTP 409 no rascunho)."""


@dataclass(frozen=True, slots=True)
class Pagamento:
    id: str
    valor: int


@dataclass(slots=True)
class _Registro:
    impressao: str
    resultado: Pagamento | None = None


def _impressao(valor: int, moeda: str) -> str:
    corpo = json.dumps({"valor": valor, "moeda": moeda}, sort_keys=True)
    return hashlib.sha256(corpo.encode()).hexdigest()


class ServidorDePagamentos:
    """``ao_cobrar`` representa a chamada ao gateway externo (que pode falhar ou demorar)."""

    def __init__(self, ao_cobrar: Callable[[int], None] = lambda valor: None) -> None:
        self._ao_cobrar = ao_cobrar
        self.cobrancas: list[Pagamento] = []
        self._registros: dict[str, _Registro] = {}
        self._trava = threading.Lock()

    def criar_pagamento(self, chave: str, valor: int, moeda: str = "BRL") -> Pagamento:
        impressao = _impressao(valor, moeda)
        with self._trava:
            registro = self._registros.get(chave)
            if registro is None:
                self._registros[chave] = _Registro(impressao)
            elif registro.impressao != impressao:
                raise ChaveReutilizadaError(chave)
            elif registro.resultado is None:
                raise EmProcessamentoError(chave)
            else:
                return registro.resultado
        return self._executar(chave, valor)

    def _executar(self, chave: str, valor: int) -> Pagamento:
        try:
            pagamento = self._cobrar(valor)
        except Exception:
            with self._trava:
                del self._registros[chave]
            raise
        with self._trava:
            self._registros[chave].resultado = pagamento
        return pagamento

    def _cobrar(self, valor: int) -> Pagamento:
        self._ao_cobrar(valor)
        pagamento = Pagamento(f"pay_{len(self.cobrancas) + 1}", valor)
        self.cobrancas.append(pagamento)
        return pagamento
