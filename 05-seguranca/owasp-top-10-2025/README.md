# OWASP Top 10:2025

O [OWASP Top 10:2025](https://owasp.org/Top10/2025/) é a oitava edição da lista, publicada em
**6 de novembro de 2025**. Em relação à anterior traz duas categorias novas (A03 e A10), uma
consolidação (SSRF foi incorporado a A01) e renomeia A07 e A09
([introdução](https://top10.owasp.org/2025/0x00_2025-Introduction/)).

A lista é **awareness**, não requisito. Para requisitos testáveis use o
[ASVS 5.0.0](../README.md#como-usar-esta-seção).

## As 10 categorias

| ID | Categoria | Pasta | O que há |
|---|---|---|---|
| A01 | [Broken Access Control](https://owasp.org/Top10/2025/A01_2025-Broken_Access_Control/) | [`a01-broken-access-control/`](a01-broken-access-control/README.md) | BOLA: filtrar por tenant na consulta, 404 (executável) |
| A02 | [Security Misconfiguration](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/) | [`a02-configuracao-insegura/`](a02-configuracao-insegura/README.md) | Checklist |
| A03 | [Software Supply Chain Failures](https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/) | [`a03-cadeia-de-suprimentos/`](a03-cadeia-de-suprimentos/README.md) | Checklist e links para [`supply-chain/`](../supply-chain/README.md) |
| A04 | [Cryptographic Failures](https://owasp.org/Top10/2025/A04_2025-Cryptographic_Failures/) | [`a04-falhas-criptograficas/`](a04-falhas-criptograficas/README.md) | Argon2id × SHA-256 (executável) |
| A05 | [Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) | [`a05-injecao/`](a05-injecao/README.md) | SQL parametrizado e escape de XSS (executável) |
| A06 | [Insecure Design](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/) | [`a06-design-inseguro/`](a06-design-inseguro/README.md) | Checklist e modelo de ameaças |
| A07 | [Authentication Failures](https://owasp.org/Top10/2025/A07_2025-Authentication_Failures/) | [`a07-falhas-de-autenticacao/`](a07-falhas-de-autenticacao/README.md) | JWT com algoritmos fixos, `exp`/`aud` (executável) |
| A08 | [Software or Data Integrity Failures](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/) | [`a08-integridade-de-software-e-dados/`](a08-integridade-de-software-e-dados/README.md) | Webhook HMAC + anti-replay (executável) |
| A09 | [Security Logging and Alerting Failures](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/) | [`a09-logging-e-alertas/`](a09-logging-e-alertas/README.md) | Checklist |
| A10 | [Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/) | [`a10-condicoes-excepcionais/`](a10-condicoes-excepcionais/README.md) | Fail closed, erro genérico com `error_id` (executável) |

Categorias de processo ou configuração (A02, A03, A06, A09) não têm um "antes e depois" de
poucas linhas que ensine algo, então trazem checklists concretos.

## Rodar os exemplos

```bash
uv run pytest 05-seguranca/owasp-top-10-2025
```

## Referências

- [OWASP Top 10:2025](https://owasp.org/Top10/2025/), índice oficial.
- [Introdução ao Top 10:2025](https://top10.owasp.org/2025/0x00_2025-Introduction/), com as mudanças da edição.
