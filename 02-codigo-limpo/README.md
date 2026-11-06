# 02. Código limpo

*Clean Code* (Robert C. Martin, 2008) é o livro mais influente do tema e também um dos
mais contestados. A posição deste guia é tratá-lo como **núcleo recomendado, com
ressalvas**: adote o que resiste às críticas e trate números e dogmas como heurísticas.

## Índice

| Tópico | Em uma frase | Exemplo |
|---|---|---|
| [Nomes](nomes/README.md) | O nome revela intenção, unidade e efeito | [`nomes/`](nomes/) |
| [Funções](funcoes/README.md) | Um nível de abstração, sem argumentos que escondem a intenção | [`funcoes/`](funcoes/) |
| [Comentários](comentarios/README.md) | Comente o porquê; o quê é papel do nome | [`comentarios/`](comentarios/) |
| [Tratamento de erros](tratamento-de-erros/README.md) | Exceções tipadas e com contexto, nunca erro engolido | [`tratamento-de-erros/`](tratamento-de-erros/) |

Os princípios de [01. Design](../01-principios-de-design/README.md) sustentam estes
tópicos: [CQS](../01-principios-de-design/cqs/README.md) em funções,
[fail fast](../01-principios-de-design/fail-fast/README.md) em erros.

## O que adotar sem medo

Mesmo os críticos mais duros reconhecem como sólido o conselho do capítulo sobre
funções: não misturar níveis de abstração; nomes descritivos, consistentes e com
verbos; funções que fazem uma coisa; sem efeitos colaterais ocultos; preferir retorno a
argumentos de saída; comando ou consulta, não os dois. O autor da crítica de 2020 (qntm)
chama isso de "conselho razoável de nível de entrada".

Também são amplamente aceitos: exceções em vez de códigos de retorno, e nomes que
revelam a intenção.

## O que tratar com ressalva

| Conselho | Ressalva |
|---|---|
| Funções muito pequenas | Ousterhout: "métodos minúsculos" geram interfaces rasas e código emaranhado. Martin admite que o "2 a 4 linhas" veio de um applet Swing e nunca foi absoluto |
| Comentários como falha | Ousterhout: comentários são cruciais para abstração e para o que o código não diz. Martin: são um "mal necessário" e é contra os gratuitos, não contra todos |
| Polimorfismo no lugar de `if/switch`, DRY, funções pequenas | Muratori: em laços quentes o custo é medido (ver abaixo); em código dominado por I/O costuma ser irrelevante |
| Limites numéricos (linhas, argumentos) | Servem de alarme, não de regra. Fowler prefere separar *intenção* de *implementação* |
| TDD como disciplina fixa | Ousterhout prefere escrever algumas classes e depois os testes; Martin defende as três leis e o ciclo red-green-refactor. Tema aberto |

## As críticas, em ordem

### qntm, 2020: "It's probably time to stop recommending Clean Code"

A crítica de fundo é que muito do código de exemplo do livro é de má qualidade e que o
texto é subjetivo: não existem definições empíricas de "código limpo". Ao mesmo tempo,
o autor concorda com boa parte dos conselhos sobre funções (acima) e com o diagnóstico
de que argumentos booleanos opacos são ruins, ainda que discorde do raciocínio de que
"fazem mais de uma coisa".

### Casey Muratori, 2023: "Clean Code, Horrible Performance"

Muratori mede o custo de aplicar regras do livro (polimorfismo no lugar de
`if/switch`, não conhecer detalhes internos dos objetos, funções pequenas, uma coisa por
função) em um laço de cálculo de áreas de formas. Segundo os números dele: trocar
polimorfismo por `switch` rendeu cerca de 1,5x (35 para 24 ciclos por forma); uma
tabela de consulta com a estrutura achatada, cerca de 10x (3,0 a 3,5 ciclos). Com mais
uma propriedade na conta, a tabela chega a quase 15x. O DRY não entrou no benchmark.

**Como ler:** é um microbenchmark de laço quente, o cenário em que isso mais pesa
(jogos, simulação, processamento numérico). Não se generaliza para handlers HTTP ou
código dominado por I/O, onde o gargalo está em outro lugar. Medir o seu caso vence
qualquer regra geral.

### John Ousterhout × Robert C. Martin, 2024–2025

O [debate público](https://github.com/johnousterhout/aposd-vs-clean-code) entre o autor
de *A Philosophy of Software Design* e o de *Clean Code* é a leitura mais equilibrada:

- **Tamanho de método.** Ousterhout critica os métodos minúsculos e os limites
  numéricos; defende módulos **profundos** (muita funcionalidade atrás de uma interface
  simples) e chama de **rasos** os que têm interface quase tão complexa quanto a
  implementação. Martin recomenda funções curtas, mas diz que "2 a 4 linhas" não eram
  absolutas e prefere decompor demais e depois fazer *inline*. Ambos aceitam que
  modularidade importa e que decompor demais é possível.
- **Comentários.** Ousterhout quer mais; Martin os chama de mal necessário e se
  diz contra os gratuitos. Concordam que APIs públicas pedem comentário de interface.
- **TDD.** Ousterhout reconhece ter descrito o TDD de forma inexata e mantém a
  preferência por escrever algumas classes antes dos testes.

Nota de leitura: as posições acima vêm do diálogo publicado; os livros em si não
foram fonte direta deste guia.

## Como usar estes tópicos

1. Comece pelos exemplos: cada tópico prova com teste o problema concreto da versão
   ruim, e não só o gosto.
2. Trate o conselho como pergunta, não como veredito: "isso reduz o custo de mudar este
   código?".
3. Deixe a **formatação** para uma ferramenta (formatador e linter do projeto); discutir
   estilo em revisão de código é desperdício quando uma ferramenta decide por todos.

## Referências

- Robert C. Martin, *Clean Code: A Handbook of Agile Software Craftsmanship*, Prentice Hall, 2008.
- qntm, [*It's probably time to stop recommending Clean Code*](https://qntm.org/clean), 2020.
- Casey Muratori, [*"Clean" Code, Horrible Performance*](https://www.computerenhance.com/p/clean-code-horrible-performance), 2023.
- John Ousterhout e Robert C. Martin, [*A Philosophy of Software Design* vs *Clean Code*](https://github.com/johnousterhout/aposd-vs-clean-code), 2024–2025.
- John Ousterhout, [*A Philosophy of Software Design*](https://web.stanford.edu/~ouster/cgi-bin/book.php), livro e página do autor.
- Martin Fowler, [*Function Length*](https://martinfowler.com/bliki/FunctionLength.html).
