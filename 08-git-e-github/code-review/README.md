# Code review

> O objetivo principal da revisão é garantir que a saúde geral do código melhore com o tempo.
> Google Engineering Practices

| | |
|---|---|
| **Origem** | Google, [The Standard of Code Review](https://google.github.io/eng-practices/review/reviewer/standard.html) |
| **Resolve** | Revisões que travam por perfeccionismo ou aprovam qualquer coisa |
| **Em uma frase** | Aprove quando a mudança melhora o código, mesmo que não esteja perfeita |

## Ordem do que olhar

O guia do Google lista o que revisar
([What to look for](https://google.github.io/eng-practices/review/reviewer/looking-for.html)):
design, funcionalidade, complexidade, testes, nomes, comentários, estilo e documentação.
Uma ordem prática, do mais caro ao mais barato de corrigir depois:

1. **Segurança:** entrada validada? autorização no lugar certo? segredo em código ou log?
2. **Correção:** a regra de negócio está certa? bordas e erros tratados?
3. **Design:** a mudança está na camada certa? cria acoplamento desnecessário?
4. **Testes:** provam o comportamento? falhariam se o código estivesse errado?
5. **Legibilidade:** nomes, tamanho de funções, comentários que explicam o porquê.
6. **Estilo:** deixe para o linter e o formatador.

## Tom

- Comente o código, não a pessoa.
- Diferencie **bloqueante** de **sugestão** (prefixos como `nit:` ajudam).
- Explique o porquê e, quando possível, aponte a fonte.
- Elogie o que está bom: reforça o padrão que você quer ver.

Checklist pronto: [checklists/code-review.md](../../checklists/code-review.md).

## Quando não aplicar

- Mudanças triviais e automatizadas (atualização de lockfile com CI verde) podem ser
  aprovadas sem leitura linha a linha, desde que os checks sejam confiáveis.

## Referências

- Google, [Code Review Developer Guide](https://google.github.io/eng-practices/review/).
