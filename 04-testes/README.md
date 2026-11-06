# 04. Testes

Um teste vale pela confiança que dá, relativa ao que custa para escrever, rodar e manter.
Esta seção reúne as práticas que mais aumentam essa razão: escolher bem os níveis de teste,
escrever testes legíveis, usar dublês com critério e medir se a suíte realmente protege o
código.

| Tópico | O que ensina | Exemplo executável |
|---|---|---|
| [Pirâmide e troféu](piramide-e-trofeu/README.md) | Como distribuir testes entre unidade, integração e ponta a ponta; cobertura não é qualidade | só README |
| [TDD](tdd/README.md) | O ciclo red, green, refactor e o que ele revela | `ruim.py`, `bom.py`, teste |
| [AAA e Given-When-Then](aaa-given-when-then/README.md) | Estrutura e nomes de testes legíveis | [`test_aaa_given_when_then.py`](aaa-given-when-then/test_aaa_given_when_then.py) |
| [Dublês de teste](dubles-de-teste/README.md) | A taxonomia de Meszaros; prefira fakes a mocks de interação | `ruim.py`, `bom.py`, teste |
| [Property-based testing](property-based/README.md) | Propriedades que valem para toda entrada, com Hypothesis | `ruim.py`, `bom.py`, teste |
| [Mutation testing](mutation/README.md) | Estragar o código de propósito para medir a suíte | `ruim.py`, `bom.py`, teste |
| [Testes de contrato](testes-de-contrato/README.md) | Garantir que o dublê e o serviço real concordam | `ruim.py`, `bom.py`, teste |

## Uma nota sobre cobertura

Um piso de cobertura (por exemplo, 70%) é uma **política do projeto**, útil como alarme,
e não uma lei da engenharia. Kent C. Dodds, ao discutir o tema, diz sobre o próprio 70% que
"I made that number up... no science there". Cobertura mede quais linhas rodaram, não se
alguém verificou o resultado; por isso a seção inclui [mutation testing](mutation/README.md)
e [property-based testing](property-based/README.md) como complementos.

## Convenção

Os exemplos seguem o padrão do repositório: `ruim.py`, `bom.py` e `test_<tópico>.py`, em que o
teste demonstra o defeito da versão ruim e prova a boa. Os testes são rápidos e
determinísticos: sem rede, sem `sleep` real, com relógios e geradores falsos. Rode com
`uv run pytest 04-testes`.
