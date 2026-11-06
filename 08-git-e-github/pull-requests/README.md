# Pull Requests

> Um PR é uma proposta de mudança acompanhada do seu raciocínio.

| | |
|---|---|
| **Origem** | Fluxo de trabalho do GitHub; práticas de revisão do [Google Engineering Practices](https://google.github.io/eng-practices/) |
| **Resolve** | Mudanças grandes, sem contexto e que chegam à branch principal sem verificação |
| **Em uma frase** | PR pequeno, com uma intenção, descrição clara, issue vinculada e CI verde |

## Práticas

1. **Pequeno e com uma intenção.** O guia do Google recomenda mudanças pequenas porque são
   revisadas mais rápido e com mais cuidado ([Small CLs](https://google.github.io/eng-practices/review/developer/small-cls.html)).
2. **Descrição que se sustenta sozinha:** o que muda, por quê, como verificar
   ([Writing good CL descriptions](https://google.github.io/eng-practices/review/developer/cl-descriptions.html)).
3. **Vincule a issue** com palavras-chave (`Closes #12`): a issue fecha no merge
   ([documentação](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue)).
4. **Draft PR** para pedir opinião cedo, antes de estar pronto.
5. **Auto-revisão** do diff no GitHub antes de pedir revisão.
6. **Merge por squash** quando os commits intermediários não importam; a mensagem final segue Conventional Commits.
7. **Branch protegida:** PR obrigatório, checks obrigatórios e histórico linear via
   [rulesets](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/about-rulesets).

## Nomes de branch

```text
feat/descontos-progressivos
fix/token-expirado
docs/readme-instalacao
```

## Quando não aplicar

- Em repositório pessoal de rascunho, PR obrigatório é burocracia. Assim que houver CI,
  deploy ou outra pessoa, passe a usar.

## Referências

- Google, [Engineering Practices](https://google.github.io/eng-practices/).
- GitHub Docs, [About pull requests](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests).
