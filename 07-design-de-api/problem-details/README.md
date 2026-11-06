# Problem Details: erros de API em RFC 9457

> "HTTP status codes cannot always convey enough information about errors to be helpful...
> this specification defines simple JSON and XML document formats to describe the specifics
> of a problem encountered: 'problem details'."
> RFC 9457, seção 1

| | |
|---|---|
| **Origem** | RFC 9457 (Nottingham, Wilde e Dalal, julho de 2023, *Standards Track*), que **obsoleta a RFC 7807** |
| **Resolve** | Cada API inventando seu próprio formato de erro, ou devolvendo erro com `200 OK` |
| **Em uma frase** | Um formato padrão e legível por máquina para erros HTTP: `application/problem+json` |

## O problema

Em [`ruim.py`](ruim.py), `tratar` devolve `200 OK` com `{"error": "..."}`:

- **o status mente.** Clientes HTTP genéricos, caches, proxies e a monitoria veem sucesso;
- **o formato é só desta API**, e cada consumidor precisa descobri-lo;
- **vaza detalhe interno.** `str(erro)` pode carregar SQL, caminho de arquivo ou nome de
  tabela: o [teste](test_problem_details.py) mostra uma tabela do banco aparecendo na
  resposta.

## A solução

O corpo é um objeto JSON com o media type `application/problem+json`. Membros definidos
pelo RFC (todos opcionais):

| Membro | Significado |
|---|---|
| `type` | URI que identifica o **tipo** do problema (é o identificador principal). Padrão: `about:blank` |
| `title` | resumo curto e legível do tipo; **não** deve mudar de ocorrência para ocorrência (exceto tradução) |
| `status` | o status HTTP usado; consultivo, e deve ser **igual** ao status real da resposta |
| `detail` | explicação desta ocorrência, focada em ajudar o cliente a corrigir o problema, não em depuração |
| `instance` | URI que identifica esta ocorrência específica (útil para suporte) |

E **extensões** específicas do tipo (o RFC cita `balance` e `errors` nos seus exemplos);
clientes devem **ignorar** extensões que não conhecem, o que permite evoluir o tipo.

Quando `type` é `about:blank`, o problema não tem semântica além do status HTTP e o
`title` deve ser a frase padrão do status (por exemplo, "Not Found" para 404).

Em [`bom.py`](bom.py), `tratar` converte exceções de domínio em respostas:

```http
HTTP/1.1 403 Forbidden
Content-Type: application/problem+json

{
  "type": "https://api.exemplo.com/problemas/saldo-insuficiente",
  "title": "Saldo insuficiente.",
  "status": 403,
  "detail": "Seu saldo é 30, mas a operação custa 50.",
  "instance": "/pagamentos/abc123",
  "balance": 30
}
```

O status HTTP (`403`) serve ao software genérico; o corpo serve ao cliente que entende o
tipo, que pode agir (por exemplo, oferecer uma recarga). O teste prova: media type e status
coerentes com o corpo; membros e extensão; erros de validação listados com ponteiro por
campo; `about:blank` com a frase do status; extensão que **não** sobrescreve um membro
padrão; e erro inesperado virando um `500` genérico, **sem** vazar a mensagem da exceção.

Dicas:

- Use **URIs absolutas** em `type` e `instance`; relativas podem ser resolvidas de modo
  inesperado. O `type` deveria apontar para documentação legível do problema, mas o
  consumidor não deve acessá-la automaticamente.
- Não faça o cliente interpretar `detail`: ponha dados para máquinas em extensões.
- Os mesmos erros devem aparecer no [OpenAPI](../openapi/README.md) como resposta
  `application/problem+json`.

## Quando não aplicar

- **APIs que não são HTTP/JSON**, ou protocolos com mecanismo de erro próprio (gRPC, GraphQL
  com `errors`), usam o formato nativo.
- **APIs públicas já em produção com outro formato**: migrar é uma mudança incompatível;
  planeje como [versão nova](../versionamento/README.md) em vez de trocar na hora.
- Um `500` nunca deve explicar *por quê* em detalhe para o cliente; registre o detalhe em
  [log estruturado](../../06-operabilidade/logs-estruturados/README.md) com o identificador
  da ocorrência (`instance`) e responda genericamente.

## Relações

- Os erros de [idempotência](../../06-operabilidade/idempotencia/README.md) (400, 409, 422)
  são exemplos de uso: o rascunho do `Idempotency-Key` mostra respostas nesse formato.
- [Paginação](../paginacao/README.md) também precisa de erro claro para um cursor inválido.

## Referências

- M. Nottingham, E. Wilde, S. Dalal, [RFC 9457: *Problem Details for HTTP APIs*](https://www.rfc-editor.org/rfc/rfc9457.html), 2023 (obsoleta a [RFC 7807](https://www.rfc-editor.org/rfc/rfc7807.html)).
- [RFC 9110: *HTTP Semantics*](https://www.rfc-editor.org/rfc/rfc9110.html), seção 15 (códigos de status).
