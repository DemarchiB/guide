# Guia de apoio: harness e condução do trabalho com IA

Cobre o que se monta uma vez e depois molda todas as sessões: o que é carregado em toda tarefa, como a sessão é conduzida, Skills e subagentes, e os arquivos que uma ferramenta específica precisa para consumir as instruções canônicas. O que o agente observa ao executar uma tarefa está em [ia.md](ia.md); este arquivo só é lido quando se configura ou se ajusta o trabalho com IA.

**Aplica-se a:** todo projeto que usa agentes de IA.
**Leia quando:** for escrever ou revisar `AGENTS.md` e Skills, configurar uma ferramenta ou subagente, revisar um adaptador, ou entender por que uma sessão está cara ou pouco produtiva.

## 1. Harness e economia de contexto

**Harness** é tudo o que molda como o agente usa as ferramentas que tem: `AGENTS.md`, Skills, specs, ADRs, sensores e configuração de permissões. Agente sem harness tem acesso, mas não contexto nem limites.

O contexto é pago em toda sessão, e mais contexto não é melhor contexto — texto de processo em excesso compete com o problema, e o agente passa a raciocinar sobre procedimento em vez de sobre a tarefa:

1. **Carregue sempre só o que o agente erraria sem saber**: comandos reais, convenções não óbvias, restrições críticas e desvios. O que ele descobre lendo a árvore ou o manifesto não entra. O teste de cada linha é *uma tarefa típica sairia errada sem isto?*
2. **Escreva instruções concretas e verificáveis.** "Rode `ctest --preset host`" é acionável; "garanta a qualidade" é ruído.
3. **Carregue detalhes sob demanda**: o domínio quando a tarefa o toca, o `AGENTS.md` aninhado da pasta aplicável, a Skill do procedimento, o template ao criar documento. A declaração de domínios no projeto é o catálogo do que existe, nunca uma ordem de carregar tudo.
4. **Não use texto para impor ações que exigem garantia**: hook, sensor, permissão e proteção de branch são o mecanismo correto. Uma regra escrita reduz a frequência de um erro; só o mecanismo o impede.
5. **Arquitetura não é entrada global por padrão.** Leia `ARCHITECTURE.md` quando a tarefa atravessar componentes, interfaces, variantes, build ou limites de memória. Para um arquivo localizado, o `AGENTS.md` mais próximo, o arquivo alterado e suas dependências bastam.

## 2. Condução da sessão

Onde mais se ganha em custo e em qualidade não é no texto do harness: é em como a sessão é conduzida.

1. **Uma tarefa por sessão.** O contexto inteiro é reenviado a cada turno: numa sessão longa o custo cresce mais rápido que o trabalho feito, e a qualidade cai quando a janela se enche de tentativas antigas. Tarefa terminada, sessão nova.
2. **Aponte os arquivos.** Dizer o que ler é mais barato e mais preciso do que deixar o agente procurar; busca cega pela árvore é o gasto invisível de uma sessão.
3. **Isole investigação ampla** num contexto separado — subagente ou sessão auxiliar — que devolve conclusões e evidências, não a transcrição do que leu.
4. **Caminho errado não se corrige empilhando.** Se a abordagem se mostrou errada, volte ao último ponto bom ([git.md](git.md), Seção *Commit e rastreabilidade*) e recomece, levando no pedido o que você aprendeu. Tentativa descartada continua influenciando o agente enquanto estiver no contexto.
5. **O que é carregado em toda sessão fica estável durante a tarefa.** Alterar `AGENTS.md` ou o harness no meio do trabalho invalida o reaproveitamento de contexto e faz repagar tudo; mudança de harness é tarefa própria.
6. **O esforço caro vai onde ele paga.** Entender, planejar, escrever spec e revisar são onde a capacidade do modelo aparece; executar um plano aceito, com sensor verde ao fim de cada passo, exige bem menos. Projeto com sensores pode delegar a execução barata; projeto sem sensores paga o modelo caro em toda tarefa, porque acertar de primeira vira a única estratégia disponível ([testes.md](testes.md), Seção *Conjunto mínimo de sensores*).

## 3. Skills: criar, usar e manter

Uma **Skill** é um procedimento reutilizável — revisar uma mudança, corrigir um defeito, analisar memória, preparar uma liberação. O formato e a mecânica de carregamento estão em [templates/skill.md](../templates/skill.md).

1. **Crie a Skill quando o procedimento for recorrente, específico do projeto, difícil de acertar sem instruções e já executado com sucesso ao menos uma vez** — não a partir de um procedimento ideal imaginado. Registre o que precisou ser explicado ou corrigido. Procedimento genérico de linguagem, de Git ou de ferramenta comum não vira Skill: o agente já o executa, e a `description` custa contexto sem contrapartida.
2. **Aponte para as regras, não as repita.** O procedimento manda aplicar os checklists dos domínios; não copia seu conteúdo.
3. **Torne determinístico o que puder ser script**, em vez de deixar o agente reinterpretar cada passo.
4. **Teste o acionamento** numa sessão nova com um pedido que deve ativar a Skill e outro parecido que não deve.
5. **Use a Skill quando o pedido corresponder a ela**; não improvise outro procedimento nem repita seu corpo no prompt.
6. **Mantenha-a junto com o procedimento.** Mudança de comando, caminho, ferramenta ou ordem exige atualizar a Skill; desvio recorrente é defeito a corrigir.
7. **Remova Skills sem uso** ou cujo procedimento o agente execute bem sem instrução; cada `description` custa contexto na descoberta.
8. **Rode `python docs/guide/tools/verificar.py`** depois de criar, renomear ou alterar uma Skill ou adaptador.

## 4. Adaptadores de ferramenta

O repositório tem uma fonte de instruções (`AGENTS.md`) e um lugar canônico para Skills (`.agents/skills/`). Ferramenta que não consome esses formatos recebe um adaptador somente se estiver em uso; regra do projeto nunca fica apenas no adaptador.

1. Prefira, nesta ordem: configuração apontando para a fonte canônica; arquivo da ferramenta que inclui a fonte; link simbólico quando sobreviver ao clone; stub textual como último recurso.
2. Stub de Skill repete somente `name` e `description` da Skill canônica e aponta o corpo para `.agents/skills/<nome>/SKILL.md`. O verificador confere a igualdade.
3. **Subagente é adaptador quando o isolamento importar** — revisão sem permissão de escrita, ou investigação ampla que consumiria o contexto principal — e segue a Skill correspondente.
4. Regra por caminho é ponteiro para o domínio aplicável, nunca cópia dele.
5. **Configuração que muda o que o agente pode executar é versionada e revisada como código**: comandos permitidos e negados, integrações e diretórios. É aqui que as proibições de [git.md](git.md), Seção *O que exige pedido explícito*, deixam de ser texto e passam a valer. Segredos nessa configuração seguem [engenharia.md](engenharia.md), Seção *Segredos e dados sensíveis*: documenta-se o nome da variável, nunca o valor.

## Checklist deste guia

- [ ] O que é carregado em toda sessão passou pelo teste "uma tarefa típica sairia errada sem isto?".
- [ ] A Skill nasceu de procedimento observado, tem acionamento testado e descreve um critério de conclusão.
- [ ] O corpo da Skill aponta para regras canônicas sem copiá-las.
- [ ] O adaptador só existe para ferramenta em uso e referencia a fonte correta.
- [ ] Configuração de permissão está versionada, sem segredo, e nega o que o guia proíbe.
- [ ] `python docs/guide/tools/verificar.py` passou.
