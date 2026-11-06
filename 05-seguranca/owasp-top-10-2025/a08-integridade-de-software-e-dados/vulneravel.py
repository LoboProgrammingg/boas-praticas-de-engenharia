"""A08: webhook com assinatura comparada com ``==`` e sem janela de tempo.

Dois defeitos: a comparação vaza informação por tempo de resposta, e uma mensagem
legítima capturada vale para sempre (replay).
"""

import hashlib
import hmac
import json
from typing import Any


def assinar(segredo: bytes, corpo: bytes) -> str:
    return hmac.new(segredo, corpo, hashlib.sha256).hexdigest()


def processar_webhook(corpo: bytes, assinatura: str, segredo: bytes) -> dict[str, Any]:
    if assinar(segredo, corpo) != assinatura:
        raise PermissionError("assinatura inválida")
    evento: dict[str, Any] = json.loads(corpo)
    return evento
