# OpenAPI: o contrato da API como documento

> "The OpenAPI Specification (OAS) defines a standard, programming language-agnostic
> interface description for HTTP APIs, which allows both humans and computers to discover
> and understand the capabilities of a service without requiring access to source code,
> additional documentation, or inspection of network traffic."
> OpenAPI Specification

| | |
|---|---|
| **Origem** | OpenAPI Initiative (Linux Foundation); herdeira da especificação Swagger |
| **Resolve** | Documentação de API escrita à mão que diverge do código, e clientes e validações feitos sem fonte única de verdade |
| **Em uma frase** | Descreva a API em um documento legível por máquina, **gerado do código** (ou que gera o código), e verifique que os dois nunca divergem |

## O problema

Em [`ruim.py`](ruim.py), a especificação é um `dict` escrito à mão, separado do
handler. Ela diz que a resposta tem `valor` (string) e `moeda`; o código devolve
`total_centavos` (inteiro) e nenhuma `moeda`. O [teste](test_openapi.py) compara a
resposta real com o schema documentado e lista as três divergências. Quem gera um cliente
ou valida respostas a partir desse documento obtém algo que não funciona.

## A solução

Tenha **uma fonte única**. Há dois caminhos legítimos:

| Abordagem | Como | Quando |
|---|---|---|
| **Code-first** | os modelos do código geram o schema (FastAPI + Pydantic) | APIs novas, time dono do serviço |
| **Spec-first** | o documento OpenAPI é escrito primeiro e gera servidor/cliente/validação | contrato negociado entre times, vários consumidores |

Em ambos, **verifique no CI** que implementação e documento concordam (testes de contrato
e linters da spec). Em [`bom.py`](bom.py), a abordagem é code-first: os modelos Pydantic
`Pedido` e `Problema` validam as respostas **e** produzem o JSON Schema que entra em
`components/schemas`. O teste:

- confere que o documento declara `openapi: "3.2.0"`, o `operationId`, o parâmetro de
  caminho e as respostas `200` e `404`;
- confirma que o `404` é documentado como `application/problem+json` (veja
  [Problem Details](../problem-details/README.md));
- confirma que todo `$ref` aponta para um schema existente;
- verifica que obrigatoriedade, `enum` e restrições (`minimum`) vêm do modelo;
- e, principalmente, que a **resposta real** obedece ao schema documentado nos dois casos.

### Versão da especificação

A versão **3.2.0** da OpenAPI Specification foi publicada em **19 de setembro de 2025**.
Em 2026-11-06, o site de especificações do projeto já listava a **3.2.1** (publicada em 10
de setembro de 2026) como a versão mais recente, além das séries 3.1.x e 3.0.x. O exemplo
usa `3.2.0`; ao começar um projeto, confira qual a versão suportada pelas ferramentas que
você usa (geradores, validadores, gateways), porque o suporte costuma chegar depois da
publicação. O Schema Object das versões 3.1 e posteriores se alinha ao JSON Schema
Draft 2020-12, que é o dialeto produzido pelo Pydantic v2.

### O que um bom documento tem

- `operationId` estável por operação (vira nome de método nos clientes gerados);
- todos os status de resposta, incluindo erros, com o schema de cada um;
- parâmetros e restrições (`minimum`, `enum`, `format`) no schema, não só na prosa;
- exemplos reais e `description` focada no comportamento observável;
- referências (`$ref`) para evitar duplicação em `components`;
- esquemas de segurança (`securitySchemes`) e, para coleções,
  [paginação](../paginacao/README.md) documentada.

## Quando não aplicar

- **APIs internas minúsculas e efêmeras**: um endpoint usado por um único script não
  precisa de contrato formal; um docstring e o teste bastam.
- **Spec gerada e nunca revisada.** O schema automático descreve o código, não a intenção:
  um campo exposto por engano aparece na documentação. Revise o diff do OpenAPI em code
  review, como código.
- **Documento como única verificação.** OpenAPI descreve forma e não comportamento
  (regras de negócio, ordem de chamadas). Mantenha testes de comportamento e de
  [contrato](../../04-testes/testes-de-contrato/README.md).
- Cuidado com a **versão** do documento: mudanças incompatíveis na API pedem a estratégia
  de [versionamento](../versionamento/README.md), não só um número novo em `info.version`.

## Relações

- Erros: [Problem Details](../problem-details/README.md).
- Coleções: [paginação](../paginacao/README.md) por cursor, com `page_size` e `page_token`.
- Evolução: [versionamento](../versionamento/README.md).
- O documento é o ponto de partida para [testes de contrato](../../04-testes/testes-de-contrato/README.md).

## Referências

- OpenAPI Initiative, [OpenAPI Specification v3.2.0](https://spec.openapis.org/oas/v3.2.0.html) (19/09/2025) e [versão mais recente](https://spec.openapis.org/oas/latest.html) (3.2.1 em 2026-11-06).
- OpenAPI Initiative, [lista de versões](https://spec.openapis.org/oas/).
- Pydantic, [*JSON Schema*](https://docs.pydantic.dev/latest/concepts/json_schema/).
- FastAPI, [*Features*](https://fastapi.tiangolo.com/features/): geração automática da documentação OpenAPI.
