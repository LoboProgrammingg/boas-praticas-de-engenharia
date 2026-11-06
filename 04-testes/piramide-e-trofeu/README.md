# Pirâmide e troféu de testes

> "Write tests. Not too many. Mostly integration."
> Guillermo Rauch, citado por Kent C. Dodds

| | |
|---|---|
| **Origem** | Test Pyramid: Mike Cohn, divulgada por Martin Fowler (2012) e Ham Vocke (2018). Testing Trophy: Kent C. Dodds (2019 e 2021) |
| **Resolve** | Suítes lentas, frágeis e caras, ou suítes rápidas que não dão confiança de que o sistema funciona |
| **Em uma frase** | Escolha a proporção de cada tipo de teste pela confiança que ele dá por unidade de custo, no seu contexto |

## O problema

Há dois modos clássicos de errar:

- **Cone de sorvete** (*ice-cream cone*): quase tudo é teste de ponta a ponta pela interface.
  Fowler resume: testes que passam pela UI são "brittle, expensive to write, and time
  consuming to run". A suíte demora, quebra por motivos alheios ao código e vira ruído.
- **Só unidade, com dublês em tudo**: a suíte é verde e rápida, mas cada peça é testada
  isolada com mocks e ninguém verifica que elas funcionam *juntas*.

## A solução

Dois modelos, que concordam no essencial (teste em vários níveis, e quanto mais alto o
nível, mais caro) e discordam na ênfase.

| | Pirâmide | Troféu |
|---|---|---|
| **Autores** | Cohn / Fowler / Vocke | Dodds (a partir de um tuíte de Guillermo Rauch) |
| **Camadas** (de baixo para cima) | unidade, integração/serviço, UI e ponta a ponta | estático (tipos, lint), unidade, **integração**, ponta a ponta |
| **Maior fatia** | unidade | integração |
| **Ideia central** | muitos testes baratos e rápidos embaixo; poucos caros em cima | confiança máxima com custo razoável: teste do jeito que o software é usado |
| **Mais natural em** | backend com muita lógica de domínio | frontend e aplicações de composição, onde a lógica está na integração dos componentes |

O *Practical Test Pyramid* de Ham Vocke detalha os níveis: unidade (*sociable* ou *solitary*,
com *stubbing*), integração (banco, serviços separados, testes de contrato), UI/ponta a
ponta, aceitação e exploratório, além de "evite duplicar testes": se uma regra já é
coberta por um teste de unidade, não repita a mesma verificação no teste de ponta a ponta.

Dodds explica a escolha com a metáfora que ele atribui a J. B. Rainsberger: jogar tinta na
parede acaba cobrindo boa parte dela, mas para acertar os cantos você precisa de um pincel;
cada tipo de teste é uma ferramenta diferente.

### Decisão por contexto, não por dogma

| Pergunta | Se a resposta é "sim" |
|---|---|
| A complexidade está em regras de negócio puras (cálculos, estados)? | mais testes de unidade, rápidos e precisos |
| A complexidade está em como as peças se conectam (HTTP, banco, componentes)? | mais testes de integração com dependências reais |
| Uma falha custa muito e o fluxo é crítico (pagamento, login)? | alguns poucos testes de ponta a ponta no caminho principal |
| Existe um serviço externo que você não controla? | [testes de contrato](../testes-de-contrato/README.md) + um dublê, não a rede real |

### Cobertura de código

Um número como "70% de cobertura" é **política do projeto**, não lei da engenharia. Dodds
diz sobre o 70%: "I made that number up... no science there", e argumenta que exigir
100% tem retornos decrescentes. Cobertura mede quais linhas rodaram, não se os testes
detectariam um defeito nelas; veja [mutation testing](../mutation/README.md). Adote um piso
se ajudar o time, mas julgue a suíte pela confiança que ela dá.

## Quando não aplicar

- **Não trate a forma como meta.** Contar testes por camada para "acertar a pirâmide" é
  confundir o instrumento com o objetivo.
- **Sistemas pequenos ou protótipos** podem ter poucos testes, de qualquer tipo, nos
  caminhos que mais doem.
- **Integração com banco real** é uma boa regra de projeto onde as divergências entre
  produção e teste custam caro, mas é uma decisão do projeto, não uma prescrição universal.

## Relações

- Os testes de unidade rápidos dependem de bons [dublês](../dubles-de-teste/README.md)
  (fakes) e de portas bem definidas ([hexagonal](../../03-arquitetura/camadas-hexagonal-clean/README.md)).
- A forma de escrever cada teste: [AAA / Given-When-Then](../aaa-given-when-then/README.md).
- Entre serviços: [testes de contrato](../testes-de-contrato/README.md).

## Referências

- Martin Fowler, [*Test Pyramid*](https://martinfowler.com/bliki/TestPyramid.html), 2012.
- Ham Vocke, [*The Practical Test Pyramid*](https://martinfowler.com/articles/practical-test-pyramid.html), 2018.
- Kent C. Dodds, [*Write tests. Not too many. Mostly integration.*](https://kentcdodds.com/blog/write-tests), 2019.
- Kent C. Dodds, [*Static vs Unit vs Integration vs E2E Testing for Frontend Apps*](https://kentcdodds.com/blog/static-vs-unit-vs-integration-vs-e2e-tests), 2021.
