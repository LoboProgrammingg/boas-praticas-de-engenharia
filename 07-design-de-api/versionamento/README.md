# Versionamento de API (estilo Stripe)

> "To date, we've maintained compatibility with every version of our API since the
> company's inception in 2011."
> Brandur Leach, Stripe, *APIs as infrastructure: future-proofing Stripe with versioning*

| | |
|---|---|
| **Origem** | Stripe, 2017 (Brandur Leach); versionamento semântico (SemVer) para bibliotecas |
| **Resolve** | Evoluir uma API sem quebrar quem já integrou, e sem manter dezenas de cópias do código |
| **Em uma frase** | Evite quebrar; quando precisar, entregue a mudança como uma nova versão, com o código falando só a versão atual |

## O problema

Em [`ruim.py`](ruim.py), `name` virou `full_name` e `balance` passou de um inteiro para um
objeto, **no lugar**. Uma integração escrita antes lê `corpo["name"]`: no instante do
deploy, ela quebra. O [teste](test_versionamento.py) mostra o `KeyError`. Uma API é um
contrato; o Stripe o descreve como algo que "não pode mudar sem considerável cooperação e
esforço" de todos os usuários.

O oposto também dói: congelar a API para sempre trava a evolução, e copiar a base de código
inteira para cada versão multiplica manutenção e bugs.

## A solução

Primeiro, **evite** a mudança incompatível. Nas palavras do Stripe, campos que existiam
devem continuar existindo, com o mesmo nome e tipo; já adicionar um endpoint novo ou um
campo que nunca existiu é seguro. Remover, renomear ou mudar o tipo de um campo não é.

Quando for inevitável, o modelo do Stripe (que [`bom.py`](bom.py) reproduz em miniatura):

| Elemento | Como funciona |
|---|---|
| **Versões rolantes, nomeadas por data** (ex.: `2017-05-24`) | cada versão traz poucas mudanças incompatíveis, o que facilita a atualização incremental |
| **Conta fixada (*pinned*)** | na primeira requisição, a conta é fixada na versão mais recente; a partir daí, toda chamada usa essa versão. Ninguém recebe quebra sem querer |
| **Override por requisição** | o cabeçalho `Stripe-Version` (no exemplo, `versao_no_cabecalho`) troca a versão de uma só chamada, útil para testar a atualização |
| **Módulos de mudança de versão** | o código só produz a representação **atual**; depois, o servidor "volta no tempo", aplicando cada módulo (`MudancaDeVersao`) até a versão alvo |

Os testes provam: uma conta fixada em `2026-01-01` continua recebendo `name` e saldo
inteiro; uma conta nova recebe a forma atual; uma versão intermediária aplica só as
mudanças posteriores a ela; o cabeçalho vale para uma requisição; atualizar a versão da conta
é decisão explícita; versão inexistente é rejeitada.

O Stripe também tem um prefixo de **versão maior** no caminho (`/v1/...`), mas o artigo diz
que reserva o direito de usá-lo e que ele não deve mudar tão cedo: mudanças de versão maior
tornam a atualização dolorosa. As mudanças do dia a dia vão pelas versões por data (quase
cem atualizações incompatíveis em seis anos, segundo o texto). O artigo
aponta o custo: compatibilidade retroativa "isn't free", e cada versão é mais código para
entender, então a equipe limita o número de mudanças incompatíveis e encapsula cada uma.

### E o SemVer?

[SemVer](https://semver.org/) (MAJOR.MINOR.PATCH) serve a **bibliotecas e SDKs** com API
pública declarada: MAJOR para mudanças incompatíveis. Para uma **API HTTP**, as estratégias
(versão no caminho `/v1`, em cabeçalho, ou por data como acima) têm trade-offs; escolha uma,
documente e mantenha. Commits convencionais marcam a quebra com `!` ou `BREAKING CHANGE`
([Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)), o que alimenta o
número MAJOR de um SDK.

## Quando não aplicar

- **API interna com um único consumidor que você controla**: mude os dois lados juntos. O
  custo de uma camada de versões não se paga.
- **Protótipo ou API ainda sem usuários**: quebre à vontade, mas comunique.
- **Versionar tudo "por precaução".** Sem mudanças incompatíveis, não há versão a criar;
  prefira mudanças aditivas.
- O modelo do Stripe exige disciplina e infraestrutura (testes por versão, documentação do
  changelog). Para APIs menores, um `/v2` quando realmente houver ruptura pode ser
  suficiente.

## Relações

- Contratos e compatibilidade são verificados por
  [testes de contrato](../../04-testes/testes-de-contrato/README.md).
- A versão e o changelog vivem no [OpenAPI](../openapi/README.md).
- Acrescentar [paginação](../paginacao/README.md) depois é uma mudança incompatível: desenhe
  as coleções paginadas desde o início.
- Mudar o formato de erro para [Problem Details](../problem-details/README.md) numa API em
  uso é uma mudança incompatível.

## Referências

- Brandur Leach, [*APIs as infrastructure: future-proofing Stripe with versioning*](https://stripe.com/blog/api-versioning), Stripe, 2017.
- [Semantic Versioning 2.0.0](https://semver.org/).
- [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).
