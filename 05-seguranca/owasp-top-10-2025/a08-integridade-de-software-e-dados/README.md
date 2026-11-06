# A08:2025 Software or Data Integrity Failures (webhooks)

| | |
|---|---|
| **Categoria** | [A08:2025 Software or Data Integrity Failures](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/) |
| **Resolve** | Aceitar dado ou código sem provar que veio de quem diz e que não foi alterado ou repetido |
| **Em uma frase** | Assine o corpo bruto, compare em tempo constante e recuse mensagens fora da janela de tempo |

## O problema

[`vulneravel.py`](vulneravel.py) tem dois defeitos num único `if`:

1. `assinar(...) != assinatura` compara strings com `!=`, que pode terminar mais cedo no primeiro
   byte diferente (ataque de timing).
2. A assinatura cobre só o corpo. Uma mensagem legítima capturada uma vez (log de proxy, rede
   comprometida) é aceita **para sempre**: o teste a reenvia e ela passa duas vezes (*replay*).

## A solução

[`seguro.py`](seguro.py):

| Controle | Por quê |
|---|---|
| HMAC-SHA256 sobre `timestamp + "." + corpo` | O timestamp passa a fazer parte do que é assinado; trocá-lo invalida a assinatura |
| Corpo em **bytes brutos**, antes de `json.loads` | Reserializar o JSON muda espaços e ordem de chaves e quebra a assinatura; parsear antes é processar dado não verificado |
| `hmac.compare_digest` sobre bytes | Tempo constante. Com `str` não ASCII ele levanta `TypeError`, então os dois lados são codificados antes |
| Janela de 300 s | Replay antigo é recusado |
| Timestamp só com dígitos ASCII | `isdigit()` aceita dígitos de outros alfabetos; `isascii()` fecha essa porta |

O teste cobre mensagem válida, replay fora da janela, corpo adulterado, timestamp trocado com a
mesma assinatura, timestamps malformados e assinatura não ASCII. O segredo nasce em tempo de
execução (`secrets.token_bytes`).

## O que falta em produção

- **Idempotência**: dentro da janela, o mesmo evento ainda pode chegar duas vezes. Guarde o ID do
  evento (com TTL) e ignore repetidos.
- **Esquema do provedor**: cabeçalhos e o que entra no HMAC variam (Asaas, Stripe etc.). Siga a
  documentação do provedor; este exemplo ilustra o padrão, não um provedor específico.
- **Rotação** do segredo do webhook, sem derrubar a integração (aceite dois segredos por um período).

## Outros casos da categoria

- **Desserialização**: nunca `pickle.loads` nem `yaml.load` (sem `SafeLoader`) em dado não confiável.
- **Pipeline**: dependências sem lockfile/hash, actions por tag móvel e artefatos sem assinatura
  são falhas de integridade; ver [`supply-chain/`](../../supply-chain/README.md).
- **Atualizações**: só instale/execute artefatos com assinatura ou proveniência verificada.

## Referências

- [OWASP A08:2025](https://owasp.org/Top10/2025/A08_2025-Software_or_Data_Integrity_Failures/)
- [Python `hmac.compare_digest`](https://docs.python.org/3/library/hmac.html)
