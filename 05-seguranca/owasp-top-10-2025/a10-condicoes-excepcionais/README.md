# A10:2025 Mishandling of Exceptional Conditions

| | |
|---|---|
| **Categoria** | [A10:2025 Mishandling of Exceptional Conditions](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/), nova em 2025 |
| **CWE típico** | [CWE-209](https://cwe.mitre.org/data/definitions/209.html) (mensagem de erro com informação sensível), [CWE-636](https://cwe.mitre.org/data/definitions/636.html) (não falhar com segurança) |
| **Resolve** | Erros que vazam detalhes, liberam acesso ou deixam o estado pela metade |
| **Em uma frase** | Quando algo quebra: negue, responda genérico, registre o detalhe e desfaça tudo |

## O problema

[`vulneravel.py`](vulneravel.py) reúne os três erros clássicos:

| Função | Defeito |
|---|---|
| `responder_erro` | Devolve `str(erro)` ao cliente: nomes de host, SQL e caminhos internos (CWE-209) |
| `esta_autorizado` | `except Exception: return True`. Se o serviço de políticas cai, **todo mundo** passa: *fail open* (CWE-636) |
| `transferir` | Debita, faz `commit`, só então descobre que a conta de destino não existe: o dinheiro some |

## A solução

[`seguro.py`](seguro.py):

| Função | Controle |
|---|---|
| `responder_erro` | Cliente recebe `{"detail": "internal error", "error_id": ...}`. O traceback vai para o log com o **mesmo** `error_id`, que é o que o suporte pede ao usuário |
| `esta_autorizado` | Qualquer exceção resulta em **negado** (fail closed) e é registrada. Só `True` autoriza |
| `transferir` | `with conexao:` envolve débito e crédito em uma transação; se o crédito falha, há rollback completo |

Os testes verificam: mensagem interna ausente da resposta e presente no log com o mesmo
`error_id`; acesso negado quando a checagem quebra; saldo da origem intacto após a falha.

## Como aplicar em FastAPI

O A10 recomenda tratar a exceção onde ela ocorre, ter um **handler global** como rede de segurança
e fazer rollback completo de transações. Esqueleto (FastAPI não é dependência deste repositório;
snippet ilustrativo, não executado aqui):

```python
@app.exception_handler(Exception)
async def unhandled(request: Request, exc: Exception) -> JSONResponse:
    error_id = uuid.uuid4().hex
    log.exception("unhandled error", extra={"error_id": error_id, "path": request.url.path})
    return JSONResponse({"detail": "internal error", "error_id": error_id}, status_code=500)
```

## Além do exemplo

- **Limites em tudo**: o OWASP resume como "nada em TI deve ser ilimitado" (timeouts, tamanho de
  corpo, paginação, rate limiting, quotas), porque recurso sem teto vira negação de serviço.
- Referência nula e outros estados inesperados (CWE-476, citado pela categoria) também contam: valide na borda.
- Alerta: erro 500 em volume anormal é sinal para [A09](../a09-logging-e-alertas/README.md).

## Referências

- [OWASP A10:2025](https://owasp.org/Top10/2025/A10_2025-Mishandling_of_Exceptional_Conditions/)
- [OWASP Error Handling Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Error_Handling_Cheat_Sheet.html)
