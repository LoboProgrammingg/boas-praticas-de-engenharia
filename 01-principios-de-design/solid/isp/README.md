# ISP: Princípio da Segregação de Interfaces

> "Clientes não devem ser forçados a depender de métodos que não usam."
> Robert C. Martin

| | |
|---|---|
| **Origem** | Robert C. Martin, ao prestar consultoria para a Xerox; publicado em *The Interface Segregation Principle*, C++ Report (1996) |
| **Resolve** | Interfaces "gordas" que forçam implementações vazias e acoplam clientes a capacidades que não usam |
| **Em uma frase** | Prefira várias interfaces pequenas, desenhadas a partir de quem as consome |

## O problema

Em [`ruim.py`](ruim.py), toda impressora precisa "saber" digitalizar e enviar fax.
A `ImpressoraSimples` passa no `isinstance`, mas mente: dois dos três métodos lançam
`NotImplementedError`, e o erro só aparece em tempo de execução, quando alguém confia
no contrato. Isso também é uma violação de **LSP**.

## A solução

Em [`bom.py`](bom.py), cada capacidade é um `Protocol` pequeno (`Imprime`,
`Digitaliza`). Cada função declara **só o que precisa**, e o type checker garante que
ninguém entregue uma impressora simples onde se espera um scanner. Com tipagem
estrutural do Python, a classe nem precisa declarar o que implementa.

## Quando não aplicar

- Não quebre uma interface coesa em pedaços de um método que sempre andam juntos.
- Interfaces devem nascer das necessidades de **clientes reais**, não de todas as
  combinações possíveis.

## Relações

- Interfaces pequenas tornam **dublês de teste** triviais.
- Facilita **DIP**: o domínio declara portas mínimas.
- Evita violações de **LSP** do tipo "método que não faz nada".

## Referências

- Robert C. Martin, *The Interface Segregation Principle*, C++ Report, 1996; retomado em *Agile Software Development: Principles, Patterns, and Practices*, 2002.
- [Interface segregation principle](https://en.wikipedia.org/wiki/Interface_segregation_principle), Wikipedia (histórico).
- Python, [PEP 544: Protocols, structural subtyping](https://peps.python.org/pep-0544/).
