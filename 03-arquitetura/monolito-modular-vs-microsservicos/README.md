# Monólito modular × microsserviços

> "This pattern has led many of my colleagues to argue that you shouldn't start a new
> project with microservices, even if you're sure your application will be big enough to
> make it worthwhile."
> Martin Fowler, *Monolith First*

| | |
|---|---|
| **Origem** | Martin Fowler, *Monolith First* e *Microservice Premium* (2015) |
| **Resolve** | Distribuir cedo demais (custo operacional alto para um produto que ainda nem provou valor) ou nunca separar nada (bola de lama) |
| **Em uma frase** | Comece com um monólito de módulos bem separados; só pague o prêmio dos microsserviços quando a complexidade do sistema justificar |

## O problema

Há dois erros opostos:

1. **Bola de lama.** Em [`ruim.py`](ruim.py), `Pedidos` lê o dicionário privado de
   `Estoque`. Sem fronteira, uma refatoração interna de um módulo quebra o outro, e dividir
   o sistema depois exigiria reescrevê-lo.
2. **Microsserviços de saída.** Fowler relata que quase todas as histórias de sucesso com
   microsserviços começaram com um monólito que cresceu demais, e que sistemas feitos como
   microsserviços "from scratch" acabaram "in serious trouble". A primeira razão é YAGNI:
   no começo você nem sabe se o produto será útil, muito menos onde ficam as fronteiras
   certas.

## A solução

Um **monólito modular**: um só processo e um só deploy, mas com módulos que expõem uma API
pública pequena e escondem o resto. Em [`bom.py`](bom.py), `Pedidos` depende da porta
`ApiDeEstoque`; hoje ela é uma chamada de função (`EstoqueLocal`). O teste
[`test_monolito_modular_vs_microsservicos.py`](test_monolito_modular_vs_microsservicos.py)
mostra três coisas:

- na versão ruim, mudar a estrutura interna do estoque quebra pedidos;
- na boa, pedidos só usa a API pública, e trocar o estoque local por um adaptador remoto
  (`EstoqueRemoto`) não altera o módulo de pedidos;
- o adaptador remoto introduz um modo de falha que a chamada local nunca teve, `FalhaDeRedeError`.
  É um exemplo pequeno do **Microservice Premium**.

### O prêmio

Microsserviços dão fronteiras fortes entre módulos e deploy independente (Lewis e Fowler),
mas, segundo Fowler, adicionam "a premium to a project's cost and risk": dependem de
deploy automatizado, monitoramento, tratamento de falhas e consistência eventual. A
decisão depende da **complexidade do sistema**: o prêmio compensa em sistemas complexos e
atrapalha nos simples. As páginas de operabilidade
deste repositório ([timeouts](../../06-operabilidade/timeouts-retries-backoff/README.md),
[circuit breaker](../../06-operabilidade/circuit-breaker/README.md),
[idempotência](../../06-operabilidade/idempotencia/README.md)) são, em boa parte, o que se
passa a precisar ao cruzar essa fronteira.

| | Monólito modular | Microsserviços |
|---|---|---|
| Deploy | um só | um por serviço |
| Chamada entre módulos | função, no mesmo processo | rede (latência, timeout, falha parcial) |
| Consistência | transação local | eventual, sagas, idempotência |
| Fronteira | disciplina e testes | processo e contrato |
| Custo operacional | baixo | alto |

### Como manter o monólito "modular"

- Cada módulo corresponde a um Bounded Context ([`../ddd`](../ddd/README.md)).
- Chamadas entre módulos passam por uma porta (`Protocol`), nunca por atributos privados ou
  tabelas alheias.
- Verifique as fronteiras automaticamente (por exemplo, com um teste que analisa os
  `import`s, como o `ast` do teste de [`../camadas-hexagonal-clean`](../camadas-hexagonal-clean/README.md)).

## Quando não aplicar

- **Microsserviços fazem sentido** quando já existem times independentes que precisam
  implantar sem coordenar, partes com requisitos de escala muito diferentes e fronteiras
  que o produto já estabilizou. Se o sistema tem essas dores, o monólito vira o gargalo.
- **"Modular" não quer dizer "um módulo por classe".** Para um script ou um CRUD pequeno,
  uma pasta única é suficiente.

*Observação sobre fontes:* "monólito modular" não é um termo que Fowler tenha definido
numa página própria; ele aparece aqui como a aplicação prática do conselho de *Monolith
First* (começar com um monólito) combinado com fronteiras explícitas entre módulos.

## Relações

- Fronteiras vêm do DDD: [`../ddd`](../ddd/README.md).
- A porta entre módulos é a mesma ideia de [`../camadas-hexagonal-clean`](../camadas-hexagonal-clean/README.md).
- Contratos entre serviços pedem [testes de contrato](../../04-testes/testes-de-contrato/README.md).

## Referências

- Martin Fowler, [*Monolith First*](https://martinfowler.com/bliki/MonolithFirst.html), 2015.
- Martin Fowler, [*Microservice Premium*](https://martinfowler.com/bliki/MicroservicePremium.html), 2015.
- James Lewis e Martin Fowler, [*Microservices*](https://martinfowler.com/articles/microservices.html), 2014.
