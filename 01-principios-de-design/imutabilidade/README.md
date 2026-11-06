# Imutabilidade

> Um valor que não muda depois de criado pode ser compartilhado, guardado e raciocinado sem medo.
> Síntese do princípio

| | |
|---|---|
| **Origem** | Programação funcional e design orientado a objetos com *value objects*; em Python, `@dataclass(frozen=True)` |
| **Resolve** | Mutação invisível: quem guardou uma referência vê o valor mudar por baixo, e o raciocínio local deixa de funcionar |
| **Em uma frase** | Em vez de alterar, devolva um valor novo |

## O problema

Em [`ruim.py`](ruim.py), `adicionar_item(carrinho: list[str], item)` altera a lista do
chamador. Se um histórico guardou a mesma lista (aliasing), ele muda junto: o "antes"
deixa de existir. Qualquer função que receba a lista pode alterá-la sem aviso.

## A solução

Em [`bom.py`](bom.py), `Carrinho` é um `dataclass(frozen=True, slots=True)` com uma
tupla, e `adicionar_item` devolve outro `Carrinho` via `dataclasses.replace`. O
[`teste`](test_imutabilidade.py) mostra que o original e o histórico ficam intactos, que
a atribuição levanta `FrozenInstanceError` e que o valor é hashável (serve de chave de
dicionário).

A mesma lógica que Fowler dá às consultas no CQS vale aqui: funções puras e valores
imutáveis podem ser introduzidos e reordenados em qualquer lugar.

## Quando não aplicar

- **Estruturas grandes em laços quentes.** Copiar a cada alteração custa; use mutação
  *local e encapsulada* ("núcleo funcional, casca imperativa").
- `frozen=True` é raso: uma lista dentro de um dataclass congelado continua mutável. Por
  isso o exemplo usa `tuple`.
- Entidades com identidade e ciclo de vida (um pedido que muda de estado) podem ser
  mutáveis, desde que o estado só mude por métodos que protegem as invariantes
  ([Tell, Don't Ask](../tell-dont-ask/README.md)).

## Relações

- Pilar das funções puras e de [CQS](../cqs/README.md).
- Reduz a necessidade de cópia defensiva e de travas em código concorrente.
- Base para *value objects* e para [fail fast](../fail-fast/README.md): valida-se uma vez, na criação.

## Referências

- Python, [`dataclasses` (frozen e slots)](https://docs.python.org/3/library/dataclasses.html).
- Martin Fowler, [*Command Query Separation*](https://martinfowler.com/bliki/CommandQuerySeparation.html), 2005.
- Martin Fowler, [*Value Object*](https://martinfowler.com/bliki/ValueObject.html).
