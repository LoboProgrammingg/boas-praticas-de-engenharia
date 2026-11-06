# Mutation testing

> "Bugs, or mutants, are automatically inserted into your production code. Your tests are
> run for each mutant. If your tests fail then the mutant is killed. If your tests passed,
> the mutant survived. The higher the percentage of mutants killed, the more effective your
> tests are."
> Stryker Mutator, *What is mutation testing?*

| | |
|---|---|
| **Origem** | Técnica de pesquisa em teste de software; ferramentas atuais: Stryker (JavaScript/TypeScript, C#, Scala) e mutmut (Python) |
| **Resolve** | Suítes com alta cobertura que não detectariam um defeito real, porque a cobertura mede linhas executadas, não verificadas |
| **Em uma frase** | Estrague o código de propósito e veja se os testes percebem |

## O problema

Em [`ruim.py`](ruim.py), a regra é `idade >= 18` e a suíte tem dois casos (30 e 10).
Eles executam todas as linhas da função: **100% de cobertura de linhas**. Ainda assim,
se alguém trocar `>=` por `>`, ou por `>= 19`, nenhum teste falha. O número de cobertura
diz que o código rodou, mas não que alguém conferiu o resultado nas bordas.

A documentação do Stryker usa exatamente este exemplo (`user.age >= 18`) para mostrar que a
cobertura de código "não diz tudo" sobre a eficácia dos testes.

## A solução

O *mutation testing* automatiza o experimento:

1. A ferramenta aplica **mutações** pequenas ao código (trocar `>=` por `>`, `+` por `-`,
   remover uma condição, devolver `True` sempre), uma por vez, gerando **mutantes**.
2. Roda a suíte contra cada mutante.
3. Se algum teste **falha**, o mutante foi **morto** (*killed*). Se todos passam, ele
   **sobreviveu** (*survived*): há comportamento que a suíte não protege.
4. O **mutation score** é a proporção de mutantes mortos.

Um mutante sobrevivente é uma pergunta concreta ("o que acontece em 18?") que vira um teste.
O [`test_mutation.py`](test_mutation.py) faz isso à mão, com uma lista de mutantes e um
minúsculo executor: a suíte fraca de `ruim.py` deixa três mutantes de fronteira vivos;
os casos 18 e 17 de [`bom.py`](bom.py) os matam, e a suíte passa a proteger a regra.

### Ferramentas

Este repositório **descreve** a técnica e não adiciona dependências; para usá-la no seu
projeto:

| Linguagem | Ferramenta |
|---|---|
| Python | [mutmut](https://github.com/boxed/mutmut) |
| JavaScript / TypeScript | [StrykerJS](https://stryker-mutator.io/docs/stryker-js/introduction/) |
| C# | [Stryker.NET](https://stryker-mutator.io/docs/stryker-net/introduction/) |
| Scala | [Stryker4s](https://stryker-mutator.io/docs/stryker4s/getting-started/) |

## Quando não aplicar

- **É caro.** Cada mutante roda (parte de) a suíte; em bases grandes, rode só nos arquivos
  alterados, no CI noturno ou em módulos críticos de regra de negócio.
- **Mutantes equivalentes.** Alguns mutantes não mudam o comportamento observável e nunca
  podem ser mortos; um score de 100% nem sempre é alcançável nem necessário.
- **Não é meta de produtividade.** Perseguir o número gera testes artificiais. Use o
  relatório para achar lacunas, não para premiar quem mata mais mutantes.
- Não resolve suíte lenta ou frágil: primeiro garanta uma suíte rápida e determinística.

## Relações

- Complementa (e questiona) a **cobertura de código**: o piso de cobertura de um projeto
  é uma política local, e Kent C. Dodds chama de "inventado" o número de 70% que muitos
  citam; veja [pirâmide e troféu](../piramide-e-trofeu/README.md).
- Sobreviventes de fronteira são ótimos candidatos a
  [property-based testing](../property-based/README.md).
- A fase *refactor* do [TDD](../tdd/README.md) depende de uma suíte que realmente protege.

## Referências

- Stryker Mutator, [*Mutation testing*](https://stryker-mutator.io/docs/), documentação introdutória.
- [mutmut](https://github.com/boxed/mutmut), mutation tester para Python.
- Kent C. Dodds, [*Write tests. Not too many. Mostly integration.*](https://kentcdodds.com/blog/write-tests), 2019 (sobre o limite arbitrário de cobertura).
