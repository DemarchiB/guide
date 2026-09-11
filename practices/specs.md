# Domínio: desenvolvimento guiado por spec

Cobre quando uma funcionalidade merece spec e como a spec é criada, seguida durante a implementação e mantida depois — por pessoa ou por agente. O formato do documento está em `../templates/spec.md`; a citação de requisitos em commits, em [engenharia.md](engenharia.md), Seção *Branch, commit e rastreabilidade*.

**Aplica-se a:** todo projeto.
**Leia quando:** for planejar uma funcionalidade maior, escrever ou revisar uma spec, implementar ou alterar uma funcionalidade que tem spec.

## 1. Quando escrever uma spec

Spec custa uma conversa e um documento antes do código. Ela se paga quando pelo menos um destes vale:

- **o comportamento precisa ser acordado antes** — há mais de uma interpretação razoável do pedido;
- **o trabalho atravessa vários módulos ou várias sessões**, e alguém (ou um agente) vai precisar retomá-lo sem a conversa original;
- **há casos de erro, limite ou tempo** que precisam ser pensados, não descobertos em campo;
- **a implementação vai ser delegada a um agente**: a spec é o critério de pronto que torna o resultado verificável ([ia.md](ia.md), Seção *Qualidade do que o agente produz*);
- **o requisito vem de cliente, norma ou outro sistema**, e precisa ser rastreável.

Não vale o custo para correção pontual, refatoração sem mudança de comportamento ou ajuste óbvio: ali o commit bem escrito é o registro.

**O que vai em cada documento:**

| Documento | Responde | Quando |
| --- | --- | --- |
| Spec | **o quê**: comportamento esperado, verificável | toda funcionalidade que atende aos critérios acima |
| ADR | **por que esta decisão**, e não as alternativas | decisão difícil de reverter que a spec exigiu; a spec aponta para ele |
| Design-doc | **como**, quando o como precisa de explicação | solução não óbvia que não é uma decisão formal |
| Plano (`docs/exec-plans/`) | **em que ordem e com que riscos** | quando a lista de *Tarefas* da spec não basta: migração, várias specs coordenadas, etapas com risco próprio |

Na maioria dos casos, a spec com sua lista de tarefas é tudo de que se precisa.

## 2. Criar uma spec

1. **Comece pelo problema e pela evidência**, não pela solução: o *Contexto* diz o que acontece hoje, o que deveria acontecer e de onde vem essa informação.
2. **Levante as dúvidas antes de escrever requisitos.** Ao usar um agente para rascunhar, peça primeiro a lista de ambiguidades e perguntas; os requisitos vêm depois das respostas. Spec escrita sobre suposição transfere a suposição para o código.
3. **Um comportamento por requisito, em EARS, verificável.** "Rápido", "adequado" e "robusto" não são verificáveis; "em até 50 ms" é.
4. **Escreva o comportamento indesejado.** Erro, limite, tempo esgotado, dado inválido, reset no meio da operação — é onde uma spec rasa falha, e o padrão EARS "Se…, então…" existe para isso.
5. **Critério de aceite diz como cada requisito é comprovado**: teste em host, ensaio em bancada, inspeção. Requisito sem forma de comprovação volta para a etapa 3.
6. **Fora de escopo é explícito.** O que não está escrito ali será assumido por alguém.
7. **Tarefas são incrementos entregáveis**, em ordem, cada um verificável sozinho e citando os requisitos que atende. O teste de um requisito entra na mesma tarefa que o implementa, não numa tarefa "escrever testes" no fim.
8. **Decisão de arquitetura que a spec exige vira ADR**, e a spec aponta para ele em vez de repetir o raciocínio.
9. **Revise antes de aprovar**: requisito ambíguo, requisito sem critério, caso de erro ausente, conflito com `ARCHITECTURE.md` ou com ADR vigente. A passagem de `rascunho` para `aprovada` é decisão de uma pessoa, mesmo quando o texto foi escrito por um agente.

## 3. Seguir uma spec

1. **Só se implementa spec `aprovada`.** Implementar rascunho é decidir o comportamento no código, sem acordo.
2. **Uma tarefa por vez, na ordem.** A tarefa é marcada `[x]` quando está implementada **e** verificada — não quando o código foi escrito.
3. **Commits citam os identificadores** dos requisitos que implementam.
4. **Divergência para o trabalho.** Quando a implementação revela requisito errado, incompleto ou inviável, pare: corrija a spec, obtenha a aprovação da mudança e só então continue. Implementar diferente e ajustar a spec depois para combinar apaga justamente a informação que a spec existia para guardar.
5. **Suposição necessária para seguir não entra no código em silêncio**: vira pergunta ou nota na spec.
6. **Ao concluir:** todos os critérios de aceite conferidos, tabela *Verificação* preenchida (o que não pôde ser verificado aparece como pendente), `Status: implementada` e `Data` atualizada. O resumo da mudança cita os requisitos atendidos.

## 4. Manter uma spec

1. **Spec implementada descreve o comportamento vigente.** Mudança de comportamento edita a spec no mesmo commit ou PR que muda o código. Requisito novo recebe número novo; requisito removido fica marcado `(removido)`, para que o número não seja reaproveitado.
2. **A lista de *Tarefas* é do trabalho em andamento.** Ao marcar a spec como `implementada`, remova a seção — o VCS guarda o histórico. Uma nova rodada de alteração cria a sua própria lista.
3. **Reprojeto completo da funcionalidade gera spec nova**; a antiga passa a `substituída por <spec>`.
4. **Funcionalidade removida leva a spec junto**, na mesma mudança. Projeto com rastreabilidade auditável mantém o arquivo com `Status: obsoleta`.
5. **Divergência encontrada entre spec e código é defeito**, de um ou de outro: relate ou corrija, nunca ignore. Quem toca uma área com spec confere se ela ainda descreve o que o código faz.

## 5. Pedidos prontos para um agente

Para rascunhar uma spec:

```text
Quero uma spec para: <descrição do que precisa ser feito e por quê>.
Siga docs/guide/practices/specs.md (Seção "Criar uma spec") e o formato de
docs/guide/templates/spec.md. Antes de escrever os requisitos, liste as
ambiguidades e perguntas que você tem e espere minhas respostas. Não
implemente nada; a spec fica com Status: rascunho.
```

Para implementar uma spec aprovada:

```text
Implemente docs/specs/<nome>.md, que está aprovada, seguindo
docs/guide/practices/specs.md (Seção "Seguir uma spec"). Uma tarefa por
vez, na ordem; marque cada uma só depois de verificada. Se algum requisito
se mostrar errado ou inviável, pare e me diga antes de continuar.
Ao terminar, entregue o resumo da mudança.
```

## Checklist deste domínio

- [ ] Funcionalidade que atende aos critérios da Seção *Quando escrever uma spec* tem spec aprovada antes do código.
- [ ] Todo requisito é verificável, tem critério de aceite, e os casos de erro e limite foram escritos.
- [ ] Nenhum requisito foi implementado de forma diferente da spec sem que a spec tenha sido corrigida e aprovada antes.
- [ ] Tarefas marcadas só depois de verificadas; commits citam os requisitos.
- [ ] Spec concluída tem `Status: implementada`, tabela *Verificação* preenchida e sem lista de tarefas.
- [ ] Mudança de comportamento em funcionalidade com spec alterou a spec na mesma mudança.
