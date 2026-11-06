# A01:2025 Broken Access Control (BOLA)

| | |
|---|---|
| **Categoria** | [A01:2025 Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/); na API é o [API1:2023 BOLA](../../api-security/README.md) |
| **CWE típico** | [CWE-639](https://cwe.mitre.org/data/definitions/639.html): autorização contornada por chave controlada pelo usuário |
| **Resolve** | Usuário autenticado lendo ou alterando objetos de outro usuário ou de outro tenant |
| **Em uma frase** | Autenticar não é autorizar: toda consulta por ID precisa carregar o escopo do dono |

## O problema

Em [`vulneravel.py`](vulneravel.py), `buscar_pedido` recebe o `tenant_id` do usuário mas **não
o usa**: a consulta é `WHERE id = ?`. Quem troca o `2` por `1` na URL lê o pedido de outra
empresa. É o erro mais comum em APIs porque o código "funciona" em todo teste feliz.

## A solução

Em [`seguro.py`](seguro.py) o escopo vai para a própria consulta (`WHERE id = ? AND tenant_id = ?`)
e o resultado vazio vira `PedidoNaoEncontradoError`, mapeada para **404**:

- Filtrar na consulta, e não "buscar e depois comparar", evita esquecer a comparação em
  um caminho de código novo.
- **404 em vez de 403** impede que o endpoint sirva de oráculo de existência: pedido alheio
  e pedido inexistente são indistinguíveis (o teste verifica isso).

O teste [`test_bola.py`](test_bola.py) mostra os dois lados: a versão vulnerável devolve o
pedido da empresa B ao usuário da empresa A; a segura não.

## Defesa em profundidade (multi-tenant com PostgreSQL)

Row-Level Security faz o banco recusar o que a aplicação esqueceu. Snippet ilustrativo (não
executado neste repositório):

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
  USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

Pontos conferidos na [documentação do PostgreSQL](https://www.postgresql.org/docs/current/ddl-rowsecurity.html):
o dono da tabela normalmente ignora as policies, a menos que você use `FORCE ROW LEVEL SECURITY`;
superusers e roles com `BYPASSRLS` **sempre** ignoram. Logo, a role de conexão da aplicação
não pode ser superuser nem `BYPASSRLS`. O `tenant_id` da sessão deve ser definido por transação
com parâmetro vinculado, nunca por f-string.

## Quando não basta

- **Middleware sozinho não é controle de acesso.** O CVE-2025-29927 do Next.js permitia pular o
  middleware com um cabeçalho interno; a própria Vercel diz que não recomenda middleware como único
  método de proteção de rotas
  ([postmortem](https://vercel.com/blog/postmortem-on-next-js-middleware-bypass)). Reverifique no
  ponto de acesso aos dados.
- **Função, não só objeto.** BOLA protege o *objeto*; operações administrativas precisam de
  checagem por *função* (API5). Use um policy engine, como em
  [`autenticacao-e-autorizacao/`](../../autenticacao-e-autorizacao/README.md).
- **SSRF** foi absorvido por A01 em 2025: o servidor que busca URLs informadas pelo usuário também
  quebra controle de acesso (rede interna, metadados de nuvem). Ver o
  [SSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html):
  allowlist de destinos e **sem seguir redirects**.

## Checklist

- [ ] Toda consulta por ID filtra por dono ou tenant na própria query.
- [ ] Objeto alheio e inexistente respondem igual (404).
- [ ] A role do banco usada pela aplicação não ignora RLS.
- [ ] Há teste automatizado com dois tenants para cada recurso novo.
- [ ] Rotas protegidas verificam acesso no handler/serviço, não só em middleware.

## Referências

- [OWASP A01:2025](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/)
- [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html)
- [PostgreSQL: Row Security Policies](https://www.postgresql.org/docs/current/ddl-rowsecurity.html)
