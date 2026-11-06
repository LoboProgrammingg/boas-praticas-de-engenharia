"""LSP violado: Quadrado herda de Retangulo e quebra o contrato da classe base.

Quem usa um Retangulo espera que mudar a largura não mude a altura.
"""


class Retangulo:
    def __init__(self, largura: float, altura: float) -> None:
        self.largura = largura
        self.altura = altura

    def definir_largura(self, largura: float) -> None:
        self.largura = largura

    def area(self) -> float:
        return self.largura * self.altura


class Quadrado(Retangulo):
    def __init__(self, lado: float) -> None:
        super().__init__(lado, lado)

    def definir_largura(self, largura: float) -> None:
        self.largura = self.altura = largura


def dobrar_largura(retangulo: Retangulo) -> float:
    retangulo.definir_largura(retangulo.largura * 2)
    return retangulo.area()
