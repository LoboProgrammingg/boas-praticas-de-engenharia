# Tell, Don't Ask

> Em vez de pedir dados a um objeto para decidir por ele, diga ao objeto o que fazer.
> Síntese do princípio, conforme Martin Fowler (2013)

| | |
|---|---|
| **Origem** | Princípio de orientação a objetos descrito por Martin Fowler (*Tell Don't Ask*, 2013); o anti-padrão correlato é o modelo de domínio anêmico (*Anemic Domain Model*, 2003) |
| **Resolve** | Regras de negócio espalhadas por quem usa o objeto, enquanto o objeto é um saco de dados sem proteção |
| **Em uma frase** | Junte os dados com as regras que os governam; quem chama diz *o quê*, o objeto decide *como* |

## O problema

Em [`ruim.py`](ruim.py), `Pedido` tem campos públicos e a regra mora em
`ServicoDePedidos.confirmar`: quem passa pelo serviço está protegido. Mas qualquer outro
código (um relatório, um script de correção) pode fazer `pedido.status = "confirmado"` e
criar um pedido vazio confirmado. A invariante depende de todos lembrarem de chamar o
serviço.

O exemplo canônico de Fowler é um `Monitor`: em vez de o chamador comparar
`getValue() > getLimit()` e disparar o alarme, o monitor dispara o alarme dentro de
`setValue`. O texto lembra que orientação a objetos é juntar dados com as funções que os
operam.

## A solução

Em [`bom.py`](bom.py), o estado é privado e só muda por `adicionar` e `confirmar`, que
checam as invariantes. O [`teste`](test_tell_dont_ask.py) prova que um pedido vazio não
confirma, que `pedido.confirmado = True` não é possível e que um pedido confirmado
fica congelado.

## Quando não aplicar

- **DTOs, leitura para tela e projeções** (por exemplo o lado de leitura de um CQRS) são
  legitimamente "ask": o objetivo é só expor dados.
- Não leve regras de **apresentação** para dentro do domínio (formatação de moeda, texto
  de tela). Isso vira o excesso oposto.
- Em linguagens com tipos algébricos e funções puras, dados simples e funções que os
  transformam são um estilo válido; o ponto continua sendo proteger as invariantes.

## Relações

- Reforça o encapsulamento e a [Lei de Demeter](../lei-de-demeter/README.md).
- Combina com [CQS](../cqs/README.md): `confirmar` é um comando, `confirmado` é uma consulta.
- Aproxima-se de [SRP](../solid/srp/README.md): o pedido muda quando as regras do pedido mudam.

## Referências

- Martin Fowler, [*Tell Don't Ask*](https://martinfowler.com/bliki/TellDontAsk.html), 2013.
- Martin Fowler, [*Anemic Domain Model*](https://martinfowler.com/bliki/AnemicDomainModel.html), 2003.
