# A06:2025 Insecure Design

[OWASP A06:2025](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/) trata do que **nenhuma
implementação perfeita conserta**: o requisito ou o fluxo já nasceu sem o controle. A introdução do
Top 10:2025 registra melhora na indústria ligada a *threat modeling* e maior ênfase em design seguro
([Introdução](https://top10.owasp.org/2025/0x00_2025-Introduction/)). Por ser processo, aqui há um
modelo de trabalho, não um par de código.

## Modelo de ameaças mínimo por feature

Para toda feature que cruza camadas (banco + API + front + worker), antes de codar:

1. **Diagrama de fluxo de dados** (Mermaid funciona bem em Markdown) com as **fronteiras de
   confiança**: navegador, API, worker, banco, terceiros (pagamento, WhatsApp).
2. **STRIDE por elemento**: Spoofing, Tampering, Repudiation, Information disclosure, Denial of
   service, Elevation of privilege.
3. **Abuse cases** ao lado dos use cases: "e se um usuário repetir isto 10 mil vezes?", "e se enviar o ID de outro tenant?".
4. **Mapear cada mitigação a um requisito ASVS** (`v5.0.0-x.y.z`) e a um teste.

Exemplo de tabela (feature "cupom de desconto"):

| Ameaça (STRIDE) | Abuse case | Mitigação | Verificação |
|---|---|---|---|
| Tampering | Cliente envia o valor do desconto no corpo | O servidor calcula o desconto; o corpo só traz o código | Teste: corpo com `desconto` é rejeitado ([mass assignment](../../api-security/README.md)) |
| Elevation of privilege | Usuário aplica cupom de outro tenant | Cupom filtrado por tenant na consulta ([A01](../a01-broken-access-control/README.md)) | Teste com dois tenants |
| Denial of service / abuso de fluxo | Script tenta milhares de códigos | Rate limit por conta e por IP, com backoff (API6 e API4) | Teste de limite |
| Repudiation | "Não fui eu que usei" | Log de auditoria com `user_id` e `request_id` ([A09](../a09-logging-e-alertas/README.md)) | Teste de log |

## Princípios de design seguro

- **Negar por padrão** (ver o policy engine em [`autenticacao-e-autorizacao/`](../../autenticacao-e-autorizacao/README.md)).
- **Menor privilégio** para usuários, tokens, roles de banco e ferramentas de agentes ([`llm-e-agentes/`](../../llm-e-agentes/README.md)).
- **Falhar fechado** ([A10](../a10-condicoes-excepcionais/README.md)).
- **Fluxos de negócio sensíveis** (cadastro, cupom, reserva, saque) com limites e detecção de abuso, não só autenticação.
- **Separar ambientes e tenants**; defesa em profundidade (aplicação **e** banco).
- **Minimizar dados**: o que não é coletado não vaza ([`lgpd/`](../../lgpd/README.md)).

## Checklist de revisão de design

- [ ] Existe diagrama com fronteiras de confiança para a feature?
- [ ] Cada ameaça relevante tem mitigação e teste?
- [ ] Os requisitos de segurança estão escritos como critérios de aceite?
- [ ] Há limite de uso (taxa, tamanho, quantidade) em cada fluxo exposto?
- [ ] O que acontece quando o serviço externo falha ou responde lixo?

## Referências

- [OWASP A06:2025](https://owasp.org/Top10/2025/A06_2025-Insecure_Design/)
- [OWASP Threat Modeling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html)
