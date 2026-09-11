# Template: spec (`docs/specs/<nome>.md`)

**Quando usar:** antes de implementar uma funcionalidade que atenda aos critérios de [practices/specs.md](../practices/specs.md), Seção *Quando escrever uma spec*. Como criar, seguir e manter a spec também está lá; este arquivo é o formato.

**Papel:** descrever o comportamento verificável de **uma funcionalidade**, enquanto ela existir. Não descreve como implementar (design-doc) nem por que uma decisão foi tomada (ADR).

**Padrões EARS** — todo requisito usa um dos cinco:

- Ubíquo: "O `<sistema>` deve `<comportamento>`"
- Evento: "Quando `<gatilho>`, o `<sistema>` deve `<resposta>`"
- Estado: "Enquanto `<estado>`, o `<sistema>` deve `<resposta>`"
- Comportamento indesejado: "Se `<condição>`, então o `<sistema>` deve `<resposta>`"
- Opcional: "Onde `<recurso presente>`, o `<sistema>` deve `<resposta>`"

**Convenções:**

- Nome do arquivo em kebab-case sem acento (`deteccao-overflow-uart.md`).
- **Identificador único no projeto inteiro:** `REQ-<PREFIXO>-NNN`, com um prefixo curto em maiúsculas por spec, declarado no cabeçalho (`REQ-UART-001`). Commit cita só o identificador; se dois arquivos tivessem `REQ-001`, a citação não diria qual. Número nunca é reaproveitado: requisito removido fica na lista marcado `(removido)`.
- `Status`: `rascunho` → `aprovada` → `implementada`; ou `substituída por <spec>`; ou `obsoleta`, só em projeto com rastreabilidade auditável.
- *Tarefas* existe só enquanto há trabalho em andamento; spec `implementada` não tem essa seção.
- A rastreabilidade até o commit vem das mensagens de commit (`git log --grep REQ-UART-001`), não de uma tabela: o hash de um commit não pode ser escrito dentro dele mesmo, e tabela de hashes mantida à mão sempre atrasa.
- Ferramenta com modo de planejamento próprio escreve o resultado neste formato e neste local, não em pasta proprietária.
- Seção sem conteúdo é omitida — "Design", por exemplo, só existe quando houver decisão de arquitetura envolvida.

````markdown
# Spec: <título curto>

- **Status:** rascunho | aprovada | implementada | substituída por <spec> | obsoleta
- **Data:** <AAAA-MM-DD da última atualização>
- **Prefixo:** <PREFIXO>

## Contexto
<O quê e por quê, em 2-3 linhas, citando a evidência que motiva a spec.>

## Requisitos
- REQ-<PREFIXO>-001 (<padrão EARS>): <requisito>
- REQ-<PREFIXO>-002 (<padrão EARS>): <requisito>

## Critérios de aceite
- [ ] <critério verificável, com o requisito que comprova>

## Tarefas
<Só enquanto houver trabalho em andamento. Cada tarefa entrega e verifica
seus requisitos, com o teste junto; marque [x] depois de verificada.>
- [ ] 1. <incremento> e seu teste (REQ-<PREFIXO>-NNN)
- [ ] 2. <incremento> e seu teste (REQ-<PREFIXO>-NNN)

## Verificação
| Requisito | Implementação | Teste |
| --- | --- | --- |
| REQ-<PREFIXO>-001 | `<arquivo ou módulo>` | `<teste, ou "pendente: motivo">` |

## Fora de escopo
<O que esta spec explicitamente não cobre.>

## Restrições
<Memória, tempo, norma, variante de produto — quando houver.>

## Design
<Link para o ADR ou design-doc. Omita a seção se não houver decisão envolvida.>
````

## Exemplo preenchido (ilustrativo)

Spec já implementada: por isso não tem a seção *Tarefas*. Durante a implementação ela tinha, por exemplo, `- [x] 1. Detecção de overflow e teste (REQ-UART-001)`.

```markdown
# Spec: Driver UART com detecção de overflow

- **Status:** implementada
- **Data:** 2026-03-14
- **Prefixo:** UART

## Contexto
O driver de UART não sinaliza quando o buffer de recepção enche, e bytes
se perdem em silêncio em rajadas de dados (ver `src/drivers/uart.c`).

## Requisitos
- REQ-UART-001 (Evento): Quando o buffer RX atingir 90% de ocupação, o driver deve sinalizar overflow.
- REQ-UART-002 (Estado): Enquanto o overflow estiver sinalizado, o driver deve descartar novos bytes recebidos.
- REQ-UART-003 (Comportamento indesejado): Se a paridade de um byte for inválida, então o driver deve descartar o byte e incrementar o contador de erro de paridade.
- REQ-UART-004 (Evento): Quando `uart_limpar_overflow` for chamada, o driver deve limpar a sinalização de overflow.

## Critérios de aceite
- [x] Cada requisito tem teste em host com mock de UART, sem hardware.
- [x] Nenhuma alocação dinâmica introduzida.

## Verificação
| Requisito | Implementação | Teste |
| --- | --- | --- |
| REQ-UART-001 | `src/drivers/uart.c` | `test/test_uart_overflow.c` |
| REQ-UART-002 | `src/drivers/uart.c` | `test/test_uart_overflow.c` |
| REQ-UART-003 | `src/drivers/uart.c` | `test/test_uart_paridade.c` |
| REQ-UART-004 | `src/drivers/uart.c` | `test/test_uart_overflow.c` |

## Fora de escopo
Mudança de baud rate.

## Restrições
Buffer RX de 256 bytes. Sem aviso novo na análise estática do projeto.

## Design
[ADR-0003](../decisions/ADR-0003-buffer-circular-uart.md)
```
