# Funções

> "The best methods are those that provide a lot of functionality but have a very simple interface."
> John Ousterhout, no debate com Robert C. Martin

| | |
|---|---|
| **Origem** | Capítulo de funções de *Clean Code* (Martin, 2008), discutido por qntm (2020), Muratori (2023) e Ousterhout (2024–2025) |
| **Resolve** | Funções que escondem a intenção atrás de flags opacas, alteram argumentos ou misturam níveis de abstração |
| **Em uma frase** | Faça uma coisa, no nível de abstração do chamador, e deixe a chamada contar o que ela faz |

## O problema

Em [`ruim.py`](ruim.py):

- `exportar(linhas, True, False)`: o que significam os dois booleanos? Inverter os dois
  continua válido e muda a saída sem erro algum.
- `aplicar_desconto(precos, percentual)` devolve `None` e **altera a lista do
  chamador** (argumento de saída). Quem guardou os preços originais os perdeu.

## A solução

Em [`bom.py`](bom.py):

| Antes | Depois |
|---|---|
| `exportar(linhas, csv, cabecalho)` | `exportar_csv(linhas, *, com_cabecalho=True)` e `exportar_tabela(...)`: um formato por função, e o booleano restante é nomeado na chamada |
| `aplicar_desconto(lista, pct)` altera | `precos_com_desconto(precos, pct)` devolve uma tupla nova |

O [`teste`](test_funcoes.py) mostra a troca silenciosa de booleanos, a perda dos preços
originais e a recusa de booleano posicional.

Recomendações que resistem às críticas: um nível de abstração por função; sem efeitos
colaterais ocultos; retorno em vez de argumento de saída; comando **ou** consulta (ver
[CQS](../../01-principios-de-design/cqs/README.md)).

## Quando não aplicar

- **Não persiga tamanho.** Ousterhout critica "métodos minúsculos" que geram interfaces
  rasas e código emaranhado; Martin admite que o "2 a 4 linhas" do livro nasceu de um
  applet Swing e nunca foi absoluto. Fowler dá o critério mais útil: separar
  *intenção* de *implementação* ([*Function Length*](https://martinfowler.com/bliki/FunctionLength.html)).
- **Flag booleana não é sempre errada.** O crítico qntm concorda que `True/False`
  opacos são ruins, mas discorda de que o motivo seja "fazer mais de uma coisa".
  Parâmetro nomeado e obrigatório (`com_cabecalho=`) resolve a legibilidade.
- **Desempenho.** Muratori mostra que, em laços quentes, polimorfismo e funções
  pequenas têm custo medido. Em código dominado por I/O, costuma ser irrelevante.
  Meça antes de abrir mão da clareza.

## Relações

- [CQS](../../01-principios-de-design/cqs/README.md) e
  [imutabilidade](../../01-principios-de-design/imutabilidade/README.md): retornar valor novo
  em vez de alterar o argumento.
- [Nomes](../nomes/README.md): o nome da função é metade da documentação.
- [SRP](../../01-principios-de-design/solid/srp/README.md) e o contraponto dos *módulos profundos*.

## Referências

- Robert C. Martin, *Clean Code*, Prentice Hall, 2008, capítulo 3.
- John Ousterhout e Robert C. Martin, [debate *APOSD* vs *Clean Code*](https://github.com/johnousterhout/aposd-vs-clean-code), 2024–2025.
- qntm, [*It's probably time to stop recommending Clean Code*](https://qntm.org/clean), 2020.
- Casey Muratori, [*"Clean" Code, Horrible Performance*](https://www.computerenhance.com/p/clean-code-horrible-performance), 2023.
- Martin Fowler, [*Function Length*](https://martinfowler.com/bliki/FunctionLength.html).
