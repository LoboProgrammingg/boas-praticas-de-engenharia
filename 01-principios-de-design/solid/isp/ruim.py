"""ISP violado: uma interface "gorda" obriga todo cliente a implementar o que não usa."""

from abc import ABC, abstractmethod


class Impressora(ABC):
    @abstractmethod
    def imprimir(self, documento: str) -> str: ...

    @abstractmethod
    def digitalizar(self, documento: str) -> bytes: ...

    @abstractmethod
    def enviar_fax(self, documento: str, numero: str) -> None: ...


class ImpressoraSimples(Impressora):
    def imprimir(self, documento: str) -> str:
        return f"impresso: {documento}"

    def digitalizar(self, documento: str) -> bytes:
        raise NotImplementedError("Esta impressora não digitaliza.")

    def enviar_fax(self, documento: str, numero: str) -> None:
        raise NotImplementedError("Esta impressora não envia fax.")
