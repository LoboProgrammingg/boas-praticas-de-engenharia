# 05. Segurança

Controles de segurança que cabem em código, em configuração de pipeline e em processo,
cada um com a fonte normativa e, quando faz sentido, um par `vulneravel` / `seguro`
**executável** e testado: o teste prova que a versão vulnerável é de fato vulnerável e que
a segura bloqueia o problema.

> Finalidade defensiva e educacional. Os exemplos usam entradas mínimas e inofensivas
> (um `' OR '1'='1` contra SQLite em memória, um `<script>` que só é escapado), sem rede e
> sem alvos reais.

## Como usar esta seção

| Fonte | Para que serve aqui |
|---|---|
| [OWASP ASVS 5.0.0](https://owasp.org/www-project-application-security-verification-standard/) | Fonte de **requisitos testáveis**: transforme cada item em critério de revisão ou de aceite. Cite sempre com a versão, no formato `v5.0.0-<capítulo>.<seção>.<requisito>` (ex.: `v5.0.0-1.2.5`), porque os IDs mudam entre versões. |
| [OWASP Top 10:2025](owasp-top-10-2025/README.md) | **Awareness**: um mapa dos riscos mais frequentes para treinar o time e priorizar. Não é checklist de conformidade. |
| [OWASP API Security Top 10:2023](api-security/README.md) | Mesmo papel do Top 10, específico para APIs. |
| [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/) | Como implementar cada controle em detalhe. |

Regra prática: ao revisar um PR, anote o risco como `A01:2025` (ou `API1:2023`) e o requisito
verificável como `v5.0.0-x.y.z`.

## Índice

| Pasta | Conteúdo | Exemplo executável |
|---|---|---|
| [`owasp-top-10-2025/`](owasp-top-10-2025/README.md) | As 10 categorias do Top 10:2025, uma pasta por categoria | A01, A04, A05, A07, A08, A10 |
| [`api-security/`](api-security/README.md) | API Top 10:2023 e mass assignment (Pydantic e Zod) | Python e TypeScript |
| [`autenticacao-e-autorizacao/`](autenticacao-e-autorizacao/README.md) | RFC 9700, PKCE, NIST SP 800-63B-4, tokens e policy engine | Policy engine |
| [`segredos/`](segredos/README.md) | Variáveis de ambiente, vaults, rotação, gitleaks | Só README |
| [`supply-chain/`](supply-chain/README.md) | SLSA, Sigstore, SBOM, lockfiles, Dependabot, GitHub Actions | Workflow endurecido |
| [`containers/`](containers/README.md) | Dockerfile e runtime endurecidos, Trivy, CIS Docker Benchmark | `Dockerfile.vulneravel` / `Dockerfile.seguro` |
| [`llm-e-agentes/`](llm-e-agentes/README.md) | OWASP LLM Top 10 (2025): saída do modelo como entrada não confiável | Python |
| [`lgpd/`](lgpd/README.md) | Incidentes (ANPD), logs sem dado pessoal, minimização | Python |

## LGPD em uma frase

Segurança e privacidade se cruzam em três pontos: o **log é tratamento de dado pessoal**,
o princípio da **necessidade** (art. 6º, III) manda coletar e guardar o mínimo, e um
incidente com risco relevante exige comunicação à ANPD e aos titulares em **3 dias úteis**.
Detalhes e fontes em [`lgpd/`](lgpd/README.md). Isto é material técnico, não parecer jurídico.

## Como rodar os exemplos

Da raiz do repositório:

```bash
uv sync
uv run pytest 05-seguranca
uv run ruff check 05-seguranca
uv run mypy 05-seguranca/owasp-top-10-2025/a01-broken-access-control   # uma pasta por vez

npm ci
npx vitest run 05-seguranca     # exemplo TypeScript de api-security
```

## Convenções desta seção

- Nenhum segredo, token ou chave real no repositório. Chaves de teste nascem em tempo de
  execução (`secrets.token_bytes`) e valores de exemplo são placeholders óbvios.
- `vulneravel.py` existe para ser lido e quebrado; `seguro.py` segue todas as regras do
  linter (inclusive as de segurança, `S`) e tipagem `mypy --strict`.
- Onde uma afirmação não pôde ser verificada em fonte primária, o texto diz isso.
