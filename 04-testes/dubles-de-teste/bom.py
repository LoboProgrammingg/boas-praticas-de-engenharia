"""Um exemplo de cada dublê da taxonomia de Meszaros, sobre portas tipadas.

* Dummy: ``NotificadorNulo`` (preenche um parâmetro que o teste ignora).
* Stub: ``RelogioFixo`` (devolve uma resposta pronta).
* Fake: ``RepositorioEmMemoria`` (implementação funcional com atalho).
* Spy: ``NotificadorEspiao`` (grava as chamadas para o teste consultar).
* Mock: ``unittest.mock.create_autospec`` sobre a porta (veja os testes).
"""

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Protocol


class EmailJaCadastradoError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class Usuario:
    email: str
    cadastrado_em: datetime


class RepositorioDeUsuarios(Protocol):
    def salvar(self, usuario: Usuario) -> None: ...

    def existe(self, email: str) -> bool: ...


class Notificador(Protocol):
    def boas_vindas(self, email: str) -> None: ...


class Relogio(Protocol):
    def agora(self) -> datetime: ...


class Cadastrar:
    def __init__(
        self, repositorio: RepositorioDeUsuarios, notificador: Notificador, relogio: Relogio
    ) -> None:
        self._repositorio = repositorio
        self._notificador = notificador
        self._relogio = relogio

    def executar(self, email: str) -> Usuario:
        if self._repositorio.existe(email):
            raise EmailJaCadastradoError(email)
        usuario = Usuario(email, self._relogio.agora())
        self._repositorio.salvar(usuario)
        self._notificador.boas_vindas(email)
        return usuario


class RepositorioEmMemoria:
    def __init__(self) -> None:
        self._usuarios: dict[str, Usuario] = {}

    def salvar(self, usuario: Usuario) -> None:
        self._usuarios[usuario.email] = usuario

    def existe(self, email: str) -> bool:
        return email in self._usuarios


class NotificadorEspiao:
    def __init__(self) -> None:
        self.enviados: list[str] = []

    def boas_vindas(self, email: str) -> None:
        self.enviados.append(email)


class NotificadorNulo:
    def boas_vindas(self, email: str) -> None:
        return None


class RelogioFixo:
    def __init__(self, instante: datetime) -> None:
        self._instante = instante

    def agora(self) -> datetime:
        return self._instante


INSTANTE = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)
