"""Um modelo único de "Cliente" para a empresa inteira.

Vendas, Cobrança e Logística usam a palavra "cliente" com significados diferentes, mas a
classe tenta servir a todos: acumula os campos de cada contexto, e cada time passa a
depender (e a quebrar) o trabalho dos outros.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Cliente:
    nome: str
    email: str
    limite_de_credito: Decimal
    dias_de_atraso: int
    endereco_de_entrega: str
    janela_de_entrega: str

    def pode_comprar_a_prazo(self) -> bool:
        return self.dias_de_atraso == 0 and self.limite_de_credito > 0
