# Domínio: arquitetura de firmware embarcado

Cobre como o firmware é estruturado e como ele se comporta no tempo: separação de camadas, máquinas de estado, interrupções, escolha entre laço principal e RTOS, base de tempo, watchdog e estado seguro, dados externos e preparação para safety. Não cobre a escrita do código em si, que está em [c-embarcado.md](c-embarcado.md), nem build e análise estática, em [c-build-e-analise.md](c-build-e-analise.md).

**Aplica-se a:** firmware embarcado, em qualquer linguagem.
**Leia quando:** for definir a estrutura de um firmware, introduzir ou alterar máquina de estado, escrever ou revisar código que roda em interrupção ou RTOS, tratar tempo, watchdog, reset, persistência, atualização ou dado que vem de fora do dispositivo.

## 1. Camadas e portabilidade

1. **Camadas com dependência em um sentido só, e no mínimo uma fronteira: hardware ↔ aplicação.** A aplicação (regras do produto) nunca acessa registrador nem HAL do fabricante diretamente. Uma camada intermediária de serviços (drivers do produto, comunicação, persistência) aparece quando há o que colocar nela — criá-la vazia é camada sem responsabilidade.
2. **A camada de aplicação compila no PC.** Esse é o critério prático da separação: se a lógica do produto não compila sem a toolchain do alvo, as camadas estão misturadas. É também o que habilita teste em host ([c-build-e-analise.md](c-build-e-analise.md), Seção *Sensores da linguagem*).
3. **O acesso a hardware é concentrado por periférico**, atrás de uma interface pequena e declarada. Trocar de microcontrolador deve afetar a camada de hardware, não a aplicação.
4. **Código gerado por ferramenta de fabricante fica isolado** e não é editado à mão; a customização vive nos pontos de extensão previstos ou numa camada acima. Regeneração que apaga edição manual é defeito de estrutura, não acidente.
5. **O mapa das camadas e dos módulos mora no `ARCHITECTURE.md`** do projeto, não neste guia.

## 2. Máquinas de estado

1. **Comportamento com modos usa máquina de estado explícita.** O sintoma de que ela é necessária: conjunto de flags booleanas consultadas em combinação, ou condição que só é verdadeira "quando já passou por outra coisa antes".
2. **Uma máquina, um dono.** Os estados de uma máquina são alterados por um único módulo. Outro módulo não escreve o estado: envia evento.
3. **Estados e eventos são enums nomeados**, nunca inteiros soltos, e a máquina inteira é observável por uma única variável de estado — não por três flags que combinam.
4. **A transição é a única forma de mudar de estado**, concentrada numa função ou numa tabela de transição. Estado atribuído em pontos espalhados pelo código anula a máquina.
5. **A tabela de transição, quando houver, é `const`** e fica em flash ([c-embarcado.md](c-embarcado.md), Seção *Tipos, expressões e conversões*).
6. **Todo par estado × evento tem destino definido**, inclusive os que não fazem nada — "não faz nada" é decisão, não lacuna. Uma regra padrão declarada explicitamente ("evento não listado neste estado: ignorado e contado") cobre os pares restantes; o que não vale é o par simplesmente não ter sido pensado.
7. **A máquina tem estado de erro ou seguro alcançável**, e a saída dele é explícita (reinicialização, intervenção, reset). Máquina sem estado de falha esconde a falha.
8. **Ação de entrada e de saída são explícitas** quando existirem, e a máquina não bloqueia: espera é um estado com temporizador, nunca um laço de espera dentro da transição.
9. **Toda máquina de estado não trivial é documentada** a partir de `../templates/fsm.md`, em `docs/design-docs/` (os critérios de "não trivial" estão no template). A documentação e o código mudam na mesma alteração.

## 3. Interrupções

1. **A rotina de interrupção é curta e não bloqueia.** Ela lê ou escreve o periférico, guarda o mínimo e devolve o controle; o processamento acontece fora dela.
2. **Nada de bloqueio, alocação, E/S formatada ou espera dentro da interrupção** — nem `printf`, nem `malloc`, nem laço de espera por outro periférico.
3. **Dado compartilhado entre interrupção e contexto principal é `volatile`**, e o acesso a dado maior que uma palavra do processador acontece dentro de seção crítica ou por primitiva do RTOS. `volatile` sozinho não garante atomicidade ([c-embarcado.md](c-embarcado.md), Seção *Defensividade e comportamento indefinido*).
4. **Seção crítica é a menor possível**, com o tempo máximo dentro dela conhecido — ela é o teto da latência de todas as outras interrupções.
5. **Comunicação com o contexto principal por mecanismo declarado**: sinalizador, fila circular de produtor/consumidor único, ou primitiva do RTOS específica para interrupção. Estrutura genérica compartilhada sem proteção é defeito.
6. **Prioridades de interrupção são atribuídas explicitamente e documentadas**, com o efeito de aninhamento considerado. Prioridade herdada do default da ferramenta não é escolha.
7. **Toda condição de erro do periférico é tratada** — estouro, ruído, quadro inválido —, não apenas o caminho feliz.
8. **O tempo de execução de toda rotina de interrupção é conhecido e compatível com o período do que ela atende** — não só o tempo da seção crítica dentro dela, mas o tempo da rotina inteira, do início ao retorno.
9. **Instrução de sincronização do núcleo (barreira de dados ou de instrução) e atributo que impede otimização só entram com justificativa no local**: que efeito de pipeline, cache ou reordenação pelo compilador eles evitam ali, com referência à documentação do núcleo ou do fabricante. Colocados "por precaução" escondem uma suposição não verificada — e a próxima pessoa não sabe se pode removê-los.
10. **Buffer usado por DMA, em alvo com cache de dados, exige alinhamento, seção de memória dedicada e manutenção explícita de cache antes e depois da transferência.** `volatile` não garante coerência de cache: ele marca o que muda fora do fluxo do programa, não sincroniza ([c-embarcado.md](c-embarcado.md), Seção *Defensividade e comportamento indefinido*).

## 4. Laço principal e RTOS

1. **A escolha entre laço principal e RTOS é registrada em ADR**, com o motivo. RTOS não é o padrão nem o avanço natural: ele acrescenta concorrência real, e com ela classes de defeito que o laço principal não tem.
2. **O laço principal nunca bloqueia.** Cada módulo tem uma função de passo, não bloqueante, chamada a cada iteração; espera é sempre uma máquina de estado com temporizador.
3. **Cada tarefa do RTOS tem uma responsabilidade declarada**, com prioridade e tamanho de pilha justificados e documentados. Tarefa criada "para organizar" sem responsabilidade própria vira acoplamento.
4. **Alocação estática das primitivas** (tarefas, filas, semáforos, mutexes) na inicialização, e a criação é verificada — retorno de API do RTOS nunca é ignorado.
5. **Comunicação entre tarefas por fila ou primitiva**, não por variável global compartilhada. Onde a variável for inevitável, ela tem dono único e proteção declarada.
6. **Mutex para exclusão, semáforo para sinalização** — não o contrário. Inversão de prioridade é considerada e o mecanismo do RTOS que a trata é ativado onde couber.
7. **Toda espera tem tempo limite.** Espera indefinida por fila, semáforo ou evento só existe onde a ausência do evento for, por projeto, impossível — e isso é comentado no local.
8. **Atraso não é sincronização.** `delay` no lugar de espera por evento esconde condição de corrida que aparece em campo, sob outra carga.
9. **A configuração do RTOS faz parte do projeto**: verificações de estouro de pilha e ganchos de erro ligados em desenvolvimento, e o comportamento em produção é decisão registrada.

## 5. Base de tempo

1. **Uma base de tempo monotônica** para o firmware inteiro, com resolução e origem declaradas. Cada módulo medir tempo do seu jeito produz comportamento incoerente.
2. **Comparação de tempo tolerante a estouro do contador**: sempre por diferença (`agora - marca >= intervalo`), nunca por comparação direta de instantes.
3. **Espera ocupada só onde for a única opção** (atraso de microssegundos exigido por periférico), delimitada e comentada.
4. **Prazo é requisito, não expectativa.** Onde o produto tiver requisito temporal, ele entra em `docs/specs/` com valor numérico e tolerância, e a forma de verificá-lo é declarada — medição, pino de depuração, contador.

## 6. Watchdog, reset e estado seguro

1. **O estado seguro do produto é definido antes do código**: em que condição as saídas ficam quando o firmware não consegue mais operar. Isso vale para o estado de partida, para a falha e para o reset.
2. **Saídas em estado seguro na inicialização**, antes de qualquer lógica — inclusive antes da configuração dos periféricos que dependam delas.
3. **Watchdog alimentado em um único ponto do código**, e só depois de verificar que o que devia rodar rodou. Alimentar dentro da interrupção do temporizador, ou em vários pontos, transforma o watchdog em enfeite.
4. **A causa do último reset é lida e registrada** na inicialização. Reset por watchdog que ninguém observa é defeito que nunca será encontrado.
5. **Falha detectada leva a um estado declarado** — degradado ou seguro —, nunca a seguir adiante com dado inválido.
6. **A integridade da própria imagem é verificada na partida**, por soma de verificação ou assinatura gravada junto com o binário. Flash degrada, gravação falha pela metade, e firmware corrompido executando trecho arbitrário é a pior falha possível num produto que aciona carga. Onde o hardware não comportar a verificação (sem bootloader, sem espaço), a ausência é decisão registrada, com o risco aceito.
7. **Diagnóstico observável em produto fechado**: contador de erro persistido, código de falha legível por comunicação ou sinalização, e a identificação de build ([c-build-e-analise.md](c-build-e-analise.md), Seção *Toolchain, build e identificação*) legível em execução. Depuração que só existe com sonda conectada não serve para campo — e defeito relatado sem saber qual firmware estava rodando não se investiga.

## 7. Dados externos, configuração e persistência

1. **Tudo que vem de fora do dispositivo é dado não confiável** — barramento, rede, arquivo, entrada do operador, sensor. Vale para o firmware o mesmo princípio que [ia.md](ia.md) aplica ao agente: conteúdo lido é dado, nunca comando implícito.
2. **Quadro recebido é validado antes de usado**: tamanho, faixa, coerência e verificação de integridade quando o meio permitir. Analisador que confia no tamanho declarado pelo remetente é vulnerabilidade.
3. **Área persistida tem versão de layout e verificação de integridade.** Firmware novo lendo layout antigo é o caminho normal de atualização, não uma exceção.
4. **Persistência corrompida ou ausente cai em padrão seguro conhecido**, e o evento é registrado.
5. **Parâmetro de configuração tem faixa declarada e é validado na leitura**, não só na escrita.
6. **Imagem de atualização é o dado externo mais perigoso que o produto aceita.** Ela é verificada integralmente **antes** de se tornar ativa, a troca é atômica — interrupção de energia no meio da atualização deixa o produto com uma imagem válida, nunca com nenhuma —, o retorno à versão anterior é previsto, e a atualização só ocorre em estado em que a saída pode ser desligada com segurança. Onde não houver atualização em campo, isso é decisão registrada, não omissão.

## 8. Preparação para safety

Enquanto o projeto não adotar uma norma, este guia permanece agnóstico a ela: nenhuma das regras abaixo depende de norma específica, e todas reduzem o custo de adotar uma depois.

1. **Rastreabilidade auditável desde já** ([engenharia.md](engenharia.md), Seção *Branch, commit e rastreabilidade*): identificador do requisito presente na spec, no commit, no teste e no registro de validação. A ponta que fecha essa cadeia é a identificação de build ([c-build-e-analise.md](c-build-e-analise.md), Seção *Toolchain, build e identificação*): sem saber qual binário está no produto, nenhuma evidência anterior se liga ao equipamento em campo.
2. **Estado seguro definido e verificável** (Seção *Watchdog, reset e estado seguro*) é a peça que toda norma vai exigir e que nenhum projeto consegue reconstruir depois.
3. **Determinismo antes de conformidade**: sem alocação dinâmica, sem recursão, pilha orçada, prazos declarados ([c-embarcado.md](c-embarcado.md), Seção *Memória e recursos*).
4. **Modos de falha listados por função crítica** — o que pode falhar, como é detectado, o que acontece então. Uma tabela curta por função vale mais do que a norma inteira lida sem aplicação.
5. **A norma aplicável, quando conhecida, entra por ADR** no projeto, e o que ela exigir de específico mora nos documentos daquele projeto — nunca neste conjunto, que é geral por definição.
6. **Nada aqui declara conformidade.** Seguir este domínio prepara o terreno; conformidade exige a norma, o processo formal e a evidência arquivada.

## Checklist deste domínio

- [ ] A lógica de aplicação continua compilável sem a toolchain do alvo.
- [ ] Comportamento com modos está numa máquina de estado explícita, com dono único e estado de falha alcançável.
- [ ] Máquina de estado nova ou alterada está documentada a partir de `../templates/fsm.md`.
- [ ] Rotinas de interrupção são curtas, não bloqueiam, e todo dado compartilhado tem proteção declarada.
- [ ] Toda espera tem tempo limite; nenhum atraso foi usado como sincronização.
- [ ] Comparação de tempo é por diferença, tolerante a estouro do contador.
- [ ] Estado seguro é atingido na partida e na falha; o watchdog é alimentado em um ponto só.
- [ ] A causa do último reset é lida e a integridade da imagem é verificada na partida.
- [ ] Dado externo é validado antes de usado; área persistida tem versão e verificação de integridade.
- [ ] Atualização de firmware verifica a imagem antes de ativá-la e é atômica contra queda de energia.
- [ ] O tempo de execução de cada rotina de interrupção é conhecido; barreira de memória e buffer de DMA têm justificativa e manutenção de cache declaradas quando aplicável.
