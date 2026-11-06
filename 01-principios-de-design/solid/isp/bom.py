"""ISP aplicado: interfaces pequenas, cada cliente depende só do que usa."""

from typing import Protocol


class Imprime(Protocol):
    def imprimir(self, documento: str) -> str: ...


class Digitaliza(Protocol):
    def digitalizar(self, documento: str) -> bytes: ...


class ImpressoraSimples:
    def imprimir(self, documento: str) -> str:
        return f"impresso: {documento}"


class Multifuncional:
    def imprimir(self, documento: str) -> str:
        return f"impresso: {documento}"

    def digitalizar(self, documento: str) -> bytes:
        return documento.encode()


def imprimir_relatorio(impressora: Imprime, relatorio: str) -> str:
    return impressora.imprimir(relatorio)


def arquivar(scanner: Digitaliza, documento: str) -> bytes:
    return scanner.digitalizar(documento)
