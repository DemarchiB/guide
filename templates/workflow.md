# Template: `docs/workflow.md`

**Quando usar:** quando o fluxo deixar de caber na seção *Fluxo* do `AGENTS.md` — plataforma de PR/MR em uso, CI, processo de liberação, mais de uma pessoa, exceções a registrar. **Não** nasce no dia zero: num projeto solo sem remoto, o `AGENTS.md` é o fluxo inteiro, e um arquivo próprio só acrescenta um lugar a manter.

**Papel:** dizer como as regras de [practices/git.md](../practices/git.md), Seção *Branch e revisão*, se realizam **neste** projeto — VCS, remoto, nomes reais das branches, forma de entrega, CI e exceções. As regras em si não são repetidas aqui: o domínio é o dono delas, e uma cópia em cada projeto divergiria na primeira alteração.

**Convenções:** o que já está na seção *Fluxo* do `AGENTS.md` não é repetido aqui — branch base e modo de trabalho do agente moram lá. VCS ou remoto ainda não escolhidos entram como `<a definir>`. Projeto em outro VCS registra aqui os comandos equivalentes aos do domínio. Seção sem conteúdo é omitida.

```markdown
# Workflow

Segue `docs/guide/practices/git.md`, Seção *Branch e revisão*.
Este arquivo registra só o que é específico deste projeto.

## Repositório
- VCS: <Git>
- Remoto: <plataforma e URL, ou "nenhum">
- Branch principal: `<main>`
- Branches de integração: <`develop`, `release/*`, ou "nenhuma">
- Entrega: <local, revisão pelo diff da branch | PR/MR em <plataforma>>
- CI: <o que roda e quando, ou "nenhum">

## Base de cada tipo de tarefa
| Tarefa | Branch base | Destino |
| --- | --- | --- |
| funcionalidade, correção | `<develop>` | `<develop>` |
| correção urgente em versão liberada | `<release/x.y>` | `<release/x.y>` e `<develop>` |

## Trabalho de agente
<O branch base e o modo local estão no AGENTS.md; que agente assíncrono entrega
por PR/MR é regra do conjunto. Aqui vai só o que depende deste remoto.>
- Agente assíncrono em uso: <sim | não>
- Proteção do tronco: <revisão obrigatória e push direto bloqueado no servidor | nenhuma>
- Comandos negados na configuração da ferramenta: <onde está esse arquivo, ou "nenhum ainda">

## Liberação de versão
<Como se cria tag, onde se arquiva o binário, quem aprova. Omita até existir.>

## Exceções
<Desvios das regras do domínio neste projeto, com motivo. Ex.: "commits só de
documentação podem ir direto para `main` quando feitos por pessoa". Omita se não houver.>
```

## Exemplo preenchido (ilustrativo)

```markdown
# Workflow

Segue `docs/guide/practices/git.md`, Seção *Branch e revisão*.
Este arquivo registra só o que é específico deste projeto.

## Repositório
- VCS: Git
- Remoto: GitHub, repositório privado da empresa
- Branch principal: `main` (só recebe merge de `develop` na liberação)
- Branches de integração: `develop`
- Entrega: local, revisão pelo diff da branch; PR no GitHub ainda não é usado
- CI: nenhum

## Base de cada tipo de tarefa
| Tarefa | Branch base | Destino |
| --- | --- | --- |
| funcionalidade, correção | `develop` | `develop` |
| correção urgente em campo | tag da versão liberada | nova tag e `develop` |

## Trabalho de agente
- Agente assíncrono em uso: não (sem PR no GitHub ainda)
- Proteção do tronco: nenhuma — `develop` e `main` dependem de disciplina, não de mecanismo
- Comandos negados na configuração da ferramenta: `.agents/permissoes.json`

## Liberação de versão
Tag `vX.Y.Z` em `main`; o `.hex` e o `.map` do build de liberação são
arquivados na pasta de liberações do servidor da engenharia.
```
