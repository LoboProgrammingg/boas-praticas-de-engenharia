# A09:2025 Security Logging and Alerting Failures

[OWASP A09:2025](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/) foi
renomeada para dar ênfase a **alerting**: log que ninguém lê, e que não dispara alerta, tem valor
mínimo ([Introdução](https://top10.owasp.org/2025/0x00_2025-Introduction/)). O
[Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) pede
logs de segurança dedicados e consistentes, separados dos de auditoria/negócio, e "nem de mais nem
de menos".

## O que registrar (eventos de segurança)

| Evento | Campos úteis (sem dado pessoal) |
|---|---|
| Falha de login, bloqueio por tentativas | `user_id` (se existir), `ip` (verifique a base legal), `request_id` |
| Falha de controle de acesso (403/404 por tenant) | `user_id`, `acao`, `recurso`, `request_id` |
| Falha de validação de entrada em volume | `endpoint`, contagem |
| Assinatura de webhook inválida | `provedor`, `motivo` ([A08](../a08-integridade-de-software-e-dados/README.md)) |
| Operações de alto valor (exclusão, exportação, mudança de papel) | `user_id`, `acao`, `alvo`, `resultado` |
| Erros 5xx | `error_id` ([A10](../a10-condicoes-excepcionais/README.md)) |

## Alertas mínimos

| Sinal | Ação |
|---|---|
| Muitas falhas de login para uma conta ou de um IP em curto intervalo | Alerta + bloqueio temporário |
| Pico de 403/404 de autorização para um mesmo usuário (varredura de IDs) | Alerta |
| Rajada de assinaturas de webhook inválidas | Alerta |
| Aumento anormal de 5xx | Alerta de plantão |
| Acesso administrativo fora do padrão | Alerta |

## Checklist

- [ ] Todo evento da tabela acima gera log estruturado com `request_id` / correlação.
- [ ] Cada evento crítico tem **alerta** com responsável e runbook.
- [ ] **Nunca** logar senha, token, CPF, cartão ou chave; mascarar na borda do logger ([`lgpd/`](../../lgpd/README.md) tem um filtro executável).
- [ ] Logs de segurança com retenção definida, acesso restrito e proteção contra adulteração.
- [ ] Valores controlados pelo usuário nunca entram crus em linhas de log (quebra de linha forja entradas).
- [ ] Teste de alerta periódico: simule o evento e confirme que alguém foi notificado.

## Referências

- [OWASP A09:2025](https://owasp.org/Top10/2025/A09_2025-Security_Logging_and_Alerting_Failures/)
- [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html)
