# Template: `docs/workflow.md`

**Quando usar:** no dia zero, antes do `AGENTS.md`, que aponta para ele.

**Papel:** dizer como as regras de [practices/engenharia.md](../practices/engenharia.md), Seção *Workflow de revisão*, se realizam **neste** projeto — VCS, remoto, nomes reais das branches, cenário vigente, CI e exceções. As regras em si não são repetidas aqui: o domínio é o dono delas, e uma cópia em cada projeto divergiria na primeira alteração.

**Convenções:** VCS ou remoto ainda não escolhidos entram como `<a definir>`. Projeto em outro VCS registra aqui os comandos equivalentes aos do domínio. Seção sem conteúdo é omitida.

```markdown
# Workflow

Segue `docs/guide/practices/engenharia.md`, Seção *Workflow de revisão*.
Este arquivo registra só o que é específico deste projeto.

## Repositório
- VCS: <Git>
- Remoto: <plataforma e URL, ou "nenhum">
- Branch principal: `<main>`
- Branches de integração: <`develop`, `release/*`, ou "nenhuma">
- Cenário vigente: <1 — local | 2 — PR/MR em <plataforma>>
- CI: <o que roda e quando, ou "nenhum">

## Base de cada tipo de tarefa
| Tarefa | Branch base | Destino |
| --- | --- | --- |
| funcionalidade, correção | `<develop>` | `<develop>` |
| correção urgente em versão liberada | `<release/x.y>` | `<release/x.y>` e `<develop>` |

## Liberação de versão
<Como se cria tag, onde se arquiva o binário, quem aprova. Omita até existir.>

## Exceções
<Desvios das regras do domínio neste projeto, com motivo. Ex.: "commits só de
documentação podem ir direto para `main` quando feitos por pessoa". Omita se não houver.>
```

## Exemplo preenchido (ilustrativo)

```markdown
# Workflow

Segue `docs/guide/practices/engenharia.md`, Seção *Workflow de revisão*.
Este arquivo registra só o que é específico deste projeto.

## Repositório
- VCS: Git
- Remoto: GitHub, repositório privado da empresa
- Branch principal: `main` (só recebe merge de `develop` na liberação)
- Branches de integração: `develop`
- Cenário vigente: 1 — local; PR no GitHub ainda não é usado
- CI: nenhum

## Base de cada tipo de tarefa
| Tarefa | Branch base | Destino |
| --- | --- | --- |
| funcionalidade, correção | `develop` | `develop` |
| correção urgente em campo | tag da versão liberada | nova tag e `develop` |

## Liberação de versão
Tag `vX.Y.Z` em `main`; o `.hex` e o `.map` do build de liberação são
arquivados na pasta de liberações do servidor da engenharia.
```
