# LSP: Princípio da Substituição de Liskov

> Se `S` é subtipo de `T`, toda propriedade comprovável sobre objetos de `T` deve valer
> também para objetos de `S`.
> Barbara Liskov e Jeannette Wing, 1994

| | |
|---|---|
| **Origem** | Barbara Liskov, keynote *Data Abstraction and Hierarchy* (1987); formalizado por Liskov e Wing em *A Behavioral Notion of Subtyping* (1994) |
| **Resolve** | Subclasses que compilam no lugar da classe base, mas mudam o comportamento esperado |
| **Em uma frase** | Herdar é prometer o mesmo comportamento, não só a mesma assinatura |

## O problema

Em [`ruim.py`](ruim.py), `Quadrado` herda de `Retangulo`. Todo método existe e o tipo
confere, mas `dobrar_largura` foi escrita para retângulos: dobrar a largura de um
retângulo 2x3 dá área 12; de um "retângulo" quadrado 2x2 dá 16 em vez de 8. O
contrato **comportamental** (pós-condição) foi quebrado.

Sinais típicos de violação: subclasse que lança `NotImplementedError`, que ignora
parâmetros, ou código cliente cheio de `isinstance` para tratar exceções à regra.

## A solução

Em [`bom.py`](bom.py), as formas não fingem ser umas as outras. Ambas cumprem o
contrato `Forma` (um `Protocol`), são imutáveis e "alterar" devolve um novo valor.
Qualquer `Forma` pode substituir outra onde só `area()` é exigida.

## Quando não aplicar

LSP não é opcional quando há substituição. A questão é **evitar a herança** quando o
contrato não pode ser cumprido: modele como tipos independentes com um contrato
mínimo comum, ou use composição.

## Relações

- É a base para o **OCP** por polimorfismo: extensões só são seguras se forem substituíveis.
- Próximo de *Design by Contract* (Meyer): pré-condições não podem ficar mais fortes, pós-condições não podem ficar mais fracas.
- Argumento central para **composição sobre herança**.

## Referências

- Barbara Liskov e Jeannette Wing, [*A Behavioral Notion of Subtyping*](https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf), ACM TOPLAS, 1994.
- [Liskov substitution principle](https://en.wikipedia.org/wiki/Liskov_substitution_principle), Wikipedia (histórico).
