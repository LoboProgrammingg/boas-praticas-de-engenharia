"""Logs estruturados: um evento por linha, em JSON, com campos pesquisáveis e sem PII.

``FormatadorJson`` usa só a biblioteca padrão (``logging`` + ``json``). O evento tem um nome
estável (``event``) e o contexto vai em campos; valores de chaves sensíveis são mascarados
por segurança, mas o objetivo é **nunca passá-los** ao logger.
"""

import json
import logging
from datetime import UTC, datetime

CHAVES_SENSIVEIS = frozenset({"cpf", "senha", "password", "token", "cartao", "authorization"})
MASCARA = "[REDACTED]"


def mascarar(contexto: dict[str, object]) -> dict[str, object]:
    return {
        chave: MASCARA if chave.lower() in CHAVES_SENSIVEIS else valor
        for chave, valor in contexto.items()
    }


class FormatadorJson(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        base: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "event": record.getMessage(),
        }
        if record.exc_info:
            base["exc"] = self.formatException(record.exc_info)
        contexto: dict[str, object] = getattr(record, "contexto", {})
        return json.dumps({**mascarar(contexto), **base}, ensure_ascii=False, default=str)


def registrar_falha_de_pagamento(log: logging.Logger, pedido_id: str, motivo: str) -> None:
    log.error("payment_failed", extra={"contexto": {"pedido_id": pedido_id, "motivo": motivo}})
