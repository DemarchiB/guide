# Template: repositório de agentes

**Quando criar:** ao escrever o primeiro agente de um contexto de uso ([agentes-pessoais.md](../agentes-pessoais.md)).

**Papel:** guarda tudo o que é texto dos agentes de um contexto — os agentes, o contexto pessoal, os casos de teste, as fichas de automação e o registro de como cada ferramenta foi configurada. É a fonte: as ferramentas de IA recebem cópias, e a troca de ferramenta parte daqui ([agentes-ferramentas.md](../agentes-ferramentas.md), Seção *Portabilidade e migração*).

**Quantos repositórios:**

- **Um por contexto de uso:** um pessoal e, se for o caso, um por empresa, guardado onde a política dela determinar. Contexto e dados de um não vão para o outro ([agentes-ferramentas.md](../agentes-ferramentas.md), Seção *Pessoal e empresa*). Vários agentes do mesmo contexto dividem o mesmo contexto pessoal, os mesmos testes de ferramenta e uma única cópia do conjunto.
- **Um agente ganha repositório próprio quando deixa de ser só texto:** passa a ter código (servidor MCP próprio, automação programada, scripts além de apoio pontual), precisa ser compartilhado com outras pessoas ou ter versão própria. Aí ele é um projeto e adota o conjunto por inteiro ([adocao.md](../adocao.md)).

**Convenções:**

- **Só existe o que tem conteúdo** ([estrutura.md](../estrutura.md), Seção *Árvore*): `automacoes/` nasce com a primeira automação; `references/` e `evals/entradas/`, quando um agente precisar.
- **Nunca entra:** senha, token ou chave — no `ferramentas.md` registra-se o nome da credencial, nunca o valor ([practices/engenharia.md](../practices/engenharia.md), Seção *Segredos e dados sensíveis*); e-mails, documentos e exportações reais; dado de outras pessoas sem anonimizar; dado da empresa no repositório pessoal.
- **Repositório remoto privado.** Mesmo sem segredos, contexto e casos de teste dizem muito sobre o seu trabalho.
- O `AGENTS.md` daqui é uma versão reduzida de [agents.md](agents.md): sem código, não há build, testes automatizados nem arquitetura a descrever.

## Árvore

```text
<agentes-contexto>/
├── README.md               o que é o repositório; lista de agentes
├── AGENTS.md               instruções para a IA que mexe neste repositório
├── ferramentas.md          como cada ferramenta foi configurada, com data
├── contexto/
│   └── sobre-mim.md        contexto pessoal (templates/contexto-pessoal.md)
├── .agents/skills/<agente>/
│   ├── SKILL.md            o agente (templates/skill.md, Esqueleto de agente)
│   ├── references/         material de apoio, se houver
│   └── evals/
│       ├── casos.md        casos de teste (templates/casos-de-teste.md)
│       └── entradas/       entradas longas, anonimizadas
├── automacoes/<nome>.md    fichas de automação (templates/automacao.md)
└── docs/guide/             este conjunto, como submódulo
```

## `README.md`

```markdown
# Agentes <pessoais | da empresa X>

Agentes de IA portáveis entre ferramentas, no método de
`docs/guide/agentes-pessoais.md`.

| Agente | Faz | Nível | Roda em |
| --- | --- | --- | --- |
| [triagem-email](.agents/skills/triagem-email/SKILL.md) | lista o que exige ação nos e-mails | 3 | <ferramentas, ver ferramentas.md> |

## Usar um agente
- Em ferramenta que suporta Skills: instale a pasta do agente (ferramentas.md diz como).
- Nas outras: cole nas instruções persistentes de um projeto ou assistente,
  nesta ordem, o bloco de `docs/guide/templates/instrucoes-chat.md`,
  `contexto/sobre-mim.md` e o corpo do `SKILL.md`.

## Atualizar o guia
`git submodule update --remote docs/guide`, depois rodar o verificador.
```

## `AGENTS.md`

```markdown
# AGENTS.md — agentes <pessoais | da empresa X>

Agentes de IA portáveis. Um agente está pronto quando segue o esqueleto de
agente e tem os casos de teste passando em pelo menos duas ferramentas.

## Convenções
Segue `docs/guide/` (submódulo). Para criar ou alterar um agente, leia
`docs/guide/agentes-pessoais.md`; para ferramentas, automação e migração,
`docs/guide/agentes-ferramentas.md`.

- Agente: `.agents/skills/<nome>/SKILL.md`, Seção "Esqueleto de agente" de
  `docs/guide/templates/skill.md`. Casos de teste em `evals/casos.md`.
- Nenhum nome de ferramenta, segredo ou dado pessoal no texto dos agentes.
- Idioma: <pt-BR>.

## Fluxo
- Branch base: `main`.
- O agente <não commita: altera e relata | commita cada mudança verificada>.

## Comandos
| Ação | Comando | Diretório |
| --- | --- | --- |
| Verificação | `python docs/guide/tools/verificar.py` | raiz |

## Ao terminar
1. Rodar a verificação.
2. Agente alterado: dizer quais casos de teste precisam rodar de novo.
3. Configuração de ferramenta alterada: atualizar `ferramentas.md` com a data.
```

## `ferramentas.md`

```markdown
# Ferramentas

Como cada ferramenta foi configurada. Passos de ferramenta mudam: confira
na documentação oficial e atualize a data sempre que mexer.

## <Ferramenta>
- **Conferido em:** AAAA-MM-DD
- **Suporte:** Skills <sim | não | parcial>; MCP <sim | não>; instruções
  persistentes <sim | não>; agendamento <sim | não>. Fonte: <link>.
- **Onde ficam as instruções persistentes:** <caminho nos menus>
- **Agentes:** <agente — nível — como está instalado (Skill | texto colado no projeto X)>
- **Conexões:** <capacidade — conector — permissão concedida — credencial (nome, nunca o valor)>
- **Diferenças observadas:** <o que os casos de teste mostraram nesta ferramenta>
```
