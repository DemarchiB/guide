# Domínio: build e análise de C embarcado

Cobre como o código C de firmware é compilado, identificado e verificado: toolchain e flags, identificação do binário, orçamento de memória, sensores da linguagem, adoção incremental de análise estática e adoção de MISRA. Como se escreve o código está em [c-embarcado.md](c-embarcado.md); as regras gerais de sensores, em [testes.md](testes.md), Seção *Conjunto mínimo de sensores*.

**Aplica-se a:** projetos com código C para microcontrolador.
**Leia quando:** for configurar toolchain ou build, introduzir ou ajustar analisador estático, adotar MISRA, registrar desvio de regra, ou investigar aviso ou achado que o build passou a acusar.

Flags e comandos aparecem na notação de GCC e CMake, como ilustração. O conjunto real de um projeto — compilador, versão, flags, ferramenta de análise — é fato daquele projeto e mora no seu `AGENTS.md` (comandos) e em ADR (escolhas).

## 1. Toolchain, build e identificação

1. **O padrão da linguagem é declarado no build** (`-std=c99`, `-std=c11`), nunca deixado no default, que muda quando a toolchain é atualizada.
2. **Aviso é tratado como erro no build de desenvolvimento e no de integração.** Base mínima `-Wall -Wextra`; para C embarcado valem também `-Wconversion`, `-Wshadow`, `-Wundef` e `-Wswitch-enum`, promovidos conforme a Seção *Adoção incremental*. Com a toolchain fixada (regra seguinte), `-Werror` não quebra por atualização surpresa do compilador. Aviso não se desliga para passar: corrige-se, ou suprime-se no local com o motivo.
3. **A toolchain é fixada e reproduzível.** O projeto declara a versão exata do compilador e guarda o meio de reproduzi-la (instalador arquivado, contêiner, preset). Produto de automação vive muitos anos: recompilar com outra versão produz binário diferente do validado.
4. **O build roda por linha de comando**, independente de IDE (por exemplo, `cmake --preset <alvo>` e `cmake --build --preset <alvo>`). Build que só existe dentro de uma IDE não é verificável por sensor nem por agente.
5. **O firmware carrega sua identificação** — versão, commit e marca de "árvore suja" — **gerada pelo build** e legível em execução, nunca digitada numa constante. O binário liberado é arquivado junto com a tag correspondente.
6. **Flash e RAM são orçados**: o consumo é extraído do mapa de memória a cada build e comparado com um limite declarado. Descobrir que a flash acabou na última funcionalidade é o defeito clássico de firmware, e ele só aparece cedo se for medido desde cedo.
7. **Extensão de compilador é decisão consciente** — em ADR quando afeta portabilidade — e o código que depende dela fica isolado na camada de hardware.
8. **O nível de otimização faz parte da configuração declarada.** Código que só funciona em um nível tem defeito — tipicamente `volatile` ausente ou comportamento indefinido —, e o defeito se corrige, não se contorna baixando a otimização.

## 2. Sensores da linguagem

Ao conjunto mínimo de [engenharia.md](engenharia.md), este domínio acrescenta:

1. **Compilador em modo estrito** — o analisador estático mais barato que existe, e o primeiro a adotar.
2. **Analisador estático dedicado** num alvo do próprio build (alvo do CMake, `make analyze`), não como passo manual.
3. **Orçamento de memória** verificado a cada build (Seção *Toolchain, build e identificação*).
4. **Complexidade limitada por sensor**, onde houver ferramenta: função acima do limite declarado falha ou entra na lista de dívida. Complexidade alta é o melhor indicador barato de onde os defeitos vão aparecer — muitas vezes uma máquina de estado implícita pedindo para virar explícita ([firmware.md](firmware.md), Seção *Máquinas de estado*).
5. **Teste em host é sensor, não luxo.** A lógica independente de hardware compila e roda no PC, num preset próprio do build; onde ainda não houver suíte, isso é pendência registrada — nunca "coberto por teste manual em bancada". O que o torna possível é a separação de camadas ([firmware.md](firmware.md), Seção *Camadas e portabilidade*); o que testar e como, em [testes.md](testes.md).
6. **O preset de host liga os sanitizers** (`-fsanitize=address,undefined`): eles encontram, com uma flag, o estouro de buffer e o comportamento indefinido que no alvo aparecem como travamento aleatório meses depois.

## 3. Adoção incremental

**Ordem num projeto sem nada:** avisos do compilador → analisador aberto na configuração padrão → conjunto de regras normativo → conformidade completa. Pular etapa produz milhares de achados e abandono da ferramenta.

**Como impedir achado novo sem parar para limpar o legado** — o mecanismo depende de quem emite o achado:

- **Compilador: catraca.** `-Werror` é tudo ou nada, sem linha de base nativa. Avança-se *por escopo* — `-Werror` só nos alvos já limpos, com `target_compile_options` por alvo, nunca flag global — e *por categoria* — `-Werror=implicit-function-declaration`, `-Werror=return-type`, `-Werror=conversion`, à medida que cada uma zera no projeto. Escopo ou categoria promovida nunca regride.
- **Analisador estático: linha de base de supressões.** Os achados existentes ficam num arquivo versionado, e o sensor falha só em achado fora dele. Alternativa equivalente: analisar apenas as linhas alteradas pelo diff.
- **A linha de base é indexada por arquivo e regra, nunca por número de linha.** Congelar `driver.c:412` faz qualquer inserção acima reabrir o achado antigo e mascarar o novo; em uma semana o sensor vira ruído e é desligado.
- **A dívida é medida e encolhe.** O tamanho da linha de base e a lista de alvos ainda sem `-Werror` ficam registrados no projeto e são revisitados; catraca sem número é adiamento.
- **Achado suprimido tem justificativa no próprio local** e, se for desvio de regra adotada, o registro da Seção *Adoção do MISRA*.
- **Código legado é migrado quando a área é tocada** por outra tarefa, nunca por mutirão, que gera diff irrevisável.

## 4. Adoção do MISRA

MISRA C é um subconjunto da linguagem publicado como documento normativo. O texto das regras **não é reproduzido aqui** — é protegido por direito autoral. Este domínio define o processo de adoção.

1. **Adoção declarada, não presumida.** O projeto registra em ADR a edição, o conjunto de regras adotado e a ferramenta que verifica. Projeto que "segue MISRA" sem esses três fatos não segue.
2. **Adesão parcial é legítima quando é explícita.** O padrão deste conjunto é o subconjunto pragmático: regras *Mandatory* na íntegra, *Required* de maior retorno, *Advisory* como recomendação. O que ficou de fora é listado, com o motivo.
3. **Desvio é registrado, não silenciado.** Todo desvio de regra adotada tem registro com identificador da regra, local, motivo técnico, análise de risco e quem aprovou. Supressão inline sem esse registro viola o processo, mesmo com a ferramenta verde.
4. **Código de terceiro é isolado e declarado fora do escopo** — HAL do fabricante, RTOS, biblioteca de comunicação —, com fronteira explícita e validação dos dados que a atravessam.
5. **[c-embarcado.md](c-embarcado.md) não substitui o documento.** Boa parte dele coincide com o espírito do MISRA e é adotável hoje, sem documento nem ferramenta — mas conformidade declarada exige os dois.

## Checklist deste domínio

- [ ] O build declara padrão e toolchain fixada e não introduziu aviso novo no escopo já promovido.
- [ ] O firmware identifica versão e commit gerados pelo build; o orçamento de flash e RAM foi verificado.
- [ ] Os sensores da linguagem rodaram; o analisador não acusa achado fora da linha de base.
- [ ] Nenhum escopo ou categoria promovida na catraca regrediu.
- [ ] Desvio de regra adotada tem registro com motivo, risco e aprovação.
