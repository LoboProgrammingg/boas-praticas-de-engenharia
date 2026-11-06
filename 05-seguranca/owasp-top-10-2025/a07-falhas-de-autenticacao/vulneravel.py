"""A07: JWT aceito sem verificar a assinatura.

Qualquer pessoa fabrica um token com as claims que quiser, inclusive ``alg: none``.
"""

from typing import Any

import jwt


def validar_token(token: str, chave: bytes) -> dict[str, Any]:
    return jwt.decode(token, options={"verify_signature": False})
