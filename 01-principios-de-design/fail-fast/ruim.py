"""Falha silenciosa: qualquer problema vira a porta padrão.

Um ``PORT=80a`` digitado errado em produção sobe o serviço na 8080 e ninguém
percebe até o balanceador não achar a aplicação.
"""

import os


def porta() -> int:
    try:
        return int(os.environ["PORT"])
    except Exception:
        return 8080
