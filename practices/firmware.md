# Domínio: estrutura de firmware embarcado

Cobre as decisões estruturais de um firmware: separação de camadas, escolha entre laço principal e RTOS, e máquinas de estado. O comportamento no tempo — interrupções, sincronização, base de tempo — está em [firmware-concorrencia.md](firmware-concorrencia.md); estado seguro, dados externos e persistência, em [firmware-robustez.md](firmware-robustez.md); a escrita do código C, em [c-embarcado.md](c-embarcado.md).

**Aplica-se a:** firmware embarcado, em qualquer linguagem.
**Leia quando:** for definir ou alterar a estrutura de um firmware, decidir entre laço principal e RTOS, ou introduzir ou alterar máquina de estado.

## 1. Camadas e portabilidade

1. **Camadas com dependência em um sentido só, e no mínimo uma fronteira: hardware ↔ aplicação.** A aplicação (regras do produto) nunca acessa registrador nem HAL do fabricante diretamente. Uma camada intermediária de serviços (drivers do produto, comunicação, persistência) aparece quando há o que colocar nela — criá-la vazia é camada sem responsabilidade.
2. **A camada de aplicação compila no PC.** Esse é o critério prático da separação: se a lógica do produto não compila sem a toolchain do alvo, as camadas estão misturadas. É também o que habilita teste em host, o sensor de maior retorno do projeto ([testes.md](testes.md), Seção *A costura*).
3. **O acesso a hardware é concentrado por periférico**, atrás de uma interface pequena e declarada. Trocar de microcontrolador deve afetar a camada de hardware, não a aplicação.
4. **Código gerado por ferramenta de fabricante fica isolado** e não é editado à mão; a customização vive nos pontos de extensão previstos ou numa camada acima. Regeneração que apaga edição manual é defeito de estrutura, não acidente.
5. **O mapa das camadas e dos módulos mora no `ARCHITECTURE.md`** do projeto, não neste guia.

## 2. Laço principal ou RTOS

1. **A escolha entre laço principal e RTOS é registrada em ADR**, com o motivo. RTOS não é o padrão nem o avanço natural: ele acrescenta concorrência real, e com ela classes de defeito que o laço principal não tem.
2. **O laço principal nunca bloqueia.** Cada módulo tem uma função de passo, não bloqueante, chamada a cada iteração; espera é sempre uma máquina de estado com temporizador.
3. **Cada tarefa do RTOS tem uma responsabilidade declarada**, com prioridade e tamanho de pilha justificados e documentados. Tarefa criada "para organizar" sem responsabilidade própria vira acoplamento.
4. **Alocação estática das primitivas** (tarefas, filas, semáforos, mutexes) na inicialização, e a criação é verificada — retorno de API do RTOS nunca é ignorado.
5. **A configuração do RTOS faz parte do projeto**: verificações de estouro de pilha e ganchos de erro ligados em desenvolvimento, e o comportamento em produção é decisão registrada.

O que acontece entre tarefas em execução — filas, exclusão, esperas com tempo limite — está em [firmware-concorrencia.md](firmware-concorrencia.md), Seção *Sincronização entre contextos*.

## 3. Máquinas de estado

1. **Comportamento com modos usa máquina de estado explícita.** O sintoma de que ela é necessária: conjunto de flags booleanas consultadas em combinação, ou condição que só é verdadeira "quando já passou por outra coisa antes".
2. **Uma máquina, um dono.** Os estados de uma máquina são alterados por um único módulo. Outro módulo não escreve o estado: envia evento.
3. **Estados e eventos são enums nomeados**, nunca inteiros soltos, e a máquina inteira é observável por uma única variável de estado — não por três flags que combinam.
4. **A transição é a única forma de mudar de estado**, concentrada numa função ou numa tabela de transição. Estado atribuído em pontos espalhados pelo código anula a máquina.
5. **A tabela de transição, quando houver, é `const`** e fica em flash ([c-embarcado.md](c-embarcado.md), Seção *Tipos, expressões e conversões*).
6. **Todo par estado × evento tem destino definido**, inclusive os que não fazem nada — "não faz nada" é decisão, não lacuna. Uma regra padrão declarada explicitamente ("evento não listado neste estado: ignorado e contado") cobre os pares restantes; o que não vale é o par simplesmente não ter sido pensado.
7. **A máquina tem estado de erro ou seguro alcançável**, e a saída dele é explícita (reinicialização, intervenção, reset). Máquina sem estado de falha esconde a falha.
8. **Ação de entrada e de saída são explícitas** quando existirem, e a máquina não bloqueia: espera é um estado com temporizador, nunca um laço de espera dentro da transição.
9. **Toda máquina de estado não trivial é documentada** a partir de `../templates/fsm.md`, em `docs/design-docs/` (os critérios de "não trivial" estão no template). A documentação e o código mudam na mesma alteração.

Máquina de estado é o que melhor se paga em teste de host: a tabela de transição é lógica pura, e o par estado × evento esquecido aparece no teste antes de aparecer em campo ([testes.md](testes.md), Seção *O que testar primeiro*).

## Checklist deste domínio

- [ ] A lógica de aplicação continua compilável sem a toolchain do alvo.
- [ ] Nenhum acesso a registrador ou HAL do fabricante entrou na camada de aplicação.
- [ ] Tarefa nova de RTOS tem responsabilidade, prioridade e pilha justificadas, e primitivas alocadas estaticamente com retorno verificado.
- [ ] Comportamento com modos está numa máquina de estado explícita, com dono único e estado de falha alcançável.
- [ ] Todo par estado × evento tem destino definido, por transição ou por regra padrão declarada.
- [ ] Máquina de estado nova ou alterada está documentada a partir de `../templates/fsm.md`.
