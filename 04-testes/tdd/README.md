# TDD: Test-Driven Development

> "Write a test for the next bit of functionality you want to add. Write the functional
> code until the test passes. Refactor both new and old code to make it well structured."
> Martin Fowler, *Test Driven Development*

| | |
|---|---|
| **Origem** | Kent Beck, *Test-Driven Development by Example* (2002), a partir do *test-first* do Extreme Programming |
| **Resolve** | Código escrito sem feedback, com bordas esquecidas e testes que só confirmam o que já foi escrito |
| **Em uma frase** | Escreva um teste que falha, escreva o mínimo para passar, refatore, repita |

## O problema

Em [`ruim.py`](ruim.py), `parcelar(100, 3)` devolve `[33, 33, 33]`: um centavo desaparece.
Ninguém tinha perguntado "e se a divisão não for exata?", e um teste escrito *depois*, a
partir do código, tende a conferir o que o código já faz (`33`) em vez do que deveria ser
verdade (a soma das parcelas é o total).

## A solução

O ciclo **red, green, refactor**:

1. **Red.** Escreva um teste do próximo comportamento e veja-o **falhar** pelo motivo
   certo. Se não falhou, ou o teste não testa nada, ou o comportamento já existia.
2. **Green.** Escreva o código mais simples que faz o teste passar.
3. **Refactor.** Com a suíte verde, melhore a estrutura sem mudar o comportamento.

O caso de `parcelar`, em ordem:

| Passo | Teste | Resultado |
|---|---|---|
| 1 | `parcelar(90, 3) == [30, 30, 30]` | red; `[total // n] * n` deixa verde |
| 2 | `soma(parcelar(100, 3)) == 100` | **red**: a soma é 99 |
| 3 | `parcelar(100, 3) == [34, 33, 33]` | green após distribuir o resto com `divmod` |
| 4 | `parcelar(100, 0)` levanta `ValueError` | red; adiciona a guarda |
| 5 | refatorar | a lista por compreensão substitui o laço |

O passo 2 é o valor do TDD: o teste que falhou **formulou a propriedade** certa antes de o
código existir e forçou a decisão de design. O código final está em [`bom.py`](bom.py), e
[`test_tdd.py`](test_tdd.py) tem a suíte resultante, incluindo a prova de que a versão
ruim perde um centavo. Para uma busca sistemática por esse tipo de borda, veja
[property-based testing](../property-based/README.md).

### Variações

- Kent Beck popularizou o ciclo; Robert C. Martin o formaliza nas "três leis" do TDD.
  Em um debate público, John Ousterhout prefere trabalhar com unidades maiores de
  funcionalidade (*bundling*) em vez de ciclos mínimos e reconheceu ter descrito o TDD de
  modo impreciso ([debate Ousterhout × Martin](https://github.com/johnousterhout/aposd-vs-clean-code)).
  A prática tem variações, e não é consenso que o ciclo mínimo seja sempre o melhor.
- **TDD não é só "ter testes".** Escrever os testes depois é válido e útil, mas é outra
  prática: perde o feedback de design que o teste escrito antes dá.

## Quando não aplicar

- **Exploração e protótipo.** Quando você ainda não sabe o que quer construir, escreva
  código descartável (um *spike*) e só depois, sabendo o que importa, escreva os testes
  (ou o TDD do código definitivo).
- **Código dominado por integração e interface gráfica**, em que o teste automatizado
  rápido é difícil de escrever primeiro. Ali, comece por testes de nível mais alto.
- **Evidência empírica.** Estudos sobre o ganho de produtividade ou qualidade do TDD são
  mistos; trate-o como disciplina útil de design e feedback, não como dogma.

## Relações

- Os testes do ciclo seguem o formato de [AAA / Given-When-Then](../aaa-given-when-then/README.md).
- A fase *refactor* só é segura com uma suíte confiável (veja [mutation](../mutation/README.md)).
- O teste que falha primeiro costuma virar um exemplo de [property-based testing](../property-based/README.md).

## Referências

- Martin Fowler, [*Test Driven Development*](https://martinfowler.com/bliki/TestDrivenDevelopment.html), 2023.
- Kent Beck, *Test-Driven Development by Example*, Addison-Wesley, 2002.
- John Ousterhout e Robert C. Martin, [*A Philosophy of Software Design* vs *Clean Code*](https://github.com/johnousterhout/aposd-vs-clean-code).
- [Test-driven development (Wikipedia)](https://en.wikipedia.org/wiki/Test-driven_development).
