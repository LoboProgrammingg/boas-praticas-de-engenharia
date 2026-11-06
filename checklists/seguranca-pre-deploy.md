# Checklist de segurança antes do deploy

Baseado no [OWASP Top 10:2025](https://owasp.org/Top10/2025/) e no
[OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/).
Detalhes e exemplos na seção 05, Segurança.

## Aplicação

- [ ] Controle de acesso por objeto em todos os endpoints (sem BOLA/IDOR)
- [ ] Senhas com Argon2id (ou bcrypt) e parâmetros recomendados pela OWASP
- [ ] Tokens com algoritmo fixo, expiração curta e validação de `aud`/`iss`
- [ ] Rate limiting em login, cadastro e recuperação de senha
- [ ] CORS com lista explícita de origens; nunca `*` com credenciais
- [ ] Cabeçalhos de segurança (CSP, HSTS, `X-Content-Type-Options`)
- [ ] Erros genéricos para o cliente, detalhes só no log interno, sem dados pessoais

## Dados

- [ ] Segredos vêm de variáveis de ambiente ou cofre, nunca do repositório
- [ ] Logs sem senha, token, documento pessoal ou cartão
- [ ] Backups testados e criptografados

## Cadeia de suprimentos

- [ ] Dependências travadas em lockfile e auditadas
- [ ] Imagem de container sem root, mínima e escaneada
- [ ] CI com permissões mínimas e actions pinadas por SHA

## Operação

- [ ] Alertas para falhas de autenticação e erros inesperados
- [ ] Plano de resposta a incidentes conhecido pelo time
- [ ] Para dados pessoais no Brasil: processo de comunicação de incidente à ANPD definido (LGPD)
