"""Uma dependência opcional derruba a página inteira.

As recomendações são um enfeite da página inicial, mas se o serviço de recomendação falha, o
usuário não consegue nem ver a página.
"""

from typing import Protocol


class Recomendador(Protocol):
    def recomendar(self, usuario: str) -> tuple[str, ...]: ...


def pagina_inicial(recomendador: Recomendador, usuario: str) -> dict[str, object]:
    return {"usuario": usuario, "recomendacoes": recomendador.recomendar(usuario)}
