# Domínio: engenharia e qualidade

Cobre como uma mudança entra no repositório e como se verifica que ela está correta: branching e revisão, commits e rastreabilidade, sensores, segredos, dependências, e o processo de conduzir a mudança do início ao fim — inclusive quando ela mexe na estrutura, num submódulo ou num arquivo gerado. Vale para qualquer contribuição, de pessoa ou de agente. O que é específico de agentes está em [ia.md](ia.md); o que é específico da documentação, em [../manutencao.md](../manutencao.md).

**Aplica-se a:** todo projeto.
**Leia quando:** for iniciar, revisar ou integrar uma mudança; preencher o `docs/workflow.md`; ou decidir quais verificações rodar antes de concluir.

## 1. Workflow de revisão

O que vale é o conceito — mudança revisável pelo diff antes de chegar ao tronco, integração decidida por uma pessoa, e trabalho de agente sempre isolado. Os comandos estão na notação do Git como ilustração; projeto em outro VCS registra os equivalentes no seu `docs/workflow.md`, sem que a regra mude.

**Branch curta, não obrigatória para tudo.** Branch de vida curta (horas ou poucos dias) é o padrão, porque é o que torna a revisão por diff possível e barata. Branch longa é o problema real: acumula divergência e vira merge irrevisável. Commit direto no tronco é legítimo quando o projeto o declara no `docs/workflow.md` — mantenedor único, mudança trivial — e os sensores rodam antes. Trabalho de agente nunca vai direto ao tronco: a branch é o que torna a ação dele reversível ([ia.md](ia.md), Seção *Limites de execução do agente*).

### Cenário 1 — Local, sem plataforma de PR/MR

1. A tarefa roda numa branch criada a partir de um branch base declarado — salvo a exceção de commit direto que o projeto tiver declarado para pessoas.
2. A revisão é feita pelo diff completo contra esse base: `git diff <base>...<branch>`. Os três pontos comparam contra o merge-base, então o que entrou no base depois não polui o diff.
3. O merge é sempre um comando executado por uma pessoa. Um agente nunca executa o merge, mesmo que a mudança pareça pronta.
4. Para trabalhar em mais de uma branch em paralelo, use `git worktree add -b <branch> ../<pasta> <base>` — cada worktree é uma pasta com sua própria branch, sobre o mesmo repositório, e os commits dela já são visíveis no diretório principal para revisão e merge.

Ressalvas de worktree:

- a mesma branch não pode estar ativa em duas worktrees — o Git recusa, e isso é proteção;
- só o histórico é compartilhado: cada worktree começa sem artefatos de build, arquivos ignorados e configuração local;
- submódulos — inclusive `docs/guide/` — não vêm populados: rode `git submodule update --init` na worktree nova;
- remova com `git worktree remove`, nunca apagando a pasta na mão;
- worktree isola o repositório, não o ambiente: trabalhos paralelos continuam disputando toolchain, portas e hardware de gravação/depuração.

Enquanto o projeto não tiver plataforma de PR/MR efetivamente em uso, o Cenário 1 é o vigente.

### Cenário 2 — Plataforma com PR/MR

1. Cada tarefa declara o **branch base**: origem da branch de trabalho e destino do PR/MR.
2. A branch da tarefa nasce desse base, nunca de outro não especificado.
3. O PR/MR volta para o mesmo base — nunca direto para a branch principal, a menos que ela seja o base declarado.
4. Revisão humana obrigatória antes do merge; o merge é ação humana.

## 2. Branch, commit e rastreabilidade

Estas convenções existem para que o diff seja revisável e para fechar a cadeia **spec → commit → revisão**.

1. **Uma branch, um assunto.** Nome `<tipo>/<assunto-curto>` em kebab-case; os tipos padrão são `feat`, `fix`, `refactor`, `docs`, `test`, `chore`, e o projeto pode trocá-los no `docs/workflow.md`. O que importa é o nome dizer o assunto; a lista fixa só evita discussão.
2. **Assunto do commit no imperativo**, até ~72 caracteres, sem ponto final. O idioma dos commits é decisão do projeto, declarada no `AGENTS.md`.
3. **O corpo explica o porquê e o impacto**, não o que o diff já mostra. Commit sem corpo só quando o assunto esgota a explicação.
4. **Commit que implementa requisito cita o identificador** (`REQ-<PREFIXO>-NNN`, `templates/spec.md`) e, quando houver, o ADR. O mesmo vale para a descrição do PR/MR. Com isso, `git log --grep REQ-UART-003` reconstrói a implementação de um requisito sem nenhuma tabela mantida à mão.
5. **Não misture assuntos no mesmo commit.** Reformatação em massa, renomeação de arquivos e mudança de comportamento vão em commits separados.
6. **Histórico compartilhado não é reescrito** sem combinação explícita entre quem trabalha nele.
7. **Finais de linha são normalizados pelo repositório** (`.gitattributes`, por exemplo `* text=auto`), não pela configuração de cada máquina. Sem isso, um editor em Windows transforma um commit de uma linha num diff do arquivo inteiro.
8. **Onde houver norma aplicável** (safety funcional, dispositivo médico), a rastreabilidade precisa ser **auditável**: o identificador aparece na spec, no commit, no teste e no registro de validação arquivado. É barata enquanto é escrita e cara quando precisa ser reconstruída.

## 3. Sensores e validação automática

Uma **regra** orienta antes de agir; um **sensor** verifica depois, automaticamente, e detecta o erro que passou pela regra. Projeto que só tem regras depende de todo mundo lembrar de tudo.

Conjunto mínimo, em ordem crescente de custo:

1. **Build** do módulo afetado.
2. **Teste direcionado** à mudança, ampliando para a suíte conforme o risco.
3. **Lint / análise estática** na configuração do próprio projeto.
4. **Links relativos da documentação** — o que impede que mover um arquivo quebre referências em silêncio. O conjunto fornece um verificador: `python docs/guide/tools/verificar.py`, que ignora blocos de código (templates contêm links que só resolvem no projeto que os usa).
5. **Varredura de segredos** antes do commit.

Regras de uso:

- os sensores existentes rodam **antes** de declarar a tarefa concluída, e quem executou informa quais rodou;
- sensor que não existe é registrado como verificação pendente, com o motivo — nunca simulado nem presumido aprovado;
- sensor que falha bloqueia a conclusão: corrigir ou relatar, não seguir adiante;
- onde o ambiente permitir, sensores rodam sozinhos (hook de pré-commit, pipeline). Sensor que depende de alguém lembrar é regra.

## 4. Segredos e dados sensíveis

1. Credencial, chave, token, certificado privado ou dado pessoal nunca vão para o repositório — nem em código, configuração, spec, ADR, exemplo ou log colado num documento.
2. O `.gitignore` faz parte do harness: cobre no mínimo artefatos de build, dependências instaladas, configuração local de máquina ou IDE, arquivos de ambiente (`.env` e equivalentes) e saídas de ferramenta. Mantê-lo correto é parte da tarefa que introduz o arquivo local — e ele nunca justifica guardar um segredo real dentro da pasta do projeto.
3. Documentação cita o **nome** da variável ou parâmetro, nunca o valor.
4. Segredo que chegou ao histórico é **rotacionado**. Apagar num commit seguinte não desfaz a exposição: o valor continua no histórico e em todo clone.
5. Dado de produção (log real, dump, base de clientes) não entra no repositório; use dado sintético.

## 5. Testes, comandos e dependências

1. **Teste existente é mecanismo de validação, não especificação absoluta.** Rode primeiro o mais direcionado, amplie conforme o risco, não declare cobertura que não foi medida, e registre a validação manual quando ela for o mecanismo real do projeto.
2. **Só se documenta comando que existe e foi executado**, com diretório, pré-requisitos e efeitos colaterais quando relevantes. Comando inferido não vira instrução oficial; nenhum comando documentado contém credencial.
3. **Dependência nova precisa ser necessária, confiável e ter versão fixada.** Nome incomum é verificado contra o registro oficial antes de instalar — typosquatting e pacote inventado por agente são o mesmo ataque.

## 6. Processo de uma mudança

Vale para pessoa e agente; o que o agente precisa observar a mais em cada etapa está em [ia.md](ia.md), Seção *Como o agente conduz uma tarefa*.

1. **Entender**: objetivo e critério de sucesso, áreas afetadas, risco, se envolve código gerado, submódulo ou dependência externa, e quais validações existem. Leia o que se aplica à área (código, specs, ADRs, domínio), rastreie as interfaces afetadas e confira o estado inicial do VCS. Pare de investigar quando houver evidência suficiente.
2. **Planejar na medida da mudança**: mudança trivial vai direto; mudança não trivial ganha um plano curto antes da primeira edição — arquivos, passos, como verificar; funcionalidade maior ganha spec ([specs.md](specs.md)).
3. **Implementar em incrementos verificáveis**: cada incremento é uma alteração coesa seguida do sensor mais barato que a verifica. Erro encontrado logo depois de uma alteração pequena tem causa óbvia; o mesmo erro depois de vinte alterações vira investigação. Mudança mínima, no estilo e nas abstrações existentes, sem refatoração não relacionada; ao mover arquivos, atualize todas as referências.
4. **Validar**: sensores do mais específico ao mais amplo; para mudança só documental, inspeção do diff e verificação de links. O que não puder ser executado é registrado com o motivo.
5. **Documentar**: uma passada, com o comportamento já estável e verificado ([../manutencao.md](../manutencao.md), Seção *Quando e como atualizar*).
6. **Encerrar com o resumo da mudança** (abaixo).

### Resumo da mudança

Toda mudança termina com um resumo curto, escrito para quem vai revisar sem ter acompanhado o trabalho. É a resposta final do agente, a descrição do PR/MR e a base do corpo do commit — o mesmo texto, não três.

```markdown
**Principais mudanças**
- <o que mudou e por quê, em termos de comportamento, estrutura ou regra — não uma lista de arquivos>

**Decisões e suposições**
- <o que foi decidido ou suposto sem confirmação, para quem revisa validar; omita se não houver>

**Verificação**
- Executado: <comandos e resultado>
- Não executado: <o que faltou e por quê>

**Pendências e riscos**
- <o que ficou para depois, o que pode quebrar, o que foi visto fora do escopo; omita se não houver>

**Arquivos**
- Criados / alterados / movidos / removidos: <lista curta; em mudança grande, agrupe por pasta>
```

O resumo diz a verdade sobre o estado: o que não foi verificado aparece como não verificado, e o que ficou pela metade aparece como pendente. "Pronto" sem verificação declarada não é pronto.

## 7. Modificações estruturais

Antes de mover ou dividir componentes: identifique a responsabilidade de cada área, mapeie dependências de entrada e saída, localize imports, scripts, configurações, pipelines e documentação afetados, verifique caminhos codificados, preserve compatibilidade ou declare a migração, e atualize o `ARCHITECTURE.md` se limites mudarem.

Evite: mover arquivos sem atualizar consumidores; criar camada sem responsabilidade própria; duplicar utilitários; reorganizar código apenas para acomodar uma IA ou uma IDE.

## 8. Submódulos e projetos externos

Todo submódulo é projeto externo por padrão — inclusive `docs/guide/`. Não altere código, configuração ou documentação dentro dele, não crie `AGENTS.md`, `ARCHITECTURE.md` ou Skills nele, não assuma permissão para enviar alterações, e documente só a interface que o projeto principal usa. Mudança num submódulo acontece apenas quando pedida explicitamente, como trabalho separado no repositório dele.

## 9. Arquivos gerados

Antes de editar um arquivo, determine se ele é gerado (cabeçalho de geração, diretório de saída, regra de build). Havendo gerador: altere a fonte, execute o processo oficial, revise todas as saídas — inclusive remoções — e valide os consumidores. Não simule à mão a saída de um gerador indisponível; registre a limitação.

## Checklist deste domínio

- [ ] A mudança seguiu o fluxo do `docs/workflow.md`; se feita por agente, em branch própria.
- [ ] Commits têm um assunto só, explicam o porquê e citam requisito ou ADR quando aplicável.
- [ ] Os sensores existentes foram executados; os ausentes, registrados como pendência.
- [ ] Nenhum segredo, credencial ou dado de produção entrou no diff.
- [ ] Nenhum comando inferido foi documentado como oficial; dependência nova tem versão fixada.
- [ ] A mudança terminou com o resumo no formato da Seção *Processo de uma mudança*, incluindo o que não foi verificado.
- [ ] Nenhum submódulo foi alterado sem pedido explícito; arquivo gerado foi alterado pela fonte.
