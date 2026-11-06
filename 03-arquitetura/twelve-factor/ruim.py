"""Fator III violado: configuração e segredo como constantes no código.

Mudar o banco de homologação para produção exige editar (e recompilar/redeployar) o código,
e a chave de API vai parar no repositório.
"""

DATABASE_URL = "postgresql://app:senha-de-producao@db.interno:5432/app"
API_KEY = "chave-de-api-escrita-no-codigo"  # nunca faça isso com uma chave real
PORTA = 8000


def descrever() -> str:
    return f"banco={DATABASE_URL} porta={PORTA}"
