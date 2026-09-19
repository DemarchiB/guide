# Domínio: concorrência e tempo em firmware

Cobre o que acontece enquanto o firmware roda: interrupções e DMA, sincronização entre contextos de execução, e a base de tempo. A estrutura do firmware está em [firmware.md](firmware.md); estado seguro e dados externos, em [firmware-robustez.md](firmware-robustez.md).

**Aplica-se a:** firmware embarcado, em qualquer linguagem.
**Leia quando:** for escrever ou revisar código que roda em interrupção ou em tarefa de RTOS, mexer em DMA, dado compartilhado, seção crítica, espera ou medida de tempo.

## 1. Interrupções

1. **A rotina de interrupção é curta e não bloqueia.** Ela lê ou escreve o periférico, guarda o mínimo e devolve o controle; o processamento acontece fora dela.
2. **Nada de bloqueio, alocação, E/S formatada ou espera dentro da interrupção** — nem `printf`, nem `malloc`, nem laço de espera por outro periférico.
3. **Dado compartilhado entre interrupção e contexto principal é `volatile`**, e o acesso a dado maior que uma palavra do processador acontece dentro de seção crítica ou por primitiva do RTOS. `volatile` sozinho não garante atomicidade ([c-embarcado.md](c-embarcado.md), Seção *Defensividade e comportamento indefinido*).
4. **Seção crítica é a menor possível**, com o tempo máximo dentro dela conhecido — ela é o teto da latência de todas as outras interrupções.
5. **Comunicação com o contexto principal por mecanismo declarado**: sinalizador, fila circular de produtor/consumidor único, ou primitiva do RTOS específica para interrupção. Estrutura genérica compartilhada sem proteção é defeito.
6. **Prioridades de interrupção são atribuídas explicitamente e documentadas**, com o efeito de aninhamento considerado. Prioridade herdada do default da ferramenta não é escolha.
7. **Toda condição de erro do periférico é tratada** — estouro, ruído, quadro inválido —, não apenas o caminho feliz.
8. **O tempo de execução de toda rotina de interrupção é conhecido e compatível com o período do que ela atende** — não só o tempo da seção crítica dentro dela, mas o da rotina inteira, do início ao retorno.
9. **Instrução de sincronização do núcleo (barreira de dados ou de instrução) e atributo que impede otimização só entram com justificativa no local**: que efeito de pipeline, cache ou reordenação pelo compilador eles evitam ali, com referência à documentação do núcleo ou do fabricante. Colocados "por precaução" escondem uma suposição não verificada — e a próxima pessoa não sabe se pode removê-los.
10. **Buffer usado por DMA, em alvo com cache de dados, exige alinhamento, seção de memória dedicada e manutenção explícita de cache antes e depois da transferência.** `volatile` não garante coerência de cache: ele marca o que muda fora do fluxo do programa, não sincroniza.

## 2. Sincronização entre contextos

1. **Comunicação entre tarefas por fila ou primitiva**, não por variável global compartilhada. Onde a variável for inevitável, ela tem dono único e proteção declarada.
2. **Mutex para exclusão, semáforo para sinalização** — não o contrário. Inversão de prioridade é considerada e o mecanismo do RTOS que a trata é ativado onde couber.
3. **Toda espera tem tempo limite.** Espera indefinida por fila, semáforo ou evento só existe onde a ausência do evento for, por projeto, impossível — e isso é comentado no local.
4. **Atraso não é sincronização.** `delay` no lugar de espera por evento esconde condição de corrida que aparece em campo, sob outra carga.

## 3. Base de tempo

1. **Uma base de tempo monotônica** para o firmware inteiro, com resolução e origem declaradas. Cada módulo medir tempo do seu jeito produz comportamento incoerente.
2. **Comparação de tempo tolerante a estouro do contador**: sempre por diferença (`agora - marca >= intervalo`), nunca por comparação direta de instantes.
3. **A leitura do tempo é substituível**, para que a lógica que depende dela seja testável em host sem esperar ([testes.md](testes.md), Seção *A costura*).
4. **Espera ocupada só onde for a única opção** (atraso de microssegundos exigido por periférico), delimitada e comentada.
5. **Prazo é requisito, não expectativa.** Onde o produto tiver requisito temporal, ele entra em `docs/specs/` com valor numérico e tolerância, e a forma de verificá-lo é declarada — medição, pino de depuração, contador.

## Checklist deste domínio

- [ ] Rotinas de interrupção são curtas, não bloqueiam e tratam as condições de erro do periférico.
- [ ] Todo dado compartilhado tem proteção declarada; nenhuma seção crítica cresceu sem que o tempo dentro dela fosse considerado.
- [ ] Barreira de memória e buffer de DMA têm justificativa no local e manutenção de cache onde se aplica.
- [ ] Toda espera tem tempo limite; nenhum atraso foi usado como sincronização.
- [ ] Comparação de tempo é por diferença, tolerante a estouro do contador.
