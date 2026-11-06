# Lei de Demeter (princípio do menor conhecimento)

> Cada unidade deve ter conhecimento limitado sobre as outras e falar apenas com seus amigos imediatos.
> Síntese do princípio

| | |
|---|---|
| **Origem** | Ian Holland, Northeastern University, no fim de 1987, no projeto Demeter |
| **Resolve** | Código que atravessa cadeias de objetos (`a.b.c.d`) e quebra quando qualquer elo muda |
| **Em uma frase** | Peça ao objeto que você conhece; não navegue pelos objetos que ele guarda |

## O problema

Em [`ruim.py`](ruim.py), `calcular_frete` faz `pedido.cliente.endereco.cidade`. A função
conhece três classes e a forma como se ligam. Para testá-la é preciso montar a cadeia
inteira: um objeto falso que só ofereça a cidade de entrega não serve, e dá
`AttributeError`.

## A solução

Em [`bom.py`](bom.py), `calcular_frete` depende de uma pergunta (`cidade_de_entrega()`),
expressa pelo `Protocol` `ComEntrega`. Como o pedido descobre a cidade é problema dele:
se o endereço de entrega passar a ser próprio do pedido, nenhum chamador muda. O
[`teste`](test_lei_de_demeter.py) usa um falso de uma linha.

## Quando não aplicar

- **Estruturas de dados puras e DTOs.** Navegar por um JSON ou um `dataclass` sem
  comportamento não é violação, é leitura de dados.
- **Interfaces fluentes e builders** (`consulta.filtrar(...).ordenar(...)`): cada chamada
  devolve o mesmo tipo, não expõe estrutura interna.
- **Delegação em excesso.** Aplicar a lei cegamente gera dezenas de métodos que só repassam
  chamadas, o *smell* chamado Middle Man
  ([Remove Middle Man](https://refactoring.com/catalog/removeMiddleMan.html)).
  Em [`bom.py`](bom.py), `Cliente.cidade()` é esse custo, aceitável aqui.

## Relações

- Forma prática de [baixo acoplamento](../coesao-e-acoplamento/README.md) e de encapsulamento.
- Anda junto com [Tell, Don't Ask](../tell-dont-ask/README.md): se você pergunta menos, depende de menos.
- Em tensão com [KISS](../kiss/README.md) quando gera camadas de repasse.

## Referências

- [Wikipedia: Law of Demeter](https://en.wikipedia.org/wiki/Law_of_Demeter).
- Martin Fowler, [*Fluent Interface*](https://martinfowler.com/bliki/FluentInterface.html).
- [Remove Middle Man](https://refactoring.com/catalog/removeMiddleMan.html), catálogo de refatorações.
