# CQS: Command-Query Separation

> Um método ou muda o estado (comando) ou devolve um resultado (consulta), mas não os dois.
> Síntese do princípio de Bertrand Meyer

| | |
|---|---|
| **Origem** | Bertrand Meyer, *Object-Oriented Software Construction* |
| **Resolve** | Leituras com efeito colateral oculto, que mudam de resultado a cada chamada e não podem ser reordenadas ou repetidas |
| **Em uma frase** | Perguntar não pode mudar a resposta |

## O problema

Em [`ruim.py`](ruim.py), `proximo_numero()` parece um getter, mas cada chamada consome
um número. Se alguém loga `numerador.proximo_numero()` para depurar e depois usa o
mesmo método para numerar a fatura, o log mostra 1 e a fatura sai com 2. Um `assert`, uma
tela de debug ou uma segunda leitura passam a alterar o sistema.

Fowler descreve a vantagem do desenho correto: consultas podem ser usadas com confiança,
introduzidas em qualquer lugar e reordenadas.

## A solução

Em [`bom.py`](bom.py), `avancar()` é o comando (devolve `None`) e `atual()` é a
consulta. O [`teste`](test_cqs.py) lê 1, 2 ou 10 vezes e sempre obtém o mesmo valor, e
confirma que só o comando muda o estado.

## Quando não aplicar

- **Operações em que separar cria uma janela de corrida.** `pop()` de uma pilha,
  `INSERT ... RETURNING` e `compare-and-swap` precisam ler e escrever atomicamente.
  Fowler mesmo admite que segue a regra quando pode e a quebra para ter seu `pop`.
- Em código concorrente, "consultar e depois comandar" pode ser incorreto; a operação
  atômica é a resposta, documentada como exceção.
- Iteradores e geradores também avançam ao serem consultados, por natureza.

## Relações

- É a semente do **CQRS**, que aplica a ideia no nível de arquitetura (modelos
  separados para escrita e leitura). Fowler avisa que, para a maioria dos sistemas, o
  CQRS adiciona complexidade arriscada ([*CQRS*](https://martinfowler.com/bliki/CQRS.html)).
- Aproxima código de funções puras e de [imutabilidade](../imutabilidade/README.md).
- Em [funções](../../02-codigo-limpo/funcoes/README.md), o Clean Code recomenda a mesma separação.

## Referências

- Martin Fowler, [*Command Query Separation*](https://martinfowler.com/bliki/CommandQuerySeparation.html), 2005.
- Martin Fowler, [*CQRS*](https://martinfowler.com/bliki/CQRS.html), 2011.
