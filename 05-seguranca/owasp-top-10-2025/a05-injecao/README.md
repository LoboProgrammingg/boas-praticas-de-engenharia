# A05:2025 Injection (SQL e XSS)

| | |
|---|---|
| **Categoria** | [A05:2025 Injection](https://owasp.org/Top10/2025/A05_2025-Injection/) |
| **CWE típico** | [CWE-89](https://cwe.mitre.org/data/definitions/89.html) (SQL), [CWE-79](https://cwe.mitre.org/data/definitions/79.html) (XSS) |
| **Resolve** | Entrada do usuário interpretada como código por um interpretador (SQL, HTML, shell) |
| **Em uma frase** | Mantenha dado e código separados: parâmetros para SQL, escape de saída para HTML |

## O problema

[`vulneravel.py`](vulneravel.py) monta SQL com f-string e HTML por concatenação. O teste usa a
entrada inofensiva `' OR '1'='1` contra uma tabela SQLite **em memória**: a condição vira
sempre verdadeira e a busca por um nome devolve todos os usuários. No HTML, um `<script>` digitado
pelo usuário chega intacto ao documento.

## A solução

[`seguro.py`](seguro.py):

- **SQL**: `execute("... WHERE nome = ?", (nome,))`. O texto viaja como parâmetro; o driver nunca o
  interpreta como SQL. O teste inclui uma propriedade (Hypothesis): para qualquer texto de entrada,
  nenhuma linha devolvida tem nome diferente do informado.
- **HTML**: `html.escape(texto, quote=True)` transforma `<`, `>`, `&` e aspas em entidades.

## Variações que o exemplo não cobre

| Caso | Controle |
|---|---|
| Identificador dinâmico (`ORDER BY coluna`) não pode ser parâmetro | Allowlist em código; nunca o input direto |
| ORM com `text()`/`raw()` | Mesmo cuidado: bind parameters (`:email`), nunca f-string |
| Comando do SO | `subprocess.run([...], shell=False)` com lista de argumentos (ASVS `v5.0.0-1.2.5`) |
| HTML em React | O JSX escapa por padrão; evite `dangerouslySetInnerHTML` e valide o esquema de `href` (`https:`/`http:`) |
| HTML inevitável | Sanitizador mantido (verifique no lockfile) + Content-Security-Policy |

## Quando não basta

`html.escape` cobre o **corpo** do HTML e atributos entre aspas. Dentro de `<script>`, de
`style` ou de URLs o contexto muda e a codificação também; por isso o caminho robusto é um
template engine com autoescape por contexto e uma CSP. XSS ainda derrota qualquer proteção de CSRF
([CSRF Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)).

## Referências

- [OWASP A05:2025](https://owasp.org/Top10/2025/A05_2025-Injection/)
- [SQL Injection Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html)
- [XSS Prevention Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html)
- [Python `sqlite3`: placeholders](https://docs.python.org/3/library/sqlite3.html) e [`html.escape`](https://docs.python.org/3/library/html.html)
