# Logs estruturados

> "A twelve-factor app never concerns itself with routing or storage of its output stream...
> each running process writes its event stream, unbuffered, to stdout."
> Adam Wiggins, *The Twelve-Factor App*, fator XI

| | |
|---|---|
| **Origem** | Fator XI do 12-Factor (logs como fluxo de eventos); prática consolidada em sistemas de busca e análise de logs |
| **Resolve** | Logs em texto livre que só se consulta com `grep`, que variam a cada ocorrência e que vazam dado pessoal |
| **Em uma frase** | Um evento por linha, em JSON, com nome estável e contexto em campos, sem dados sensíveis |

## O problema

Em [`ruim.py`](ruim.py):

```python
log.error(f"falha no pagamento do cliente {cpf} (pedido {pedido_id}): {motivo}")
```

Três problemas num só comando:

1. **Vaza PII.** O CPF foi parar no log, que costuma ter acesso mais amplo e retenção
   mais longa que o banco de dados. Logs não são lugar de CPF, senha, token nem cartão.
2. **Não dá para consultar.** A mensagem muda a cada ocorrência; "quantos pagamentos
   falharam por *timeout* hoje?" vira uma expressão regular frágil.
3. **Não é máquina-legível.** Um agregador de logs precisa de campos, não de prosa.

## A solução

Em [`bom.py`](bom.py), o formatador usa só a biblioteca padrão (`logging` e `json`) e emite
um objeto JSON por linha:

```python
log.error("payment_failed", extra={"contexto": {"pedido_id": "p1", "motivo": "timeout"}})
```

```json
{"timestamp": "2026-11-06T12:00:00+00:00", "level": "ERROR", "logger": "pagamentos",
 "event": "payment_failed", "pedido_id": "p1", "motivo": "timeout"}
```

Regras que o [`test_logs_estruturados.py`](test_logs_estruturados.py) verifica:

| Regra | Por quê |
|---|---|
| Cada linha é um JSON válido | o agregador indexa por campo |
| `event` é um **nome estável**, e os detalhes vão em campos | dá para contar e alertar por evento |
| O contexto nunca sobrescreve campos reservados (`event`, `level`...) | ninguém forja o evento |
| Chaves sensíveis (`cpf`, `senha`, `token`, `cartao`...) são mascaradas | rede de segurança |
| Exceções vão no campo `exc`, mantendo **uma linha por evento** | o parser não quebra no *stack trace* |
| Timestamp em UTC, ISO 8601 | ordenação e comparação sem ambiguidade |

A máscara é uma **última linha de defesa**, não a política. A regra é *não passar* o dado
sensível ao logger. Se precisar correlacionar, registre um identificador interno (como
`pedido_id` ou `cliente_id`), não o documento.

Escreva em `stdout` e deixe a plataforma (Docker, Kubernetes, Railway) coletar e rotear:
é o que o fator XI do 12-Factor pede.

Para correlacionar os logs de uma requisição entre si e com traces, acrescente o `trace_id`
a cada registro (veja [observabilidade](../observabilidade/README.md)).

## Quando não aplicar

- **Saída para humanos.** Em desenvolvimento local, ou em uma CLI, texto legível pode ser
  melhor; formate em JSON só onde há máquina consumindo (ou troque o formatador por
  ambiente).
- **Não registre tudo.** Log de nível `DEBUG` com payload completo de requisições vaza
  dados e custa armazenamento. Defina níveis e amostragem.
- **Mascarar por nome de chave não pega tudo.** Um CPF dentro de uma mensagem de erro de
  terceiros passa pela máscara; revise o que entra no log, não confie só no filtro.

## Relações

- Fator XI e configuração por ambiente: [12-Factor](../../03-arquitetura/twelve-factor/README.md).
- Logs são um dos três sinais de [observabilidade](../observabilidade/README.md).
- Um *fallback* ativado ([degradação elegante](../degradacao-elegante/README.md)) deve gerar
  um evento de log, para não ficar invisível.

## Referências

- Adam Wiggins, [*The Twelve-Factor App, XI. Logs*](https://12factor.net/logs).
- OWASP, [*Logging Cheat Sheet*](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) (dados que não devem ser registrados).
- Python, [*Logging HOWTO*](https://docs.python.org/3/howto/logging.html) e [*Logging Cookbook*](https://docs.python.org/3/howto/logging-cookbook.html).
