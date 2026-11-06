<div align="center">

# Boas Práticas de Engenharia

**Engenharia de software e segurança na prática: princípios, arquitetura, testes e
operação, cada um com exemplo ruim, exemplo bom e um teste que prova a diferença.**

Por [Matheus Lobo](#autor)

[![CI](https://github.com/LoboProgrammingg/boas-praticas-de-engenharia/actions/workflows/ci.yml/badge.svg)](https://github.com/LoboProgrammingg/boas-praticas-de-engenharia/actions/workflows/ci.yml)
[![CodeQL](https://github.com/LoboProgrammingg/boas-praticas-de-engenharia/actions/workflows/codeql.yml/badge.svg)](https://github.com/LoboProgrammingg/boas-praticas-de-engenharia/actions/workflows/codeql.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/LoboProgrammingg/boas-praticas-de-engenharia/badge)](https://scorecard.dev/viewer/?uri=github.com/LoboProgrammingg/boas-praticas-de-engenharia)
[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![TypeScript strict](https://img.shields.io/badge/typescript-strict-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Licença MIT](https://img.shields.io/badge/licen%C3%A7a-MIT-green)](LICENSE)

</div>

---

## Por que este guia existe

Princípios de engenharia costumam ser ensinados como regras absolutas e com exemplos
que não compilam. Este guia faz o contrário:

- **Todo exemplo roda.** Mais de 300 testes provam que a versão boa funciona e que a
  versão ruim falha exatamente onde o texto diz que falha.
- **Todo princípio tem custo.** Cada tópico tem uma seção *Quando não aplicar*:
  abstração prematura, fragmentação excessiva e cerimônia também são problemas.
- **Toda afirmação tem fonte.** Autor, ano e link para a publicação original; o que não
  pôde ser verificado está sinalizado no texto.
- **O repositório pratica o que ensina.** CI com permissões mínimas e actions pinadas por
  SHA, CodeQL, OpenSSF Scorecard, varredura de segredos, `main` protegida e cada seção
  entregue por um Pull Request revisado.

## Mapa

| Seção | O que você encontra | Tópicos |
|---|---|---|
| [01. Princípios de design](01-principios-de-design/) | SOLID, KISS, DRY e AHA, YAGNI, Lei de Demeter, composição sobre herança, CQS, fail fast, imutabilidade e a matriz de conflitos entre eles | 16 |
| [02. Código limpo](02-codigo-limpo/) | Nomes, funções, comentários, tratamento de erros e as críticas sérias ao *Clean Code* | 4 |
| [03. Arquitetura](03-arquitetura/) | Camadas, Hexagonal, Onion e Clean Architecture, DDD estratégico, CQRS, monólito modular vs microsserviços, 12-Factor e ADRs | 6 |
| [04. Testes](04-testes/) | Pirâmide e troféu, TDD, AAA, dublês de teste, property-based, mutation e testes de contrato | 7 |
| [05. Segurança](05-seguranca/) | OWASP Top 10:2025 com pares vulnerável/seguro, API Security, autenticação e autorização, segredos, supply chain, containers, LLM e agentes, LGPD | 18 |
| [06. Operabilidade](06-operabilidade/) | Observabilidade, logs estruturados, timeouts e retries com jitter, circuit breaker, idempotência e degradação elegante | 6 |
| [07. Design de API](07-design-de-api/) | Problem Details (RFC 9457), paginação por cursor, versionamento e OpenAPI | 4 |
| [08. Git e GitHub](08-git-e-github/) | Conventional Commits, Pull Requests, SemVer e changelog, code review | 4 |
| [Checklists](checklists/) | Code review, segurança antes do deploy e novo repositório, prontos para copiar | 3 |

Começando agora? Siga a ordem das seções. Procurando algo específico? Os
[checklists](checklists/) apontam para o tópico certo.

## Como cada tópico é organizado

```text
01-principios-de-design/solid/srp/
├── README.md     definição, origem, o problema, a solução, quando não aplicar, relações, referências
├── ruim.py       o problema resolvido do jeito errado
├── bom.py        o mesmo problema resolvido do jeito certo
└── test_srp.py   prova o comportamento do bom e expõe a falha do ruim
```

Em segurança, o par é `vulneravel.py` / `seguro.py`. Onde TypeScript é mais natural
(validação com Zod, por exemplo), os exemplos seguem o mesmo padrão em `.ts`.

```python
# 05-seguranca/owasp-top-10-2025/a01-broken-access-control/seguro.py
def buscar_pedido(conexao: sqlite3.Connection, pedido_id: int, tenant_id: int) -> Pedido:
    linha = conexao.execute(
        "SELECT id, tenant_id, descricao FROM pedidos WHERE id = ? AND tenant_id = ?",
        (pedido_id, tenant_id),
    ).fetchone()
    if linha is None:
        raise PedidoNaoEncontradoError(pedido_id)  # 404: não revela que o ID existe
    return Pedido(*linha)
```

## Rodando os exemplos

Pré-requisitos: [uv](https://docs.astral.sh/uv/) (Python 3.12+) e Node.js 22+.

```bash
git clone https://github.com/LoboProgrammingg/boas-praticas-de-engenharia.git
cd boas-praticas-de-engenharia

uv sync
uv run pytest                     # todos os exemplos Python
uv run pytest 05-seguranca        # só uma seção
./scripts/typecheck.sh            # mypy --strict em cada pasta de exemplo

npm ci
npm run typecheck && npm test     # exemplos TypeScript
```

## Qualidade e segurança do próprio repositório

| Verificação | Ferramenta | Quando |
|---|---|---|
| Lint e formatação | Ruff | Todo PR |
| Tipos | mypy `--strict` e TypeScript `strict` | Todo PR |
| Testes | pytest, Hypothesis e Vitest | Todo PR |
| Estrutura | Teste que exige README, par ruim/bom e teste em cada tópico | Todo PR |
| Segredos | gitleaks e *push protection* | Todo PR e todo push |
| Links | lychee | Todo PR |
| Análise de segurança | CodeQL (Python, TypeScript e Actions) | Todo PR e semanal |
| Postura de supply chain | OpenSSF Scorecard | Semanal |
| Dependências | Dependabot agrupado, com *cooldown* | Mensal |

A `main` é protegida por ruleset: Pull Request obrigatório, checks obrigatórios,
histórico linear e merge por *squash*.

## Contribuindo

Sugestões, correções e novos tópicos são bem-vindos. Leia o
[guia de contribuição](CONTRIBUTING.md) e use os modelos de issue. Falhas de segurança
devem ser reportadas de forma privada, conforme a [política de segurança](SECURITY.md).

## Autor

**Matheus Lobo** é engenheiro de software, CTO e cofundador da
[WebFrete](https://webfrete.com/autores/matheus). Trabalha com Python, FastAPI,
TypeScript, Next.js, Flutter e PostgreSQL, com foco em arquitetura de software,
Domain-Driven Design e inteligência artificial aplicada.

- GitHub: [@LoboProgrammingg](https://github.com/LoboProgrammingg)
- LinkedIn: [Matheus Lobo](https://www.linkedin.com/in/matheuslobocamara)
- Outro projeto de referência: [DDD-Structure](https://github.com/LoboProgrammingg/DDD-Structure), Domain-Driven Design em Python do modelo à produção

Se este guia foi útil, deixe uma estrela e compartilhe com o seu time. Para citar em
trabalhos acadêmicos, use o arquivo [`CITATION.cff`](CITATION.cff).

## Licença

[MIT](LICENSE) © Matheus Lobo Camara
