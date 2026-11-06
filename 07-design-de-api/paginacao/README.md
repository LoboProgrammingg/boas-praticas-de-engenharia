# Paginação: cursor (keyset) em vez de offset

> "RPCs returning collections of data must provide pagination at the outset, as adding
> pagination later is a backwards-incompatible change."
> Google AIP-158

| | |
|---|---|
| **Origem** | Google API Improvement Proposals, [AIP-158](https://google.aip.dev/158); técnica de *keyset pagination* (*seek method*) |
| **Resolve** | Páginas com itens repetidos ou pulados quando os dados mudam, e consultas que ficam mais lentas a cada página |
| **Em uma frase** | Pagine a partir da **posição** do último item visto, com um token opaco, e não por um deslocamento numérico |

## O problema

`GET /posts?page=2` com `OFFSET` significa "pule as primeiras N linhas **de agora**".
Em [`ruim.py`](ruim.py), o [teste](test_paginacao.py) mostra os dois defeitos clássicos,
numa tabela com 6 posts e páginas de 2:

| Entre a página 1 e a 2... | Página 1 | Página 2 | Defeito |
|---|---|---|---|
| entra um post novo no topo | `[6, 5]` | `[5, 4]` | o item `5` **aparece duas vezes** |
| o post `6` é removido | `[6, 5]` | `[3, 2]` | o item `4` **foi pulado** |

Além disso, o banco precisa percorrer e descartar todas as linhas puladas: `OFFSET 100000`
lê 100 mil linhas para devolver 20.

## A solução

Em [`bom.py`](bom.py), a página seguinte começa depois da **posição** do último item
devolvido, e a consulta é:

```sql
SELECT id, criado_em FROM posts
WHERE (criado_em, id) < (?, ?)
ORDER BY criado_em DESC, id DESC
LIMIT ?
```

Com um índice em `(criado_em, id)`, o custo é proporcional ao tamanho da página, não à
profundidade, e novos itens (antes do cursor) ou remoções não causam repetição nem pulo; o
teste percorre a coleção inteira nos dois cenários da tabela acima e sempre obtém
`[6, 5, 4, 3, 2, 1]`. O desempate por `id` é essencial: sem uma ordenação total e estável,
o cursor ambíguo reintroduz o problema.

As regras do AIP-158 que o exemplo segue:

| Regra | No exemplo |
|---|---|
| Paginar desde o início, porque acrescentar depois é incompatível | `listar` sempre devolve `Pagina` |
| `page_size` opcional, com padrão e máximo documentados; acima do máximo é **reduzido**, não erro | `TAMANHO_PADRAO = 50`, `TAMANHO_MAXIMO = 1000` |
| Resposta com o token da próxima página; **vazio ao fim da coleção** | `proximo_token` é `None` na última página |
| Tokens **opacos**, URL-safe, não interpretáveis pelo usuário | base64 de `[criado_em, id]` |
| Os demais parâmetros devem ser os mesmos da chamada que gerou o token | o chamador repassa filtros e ordem iguais |

> **Atenção:** base64 apenas esconde o formato; não impede que alguém decodifique ou
> forje o token. O AIP pede que o token não seja interpretável. Em produção, assine
> (HMAC) ou criptografe o token, e **valide**: um token inválido deve virar um erro 400 em
> [Problem Details](../problem-details/README.md), como faz `TokenInvalidoError` no teste.

O AIP-158 também descreve `total_size` opcional (que pode ser uma estimativa) e `skip`
opcional. Calcular o total exato custa uma segunda consulta; ofereça apenas se a interface
precisar.

## Quando não aplicar

- **Coleções pequenas e estáveis** (um punhado de itens de configuração): devolva tudo ou
  use offset sem se preocupar.
- **Ir direto à página N** ("página 37") ou mostrar "página 3 de 80" exige offset ou um
  total; cursor só navega para a próxima. Para telas de administração com dados que quase
  não mudam, offset é aceitável.
- **Ordenação por coluna não única ou mutável**: o cursor precisa de uma chave total e
  imutável (`criado_em, id`). Ordenar por algo que muda entre as páginas (ex.: "mais
  votados") exige outra estratégia, como um snapshot.
- **Tokens guardados em banco** podem expirar; defina e comunique o que o cliente deve fazer
  quando um token expira (recomeçar a listagem).

## Relações

- Erros de cursor seguem [Problem Details](../problem-details/README.md).
- A API paginada precisa ser descrita no [OpenAPI](../openapi/README.md) com os
  parâmetros `page_size` e `page_token` e o campo `next_page_token`.
- Acrescentar paginação depois é uma mudança incompatível: veja
  [versionamento](../versionamento/README.md).

## Referências

- Google, [AIP-158: *Pagination*](https://google.aip.dev/158).
- Markus Winand, [*We need tool support for keyset pagination*](https://use-the-index-luke.com/no-offset) (Use The Index, Luke).
- SQLite, [*Row Values*](https://www.sqlite.org/rowvalue.html) (comparação `(a, b) < (?, ?)`).
