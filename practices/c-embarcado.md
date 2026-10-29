# Domínio: C em alvo embarcado

Cobre como se escreve código C para microcontrolador: tipos e conversões, uso de memória, estrutura dos arquivos, nomes e contratos, comentários, defensividade e compilação condicional. Não cobre toolchain, build, análise estática nem MISRA — estão em [c-build-e-analise.md](c-build-e-analise.md) —, nem a arquitetura do firmware (camadas, interrupções, RTOS, tempo), que está em [firmware.md](firmware.md).

**Aplica-se a:** projetos com código C para microcontrolador.
**Leia quando:** for escrever ou revisar código C.

## 1. Tipos, expressões e conversões

1. **Tipos de largura explícita** (`uint8_t`, `int32_t`) em toda variável cuja largura importe: registradores, protocolos, buffers, campos persistidos. `int` e `char` só onde a largura é irrelevante.
2. **`bool` para condição lógica** (`<stdbool.h>`), não `int` nem `uint8_t` com 0/1.
3. **Não misture sinalizado e não sinalizado na mesma expressão.** A conversão implícita é silenciosa e é das fontes mais comuns de defeito em C embarcado. Onde a conversão for necessária, ela é explícita.
4. **Conversão que perde faixa ou precisão é explícita** e acompanhada da verificação que garante que o valor cabe.
5. **Ponto flutuante nunca é comparado por igualdade**, e não entra em caminho crítico de tempo sem justificativa — muitos alvos não têm FPU.
6. **`const` é o padrão**: parâmetro de ponteiro que não modifica é `const`; tabela imutável é `const` (fica em flash, não em RAM).
7. **Enum para conjunto fechado de valores**, com todos os casos tratados no `switch`. Onde houver `default`, ele leva ao tratamento de erro, nunca ao silêncio — é o que impede que um caso novo esquecido passe despercebido.
8. **Parênteses explícitos quando a expressão mistura famílias de operadores** — bit a bit, deslocamento, lógicos, relacionais, ternário. A precedência entre elas é contraintuitiva em C (`x & MASCARA == 0` compara antes de mascarar). Em aritmética simples (`a + b * c`), parêntese a mais é ruído.
9. **Tamanho usa `size_t`; endereço como inteiro usa `uintptr_t`.** A largura de ambos varia entre plataformas, e são os tipos que o padrão garante caberem no alvo.

## 2. Memória e recursos

1. **Sem alocação de heap em tempo de execução** (`malloc`/`free` ou equivalentes). Fragmentação e falha de alocação não aparecem em teste e aparecem em campo, meses depois. Onde memória variável for necessária: alocação única na inicialização, ou pool de blocos de tamanho fixo com capacidade declarada e esgotamento tratado — em ambos os casos registrado em ADR.
2. **Sem recursão e sem arranjo de tamanho variável (VLA)**: ambos tornam o consumo de pilha indeterminável.
3. **Todo buffer tem tamanho conhecido em compilação**, e todo acesso indexado com índice vindo de fora do módulo tem limite verificado.
4. **Consumo de pilha é orçado, não descoberto**: a pilha de cada tarefa ou contexto é dimensionada, e o projeto documenta como isso foi verificado (marca d'água, análise da toolchain) ou registra a verificação como pendente.
5. **Escopo mínimo.** Variável usada por um só arquivo é `static`; variável global compartilhada tem dono declarado — um módulo que a escreve —, e os demais leem por função de acesso.
6. **Estrutura de protocolo ou persistência não depende de layout implícito**: alinhamento, preenchimento e ordem de bytes são tratados na serialização, nunca assumidos do compilador.

## 3. Estrutura, nomes e interface

1. **Um módulo = um `.c` + um `.h`**, com a responsabilidade declarada no topo do header. Módulo com estado, que tem ou pode vir a ter mais de uma instância, parte de `../templates/modulo-c.md`.
2. **Todo símbolo público leva o prefixo do módulo** (`motor_ligar`, `MOTOR_ESTADO_PARADO`; ou `Motor_ligar` na forma de `templates/modulo-c.md`). C não tem espaço de nomes: o prefixo evita colisão no link e torna a origem visível na revisão e na busca textual. A convenção de caixa e o idioma dos identificadores são decisão do projeto, declarada no `AGENTS.md`.
3. **A unidade faz parte do nome** sempre que a grandeza tiver uma: `timeout_ms`, `corrente_ma`, `tensao_mv`. Elimina uma classe de defeito que nenhum analisador detecta, a custo zero.
4. **Identificador reservado não se usa.** Nome começando com dois sublinhados, ou sublinhado e maiúscula, é reservado à implementação — inclusive em guarda de inclusão: `__MODULO_H__` é comportamento indefinido; o correto é `MODULO_H`.
5. **O header expõe interface, nunca implementação**: sem definição de variável, sem corpo de função não `inline`, sem `#include` que só a implementação usa. Guarda de inclusão em todo header.
6. **Cada função pública tem contrato no header**, com os itens que se aplicam a ela e que a assinatura não deixa óbvios: o que faz, pré-condições, faixa e unidade de cada parâmetro, aceitação ou não de ponteiro nulo, posse e tempo de vida de ponteiro recebido ou retornado, contexto de execução permitido (tarefa, laço principal, interrupção) e o significado de cada retorno de erro. É o que torna a regra de validação verificável na revisão — e é o material que uma norma de safety vai exigir depois. Item que não se aplica é omitido, não preenchido com "—".
7. **Sem número mágico.** Valor com significado é `const`, `enum` ou máscara nomeada; registrador é acessado por campos e máscaras com nome.
8. **Função tem uma responsabilidade.** Função que precisa de comentário de seção interna costuma ser duas. O limite objetivo é o de complexidade, medido por sensor ([c-build-e-analise.md](c-build-e-analise.md), Seção *Sensores da linguagem*) — contar linhas pune tabela e `switch` de máquina de estado, que são longos e simples.
9. **Toda função tem protótipo**; lista de parâmetros vazia é `(void)`.
10. **Macro só onde função não serve.** Constante é `const` ou `enum`; cálculo é função (`static inline` quando o custo importar). Macro restante tem parênteses em cada uso do argumento e não tem efeito colateral no argumento.
11. **Sem `goto`**, exceto o salto para um bloco único de limpeza no fim da própria função.
12. **Código morto não fica no repositório** — nem comentado, nem sob `#if 0`. O histórico do VCS guarda a alternativa antiga.
13. **O `.c` inclui o próprio header primeiro**: é o que prova que o header é autossuficiente. A ordem dos demais é estilo do projeto. Um header inclui diretamente tudo de que depende, e caminho de include parte das raízes declaradas no build, sem `../`.
14. **Header incluível por C++** (teste em host costuma ser C++): `extern "C"` sob `#ifdef __cplusplus` no próprio header, em vez de exigir a adaptação de quem inclui; e nenhum identificador que seja palavra reservada de C++ (`this`, `new`, `class`).

## 4. Comentários

Comentário é texto que nenhum sensor verifica: envelhece sem aviso e, quando fica falso, engana mais do que a ausência dele. Por isso entra só onde diz o que o código não consegue dizer.

1. **Comente o porquê, nunca o quê.** Decisão não óbvia, restrição de hardware ou de norma, contorno de errata ou de defeito de fornecedor e risco aceito ficam comentados no local, com o motivo. O que o código faz, ele mesmo mostra; repetir isso em texto dobra a manutenção e diverge na primeira alteração.
2. **Nome claro e função pequena antes de comentário.** Trecho que precisa de explicação para ser entendido pede um nome melhor ou uma função extraída com o nome do que faz (Seção *Estrutura, nomes e interface*). Comentário que compensa nome ruim é o primeiro a ficar falso.
3. **Curto: uma linha, no máximo duas ou três.** Explicação que não cabe nisso vai para design-doc, ADR ou referência, e o comentário aponta para ela.
4. **Comentário descreve o código, não a mudança.** "Adicionado", "corrigido", "agora faz X", "antes era Y" são histórico e moram na mensagem de commit e no resumo da mudança. Código desativado não fica comentado (Seção *Estrutura, nomes e interface*, regra do código morto).
5. **Comentário de documentação (Doxygen) só em interface pública, e resumido**: o contrato da Seção *Estrutura, nomes e interface*, limitado ao que a assinatura não diz — sem repetir nome, tipos ou parâmetros que se explicam sozinhos. Função `static` não leva bloco de documentação; se precisar de algo, é a linha do porquê.
6. **Comentário fora do escopo da tarefa não se altera**: nem remoção, nem reescrita, nem reformatação. A exceção é o comentário que a própria mudança tornou falso, corrigido ou removido na mesma alteração.
7. **`TODO` só com motivo concreto, em uma linha**: o que falta e o que impede de fazer agora, ou a referência da pendência (issue, spec). `TODO` genérico ("melhorar", "revisar") não entra.
8. **Idioma e forma seguem o projeto**: o idioma declarado no `AGENTS.md` e, na falta dele, o que o arquivo já usa; o mesmo vale para o estilo (`//` ou `/* */`, marcadores Doxygen).

## 5. Defensividade e comportamento indefinido

1. **Função pública valida o que vem de fora do módulo**: ponteiro nulo, índice fora de faixa, enum inválido, tamanho incoerente.
2. **Retorno de erro é verificado, ou descartado explicitamente** com `(void)` e o motivo. Função que pode falhar retorna estado de erro; não sinaliza falha por valor mágico dentro da faixa útil nem mistura status, quantidade e código de erro no mesmo retorno. A causa da falha é propagada ou convertida explicitamente para quem chama, nunca perdida.
3. **Erro tem um tipo próprio** (enum de resultado) usado pelo projeto inteiro, em vez de cada módulo inventar sua convenção.
4. **Suposição sobre o alvo vira verificação de compilação**: tamanho de estrutura persistida ou trafegada, largura de tipo, potência de dois de buffer circular, coerência entre enum e tamanho de tabela — tudo por `_Static_assert` (ou macro equivalente em C99). Falha de compilação custa segundos; a mesma suposição quebrada em campo custa uma visita.
5. **`assert` de execução é para invariante de programação**, verificada em desenvolvimento; nunca para validar entrada externa, que é tratada sempre, também em produção.
6. **Comportamento indefinido nunca é recurso**: deslocamento maior ou igual à largura do tipo, estouro de sinalizado, variável não inicializada, ponteiro para objeto fora de escopo, violação de aliasing. O compilador otimiza em cima disso, e o sintoma aparece longe da causa.
7. **`volatile` marca o que muda fora do fluxo do programa** — registrador, variável escrita por interrupção. `volatile` não sincroniza: acesso compartilhado precisa de seção crítica ou primitiva do RTOS ([firmware-concorrencia.md](firmware-concorrencia.md), Seção *Interrupções*).

## 6. Compilação condicional

1. **Opção de compilação vale `0` ou `1`** e é testada com `#if (OPCAO == 1)` — `#ifdef` não distingue "desligada" de "esquecida". Com `-Wundef` o compilador acusa a opção não definida.
2. **Macros de seleção de variante ou produto são mutuamente exclusivas**; combinação inválida é rejeitada por asserção estática ou pelo script de build.
3. **O `#if` fica perto do código que condiciona.** Condicional distante obriga quem revisa a procurar o efeito em outro lugar.
4. **Alteração num trecho condicional revisa os dois ramos**, em cada variante afetada — e, onde houver CI, compila todas as variantes. O ramo que o build atual não usa quebra em silêncio.

## Checklist deste domínio

- [ ] Tipos de largura explícita onde a largura importa; nenhuma conversão implícita entre sinalizado e não sinalizado.
- [ ] Nenhuma alocação dinâmica, recursão ou VLA introduzida.
- [ ] Símbolos públicos com prefixo do módulo, grandezas com unidade no nome, nenhum número mágico.
- [ ] Função pública nova ou alterada tem contrato no header, valida entrada externa e tem retorno de erro verificado.
- [ ] Nenhum identificador reservado, código morto ou `#if 0` entrou no diff.
- [ ] Comentário novo explica um porquê em até três linhas, não narra a mudança, e nenhum comentário fora do escopo foi alterado.
- [ ] Suposição sobre o alvo foi afirmada por asserção estática.
- [ ] Toda condicional de compilação alterada teve os dois ramos revisados.
