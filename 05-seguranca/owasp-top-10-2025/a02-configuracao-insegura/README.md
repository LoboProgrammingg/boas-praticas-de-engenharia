# A02:2025 Security Misconfiguration

[OWASP A02:2025](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/). Categoria de
**configuração**: o código está certo e a instalação, o ambiente ou o padrão do framework não.
Por isso é um checklist, não um par `vulneravel`/`seguro`.

## Checklist

**Aplicação**

- [ ] `DEBUG` desligado e páginas de erro genéricas fora de desenvolvimento (ver [A10](../a10-condicoes-excepcionais/README.md)).
- [ ] Documentação interativa da API (`/docs`, GraphQL introspection) restrita fora de dev, se a API não for pública.
- [ ] CORS com **allowlist explícita**; nunca `"*"` junto com credenciais.
- [ ] Credenciais e chaves padrão trocadas; nenhum segredo no código ([`segredos/`](../../segredos/README.md)).
- [ ] Upload: tipo real validado (não só `Content-Type`), nome gerado, tamanho limitado, fora do webroot ([File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)).

**Cabeçalhos HTTP** (prática comum; valide cada um contra a documentação do navegador/framework)

| Cabeçalho | Valor de partida |
|---|---|
| `Strict-Transport-Security` | `max-age=63072000; includeSubDomains` (só use `preload` depois de validar todos os subdomínios) |
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Content-Security-Policy` | `default-src 'self'; frame-ancestors 'none'; base-uri 'self'; object-src 'none'` (apps reais costumam precisar de nonce por requisição) |
| `Permissions-Policy` | Desabilitar o que não usa: `camera=(), microphone=(), geolocation=()` |

**Infraestrutura**

- [ ] Banco e Redis **não** expostos ao host/internet; Redis com senha ou ACL.
- [ ] Containers endurecidos ([`containers/`](../../containers/README.md)): não-root, rootfs somente leitura, sem `privileged`.
- [ ] Portas abertas só as necessárias; ambientes dev/staging/prod com a **mesma** configuração base (IaC) e valores diferentes.
- [ ] Permissões de buckets/filas/chaves de nuvem no mínimo necessário; revisão periódica.
- [ ] Serviços e módulos não usados desligados.

**Automatize a verificação**: Scorecard, `trivy config` (misconfiguration em IaC/Dockerfile), revisão
de PR com este checklist, e testes que falham se um cabeçalho obrigatório sumir.

## Referências

- [OWASP A02:2025](https://owasp.org/Top10/2025/A02_2025-Security_Misconfiguration/)
- [Trivy: container image e misconfig](https://trivy.dev/latest/docs/target/container_image/)
