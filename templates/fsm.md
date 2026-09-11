# Template: máquina de estado (`docs/design-docs/fsm-<nome>.md`)

**Papel:** documentar uma máquina de estado de forma verificável contra o código — a tabela de transição é o contrato.

**Quando documentar uma máquina de estado** — a máquina precisa atender a pelo menos um destes:

- o comportamento não fica evidente lendo o enum de estados e a função de transição — guardas, temporizadores, eventos que só valem em alguns estados;
- controla saída física, comunicação ou qualquer comportamento observável do produto;
- é consultada ou alterada por mais de um módulo (mesmo que o dono seja um só);
- implementa comportamento descrito por um requisito em `docs/specs/`.

**Quando não documentar:** máquina local e trivial, cujo código já é a documentação legível — um documento a mais só criaria uma segunda fonte para divergir.

**Convenções:** um arquivo por máquina; o nome do arquivo, os nomes dos estados e os nomes dos eventos são **os mesmos identificadores usados no código**, sem tradução nem sinônimo — é isso que torna a documentação verificável contra a implementação. A tabela de transição é a fonte da verdade do documento: se o código e a tabela divergirem, um dos dois é defeito, e a divergência não se resolve apagando a linha da tabela. Documento e código mudam na mesma alteração ([practices/firmware.md](../practices/firmware.md), Seção *Máquinas de estado*). Seção sem conteúdo (Invariantes, por exemplo) é omitida; Tabela de transição e Comportamento em falha nunca.

```markdown
# FSM: <nome>

- **Módulo dono:** <arquivo .c que altera o estado>
- **Requisitos atendidos:** <REQ-<PREFIXO>-NNN, ... ou "—">
- **Estado inicial:** <ESTADO>
- **Estado seguro / de falha:** <ESTADO, e como se sai dele>

## Propósito
<O que esta máquina controla, em 2-3 linhas. Por que é uma máquina de
estado e não uma sequência direta.>

## Estados
| Estado | Significado | Saídas / efeito enquanto ativo | Tempo limite |
| --- | --- | --- | --- |
| `<ESTADO>` | <o que significa estar aqui> | <o que o produto faz> | <prazo e destino, ou "—"> |

## Eventos
| Evento | Origem | Dado associado |
| --- | --- | --- |
| `<EVENTO>` | <interrupção, tarefa, temporizador, comando externo> | <payload, ou "—"> |

## Tabela de transição
Todo par estado × evento tem destino. Onde nada acontece, escreva
`— (ignorado)` e o motivo; lacuna não é o mesmo que decisão.

| Estado atual | Evento | Condição | Próximo estado | Ação na transição |
| --- | --- | --- | --- | --- |
| `<ESTADO>` | `<EVENTO>` | <guarda, ou "—"> | `<ESTADO>` | <ação, ou "—"> |

## Invariantes
- <o que é sempre verdade, em qualquer estado — tipicamente sobre saídas
  físicas e recursos.>

## Comportamento em falha
<O que acontece diante de evento inesperado, tempo esgotado, dado
inválido ou reset. Qual estado é alcançado e como o evento é registrado.>

## Verificação
<Como se comprova que a implementação corresponde a esta tabela: teste em
host por par estado × evento, teste em bancada, inspeção. O que ainda não
existe entra como pendência, não como feito.>
```

## Exemplo preenchido (ilustrativo)

```markdown
# FSM: acionamento_saida

- **Módulo dono:** `app/acionamento.c`
- **Requisitos atendidos:** REQ-ACION-001, REQ-ACION-002
- **Estado inicial:** `ACION_DESLIGADO`
- **Estado seguro / de falha:** `ACION_FALHA` — saída desligada; sai apenas por reset.

## Propósito
Controla a saída de potência respeitando um intervalo mínimo de 30 s entre
desligar e religar. É máquina de estado porque a permissão de ligar depende
do que aconteceu antes, não só do comando atual.

## Estados
| Estado | Significado | Saídas / efeito enquanto ativo | Tempo limite |
| --- | --- | --- | --- |
| `ACION_DESLIGADO` | Repouso, apto a ligar | Saída desligada | — |
| `ACION_LIGADO` | Saída acionada | Saída ligada | — |
| `ACION_BLOQUEIO` | Intervalo mínimo após desligar | Saída desligada | 30 s → `ACION_DESLIGADO` |
| `ACION_FALHA` | Sobrecorrente detectada | Saída desligada | — |

## Eventos
| Evento | Origem | Dado associado |
| --- | --- | --- |
| `EV_COMANDO_LIGAR` | Tarefa de comunicação | — |
| `EV_COMANDO_DESLIGAR` | Tarefa de comunicação | — |
| `EV_SOBRECORRENTE` | Interrupção do comparador | corrente medida, em mA |
| `EV_TICK` | Base de tempo, a cada 10 ms | — |

## Tabela de transição
| Estado atual | Evento | Condição | Próximo estado | Ação na transição |
| --- | --- | --- | --- | --- |
| `ACION_DESLIGADO` | `EV_COMANDO_LIGAR` | — | `ACION_LIGADO` | liga saída |
| `ACION_DESLIGADO` | `EV_COMANDO_DESLIGAR` | — | — (ignorado) | já está desligado |
| `ACION_DESLIGADO` | `EV_TICK` | — | — (ignorado) | nada temporizado |
| `ACION_LIGADO` | `EV_COMANDO_LIGAR` | — | — (ignorado) | já está ligado |
| `ACION_LIGADO` | `EV_COMANDO_DESLIGAR` | — | `ACION_BLOQUEIO` | desliga saída, marca instante |
| `ACION_LIGADO` | `EV_TICK` | — | — (ignorado) | sem limite de tempo ligado |
| `ACION_BLOQUEIO` | `EV_COMANDO_LIGAR` | — | — (ignorado) | intervalo mínimo não cumprido |
| `ACION_BLOQUEIO` | `EV_COMANDO_DESLIGAR` | — | — (ignorado) | já está desligado |
| `ACION_BLOQUEIO` | `EV_TICK` | decorrido < 30 s | — (ignorado) | aguarda |
| `ACION_BLOQUEIO` | `EV_TICK` | decorrido ≥ 30 s | `ACION_DESLIGADO` | — |
| qualquer, exceto `ACION_FALHA` | `EV_SOBRECORRENTE` | — | `ACION_FALHA` | desliga saída, persiste código de falha |
| `ACION_FALHA` | qualquer | — | — (ignorado) | sai apenas por reset |

## Invariantes
- A saída só está energizada em `ACION_LIGADO`.
- Entre um desligamento e a próxima partida decorrem pelo menos 30 s.

## Comportamento em falha
Evento fora da faixa do enum é contado e descartado. `ACION_FALHA`
persiste o código de falha e mantém a saída desligada; na inicialização
seguinte, a causa do último reset e o código persistido são lidos e
registrados, e a máquina parte de `ACION_DESLIGADO`.

## Verificação
Teste em host cobrindo cada linha da tabela: pendente — a suíte de host
ainda não existe neste projeto. Hoje a verificação é manual em bancada,
registrada no relatório de validação.
```
