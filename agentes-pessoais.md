# Agentes pessoais — criar agentes de IA portáveis

Este arquivo é para a pessoa que quer criar agentes de IA para o próprio trabalho — ler os e-mails e dizer o que precisa ser feito, resumir documentos — e para a IA que ela chamar explicitamente para ajudar nisso. Não está na tabela de roteamento do `PROJECT_GUIDE.md` e não é lido numa tarefa de projeto.

O objetivo é que o agente pertença a quem o escreveu, não à ferramenta: o mesmo agente roda num chat de IA pessoal, na ferramenta que a empresa disponibiliza e na que vier depois. Este conjunto guarda o método e os templates; os agentes, o contexto pessoal e os dados moram num repositório de agentes de quem os criou ([templates/repositorio-agentes.md](templates/repositorio-agentes.md)), nunca aqui.

Este arquivo cobre o que é um agente, os níveis 1 e 2 — escrever, testar e salvar o agente com o seu contexto — e os pedidos prontos. Ligar ferramentas, automatizar e migrar estão em [agentes-ferramentas.md](agentes-ferramentas.md).

**Leia quando:** for criar um agente, testá-lo ou montá-lo com o seu contexto numa ferramenta de IA.

## 1. O que é um agente

Um agente é um modelo de IA com três coisas:

1. **Instruções:** o texto que diz o objetivo, os passos, as regras e o formato da resposta.
2. **Ferramentas:** acesso a algo fora da conversa — ler e-mails, abrir arquivos, consultar uma agenda.
3. **Um loop:** em vez de responder uma vez, o modelo decide o próximo passo, usa uma ferramenta, vê o resultado e repete até terminar.

Pedido "veja meus e-mails e diga o que preciso fazer": o agente busca os não lidos, abre os que parecem relevantes, lê um anexo quando precisa e devolve uma lista de tarefas. Ninguém programou essa sequência; o modelo a decide a partir das instruções.

Sem ferramentas e sem loop, o mesmo texto de instruções já é útil — é o nível 1. Agente não é uma tecnologia à parte: é um texto bem escrito que ganha acesso e autonomia um passo de cada vez (Seção *Os quatro níveis*).

## 2. Mapa de termos

| Termo | O que é | Portátil? |
| --- | --- | --- |
| Prompt | Texto que diz à IA o que fazer numa conversa. | Sim: é texto. |
| Instruções persistentes | Texto que a ferramenta carrega em toda conversa de um projeto, assistente ou espaço de trabalho: contexto pessoal e o agente. | O texto, sim; o lugar onde ele é colado muda de ferramenta para ferramenta. |
| Skill | Pasta com um `SKILL.md` no padrão aberto Agent Skills: nome, descrição de quando usar e instruções, mais arquivos de apoio opcionais. A ferramenta lê só nome e descrição de todas e carrega o resto quando a tarefa pede. | Sim, nas ferramentas que suportam o padrão; nas outras, o corpo do `SKILL.md` é colado como texto. |
| Conector / MCP | Ligação da IA a um sistema externo (e-mail, agenda, arquivos). O Model Context Protocol (MCP) é o protocolo aberto usado para isso por boa parte das ferramentas. | Em parte: o protocolo é aberto, mas conexão, login e permissão são configurados em cada ferramenta. |
| Subagente | Outra instância de IA que o agente principal chama para uma parte da tarefa, com contexto próprio. | Não: recurso de cada ferramenta. |
| `AGENTS.md` | Arquivo de instruções que ferramentas de IA para código leem automaticamente da raiz de um repositório. | Sim, entre as ferramentas que o leem. |
| Automação | O agente roda sozinho, por horário ou evento, sem ser chamado. | O agendamento, não: é configurado em cada ferramenta. A descrição do que a automação faz, sim. |

**O que é texto viaja; conexão, permissão e agendamento se refazem em cada ferramenta.** Por isso tudo que é texto — instruções, contexto pessoal, casos de teste — mora num repositório seu, versionado, e a ferramenta é só o lugar onde o agente roda. Trocar de ferramenta ou de empresa passa a ser reconfigurar o acesso e conferir os testes, não reescrever os agentes.

## 3. Os quatro níveis

| Nível | O que é | Exige da ferramenta | Sobe para o próximo quando |
| --- | --- | --- | --- |
| 1. Prompt reutilizável | O agente escrito como texto e colado junto com a entrada. | Um chat. | Os casos de teste passam com o texto colado à mão, em pelo menos duas ferramentas. |
| 2. Assistente com contexto | Agente e contexto pessoal salvos nas instruções persistentes. | Instruções persistentes. | Levar a entrada até a IA à mão virou o gargalo (copiar e-mails um a um, anexar os mesmos arquivos). |
| 3. Agente com ferramentas | O agente busca a entrada sozinho, por um conector. | Conectores. | Rodou muitas vezes sem erro, e a tarefa se repete num horário ou evento previsível. |
| 4. Automação | O agente roda sem ser chamado e entrega o resultado onde você vai ver. | Agendamento ou gatilhos. | — |

1. **Comece no nível 1, sempre.** O valor do agente está no texto; um texto ruim ligado ao seu e-mail só erra mais rápido e com mais acesso.
2. **Suba um nível de cada vez, e só com os casos de teste passando.** Cada nível acrescenta um ponto de falha — contexto que interfere, conexão, ausência de quem revise —; subir dois de uma vez deixa sem saber qual deles falhou.
3. **Nem todo agente precisa chegar ao nível 4.** Um resumo de documento pedido quando é preciso fica bem no nível 2; automatizar o que é ocasional só acrescenta custo e algo a manter.

Os níveis 3 e 4 estão em [agentes-ferramentas.md](agentes-ferramentas.md).

## 4. Nível 1 — prompt reutilizável

Um agente tem estas partes, nesta ordem:

| Parte | Diz | Exemplo (triagem de e-mail) |
| --- | --- | --- |
| Objetivo | O resultado, numa frase. | Dizer o que exige ação minha nos e-mails recebidos. |
| Entrada | O que o agente recebe e de onde. | Os e-mails das últimas 24 horas. |
| Passos | O caminho, numerado. | Ignorar newsletters e notificações automáticas; de cada e-mail restante, extrair quem pede, o quê e o prazo; classificar. |
| Regras | Limites e o que fazer na dúvida. | Nunca inventar prazo: sem prazo escrito, "sem prazo". Nunca responder nem apagar e-mails. |
| Formato da saída | A estrutura exata. | Tabela: Prioridade, Remetente, O que fazer, Prazo. |
| Exemplo de saída | Uma saída curta, pronta. | Duas linhas da tabela preenchidas. |

Em arquivo, o agente é uma Skill, no esqueleto de agente de [templates/skill.md](templates/skill.md): o frontmatter dá nome e descrição, e as partes acima formam o corpo. O corpo funciona sozinho, colado em qualquer chat.

Ao escrever:

1. **Escreva para quem não conhece você nem a tarefa.** A IA só sabe o que está no texto; o que "todo mundo sabe" na sua área precisa estar no agente ou no contexto pessoal (nível 2).
2. **Diga o que fazer na dúvida, não só o caminho esperado.** Sem instrução, o modelo preenche a lacuna com uma suposição plausível — é daí que vem o prazo inventado.
3. **Dê o formato da saída exato e um exemplo.** É o que mais varia de um modelo para outro, e um exemplo segura a forma melhor do que uma descrição.
4. **Nenhum nome de ferramenta no texto.** "Os e-mails recebidos", não o nome do conector; "os documentos anexados", não o caminho num serviço de arquivos. É o que deixa o mesmo texto rodar em qualquer ferramenta e só mudar quando a tarefa muda.
5. **Nenhum dado pessoal no agente.** O agente descreve o trabalho; quem você é fica no contexto pessoal, e os dados de cada execução chegam como entrada.
6. **Mantenha curto.** Cada linha é lida em toda execução. Corte o que o modelo faria certo sem ela — o mesmo teste de [practices/ia-harness.md](practices/ia-harness.md), Seção *Harness e economia de contexto*.

Para testar e melhorar:

1. **Separe de três a cinco entradas reais**, com pelo menos uma difícil (e-mail ambíguo, documento longo) e uma que o agente deve ignorar. Anonimize nomes e dados pessoais antes de guardá-las.
2. **Escreva antes o que cada saída precisa ter**, em critérios verificáveis — "lista o prazo de sexta", "não inclui a newsletter" —, nunca "ficar bom". Critério escrito depois de ver a saída tende a aceitar o que saiu.
3. **Ajuste o texto e rode de novo todos os casos**, não só o que falhou: a correção de um caso costuma quebrar outro.
4. **Rode em pelo menos duas ferramentas** antes de subir de nível. Diferença de resultado entre elas quase sempre aponta uma instrução ambígua.

Os casos de teste são os sensores do agente: sem eles não há como saber se uma mudança no texto, no modelo ou na ferramenta piorou o resultado. Rode-os de novo sempre que um dos três mudar. Eles ficam junto do agente, no formato de [templates/casos-de-teste.md](templates/casos-de-teste.md).

## 5. Nível 2 — assistente com contexto

O nível 2 elimina o trabalho de colar o agente a cada conversa: o texto fica salvo nas instruções persistentes de um projeto, assistente personalizado ou espaço de trabalho. Toda ferramenta de chat de IA tem algum lugar assim, cada uma com um nome; o passo a passo de cada ferramenta fica registrado no repositório de agentes, não aqui, porque muda com frequência.

O que vai nas instruções, nesta ordem:

1. **As práticas gerais de trabalho com IA:** o bloco de [templates/instrucoes-chat.md](templates/instrucoes-chat.md), como está.
2. **O contexto pessoal:** papel e área de atuação, prioridades, como prefere as respostas, siglas e termos da sua área. Escrito uma vez, num arquivo do repositório ([templates/contexto-pessoal.md](templates/contexto-pessoal.md)), e reaproveitado por todos os agentes.
3. **O agente:** o corpo do `SKILL.md`. Um projeto ou assistente por agente mantém as instruções curtas e evita que um agente siga as regras de outro.

Regras:

1. **A fonte é o repositório, não a ferramenta.** Para mudar o agente, edite o arquivo e cole de novo. Editar direto na ferramenta cria uma segunda versão, que se perde na próxima troca de ferramenta.
2. **Nada de segredo ou dado sensível nas instruções** — senhas, números de documentos, saúde, finanças, dados de outras pessoas. As instruções ficam guardadas na ferramenta e são enviadas em toda conversa.
3. **Contexto da empresa fica na ferramenta da empresa.** O contexto pessoal pode ir para a ferramenta da empresa; o contexto e os dados da empresa não vão para ferramentas pessoais.
4. **Rode os casos de teste de novo depois de montar o assistente.** O contexto muda o comportamento: uma preferência por "respostas curtas" pode cortar justamente a tabela que o agente deveria produzir.
5. **Material de apoio** (glossário, modelo de relatório) vai para a pasta `references/` da Skill e é anexado ao projeto quando a ferramenta permite. Se não permitir, o essencial entra no próprio texto do agente.

## 6. Pedidos prontos

Ajuste o que está entre `<>`. Os pedidos supõem um repositório de agentes com este conjunto em `docs/guide/` ([templates/repositorio-agentes.md](templates/repositorio-agentes.md)); fora dele, troque o caminho pelo endereço do conjunto ou cole o arquivo citado.

Criar o repositório de agentes:

```text
Crie um repositório de agentes <pessoal | da empresa X> nesta pasta, seguindo
templates/repositorio-agentes.md do conjunto em <endereço do conjunto>, com o
conjunto como submódulo em docs/guide. Ainda sem nenhum agente.
```

Criar um agente (nível 1):

```text
Quero um agente que <faça X>. Siga docs/guide/agentes-pessoais.md (Seção
"Nível 1 — prompt reutilizável") e a Seção "Esqueleto de agente" de
docs/guide/templates/skill.md. Antes de escrever, pergunte o que faltar sobre
entrada, saída e regras. Crie também evals/casos.md pelo
docs/guide/templates/casos-de-teste.md, com os critérios, sem rodar nada.
```

Rodar um caso de teste — numa conversa nova, na ferramenta que você quer conferir, sem mais nada antes:

```text
<corpo do SKILL.md do agente>

Entrada:
<entrada do caso>
```

Avaliar as saídas:

```text
Avalie as saídas abaixo contra os critérios de .agents/skills/<agente>/evals/casos.md.
Para cada caso, diga se passou e, se falhou, que critério falhou e que
mudança no texto do agente corrigiria, sem quebrar os outros casos. Registre
a rodada na tabela de execuções (ferramenta: <...>, modelo: <...>).
<saídas, identificadas pelo caso>
```

Subir um agente de nível:

```text
Quero levar o agente <nome> ao nível <n>. Siga docs/guide/agentes-pessoais.md
e docs/guide/agentes-ferramentas.md. Liste o que muda no SKILL.md, as
capacidades e permissões a configurar e os casos de teste novos; não
configure nada na ferramenta.
```

Criar a ficha de uma automação:

```text
Quero que o agente <nome> rode <quando>, entregando <o quê> em <onde>. Crie a
ficha em automacoes/ pelo docs/guide/templates/automacao.md e aponte o que, na
Seção "Nível 4 — automação" de docs/guide/agentes-ferramentas.md, a
automação ainda não atende.
```

Migrar para uma ferramenta nova:

```text
Vou passar a usar <ferramenta>. Siga docs/guide/agentes-ferramentas.md (Seção
"Portabilidade e migração"): confira na documentação oficial de <ferramenta>
o suporte a Skills, MCP, instruções persistentes e agendamento, registre em
ferramentas.md e monte o plano de migração por agente.
```

## 7. Checklist

- [ ] O agente segue [templates/skill.md](templates/skill.md), Seção *Esqueleto de agente*, sem nome de ferramenta, segredo ou dado pessoal no texto.
- [ ] Os casos de teste foram escritos antes do uso, com critérios verificáveis e entradas anonimizadas, e passam em pelo menos duas ferramentas.
- [ ] O agente subiu um nível de cada vez, com os casos passando a cada subida.
- [ ] Nível 3 ou mais: capacidades declaradas, somente leitura por padrão e ação externa com aprovação configurada na ferramenta ([agentes-ferramentas.md](agentes-ferramentas.md), Seção *Nível 3 — agente com ferramentas*).
- [ ] Nível 4: ficha em `automacoes/`, saída revisável e o caminho para desligar descrito.
- [ ] O `ferramentas.md` do repositório está atualizado, com a data da conferência.
- [ ] As seções *Fontes* deste arquivo e de [agentes-ferramentas.md](agentes-ferramentas.md) foram conferidas há menos de seis meses; se não, confira antes de confiar nelas.

## Fontes

Conferidas em 2026-10-12. Afirmações sobre padrões e suporte das ferramentas mudam: confira de novo antes de confiar nelas depois de alguns meses.

- Agent Skills — especificação, formato aberto criado pela Anthropic e lista de ferramentas compatíveis de vários fornecedores: <https://agentskills.io/specification> e <https://agentskills.io>.
- Model Context Protocol — protocolo aberto para ligar aplicações de IA a sistemas externos, suportado por assistentes de chat e ferramentas de desenvolvimento de vários fornecedores; mantido na Agentic AI Foundation, da Linux Foundation: <https://modelcontextprotocol.io/docs/getting-started/intro> e <https://aaif.io>.
- `AGENTS.md` — formato aberto de instruções para agentes de código, mantido na Agentic AI Foundation, com a lista de ferramentas que o leem: <https://agents.md>.
