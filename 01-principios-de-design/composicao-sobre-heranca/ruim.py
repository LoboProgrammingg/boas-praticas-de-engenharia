"""Herança usada só para reaproveitar código.

A lógica de reenvio nasce presa a ``NotificadorSmtp``. Para ter o mesmo
comportamento no SMS seria preciso outra subclasse com o laço copiado, e cada nova
combinação (reenvio + registro, por exemplo) multiplica as classes.
"""


class FalhaTransitoriaError(Exception):
    pass


class NotificadorSmtp:
    def __init__(self, falhas_iniciais: int = 0) -> None:
        self.enviados: list[str] = []
        self._falhas_restantes = falhas_iniciais

    def enviar(self, mensagem: str) -> None:
        if self._falhas_restantes > 0:
            self._falhas_restantes -= 1
            raise FalhaTransitoriaError
        self.enviados.append(mensagem)


class NotificadorSmtpComReenvio(NotificadorSmtp):
    def enviar(self, mensagem: str) -> None:
        for tentativa in range(3):
            try:
                super().enviar(mensagem)
            except FalhaTransitoriaError:
                if tentativa == 2:
                    raise
            else:
                return


class NotificadorSms:
    def __init__(self, falhas_iniciais: int = 0) -> None:
        self.enviados: list[str] = []
        self._falhas_restantes = falhas_iniciais

    def enviar(self, mensagem: str) -> None:
        if self._falhas_restantes > 0:
            self._falhas_restantes -= 1
            raise FalhaTransitoriaError
        self.enviados.append(mensagem)
