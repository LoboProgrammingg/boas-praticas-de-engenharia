# Conventional Commits

> Uma convenção leve para mensagens de commit que se encaixa no Versionamento Semântico.

| | |
|---|---|
| **Origem** | Especificação [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/), inspirada nas convenções do projeto Angular |
| **Resolve** | Históricos ilegíveis ("ajustes", "wip", "fix") e changelogs escritos à mão |
| **Em uma frase** | `tipo(escopo): descrição` no imperativo, corpo explicando o porquê |

## Formato

```text
<tipo>[escopo opcional][!]: <descrição>

[corpo opcional: o porquê da mudança]

[rodapé(s) opcional(is): BREAKING CHANGE: ..., Closes #12]
```

| Tipo | Quando usar | Efeito no SemVer |
|---|---|---|
| `feat` | Nova funcionalidade | MINOR |
| `fix` | Correção de bug | PATCH |
| `feat!` ou rodapé `BREAKING CHANGE:` | Quebra de compatibilidade | MAJOR |
| `docs`, `test`, `refactor`, `perf`, `build`, `ci`, `chore`, `style` | Demais mudanças | nenhum |

## Ruim vs bom

```text
# Ruim
ajustes
fix
mudei o login e arrumei a tela de pedidos

# Bom
fix(auth): reject expired refresh tokens

Tokens expirados eram aceitos porque a validação comparava datas sem fuso.
Agora todas as datas são UTC.

Closes #42
```

Cada commit faz **uma** coisa. Se a mensagem precisa de "e", provavelmente são dois commits.

## Quando não aplicar

- Em branches de trabalho local, commits intermediários podem ser informais **se** o merge
  for por *squash* com uma mensagem final no padrão.
- Não force o padrão em repositórios cuja convenção já é outra: consistência vale mais.

## Ferramentas

- [commitlint](https://commitlint.js.org/) ou o hook `conventional-pre-commit` do pre-commit para validar mensagens.
- [release-please](https://github.com/googleapis/release-please) para gerar changelog e versão a partir dos commits.

## Referências

- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/pt-br/v1.0.0/).
