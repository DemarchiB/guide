# Template: `AGENTS.md`

**Quando usar:** no dia zero, depois de `ARCHITECTURE.md` (`adocao.md`). Aninhado, quando uma pasta tiver convenção própria.

**Papel:** índice operacional carregado em **toda** sessão de agente. Contém só o que o agente erraria sem saber: comandos reais, convenções que fogem do padrão, restrições críticas, desvios deste conjunto e onde está o que não é óbvio. Não é visão geral do repositório (o agente lê a árvore), não é cópia de `ARCHITECTURE.md` e não contém instrução genérica ("escreva código limpo") — tudo isso custa contexto em toda sessão sem melhorar o resultado ([practices/ia-harness.md](../practices/ia-harness.md), Seção *Harness e economia de contexto*).

**Convenções:**

- **Curto, porque cada linha é paga em toda sessão.** O teste de cada linha: *uma tarefa típica deste projeto sairia errada sem ela?* Conteúdo que só algumas tarefas usam vai para um `AGENTS.md` aninhado, uma Skill ou um documento em `docs/` com link — é o critério, e não uma contagem de linhas, que decide.
- **Somente comandos verificados.** Comando que ninguém rodou entra como `<a verificar>`, nunca como oficial.
- **Sensor que não existe aparece como ausente**, não é omitido: a linha `| Testes | <a definir: sem suíte> | — |` diz ao agente que ele não tem como se verificar sozinho, e é o que impede que ele declare "testado". ([practices/testes.md](../practices/testes.md), Seção *Conjunto mínimo de sensores*)
- **Seção sem conteúdo é omitida**, exceto *Comandos* e *Fluxo*, que existem desde o dia zero, mesmo com marcações. *Fluxo* fica aqui, e não num arquivo à parte, porque o agente precisa dela em toda tarefa. Ela tem só os dois fatos que ele não tem como deduzir — o branch base e se ele commita —; o resto do fluxo é regra do conjunto ([practices/git.md](../practices/git.md)), e repeti-la aqui custa contexto em toda sessão e diverge na primeira alteração.
- **Aninhamento:** o `AGENTS.md` de uma subárvore (componente, pasta com ferramental próprio) descreve só aquela pasta e nunca repete regra do raiz; o raiz aponta para ele no *Onde fica o quê*. As ferramentas carregam o mais próximo do arquivo alterado; ferramenta que não faz isso recebe o mesmo adaptador do raiz em cada pasta.
- **Pastas que o agente não deve abrir** (saídas de build, binários) se resolvem no `.gitignore` ou na configuração de permissões da ferramenta, não com texto aqui.
- Ferramenta que não lê `AGENTS.md` recebe um adaptador, nunca uma cópia ([practices/ia-harness.md](../practices/ia-harness.md), Seção *Adaptadores de ferramenta*).

```markdown
# AGENTS.md

<2-3 linhas: o que o projeto é e quando uma contribuição está pronta.>

## Convenções
Segue `docs/guide/` (<submódulo | cópia do commit `<hash>`>). No início de
toda tarefa, leia `docs/guide/PROJECT_GUIDE.md` — ele diz o que mais ler.

- Domínios aplicáveis: <engenharia, ia, ...>
- Desvios do guia: <regra — motivo — ADR, ou omita a linha>
- Idioma: documentação em <pt-BR>; identificadores e comentários em <...>; commits em <...>.
- <Convenção deste projeto que foge do padrão da linguagem ou ferramenta.>

## Fluxo
- Branch base das tarefas: `<develop>`.
- O agente <não commita: deixa as alterações na árvore de trabalho e entrega o resumo | commita cada incremento verificado na própria branch>.
- <Desvio da nomenclatura de branch do conjunto, ou ponteiro para `docs/workflow.md`; omita as duas linhas se não houver.>

## Comandos
| Ação | Comando | Diretório |
| --- | --- | --- |
| Configurar | `<comando>` | `<dir>` |
| Build | `<comando>` | `<dir>` |
| Testes | `<comando>` | `<dir>` |
| Lint / análise | `<comando>` | `<dir>` |
| Links da documentação | `python docs/guide/tools/verificar.py` | raiz |

## Onde fica o quê
<Só o que a árvore não deixa óbvio, e os AGENTS.md aninhados.>
- `<caminho>` — <o que é, quando ler>

## Restrições críticas
- <limite que nunca pode ser violado: interface pública, memória, protocolo, norma>

## Ao terminar
1. Rodar os comandos de build, testes e análise que se aplicam à mudança.
2. Atualizar a documentação afetada, uma vez, com o comportamento já verificado.
3. Entregar o resumo da mudança no formato de
   `docs/guide/practices/engenharia.md`, Seção *Processo de uma mudança*.
```

## Exemplo preenchido (ilustrativo)

Projeto fictício de firmware, o mesmo dos demais exemplos. Repare na pendência marcada na tabela de comandos e na ausência de visão geral do repositório.

```markdown
# AGENTS.md

Firmware do módulo de comunicação: expõe UART e Ethernet ao controlador
principal. Uma contribuição está pronta quando o comportamento novo tem spec,
os testes em host passam e o orçamento de RAM não piora.

## Convenções
Segue `docs/guide/` (submódulo). No início de toda tarefa, leia
`docs/guide/PROJECT_GUIDE.md` — ele diz o que mais ler.

- Domínios aplicáveis: engenharia, ia, c-embarcado, c-build-e-analise, firmware.
- Desvios do guia: alocação única do pool da pilha TCP/IP na inicialização — ADR-0002.
- Idioma: documentação, identificadores e commits em pt-BR.
- Funções públicas no formato `Modulo_acao` (`Uart_enviar`); tipos em PascalCase.

## Fluxo
- Branch base das tarefas: `develop`.
- O agente não commita: deixa as alterações na árvore de trabalho e entrega o
  resumo.

## Comandos
| Ação | Comando | Diretório |
| --- | --- | --- |
| Configurar | `cmake --preset alvo-debug` | raiz |
| Build | `cmake --build --preset alvo-debug` | raiz |
| Testes em host | `cmake --preset host && ctest --preset host` | raiz |
| Análise estática | `cmake --build --preset alvo-debug --target analise` | raiz |
| Uso de memória | `cmake --build --preset alvo-debug --target tamanho` | raiz |
| Links da documentação | `python docs/guide/tools/verificar.py` | raiz |
| Varredura de segredos | `<a definir: nenhuma ferramenta adotada>` | — |

## Onde fica o quê
- `src/net/AGENTS.md` — regras da pilha TCP/IP; ler antes de mexer em `src/net/`.
- `third_party/` — código de fornecedor, fora do escopo de análise; não editar.

## Restrições críticas
- RAM livre não pode cair abaixo de 4 KB (alvo `tamanho`).
- Protocolo serial compatível com a versão 1.4 do controlador.

## Ao terminar
1. Rodar build, testes em host e análise estática.
2. Atualizar a documentação afetada, uma vez, com o comportamento já verificado.
3. Entregar o resumo da mudança no formato de
   `docs/guide/practices/engenharia.md`, Seção *Processo de uma mudança*.
```
