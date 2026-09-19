# Estrutura documental do projeto

Cobre onde cada informação mora num projeto que adotou o conjunto: a árvore de arquivos, o papel de cada documento, a regra de decisão para registrar algo e o mínimo exigido das áreas sem template. Como manter esses documentos verdadeiros ao longo do tempo é assunto de [manutencao.md](manutencao.md).

**Leia este arquivo quando:** for decidir onde registrar uma informação, criar, mover ou remover um documento, ou reorganizar a estrutura documental.

## 1. Árvore

```text
<projeto>/
├── README.md               obrigatório — apresentação para pessoas
├── AGENTS.md               obrigatório — índice operacional, carregado em toda sessão de agente
├── ARCHITECTURE.md         obrigatório — mapa arquitetural, único no projeto
├── .agents/
│   └── skills/<nome>/SKILL.md   workflows reutilizáveis (padrão Agent Skills)
├── docs/
│   ├── guide/              este conjunto (submódulo) — nunca editado aqui
│   ├── workflow.md         fluxo de revisão, quando não couber na seção Fluxo do AGENTS.md
│   ├── specs/              requisitos (EARS)
│   ├── decisions/          ADRs
│   ├── design-docs/        designs informais e máquinas de estado
│   ├── exec-plans/         planos de trabalho com várias etapas
│   ├── references/         o que o projeto sabe sobre dependências externas
│   └── generated/          artefatos produzidos por automação, se versionados
└── <código, testes, configuração>
```

**Só existe o que tem conteúdo.** Os três obrigatórios nascem no dia zero (`adocao.md`); toda outra pasta e arquivo nasce com o primeiro conteúdo real. Pasta vazia "para o futuro" é o antipadrão da árvore preenchida: gasta atenção de quem lê e sugere que falta algo.

Arquivo ou pasta exigido por uma ferramenta específica de IA não faz parte da estrutura: quando existe, é adaptador do `AGENTS.md` ou de `.agents/skills/`, criado só para ferramenta em uso — regra em [practices/ia-harness.md](practices/ia-harness.md), Seção *Adaptadores de ferramenta*.

## 2. Catálogo de documentos

A definição completa do papel de cada documento — o que ele é, o que não é, e quando nasce — está no template. Esta tabela é o resumo de uma linha.

| Local | Papel | Template |
| --- | --- | --- |
| `README.md` | Apresentação: propósito, pré-requisitos, primeiro uso. | `templates/readme.md` |
| `AGENTS.md` | Índice operacional curto: comandos, convenções não óbvias, restrições. Pode ser aninhado por subárvore. | `templates/agents.md` |
| `ARCHITECTURE.md` | Componentes, limites, interfaces e dependências. **Único** — nunca aninhado. | `templates/architecture.md` |
| `docs/workflow.md` | Fluxo de revisão deste projeto, quando não couber na seção *Fluxo* do `AGENTS.md`: liberação, CI, PR/MR, exceções. | `templates/workflow.md` |
| `docs/specs/<nome>.md` | Requisitos de uma funcionalidade, em EARS. | `templates/spec.md` |
| `docs/decisions/ADR-NNNN-<slug>.md` | Decisão de arquitetura e alternativas descartadas. | `templates/adr.md` |
| `docs/references/<dependência>.md` | Conhecimento do projeto sobre uma dependência externa. | `templates/referencia.md` |
| `docs/design-docs/fsm-<nome>.md` | Máquina de estado. | `templates/fsm.md` |
| `.agents/skills/<nome>/SKILL.md` | Workflow especializado, carregado sob demanda. | `templates/skill.md` |
| `<modulo>.h` + `<modulo>.c` | Módulo C com estado. | `templates/modulo-c.md` |

## 3. Onde registrar uma informação

Siga a primeira linha que se aplica.

| A informação... | Vai para |
| --- | --- |
| é detalhe local que o código já deixa claro | o próprio código — não documente |
| é convenção que só vale dentro de uma pasta ou componente | `AGENTS.md` aninhado naquela pasta (o da raiz aponta para ele) |
| é necessária em quase toda tarefa e o agente não a descobriria sozinho | `AGENTS.md` da raiz, em uma linha ou um link |
| descreve componentes, limites ou o que existe **entre** as partes | `ARCHITECTURE.md` |
| é comportamento esperado de uma funcionalidade | `docs/specs/` |
| é comportamento que pode ser verificado automaticamente | um teste, não um documento ([practices/testes.md](practices/testes.md)) |
| é decisão que alguém vai questionar antes de mudar algo relacionado | `docs/decisions/` (critérios em `templates/adr.md`) |
| é design ou decisão que precisa de explicação, sem a formalidade de um ADR | `docs/design-docs/` |
| é um plano de trabalho com etapas, riscos ou migração que não cabe nas tarefas de uma spec | `docs/exec-plans/` |
| é procedimento recorrente, difícil de acertar sem instruções | Skill em `.agents/skills/` |
| explica uma dependência externa no contexto do projeto | `docs/references/` |
| é produzida por automação | `docs/generated/`, se precisar ser versionada |
| é o branch base, ou como o trabalho do agente é entregue | a seção *Fluxo* do `AGENTS.md` — é preciso em toda tarefa |
| é o resto do fluxo de revisão: liberação, CI, PR/MR, exceções | `docs/workflow.md`, quando houver o que escrever |
| é desvio de uma regra deste conjunto | uma linha no `AGENTS.md` e, se não for trivial, ADR |
| é prática geral, válida para vários projetos | este conjunto — pelo procedimento de `manutencao-do-conjunto.md`, nunca editando a cópia do projeto |

Se nenhuma linha tiver conteúdo suficiente para justificar um arquivo, não crie o arquivo.

## 4. Áreas sem template

Estas áreas têm formato livre. O que se exige é o mínimo abaixo; um template só nasce quando o segundo documento real da área mostrar a forma repetida.

Specs, ADRs, design-docs e planos começam com `Status` e `Data` da última atualização — é o que permite distinguir o vigente do histórico sem abrir o VCS.

- **`docs/design-docs/`** — Status `rascunho | vigente | obsoleto`. Mínimo: propósito, a alternativa descartada e por quê. Máquina de estado usa `templates/fsm.md`.
- **`docs/exec-plans/`** — Status `ativo | concluído | abandonado`. Mínimo: objetivo, etapas em ordem com o risco de cada uma, critério de conclusão. O plano muda de status, não de pasta: mover arquivo quebra link. Plano concluído sem valor histórico pode ser apagado — o VCS guarda.
- **`docs/generated/`** — só artefato produzido automaticamente. Mínimo: fonte, gerador e comando de regeneração identificados no próprio arquivo ou num `README.md` da pasta.

## 5. Nomes

- Arquivos de documentação em kebab-case, sem acento nem espaço: `deteccao-overflow-uart.md`.
- Maiúsculas só nos arquivos de entrada procurados por nome: `README.md`, `AGENTS.md`, `ARCHITECTURE.md`, `SKILL.md`.
- Nome de Skill segue a especificação (`templates/skill.md`): minúsculas, números e hífens.
- Identificadores citados na documentação (estados, eventos, funções) são escritos exatamente como no código.
