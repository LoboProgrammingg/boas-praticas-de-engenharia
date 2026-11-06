# Cadeia de suprimentos de software

| | |
|---|---|
| **Fontes** | [SLSA v1.2](https://slsa.dev/spec/), [Sigstore](https://docs.sigstore.dev/cosign/signing/overview/), [OpenSSF Scorecard](https://github.com/ossf/scorecard/blob/main/docs/checks.md), [GitHub: secure use](https://docs.github.com/en/actions/reference/security/secure-use) |
| **Resolve** | Dependência maliciosa, pipeline sequestrado, artefato adulterado entre o build e a produção |
| **Em uma frase** | Fixe o que entra, dê o mínimo de poder ao pipeline e assine o que sai |

Resumo de revisão por categoria: [A03:2025](../owasp-top-10-2025/a03-cadeia-de-suprimentos/README.md).

## Os controles de maior retorno

| Controle | Efeito |
|---|---|
| Actions fixadas por **SHA** | Uma tag móvel pode ser reapontada para código malicioso; o SHA, não |
| `permissions:` mínimas e `GITHUB_TOKEN` somente leitura | Um passo comprometido não escreve no repositório |
| **OIDC** em vez de chave de nuvem | Credencial de curta duração, presa a repositório/ambiente |
| **Cooldown** de dependências | Dá tempo para a comunidade detectar e remover um pacote malicioso recém-publicado antes de ele chegar ao seu projeto |
| Lockfile + instalação reprodutível | O que roda em produção é o que foi testado |
| Assinatura e proveniência (Sigstore, SLSA) | O consumidor prova de onde veio o artefato |
| SBOM | Saber o que há dentro quando sair o próximo CVE |

## SLSA v1.2

A versão vigente é a **v1.2** (status "Approved"; a v1.1 consta como "Retired"). O *Build Track*
tem níveis L0 a L3: L1 exige que exista *provenance* (previne erro, é trivial de forjar); L2, provenance
**assinada gerada por plataforma hospedada**; L3, plataforma de build endurecida, que protege também contra
adulteração *durante* o build. A v1.2 acrescenta o **Source Track**, sobre o processo de desenvolvimento do código-fonte.
Atestados sozinhos dão Build L2; o L3 exige que o build rode em *reusable workflow*, isolado do workflow chamador
([OWASP DevSecOps Guideline](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-3-Build/2-3-6-Supply-Chain-Security/2-3-6-2-Artifact-Signing-and-Provenance/)).

O NIST SP 800-218 Rev.1 (SSDF v1.2) estava em *Initial Public Draft* (2025-12-17) na última verificação;
não confirmei se virou final.

## Workflow de CI endurecido

Exemplo mínimo. O [`ci.yml` deste repositório](../../.github/workflows/ci.yml) é um caso real com
os mesmos controles (SHAs fixados, `permissions: contents: read`, `persist-credentials: false`).

```yaml
name: ci

on:
  pull_request:            # nunca pull_request_target para rodar código de PR

permissions: {}            # nega tudo no topo; cada job pede o mínimo

jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false   # o token não fica em .git/config
      - uses: astral-sh/setup-uv@68559e99cc807c1eb7e9238fd43a15bba460eec2 # v10.3.3
      - name: Conferir título do PR
        env:
          TITLE: ${{ github.event.pull_request.title }}   # via env, nunca direto em run:
        run: echo "$TITLE"
      - run: uv sync --locked
      - run: uv run pytest
```

| Linha | Controle |
|---|---|
| `uses: ...@<sha> # vX.Y.Z` | Pin por SHA, com a versão em comentário para o Dependabot atualizar |
| `permissions: {}` + por job | Privilégio mínimo |
| `persist-credentials: false` | Evita deixar o token no disco do runner |
| `env: TITLE:` | Evita *script injection* |
| `uv sync --locked` | Falha se o lockfile estiver desatualizado |

### Script injection

`run: echo "${{ github.event.pull_request.title }}"` é **vulnerável**: o texto do título é
substituído *antes* do shell rodar, então um título com aspas e comandos vira código. Passe o valor
por variável de ambiente (como acima) ou como argumento de uma action
([GitHub: secure use](https://docs.github.com/en/actions/reference/security/secure-use)).

### `pull_request_target` e `workflow_run`

Rodam com as permissões e os secrets do branch principal. Combinados com *checkout* do código do PR
(não confiável), permitem tomada do repositório. O check **Dangerous-Workflow** do Scorecard (severidade
Critical) procura exatamente isso: gatilho perigoso com checkout do PR e contexto não confiável em scripts.

### Deploy por OIDC, sem chave de longa duração

Esqueleto; a action de login depende do seu provedor de nuvem.

```yaml
  deploy:
    runs-on: ubuntu-latest
    environment: production      # permite required reviewers
    permissions:
      id-token: write            # pede o token OIDC ao GitHub
      contents: read
    steps:
      - uses: <action-de-login-do-seu-provedor>@<sha-de-40-caracteres>
        with:
          role-to-assume: <identificador-da-role>   # trust policy limitada a repo + environment
```

O provedor valida as *claims* do token (por exemplo `sub` no formato
`repo:org/repo:environment:prod`) antes de entregar credenciais temporárias
([GitHub: OIDC](https://docs.github.com/en/actions/concepts/security/openid-connect)).

## Dependências

### Dependabot com cooldown

O `cooldown` vale para *version updates* (não para *security updates*, que continuam rápidos). Campos:
`default-days`, `semver-major-days`, `semver-minor-days`, `semver-patch-days`, `include` e `exclude`
(valores de 1 a 90 dias). Segundo a [referência](https://docs.github.com/en/code-security/reference/supply-chain-security/dependabot-options-reference),
há um padrão de 3 dias mesmo sem configurar.

```yaml
version: 2
updates:
  - package-ecosystem: pip          # "uv" se o projeto usa uv.lock
    directory: "/"
    schedule: { interval: weekly }
    cooldown: { default-days: 7, semver-major-days: 30, semver-patch-days: 3 }
  - package-ecosystem: npm
    directory: "/"
    schedule: { interval: weekly }
    cooldown: { default-days: 7 }
  - package-ecosystem: github-actions
    directory: "/"
    schedule: { interval: weekly }
  - package-ecosystem: docker
    directory: "/"
    schedule: { interval: weekly }
```

Limitação relatada por usuários: o cooldown do Dependabot para `uv` filtrava só a dependência
direta (issue [dependabot-core #13816](https://github.com/dependabot/dependabot-core/issues/13816), não é documentação oficial).
Por isso o OWASP recomenda **forçar o cooldown também no gerenciador de pacotes**
([guia](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-3-Build/2-3-2-Software-Composition-Analysis/2-3-2-2-Dependency-Management-and-Cooldown-Policies/)):

| Gerenciador | Configuração (segundo o guia) |
|---|---|
| uv | `[tool.uv] exclude-newer = "7 days"` (duração relativa a partir do uv 0.9.17) |
| npm | `.npmrc` com `min-release-age=7` (dias, npm 11.10 ou superior) |
| pnpm | `minimumReleaseAge` (em minutos, pnpm 10.16 ou superior) |
| pip | `--uploaded-prior-to=P7D` (pip 26.1 ou superior; a flag existe no pip 26.2.1 testado aqui) |

### Instalação reprodutível e auditoria

Comandos conferidos nos `--help` locais (uv 0.10.9, pip-audit 2.7.3, npm):

```bash
# Python
uv sync --locked                    # falha se uv.lock não bate com pyproject.toml
pip-audit -r requirements.txt       # -r: arquivo de requisitos; -s osv usa o OSV como serviço

# Node
npm ci --ignore-scripts             # nunca `npm install` em CI; sem scripts de instalação
npm audit --omit=dev --audit-level=high
npm audit signatures                # verifica assinaturas/proveniência do registry

# Multi-ecossistema (OSV-Scanner, conforme a documentação oficial)
osv-scanner scan source -r .
osv-scanner scan -L package-lock.json
```

Hashes no Python: com um `requirements.txt` que traga hashes, `pip install --require-hashes -r requirements.txt`
(usado em [`containers/`](../containers/README.md)) equivale à integridade do `package-lock.json`.

## Assinatura, SBOM e proveniência

*Keyless signing* do Sigstore: o Fulcio emite um certificado de curta duração ligado a uma identidade OIDC, o
evento fica no Rekor (log de transparência) e a chave privada é descartada
([docs](https://docs.sigstore.dev/cosign/signing/overview/)). Assine sempre por **digest**, nunca por tag.

Esqueleto de release (não executado aqui; troque os `<sha>` pelos SHAs reais das versões que você revisou):

```yaml
permissions:
  contents: read
  packages: write
  id-token: write
  attestations: write
steps:
  # ... docker/build-push-action => steps.build.outputs.digest
  - uses: sigstore/cosign-installer@<sha>
  - run: cosign sign --yes "ghcr.io/org/app@${DIGEST}"
    env:
      DIGEST: ${{ steps.build.outputs.digest }}
  - uses: anchore/sbom-action@<sha>
    with:
      image: ghcr.io/org/app@${{ steps.build.outputs.digest }}
      format: cyclonedx-json
      output-file: sbom.cdx.json
  - uses: actions/attest@<sha>
    with:
      subject-name: ghcr.io/org/app
      subject-digest: ${{ steps.build.outputs.digest }}
      push-to-registry: true
```

A [`actions/attest`](https://github.com/actions/attest) gera por padrão um atestado de **SLSA build
provenance** (formato in-toto, assinado com certificado Sigstore efêmero).

Verificação pelo consumidor:

```bash
cosign verify ghcr.io/org/app@sha256:<digest> \
  --certificate-identity="https://github.com/org/app/.github/workflows/release.yml@refs/heads/main" \
  --certificate-oidc-issuer=https://token.actions.githubusercontent.com

gh attestation verify oci://ghcr.io/org/app@sha256:<digest> --repo org/app
```

`--certificate-identity` e `--certificate-oidc-issuer` são obrigatórios na verificação keyless
(documentação do Sigstore e guia do OWASP); `gh attestation verify` aceita `oci://<imagem>` e
`--repo`/`--owner` (conferido em `gh attestation verify --help`). Atestados em repositórios privados
dependem do plano do GitHub; confirme na documentação antes de adotar.

## Registries e *trusted publishing*

PyPI, RubyGems, crates.io, npm e NuGet oferecem publicação por OIDC, sem token de longa duração no CI
([GitHub Blog](https://github.blog/security/supply-chain-security/our-plan-for-a-more-secure-npm-supply-chain/)).
Prefira-a a tokens estáticos e proteja o ambiente de release com revisores obrigatórios.

## OpenSSF Scorecard

O Scorecard automatiza a checagem dos controles acima. Os checks mais ligados a este tema: **Dangerous-Workflow**
(Critical), **Token-Permissions** (High), **Pinned-Dependencies** (Medium), **Dependency-Update-Tool** (High),
**Signed-Releases** (High), **Vulnerabilities** (High), **SAST** (Medium) e **Security-Policy** (Medium).
Para Actions, uma tag só conta como "fixada" se houver *immutable release* publicado; o SHA sempre conta
([checks](https://github.com/ossf/scorecard/blob/main/docs/checks.md)).

## Checklist

- [ ] Todas as actions por SHA, com comentário de versão, atualizadas pelo Dependabot.
- [ ] `permissions: {}` no topo e escrita só onde necessária.
- [ ] Nenhum `${{ github.event.* }}` dentro de `run:`; nenhum `pull_request_target` com checkout do PR.
- [ ] Deploy e publicação por OIDC.
- [ ] Cooldown no bot **e** no gerenciador.
- [ ] `--locked` / `npm ci --ignore-scripts` no CI.
- [ ] Imagens assinadas por digest, com SBOM e proveniência.

## Referências

- [SLSA v1.2](https://slsa.dev/spec/)
- [Sigstore: cosign](https://docs.sigstore.dev/cosign/signing/overview/)
- [OWASP DevSecOps Guideline: assinatura e proveniência](https://owasp.github.io/DevSecOpsGuideline/2-Process/2-3-Build/2-3-6-Supply-Chain-Security/2-3-6-2-Artifact-Signing-and-Provenance/)
- [GitHub: secure use reference](https://docs.github.com/en/actions/reference/security/secure-use)
- [OSV-Scanner: uso](https://google.github.io/osv-scanner/usage/) e [pip-audit](https://github.com/pypa/pip-audit)
