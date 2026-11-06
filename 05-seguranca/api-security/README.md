# Segurança de APIs (OWASP API Security Top 10:2023)

| | |
|---|---|
| **Fonte** | [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/), a edição vigente (não encontrei edição posterior) |
| **Resolve** | Riscos específicos de APIs, que o Top 10 geral cobre só de passagem |
| **Em uma frase** | Valide a forma da entrada com schema **fechado**, autorize por objeto **e** por função, e limite o consumo |

## Os 10 riscos

| ID | Risco | Onde está neste repositório |
|---|---|---|
| API1 | Broken Object Level Authorization | [A01](../owasp-top-10-2025/a01-broken-access-control/README.md) (executável) |
| API2 | Broken Authentication | [A07](../owasp-top-10-2025/a07-falhas-de-autenticacao/README.md), [`autenticacao-e-autorizacao/`](../autenticacao-e-autorizacao/README.md) |
| API3 | Broken Object Property Level Authorization (funde *Excessive Data Exposure* e *Mass Assignment*) | **Esta pasta** (executável) |
| API4 | Unrestricted Resource Consumption | Limites e rate limiting, ver abaixo e [A10](../owasp-top-10-2025/a10-condicoes-excepcionais/README.md) |
| API5 | Broken Function Level Authorization | Policy engine em [`autenticacao-e-autorizacao/`](../autenticacao-e-autorizacao/README.md) |
| API6 | Unrestricted Access to Sensitive Business Flows | [A06](../owasp-top-10-2025/a06-design-inseguro/README.md) |
| API7 | Server Side Request Forgery | Allowlist e sem redirects, ver [A01](../owasp-top-10-2025/a01-broken-access-control/README.md#quando-não-basta) |
| API8 | Security Misconfiguration | [A02](../owasp-top-10-2025/a02-configuracao-insegura/README.md) |
| API9 | Improper Inventory Management | Abaixo |
| API10 | Unsafe Consumption of APIs | Abaixo |

## API3: mass assignment e exposição excessiva

### O problema

[`vulneravel.py`](vulneravel.py): o corpo vira atributos do usuário. O modelo Pydantic usa
`extra="allow"` e a função copia **tudo** com `setattr`, então um `PATCH /users/me` com
`{"display_name": "Ana", "is_admin": true, "tenant_id": 99}` promove o usuário e o muda de tenant.
Na saída, o objeto inteiro é serializado, incluindo `senha_hash`.
O equivalente em TypeScript está em [`vulneravel.ts`](vulneravel.ts): `Object.assign(usuario, corpo)`
sobre um schema "solto" (`z.looseObject`).

### A solução

[`seguro.py`](seguro.py):

- **Entrada**: `ConfigDict(extra="forbid")` rejeita qualquer campo não declarado (HTTP 422 no FastAPI) e
  a função atribui explicitamente só `display_name`. O padrão do Pydantic é `extra="ignore"`: o campo
  extra é descartado em silêncio, o que evita a escalada, mas esconde tentativas; `forbid` as
  torna visíveis e testáveis.
- **Saída**: `PerfilPublico` declara o que sai. Nunca serialize o modelo de banco direto.

[`seguro.ts`](seguro.ts) usa Zod com `.strict()`, que rejeita chaves desconhecidas com `ZodError`.
No Zod 4 (versão 4.6.7 no `package-lock.json`), `.strict()` continua disponível; a tipagem da
biblioteca sugere `z.strictObject(...)` como forma preferida, equivalente.

Testes: [`test_mass_assignment.py`](test_mass_assignment.py) (8) e
[`mass-assignment.test.ts`](mass-assignment.test.ts) (4) provam os dois lados.

```bash
uv run pytest 05-seguranca/api-security
npx vitest run 05-seguranca/api-security
```

## API4: consumo sem limite

- Rate limit por (IP + identificador) e por conta, com `429` e `Retry-After`; contador em Redis
  (`INCR` + `EXPIRE`) ou biblioteca mantida (verifique no lockfile antes de adotar).
- Teto de tamanho de corpo, de itens por página (`limit` máximo), de profundidade e de uploads.
- Timeouts em chamadas de saída e em consultas ao banco.
- Operações caras (exportações, buscas) assíncronas e com cota.

## API9: inventário

Mantenha a lista de versões e ambientes expostos (incluindo `/docs` de staging, versões antigas
`/v1`, endpoints de debug). Versão que ninguém mantém continua respondendo e continua vulnerável.

## API10: consumo inseguro de APIs de terceiros

Trate a **resposta** de uma API externa como entrada não confiável: valide com schema (Pydantic/Zod),
defina timeouts e limite de tamanho, não siga redirects para destinos não esperados, e não propague
o erro cru do terceiro ao seu cliente.

## Referências

- [OWASP API Security Top 10:2023](https://owasp.org/API-Security/editions/2023/en/0x11-t10/)
- [CWE-915: mass assignment](https://cwe.mitre.org/data/definitions/915.html)
- [Pydantic: Models](https://docs.pydantic.dev/latest/concepts/models/) e [Zod API](https://zod.dev/api)
- [OWASP Mass Assignment Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html)
