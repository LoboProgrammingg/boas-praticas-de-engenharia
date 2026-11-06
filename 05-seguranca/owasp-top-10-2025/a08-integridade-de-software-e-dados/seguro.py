"""A08: assinatura HMAC-SHA256 sobre o corpo **bruto**, com timestamp anti-replay.

* a assinatura cobre ``timestamp + "." + corpo``: o atacante não consegue reaproveitar
  a mesma assinatura com outro horário;
* o corpo é verificado como bytes, antes de qualquer ``json.loads``;
* a comparação usa ``hmac.compare_digest`` (tempo constante);
* mensagens fora da janela de tolerância são recusadas.

O esquema real (cabeçalhos, o que entra no HMAC) varia por provedor: siga a documentação
do provedor. Em produção, deduplique também pelo ID do evento (idempotência).
"""

import hashlib
import hmac
import json
from typing import Any

TOLERANCIA_SEGUNDOS = 300


class AssinaturaInvalidaError(Exception):
    pass


def assinar(segredo: bytes, timestamp: str, corpo: bytes) -> str:
    return hmac.new(segredo, timestamp.encode() + b"." + corpo, hashlib.sha256).hexdigest()


def processar_webhook(
    corpo: bytes, timestamp: str, assinatura: str, segredo: bytes, agora: float
) -> dict[str, Any]:
    if not timestamp.isascii() or not timestamp.isdigit():
        raise AssinaturaInvalidaError("timestamp inválido")
    if abs(agora - int(timestamp)) > TOLERANCIA_SEGUNDOS:
        raise AssinaturaInvalidaError("fora da janela de tolerância")
    esperada = assinar(segredo, timestamp, corpo)
    if not hmac.compare_digest(esperada.encode(), assinatura.encode()):
        raise AssinaturaInvalidaError("assinatura inválida")
    evento: dict[str, Any] = json.loads(corpo)
    return evento
