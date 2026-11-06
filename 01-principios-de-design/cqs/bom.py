"""CQS aplicado: comando altera e não retorna; consulta retorna e não altera.

``atual`` pode ser chamado quantas vezes for preciso (log, assert, tela) sem
efeito colateral. Só ``avancar`` consome um número.
"""


class NumeradorDeFaturas:
    def __init__(self) -> None:
        self._contador = 0

    def avancar(self) -> None:
        self._contador += 1

    def atual(self) -> int:
        return self._contador
