# AGENTS.md — conjunto de convenções

**Escopo:** este arquivo só vale para tarefas que **alteram este conjunto**. Num projeto que o adotou ele aparece como `docs/guide/AGENTS.md`; se você está apenas consultando o guia a partir de um projeto, ignore este arquivo e siga o `AGENTS.md` da raiz do projeto.

## Objetivo
Manter um conjunto de convenções, independente de ferramenta de IA, que outros projetos adotam sem alteração. Uma contribuição está pronta quando o verificador passa, cada regra tem um dono só e se justifica como boa prática, e o commit declara o impacto para quem já adotou.

## Convenções
Este repositório segue a si mesmo ([PROJECT_GUIDE.md](PROJECT_GUIDE.md)), com os domínios `engenharia`, `git` e `ia`; `practices/ia-harness.md` é guia de apoio, lido apenas ao mexer em harness, Skills, subagentes ou adaptadores. Não tem `ARCHITECTURE.md` nem `docs/workflow.md` — não há código, e a organização está em `manutencao-do-conjunto.md`, Seção *Que conteúdo entra, e onde*.

- Conteúdo em português (pt-BR); nomes de arquivo em kebab-case sem acento.
- Nenhuma convenção, nome de arquivo ou recurso exclusivo de uma ferramenta de IA entra como regra.

## Comandos
| Ação | Comando | Diretório |
| --- | --- | --- |
| Verificação (links, includes, seções citadas, Skills, duplicação; gitlinks excluídos) | `python tools/verificar.py` | raiz |

Requer Python 3.8+, sem dependências.

## Fluxo
- Branch base: `main`.
- O agente não commita: altera os arquivos e relata.

## Restrições críticas
- Nenhum fato específico de um projeto entra aqui.
- Uma regra tem um dono só (`manutencao-do-conjunto.md`, Seção *Para onde vai um trecho que precisa sair*).
- Antes de escrever uma regra, procure se ela já existe (`grep -ri`) e diga por que ela é boa prática.
- Regra nova entra no arquivo cujo **gatilho de leitura** corresponde a ela, não no arquivo do assunto mais próximo (`manutencao-do-conjunto.md`, Seção *Custo de contexto e divisão de arquivos*).

## Ao terminar
1. Rodar `python tools/verificar.py`.
2. Conferir o checklist de `manutencao-do-conjunto.md`.
3. Entregar o resumo da mudança (`practices/engenharia.md`, Seção *Processo de uma mudança*), com os trailers `Impacto-adocao` propostos para o commit, quando aplicável.
