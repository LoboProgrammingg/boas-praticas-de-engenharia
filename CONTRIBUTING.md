# Como contribuir

Obrigado por querer melhorar este guia. Toda contribuição passa por Pull Request,
revisão e CI verde, inclusive as do mantenedor.

## Antes de começar

- Procure uma [issue](https://github.com/LoboProgrammingg/boas-praticas-de-engenharia/issues) existente ou abra uma usando os modelos.
- Correções pequenas (erro de digitação, link quebrado) podem ir direto para PR.

## Ambiente

```bash
uv sync                      # Python 3.12+
npm ci                       # Node 22+
uv run pytest                # testes Python
./scripts/typecheck.sh       # mypy --strict por pasta de exemplo
npm run typecheck && npm test
```

## Padrão de um tópico

Cada tópico é uma pasta com:

| Arquivo | Conteúdo |
|---|---|
| `README.md` | Definição, tabela Origem/Resolve/Em uma frase, O problema, A solução, **Quando não aplicar**, Relações, Referências |
| `ruim.py` / `bom.py` | O mesmo problema resolvido do jeito errado e do jeito certo (em segurança: `vulneravel.py` / `seguro.py`) |
| `test_<topico>.py` | Prova o comportamento do exemplo bom **e** expõe a falha do ruim |

Use o tópico [SRP](01-principios-de-design/solid/srp/) como gabarito. Exemplos em
TypeScript seguem o mesmo padrão (`ruim.ts`, `bom.ts`, `<topico>.test.ts`).

## Regras de conteúdo

- **Fonte primária** para toda afirmação: autor, ano e link. Se não for possível verificar,
  não afirme.
- Explique o custo: todo princípio tem situações em que não deve ser aplicado.
- Exemplos mínimos, tipados (`mypy --strict` e TypeScript `strict`), sem rede e determinísticos.
- Segurança: nada de payloads de exploração reais nem strings com formato de segredo.
- Texto em português do Brasil; termos técnicos consagrados podem ficar em inglês.

## Commits e Pull Requests

- [Conventional Commits](https://www.conventionalcommits.org/pt-br/v1.0.0/): `feat(seguranca): add CSRF topic`.
- Um PR por tópico ou seção, com `Closes #n` e o checklist do template preenchido.
- Merge por *squash*; a branch é apagada após o merge.

## Código de conduta

Ao participar, você concorda com o [Código de Conduta](CODE_OF_CONDUCT.md).
