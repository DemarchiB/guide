# Template: ficha de automação (`automacoes/<nome>.md`)

**Quando criar:** antes de ligar uma automação ([agentes-ferramentas.md](../agentes-ferramentas.md), Seção *Nível 4 — automação*).

**Papel:** descreve uma automação de forma que ela possa ser revista, pausada, desligada e recriada em outra ferramenta. O agendamento fica na ferramenta; a ficha é o registro que sobrevive a ela.

**Convenções:**

- **Uma ficha por automação**, com o nome do arquivo igual ao que aparece na ferramenta, para achar uma pela outra.
- **Pede aprovação** repete, para esta automação, o que o agente já declara; se a automação concede menos que o agente pede, vale o menor.
- **Atualize a ficha antes de mudar a automação** na ferramenta, não depois: é o que mantém a ficha verdadeira.
- **Revisão** a cada poucos meses: a automação ainda é lida, as permissões ainda são as mínimas e os casos de teste do agente passam. Automação sem uso é desligada e a ficha, apagada.

```markdown
# Automação: <nome>

- **Agente:** `.agents/skills/<agente>/`
- **Gatilho:** <horário: dias, hora e fuso | evento: o que dispara>
- **Onde roda:** <ferramenta> — configuração em `ferramentas.md`
- **Permissões concedidas:** <capacidade — permissão>
- **Saída:** <o que entrega e onde chega>
- **Pede aprovação antes de:** <ações | nada: só entrega a saída>
- **Se falhar:** <como você fica sabendo>
- **Pausar / desligar:** <onde e como>
- **Registro das execuções:** <onde ver>
- **Criada em:** AAAA-MM-DD · **Última revisão:** AAAA-MM-DD
```

## Exemplo preenchido (ilustrativo)

```markdown
# Automação: triagem-matinal

- **Agente:** `.agents/skills/triagem-email/`
- **Gatilho:** dias úteis, 8h (America/Sao_Paulo)
- **Onde roda:** Ferramenta A — configuração em `ferramentas.md`
- **Permissões concedidas:** ler e-mails recebidos — somente leitura
- **Saída:** a tabela de pendências, como nova conversa na Ferramenta A
- **Pede aprovação antes de:** nada; a automação só lê e entrega a tabela
- **Se falhar:** a ferramenta avisa por notificação; sem tabela até as 9h,
  rodar à mão
- **Pausar / desligar:** tarefas agendadas da Ferramenta A → triagem-matinal
- **Registro das execuções:** histórico de tarefas agendadas da Ferramenta A
- **Criada em:** 2026-11-03 · **Última revisão:** 2026-11-03
```
