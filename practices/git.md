# Domínio: Git e entrega do trabalho

Cobre como uma mudança sai da máquina e chega ao tronco: branch, commit, rastreabilidade, revisão e o que um agente pode fazer no Git — em sessão local e em execução assíncrona. O processo de conduzir a mudança está em [engenharia.md](engenharia.md).

**Aplica-se a:** todo projeto versionado.
**Leia quando:** for entregar, revisar ou integrar uma mudança, ou configurar o que um agente pode executar.

Os comandos estão na notação do Git, como ilustração; projeto em outro VCS registra os equivalentes no seu `AGENTS.md` ou em `docs/workflow.md`.

## 1. O agente propõe, uma pessoa integra

A unidade de entrega de um agente é uma **proposta revisável** — uma branch, e um PR/MR quando houver plataforma —, nunca uma integração. Isso não muda entre trabalhar local e na nuvem; o que muda é quem escreve o commit e como a proposta chega à revisão, e isso o projeto declara na seção *Fluxo* do seu `AGENTS.md`.

Duas consequências:

- **Proibição em texto não é garantia.** O que impede um push indevido é proteção de branch no servidor e lista de comandos negados na configuração da ferramenta ([ia-harness.md](ia-harness.md), Seção *Adaptadores de ferramenta*). As regras abaixo orientam; o mecanismo é que segura.
- **Dentro da branch dele, tudo que o agente faz é reversível — e por isso é livre.** É a branch que torna a autonomia barata: sem ela, cada ação precisa de permissão e o trabalho vira supervisão.

## 2. Branch e revisão

1. **Branch curta, um assunto.** Nome `<tipo>/<assunto-curto>` em kebab-case; tipos padrão `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, trocáveis pelo projeto. O problema real não é a quantidade de branches: é a branch longa, que acumula divergência e vira merge irrevisável.
2. **Toda tarefa declara o branch base** — de onde a branch nasce e para onde a mudança volta; o padrão do projeto fica na seção *Fluxo* do `AGENTS.md`. Trabalho de agente nasce de um base declarado e nunca vai direto ao tronco; commit direto no tronco por uma pessoa é legítimo quando o projeto o declara (mantenedor único, mudança trivial) e os sensores rodaram antes.
3. **A revisão é pelo diff completo contra o base**: `git diff <base>...<branch>`. Os três pontos comparam contra o merge-base, então o que entrou no base depois não polui o diff.
4. **O merge é ação de uma pessoa**, em qualquer cenário — mesmo com a mudança pronta e os sensores verdes.
5. **Trabalho em paralelo usa worktree**: `git worktree add -b <branch> ../<pasta> <base>`. É o que permite deixar um agente trabalhando sem travar o que você está editando. Ressalvas: a mesma branch não fica ativa em duas worktrees (o Git recusa, e isso é proteção); só o histórico é compartilhado, então a worktree nasce sem artefatos de build e sem configuração local; submódulos — inclusive `docs/guide/` — exigem `git submodule update --init`; remova com `git worktree remove`, nunca apagando a pasta; e worktree isola o repositório, não o ambiente — trabalhos paralelos continuam disputando toolchain, portas e hardware de gravação.

## 3. Commit e rastreabilidade

1. **Assunto no imperativo**, até ~72 caracteres, sem ponto final; o corpo explica o porquê e o impacto, não o que o diff já mostra. O idioma é decisão do projeto, declarada no `AGENTS.md`.
2. **Commit pequeno e frequente é ponto de retorno.** Vale para pessoa e mais ainda para agente: uma sessão que produz um único commit gigante só pode ser desfeita inteira, e a parte boa vai junto. Um commit por incremento verificado ([engenharia.md](engenharia.md), Seção *Processo de uma mudança*) é o que permite voltar um passo em vez de recomeçar.
3. **O que entra no commit é escolhido, não varrido.** Adicione os caminhos da tarefa; `git add -A` num repositório com trabalho preexistente, artefato de build ou arquivo local leva para o diff o que ninguém pediu. Confira `git status` e `git diff` antes de começar e antes de commitar.
4. **Commit que implementa requisito cita o identificador** (`REQ-<PREFIXO>-NNN`, `templates/spec.md`) e o ADR quando houver — no commit e na descrição do PR/MR. Assim `git log --grep REQ-UART-003` reconstrói a implementação de um requisito sem nenhuma tabela mantida à mão.
5. **Não misture assuntos.** Reformatação em massa, renomeação de arquivos e mudança de comportamento vão em commits separados.
6. **Histórico compartilhado não é reescrito** sem combinação explícita entre quem trabalha nele.
7. **Finais de linha são normalizados pelo repositório** (`.gitattributes`, por exemplo `* text=auto`), não pela configuração de cada máquina. Sem isso, um editor em Windows transforma um commit de uma linha num diff do arquivo inteiro.
8. **Onde houver norma aplicável**, a rastreabilidade precisa ser auditável: o identificador aparece na spec, no commit, no teste e no registro de validação arquivado. É barata enquanto é escrita e cara quando precisa ser reconstruída.

## 4. Agente em sessão local

O padrão é **o agente não commitar**: ele edita os arquivos, entrega o resumo e para; quem commita é a pessoa, depois de olhar o diff. Nada entra no histórico antes de ter sido revisado, e o que se revisa é exatamente o que o agente fez, sem mensagem de commit nenhuma explicando o que ele achou que fez.

O projeto escolhe um dos dois modos e o declara na seção *Fluxo* do `AGENTS.md`:

| Modo | O agente | A pessoa |
| --- | --- | --- |
| **Árvore de trabalho** (padrão) | edita e entrega o resumo, sem commitar | revisa o diff não commitado, commita e integra |
| **Commit na branch** | commita cada incremento verificado na branch de trabalho | revisa `git diff <base>...<branch>` e integra |

**O que o modo padrão custa é o ponto de retorno**, e ele se compra de volta commitando por incremento em vez de só no fim: o agente para ao concluir cada passo do plano, você confere e commita, e o passo seguinte parte de um estado bom conhecido ([engenharia.md](engenharia.md), Seção *Processo de uma mudança*). Sem isso, um caminho errado no meio de uma sessão longa leva junto o que já estava bom. O modo **commit na branch** existe para quando essa parada não é prática — refatoração ampla, ou agente trabalhando enquanto você faz outra coisa — e exige branch exclusiva dele.

Em ambos, o merge, o push ao tronco e a reescrita de histórico são da pessoa; e em ambos o agente confere o estado inicial do VCS antes de tocar em qualquer arquivo — alteração preexistente não é sobrescrita, não é formatada e não entra no diff da tarefa.

## 5. Agente assíncrono e PR/MR

Quando o agente roda sem alguém acompanhando — na nuvem, por tarefa agendada ou a partir de uma issue —, **a entrega dele é sempre um PR/MR aberto contra o base declarado**. Não é escolha do projeto e não há modo alternativo: PR é proposta, passa pela mesma revisão de qualquer outra e é onde os sensores rodam sem depender de alguém lembrar. Projeto sem plataforma de PR não roda agente assíncrono.

1. **O agente faz push da própria branch e abre o PR/MR**; nunca push para o base nem para o tronco.
2. **O merge continua humano, garantido por mecanismo**: revisão obrigatória e proibição de push direto no tronco, configuradas no servidor. Agente com permissão de merge é configuração errada, não regra desobedecida.
3. **Um PR, um assunto, pequeno.** PR grande gerado por agente é irrevisável, e é onde o defeito passa. O que não cabe num PR revisável vira spec com tarefas, uma por PR ([specs.md](specs.md)).
4. **A descrição do PR é o resumo da mudança** ([engenharia.md](engenharia.md), Seção *Resumo da mudança*) — o mesmo texto, incluindo o que não foi verificado. PR que não declara isso transfere para quem revisa um trabalho que ninguém fez.
5. **CI é o porteiro.** PR com sensor vermelho não é revisado: o agente corrige e atualiza o PR. Sem CI, o PR declara quais sensores rodaram e onde.
6. **Resposta à revisão vem em commits novos na mesma branch**, nunca em push forçado que apague o histórico que a revisão comentou. Limpar o histórico, se o projeto quiser, é decisão de quem integra, no merge.
7. **O agente não aprova, não integra e não fecha o próprio PR**, e não aceita mudança de escopo vinda da revisão: escopo novo é PR novo.

## 6. O que exige pedido explícito

Livre: ação reversível e contida na branch de trabalho. Exige pedido explícito na tarefa tudo que tenha efeito fora dela:

- merge, rebase ou push no tronco, em branch de integração ou em qualquer histórico compartilhado;
- `push --force` (inclusive `--force-with-lease`) em branch não exclusiva do agente, e `commit --amend` em commit já enviado;
- `reset --hard`, `checkout .`, `clean -fd` e qualquer comando que descarte trabalho não versionado — o que foi descartado não volta;
- apagar branch alheia, mover ou apagar tag;
- alterar submódulo, projeto externo ou ambiente compartilhado ([engenharia.md](engenharia.md), Seção *Submódulos e arquivos gerados*);
- alterar hooks, configuração de CI, credenciais ou permissões de acesso.

## Checklist deste domínio

- [ ] O trabalho saiu de um base declarado, numa branch de um assunto só.
- [ ] O estado inicial do VCS foi conferido e nenhuma alteração preexistente entrou no diff.
- [ ] O que entrou em cada commit foi escolhido por caminho, não varrido.
- [ ] Commits explicam o porquê e citam requisito ou ADR quando aplicável.
- [ ] Nenhum merge, push ao tronco ou reescrita de histórico compartilhado foi feito pelo agente.
- [ ] PR/MR aberto por agente tem um assunto, traz o resumo da mudança e não foi aprovado nem integrado por ele.
