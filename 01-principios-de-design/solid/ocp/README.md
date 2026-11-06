# OCP: Princípio Aberto/Fechado

> "Entidades de software devem ser abertas para extensão, mas fechadas para modificação."

| | |
|---|---|
| **Origem** | Bertrand Meyer, *Object-Oriented Software Construction* (1988); reinterpretado por Robert C. Martin (*The Open-Closed Principle*, C++ Report, 1996) com ênfase em polimorfismo |
| **Resolve** | Funções que precisam ser editadas (e retestadas) a cada nova variação de comportamento |
| **Em uma frase** | Acrescente comportamento escrevendo código novo, não alterando código estável |

## O problema

Em [`ruim.py`](ruim.py), todo desconto novo é mais um `if` na mesma função. Cada
alteração arrisca quebrar os descontos que já funcionavam, e um desconto que ninguém
lembrou de adicionar passa **em silêncio** como preço cheio, como mostra o teste.

## A solução

Em [`bom.py`](bom.py), os descontos ficam numa `TabelaDeDescontos`. Uma nova regra é
**registrada**, não editada; um nome desconhecido falha alto em vez de cobrar errado.
Em Python, uma função (ou um `Protocol`) basta como ponto de extensão; não é preciso
uma hierarquia de classes.

## Quando não aplicar

- Um `if` com duas variações estáveis não precisa de ponto de extensão. Criar abstrações
  para variações que nunca aconteceram é especulação (YAGNI).
- Aplique quando a **terceira** variação aparecer e o padrão de mudança ficar claro.

## Relações

- Depende de polimorfismo e de **DIP**: o código estável conhece só a abstração.
- Em tensão com **KISS** e **YAGNI** quando a extensão é imaginada.
- **LSP** garante que as extensões possam substituir umas às outras com segurança.

## Referências

- Bertrand Meyer, *Object-Oriented Software Construction*, Prentice Hall, 1988.
- Robert C. Martin, [*The Open Closed Principle*](https://blog.cleancoder.com/uncle-bob/2014/05/12/TheOpenClosedPrinciple.html), 2014.
