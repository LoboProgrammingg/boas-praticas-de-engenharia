"""A07: verificação de JWT conforme o RFC 8725 (JWT BCP).

* lista **fixa** de algoritmos (nunca derivada do header do próprio token);
* ``exp``, ``iat``, ``sub``, ``aud`` e ``iss`` obrigatórios;
* ``aud`` e ``iss`` conferidos contra os valores esperados;
* uma chave, um algoritmo (não misture HS256 e RS256 no mesmo verificador).
"""

from datetime import UTC, datetime, timedelta
from typing import Any

import jwt

ALGORITMOS = ["HS256"]
AUDIENCIA = "api.exemplo.test"
EMISSOR = "https://auth.exemplo.test"
VALIDADE = timedelta(minutes=15)
FOLGA_DE_RELOGIO_SEGUNDOS = 10


class TokenInvalidoError(Exception):
    pass


def emitir_token(chave: bytes, subject: str, agora: datetime | None = None) -> str:
    agora = agora or datetime.now(UTC)
    claims = {
        "sub": subject,
        "aud": AUDIENCIA,
        "iss": EMISSOR,
        "iat": agora,
        "exp": agora + VALIDADE,
    }
    return jwt.encode(claims, chave, algorithm=ALGORITMOS[0])


def validar_token(token: str, chave: bytes) -> dict[str, Any]:
    try:
        return jwt.decode(
            token,
            chave,
            algorithms=ALGORITMOS,
            audience=AUDIENCIA,
            issuer=EMISSOR,
            options={"require": ["exp", "iat", "sub", "aud", "iss"]},
            leeway=FOLGA_DE_RELOGIO_SEGUNDOS,
        )
    except jwt.InvalidTokenError as erro:
        raise TokenInvalidoError(str(erro)) from erro
