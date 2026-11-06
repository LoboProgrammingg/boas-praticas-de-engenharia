"""Dublê que mente: um ``Mock`` sem especificação aceita qualquer chamada.

O repositório real renomeou ``adicionar`` para ``salvar``, mas o caso de uso ainda chama
``adicionar``. Um teste com ``Mock()`` continua verde, e o código quebra em produção.
"""

from typing import Any


class RepositorioDeUsuarios:
    """Implementação real (depois de renomear ``adicionar`` para ``salvar``)."""

    def __init__(self) -> None:
        self._emails: set[str] = set()

    def salvar(self, email: str) -> None:
        self._emails.add(email)


class Cadastrar:
    def __init__(self, repositorio: Any, notificador: Any) -> None:
        self._repositorio = repositorio
        self._notificador = notificador

    def executar(self, email: str) -> None:
        self._repositorio.adicionar(email)
        self._notificador.boas_vindas(email)
