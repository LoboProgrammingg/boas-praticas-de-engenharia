"""CQS violado: uma "consulta" que também altera o estado.

``proximo_numero`` parece um getter, mas cada leitura consome um número. Logar o
valor e depois usá-lo já gera dois números diferentes.
"""


class NumeradorDeFaturas:
    def __init__(self) -> None:
        self._contador = 0

    def proximo_numero(self) -> int:
        self._contador += 1
        return self._contador
