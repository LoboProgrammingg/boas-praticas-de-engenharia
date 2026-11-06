# KISS: Keep It Simple

> "Simple is better than complex. Complex is better than complicated."
> PEP 20, *The Zen of Python*

| | |
|---|---|
| **Origem** | Expressão de engenharia citada pela marinha dos EUA em 1960, associada ao engenheiro Kelly Johnson (Lockheed Skunk Works): o jato deveria ser reparável em campo, por um mecânico comum, com poucas ferramentas |
| **Resolve** | Soluções com mais peças do que o problema exige, difíceis de ler, testar e mudar |
| **Em uma frase** | Entre duas soluções que resolvem o problema, fique com a que tem menos peças móveis |

## O problema

Código complicado costuma nascer de boa intenção: "e se amanhã precisarmos de outra
estratégia?". Em [`ruim.py`](ruim.py), somar uma lista de preços exige uma classe
abstrata, uma implementação, uma fábrica e um registro por nome. São três classes
para fazer o que `sum` faz, e um erro de digitação no nome da estratégia só aparece
em tempo de execução (`KeyError`).

## A solução

Em [`bom.py`](bom.py) existe uma função de uma linha. O teste
[`test_kiss.py`](test_kiss.py) mostra que as duas versões dão o mesmo resultado, que a
ruim define três classes e a boa nenhuma, e que o dinheiro continua em `Decimal`.

Um bom teste de simplicidade: dá para explicar a solução em uma frase? O próprio PEP 20
diz que, se a implementação é difícil de explicar, é uma má ideia.

## Quando não aplicar

- **Simples não é ingênuo.** Ignorar concorrência, fuso horário ou usar `float` para
  dinheiro não é KISS, é simplismo. O teste prova: `sum([0.1, 0.2]) != 0.3`, e por isso
  a versão boa usa `Decimal`.
- **Complexidade essencial existe.** Se o domínio é complicado (impostos, contratos),
  KISS pede a modelagem mais simples *que ainda represente a regra*, não menos que isso.
- Simplicidade se mede em quem vai ler e mudar o código, não em contagem de linhas.

## Relações

- Reforça [YAGNI](../yagni/README.md): ambos recusam estrutura sem uso real.
- Em tensão com [SRP](../solid/srp/README.md) e OCP quando levados ao extremo: classes
  demais também são complexidade.
- Aproxima-se do princípio da menor surpresa (POLA): código simples surpreende menos.

## Referências

- [PEP 20, *The Zen of Python*](https://peps.python.org/pep-0020/).
- [Wikipedia: KISS principle](https://en.wikipedia.org/wiki/KISS_principle), para a origem histórica.
- Kent Beck, regras de design simples, em [Martin Fowler, *Beck Design Rules*](https://martinfowler.com/bliki/BeckDesignRules.html), 2015.
