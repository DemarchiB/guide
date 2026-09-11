# Template: `ARCHITECTURE.md`

**Quando usar:** no dia zero, primeiro documento depois de montar o conjunto — é o que dá vocabulário (componentes, limites, dependências) a todos os outros.

**Papel:** mapa arquitetural de alto nível — componentes, dependências, fluxos, interfaces e limites externos, restrições a preservar, pontos não determinados. **Único no projeto**: o que ele tem de mais valioso é o que existe *entre* as partes, e um mapa por pasta descreve bem cada pedaço enquanto ninguém descreve as interfaces. Não descreve funções nem arquivos um a um; detalhe que não cabe no mapa vira design-doc ou referência, com link daqui. Não é carregado em toda sessão — é lido quando a tarefa atravessa componentes ou mexe em interface. Em projeto de um componente só (uma biblioteca, por exemplo) ele é curto: visão geral, dependências externas e restrições a preservar; seções sem conteúdo são omitidas. Existe mesmo assim para que o lugar das restrições arquiteturais seja o mesmo em todo projeto.

**Convenções:** a tabela de componentes lista o que **este projeto implementa**, ainda que seja pouco; serviço de terceiros, plataforma gerenciada ou API externa entram em "Dependências e interfaces externas", com o limite do que não deve vazar para o resto do sistema — projeto que delega quase tudo a um serviço externo terá poucas linhas na primeira tabela e várias na segunda, e isso é a descrição correta, não uma lacuna. O que ainda não foi decidido vai em "Pontos não determinados", nunca em suposição. Descrever estrutura que ainda não existe é legítimo desde que rotulada como planejada — o proibido é apresentar intenção como fato consumado.

```markdown
# Arquitetura

## Visão geral
<O sistema em 3-5 linhas: o que faz, onde roda, quais são suas fronteiras.>

## Domínios e componentes
| Componente | Responsabilidade | Caminho |
| --- | --- | --- |
| <nome> | <responsabilidade única> | `<caminho>` |

## Fluxos principais
<1-3 fluxos ponta a ponta, em texto ou diagrama simples.>

## Dependências e interfaces externas
| Dependência | Uso | Limite |
| --- | --- | --- |
| <nome> | <para que serve> | <o que não deve vazar para o resto do sistema> |

## Restrições a preservar
- <compatibilidade, protocolo, limite de memória/timing, norma aplicável>

## Pontos não determinados
- <incerteza registrada como incerteza, nunca preenchida por suposição>
```

## Exemplo preenchido (ilustrativo)

```markdown
# Arquitetura

## Visão geral
Firmware do módulo de comunicação, rodando sobre um RTOS em microcontrolador
de 32 bits. Recebe comandos do controlador principal por UART, expõe a mesma
função por Ethernet, e não guarda estado persistente além da configuração de
rede. Não implementa regra de negócio: traduz e transporta.

## Domínios e componentes
| Componente | Responsabilidade | Caminho |
| --- | --- | --- |
| Drivers | Acesso a periférico, sem lógica de protocolo | `src/drivers/` |
| Rede | Pilha TCP/IP e adaptação do protocolo serial | `src/net/` |
| Aplicação | Máquina de estados, arbitragem entre canais | `src/app/` |

## Fluxos principais
Recepção serial: ISR da UART → fila → task de protocolo → máquina de estados
→ resposta pela mesma via.
Recepção por rede: pilha TCP/IP → adaptador → a mesma máquina de estados, que
não sabe por qual canal o comando chegou.

## Dependências e interfaces externas
| Dependência | Uso | Limite |
| --- | --- | --- |
| RTOS | Escalonamento e filas | APIs de heap só na inicialização, em `src/app/init.c` |
| Pilha TCP/IP | Ethernet | Acessível apenas por `src/net/`; nenhum outro módulo inclui seus headers |

## Restrições a preservar
- Compatibilidade do protocolo serial com a versão 1.4 do controlador.
- Sem alocação dinâmica depois da inicialização.
- Uma única máquina de estados para os dois canais — duplicá-la por canal já
  foi tentado e descartado (ver `docs/decisions/`).

## Pontos não determinados
- Estratégia de atualização remota de firmware: `<a definir>` — nenhuma
  decisão registrada até hoje.
- Limite de conexões simultâneas por Ethernet: `<a verificar: valor atual vem
  da configuração da pilha, não foi medido em campo>`.
```
