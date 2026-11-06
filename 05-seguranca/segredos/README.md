# Segredos

| | |
|---|---|
| **Resolve** | Credenciais em código, logs, imagens e histórico do Git |
| **Em uma frase** | Segredo vive no ambiente ou num vault, nunca no repositório; se vazou, **rotacione primeiro** |

## Regras

1. **Nunca em código, log ou commit.** Isso inclui `Dockerfile` (`ENV`/`ARG`), `docker-compose.yml`,
   arquivos de teste e comentários. Chaves de teste nascem em tempo de execução
   (`secrets.token_bytes(32)`), como nos exemplos desta seção.
2. **Configuração por variável de ambiente**, lida em um único ponto e tipada. Segredos como
   `SecretStr`, para que `repr()` e logs não imprimam o valor.
3. **`.env` fora do Git** (`.gitignore`), com um `.env.example` que traz só nomes e valores fictícios.
4. **Produção via vault ou secret manager** da plataforma, injetado em tempo de execução. Prefira
   credenciais **de curta duração** (OIDC no CI, ver [`supply-chain/`](../supply-chain/README.md)) a chaves estáticas.
5. **Menor privilégio por segredo**: uma chave por serviço e por ambiente, com o escopo mínimo.
6. **Nada de segredo estruturado em um único secret** do CI (JSON/YAML/XML): a redação de logs do
   GitHub falha em dados estruturados; registre também segredos derivados (JWT gerado, base64)
   ([GitHub: secure use](https://docs.github.com/en/actions/reference/security/secure-use)).
7. **Pepper** de senhas, se usado, em vault/HSM, separado do banco
   ([Password Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html)).

### Configuração tipada (exemplo)

`pydantic-settings` **não** é dependência deste repositório; o snippet é ilustrativo. Adicione-o ao
seu projeto e confirme a versão no lockfile.

```python
from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    database_url: SecretStr
    jwt_signing_key: SecretStr
    webhook_secret: SecretStr
```

`.env.example`, só com nomes:

```bash
DATABASE_URL=<defina-via-variavel-de-ambiente>
JWT_SIGNING_KEY=<defina-via-variavel-de-ambiente>
WEBHOOK_SECRET=<defina-via-variavel-de-ambiente>
```

## Detecção com gitleaks

Os subcomandos e flags abaixo foram conferidos com `gitleaks <comando> --help` na versão **8.30.1**.
O `--help` raiz desta versão lista `git`, `dir` e `stdin` (sem `detect` nem `protect`).

```bash
gitleaks git .                  # histórico de um repositório Git
gitleaks git --staged           # só o que está no stage (pre-commit)
gitleaks dir ./pasta            # uma pasta ou arquivos, sem olhar o Git
gitleaks dir . --redact         # sem imprimir o valor encontrado nos logs
gitleaks git . -v               # saída detalhada
gitleaks git . -f sarif -r relatorio.sarif   # relatório (json, csv, junit, sarif, template)
```

Outras opções confirmadas no `--help`: `-c/--config` (arquivo de regras), `-b/--baseline-path`
(ignorar achados já conhecidos), `-i/--gitleaks-ignore-path` (arquivo `.gitleaksignore`),
`--exit-code`, `--max-decode-depth` (padrão 5) e `--ignore-gitleaks-allow` (ignora comentários
`gitleaks:allow`).

Use em três lugares: **pre-commit** (`gitleaks git --staged`), **CI** (este repositório roda a
[gitleaks-action](../../.github/workflows/ci.yml) com `fetch-depth: 0` para varrer o histórico) e
**push protection** do GitHub. Nunca contorne o hook com `--no-verify`.

## Vazou. E agora?

A ordem importa:

1. **Rotacione/revogue o segredo imediatamente.** Quem já copiou o valor continua com ele; remover
   do Git não revoga nada.
2. Verifique nos logs do provedor se houve uso indevido no intervalo de exposição.
3. Só depois limpe o histórico (reescrita com ferramenta apropriada), ciente de que *forks*, clones e
   caches de CI podem manter cópias.
4. Se o log do CI mostrou o valor, apague o log e rotacione.
5. Registre o incidente. Se envolver dado pessoal de terceiros, avalie a comunicação à ANPD
   ([`lgpd/`](../lgpd/README.md)).

## Referências

- [gitleaks](https://github.com/gitleaks/gitleaks)
- [OWASP Secrets Management Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html)
- [GitHub: push protection](https://docs.github.com/en/code-security/secret-scanning/introduction/about-push-protection)
- [The Twelve-Factor App: Config](https://12factor.net/config)
