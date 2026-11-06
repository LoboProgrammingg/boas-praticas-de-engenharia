# SemVer e changelog

> Dado um número de versão MAJOR.MINOR.PATCH: MAJOR para mudanças incompatíveis,
> MINOR para funcionalidades compatíveis e PATCH para correções compatíveis.

| | |
|---|---|
| **Origem** | Tom Preston-Werner, [Semantic Versioning 2.0.0](https://semver.org/lang/pt-BR/); Olivier Lacan, [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) |
| **Resolve** | Versões que não dizem nada sobre o risco de atualizar |
| **Em uma frase** | O número da versão é um contrato; o changelog é escrito para pessoas |

## Regras essenciais

- `1.4.2 → 1.4.3`: só correções. Atualize sem medo.
- `1.4.2 → 1.5.0`: funcionalidade nova, compatível.
- `1.4.2 → 2.0.0`: algo quebrou. Leia o changelog antes.
- `0.y.z`: desenvolvimento inicial; qualquer coisa pode mudar.
- Uma versão publicada **nunca** é alterada; corrija com uma nova versão.

## Changelog

Agrupe por versão e por tipo: `Adicionado`, `Alterado`, `Obsoleto`, `Removido`,
`Corrigido`, `Segurança`. Mantenha uma seção `[Não lançado]` no topo. Changelog não
é dump do `git log`: escreva o impacto para quem usa. Exemplo vivo:
[CHANGELOG.md deste repositório](../../CHANGELOG.md).

## Quando não aplicar

- Aplicações que não são consumidas como dependência (um site, um serviço interno) podem
  versionar por data ou por build. SemVer brilha em **bibliotecas e APIs**.

## Referências

- [Semantic Versioning 2.0.0](https://semver.org/lang/pt-BR/).
- [Keep a Changelog 1.1.0](https://keepachangelog.com/pt-BR/1.1.0/).
