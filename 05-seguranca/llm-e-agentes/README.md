# LLMs e agentes: a saída do modelo é entrada não confiável

| | |
|---|---|
| **Fontes** | [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/); [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) |
| **Resolve** | Texto gerado por um modelo virando comando, SQL, HTML ou chamada de ferramenta sem validação |
| **Em uma frase** | Valide e autorize o que o modelo pede como validaria um formulário vindo da internet |

## Os riscos centrais

Itens do LLM Top 10 (2025), lista completa em [genai.owasp.org](https://genai.owasp.org/llm-top-10/):

| ID | Risco | Relação com esta pasta |
|---|---|---|
| LLM01 | Prompt Injection | Qualquer texto que o modelo leia (página, e-mail, documento, resultado de ferramenta) pode conter instruções |
| LLM05 | Improper Output Handling | Validação insuficiente da saída do modelo antes de passá-la a outros componentes |
| LLM06 | Excessive Agency | Sistema com ferramentas ou permissões além do necessário |

(LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM07
System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation e LLM10 Unbounded
Consumption completam a lista.)

Existe ainda o **OWASP Top 10 for Agentic Applications for 2026**, publicado em 9 de dezembro de 2025,
um framework revisado por mais de 100 especialistas sobre agentes autônomos que planejam e agem. A página
que li traz apenas a introdução; **não verifiquei os itens individuais**, então não os listo aqui.
Também não confirmei se há um LLM Top 10 mais novo que o de 2025.

## O problema

Injeção de prompt não tem uma "correção" no texto do prompt: não existe filtro que garanta que o
modelo nunca obedecerá a uma instrução escondida em um documento. O que se controla é **o que a saída do modelo
pode causar**. [`vulneravel.py`](vulneravel.py) faz o oposto: lê o JSON gerado e executa
`getattr(loja, chamada["ferramenta"])(**argumentos)`. Se um documento envenenado convencer o modelo a
emitir `{"ferramenta": "apagar_tudo"}`, os pedidos somem. O teste usa uma loja em memória e prova isso.

## A solução em camadas

[`seguro.py`](seguro.py):

| Camada | Implementação |
|---|---|
| **Allowlist** de ferramentas | Só `consultar_pedido` e `cancelar_pedido` existem como tipos válidos (união discriminada Pydantic) |
| **Schema fechado** | `extra="forbid"`, `pedido_id` inteiro positivo; JSON inválido, tipo errado ou campo extra (ex.: `usuario_id`) vira `SaidaInvalidaError` |
| **Identidade da sessão, não do modelo** | O pedido precisa pertencer ao `usuario_id` autenticado; pedido alheio é `PedidoNaoEncontradoError` |
| **Menor privilégio** | O agente não tem ferramenta destrutiva além do cancelamento; não existe `apagar_tudo` a ser chamado |
| **Humano no circuito** | `cancelar_pedido` exige `aprovado_por_humano=True`; sem isso, `AprovacaoNecessariaError` |

O teste [`test_saida_do_llm.py`](test_saida_do_llm.py) cobre ferramenta fora da lista, cinco formas de saída malformada,
consulta válida, tentativa de tocar em pedido de outro usuário e o fluxo de aprovação.

## Outras regras para quem constrói agentes

- **Saída que vira SQL, HTML ou shell**: aplique os controles de [A05](../owasp-top-10-2025/a05-injecao/README.md)
  (parâmetros, escape, `shell=False`); o modelo é só mais uma fonte de entrada.
- **Dados externos são entrada não confiável**: marque e isole conteúdo recuperado (RAG, web, e-mail) do que são
  instruções suas, e não dê ao mesmo contexto acesso simultâneo a dados privados e a um canal de saída.
- **Credenciais**: ferramentas recebem credenciais com escopo mínimo e curtas, nunca a chave do usuário nem a sua.
- **Limites**: orçamento de tokens, de chamadas e de tempo por tarefa (LLM10).
- **Registro**: logue ferramenta, argumentos validados e decisão de aprovação, **sem** dado pessoal
  ([`lgpd/`](../lgpd/README.md)).

## Quando não basta

Este exemplo valida *formato* e *autorização*. Ele não impede que o modelo escolha uma consulta
válida mas indesejada (por exemplo, cancelar o pedido errado do próprio usuário), por isso a aprovação humana para ações
destrutivas continua necessária. Segurança de LLM é defesa em profundidade, não um único filtro.

## Referências

- [OWASP Top 10 for LLM Applications 2025](https://genai.owasp.org/llm-top-10/)
- [OWASP Top 10 for Agentic Applications for 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- [Pydantic: Models](https://docs.pydantic.dev/latest/concepts/models/)
