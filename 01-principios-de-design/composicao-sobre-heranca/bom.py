"""Composição: decoradores com a mesma interface, combináveis em qualquer ordem.

``ComReenvio`` e ``ComRegistro`` embrulham qualquer ``Notificador``. Nenhum conhece
SMTP ou SMS, e as combinações saem da montagem, não de novas classes.
"""

from typing import Protocol


class FalhaTransitoriaError(Exception):
    pass


class Notificador(Protocol):
    def enviar(self, mensagem: str) -> None: ...


class _FalhasSimuladas:
    """Simula um canal instável; compartilhado por composição, não por herança."""

    def __init__(self, quantidade: int) -> None:
        self._restantes = quantidade

    def disparar(self) -> None:
        if self._restantes > 0:
            self._restantes -= 1
            raise FalhaTransitoriaError


class NotificadorSmtp:
    def __init__(self, falhas_iniciais: int = 0) -> None:
        self.enviados: list[str] = []
        self._falhas = _FalhasSimuladas(falhas_iniciais)

    def enviar(self, mensagem: str) -> None:
        self._falhas.disparar()
        self.enviados.append(mensagem)


class NotificadorSms:
    def __init__(self, falhas_iniciais: int = 0) -> None:
        self.enviados: list[str] = []
        self._falhas = _FalhasSimuladas(falhas_iniciais)

    def enviar(self, mensagem: str) -> None:
        self._falhas.disparar()
        self.enviados.append(mensagem)


class ComReenvio:
    def __init__(self, interno: Notificador, tentativas: int = 3) -> None:
        self._interno = interno
        self._tentativas = tentativas

    def enviar(self, mensagem: str) -> None:
        for tentativa in range(1, self._tentativas + 1):
            try:
                self._interno.enviar(mensagem)
            except FalhaTransitoriaError:
                if tentativa == self._tentativas:
                    raise
            else:
                return


class ComRegistro:
    def __init__(self, interno: Notificador, registro: list[str]) -> None:
        self._interno = interno
        self._registro = registro

    def enviar(self, mensagem: str) -> None:
        self._registro.append(f"enviando: {mensagem}")
        self._interno.enviar(mensagem)
