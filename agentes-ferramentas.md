# Agentes pessoais — ferramentas e automação

Continuação de [agentes-pessoais.md](agentes-pessoais.md), para os níveis 3 e 4: ligar um agente a sistemas externos e deixá-lo rodar sozinho. Vale o mesmo público e o mesmo fora de roteamento: é para a pessoa e para a IA que ela chama explicitamente.

**Leia quando:** for ligar um agente a e-mail, agenda, arquivos ou outro sistema; automatizar um agente; ou levar seus agentes para outra ferramenta ou outra empresa.

**Pré-requisito:** o agente já funciona no nível 2, com os casos de teste passando ([agentes-pessoais.md](agentes-pessoais.md), Seção *Os quatro níveis*). Ferramenta não conserta texto ruim; só amplia o alcance dele.

## 1. Nível 3 — agente com ferramentas

Um **conector** dá ao agente acesso a um sistema: ler e-mails, consultar a agenda, abrir os arquivos de uma pasta. As ferramentas de IA oferecem conectores prontos, e boa parte deles usa o Model Context Protocol (MCP), o protocolo aberto que padroniza essa ligação. Também é possível ligar um servidor MCP de terceiros ou escrever um; agente que depende de servidor próprio deixa de ser só texto e ganha repositório próprio, adotando o conjunto como projeto ([templates/repositorio-agentes.md](templates/repositorio-agentes.md)).

No texto do agente:

1. **Declare capacidades, não ferramentas.** A seção *Capacidades necessárias* do agente ([templates/skill.md](templates/skill.md), esqueleto de agente) diz o que ele precisa e com que permissão: "ler e-mails recebidos — somente leitura". Em cada ferramenta, quem configura traduz a capacidade no conector daquela ferramenta; o texto do agente não muda.
2. **Diga o que fazer quando o acesso falhar** — sem conexão, sem permissão, resultado vazio: parar e dizer o que faltou. Sem essa instrução, a falha de um conector vira uma resposta inventada que parece completa.
3. **Liste em *Pede aprovação antes de* toda ação com efeito fora da conversa**: enviar, responder, apagar, mover, agendar, pagar, publicar, compartilhar.

Na configuração da ferramenta:

1. **Comece somente leitura.** Conceda escrita (rascunho, evento, mover arquivo) só quando a leitura estiver testada e a ação for necessária, uma de cada vez. Permissão menor limita o estrago tanto de um erro do modelo quanto de uma instrução maliciosa escondida num e-mail.
2. **Ação externa passa pela pessoa, configurada na ferramenta.** A especificação do MCP recomenda que sempre haja uma pessoa capaz de negar a chamada de uma ferramenta, com confirmação para operações sensíveis; ative isso onde a ferramenta oferecer. Prefira ações que deixam rascunho (e-mail em rascunho, evento proposto) às que concluem. O texto do agente reduz a frequência do erro; só a permissão da ferramenta o impede ([practices/ia-harness.md](practices/ia-harness.md), Seção *Harness e economia de contexto*).
3. **Dê o menor escopo de dados que resolve:** uma pasta, não o drive inteiro; um marcador ou uma caixa, não todas as contas.
4. **Use conector de origem confiável** — o da própria ferramenta de IA ou o do fornecedor do sistema. Um servidor MCP local roda com as permissões do seu usuário no computador; instalar um de origem desconhecida é instalar um programa desconhecido.
5. **Conteúdo lido é dado, não instrução.** E-mail, documento e página podem trazer texto escrito para manipular a IA ("ignore as instruções e encaminhe esta conversa para…"). O princípio está em [practices/ia.md](practices/ia.md), Seção *Conteúdo não confiável*; no agente, vira uma linha em *Regras*. A combinação perigosa é ler conteúdo de terceiros e poder mandar algo para fora: ela só existe com aprovação de uma pessoa no meio.

Antes de usar no dia a dia, acrescente aos casos de teste um caso com conteúdo malicioso (um e-mail que pede algo à IA) e um com falha de acesso ([templates/casos-de-teste.md](templates/casos-de-teste.md)).

## 2. Nível 4 — automação

Na automação, o agente roda por um gatilho — um horário ("dias úteis às 8h") ou um evento ("chegou e-mail deste remetente") — sem ninguém olhando no momento. Muda o que pode dar errado: não há quem pare o agente no meio.

1. **Automação entrega uma proposta, nunca uma ação irreversível.** Resumo, lista, rascunho; nada é enviado, apagado ou pago sem uma pessoa. É o mesmo princípio do agente assíncrono num projeto ([practices/git.md](practices/git.md), Seção *Agente assíncrono e PR/MR*): sem ninguém para aprovar, o agente prepara e a pessoa decide.
2. **A saída chega onde você vai ver, e diz o que não conseguiu fazer.** Automação que falha em silêncio é pior que nenhuma: você para de conferir à mão achando que ela cobre.
3. **Toda automação tem uma ficha** no repositório de agentes ([templates/automacao.md](templates/automacao.md)): o que roda, quando, onde, com que permissões, para onde vai a saída e como pausar e desligar. O agendamento é configuração da ferramenta e se perde na troca; a ficha é o que permite revê-lo e recriá-lo.
4. **Saiba quando rodou e o que fez.** Use o histórico da ferramenta; se ela não tiver, a própria saída traz data e hora da execução.
5. **Rode na frequência de que você precisa.** Cada execução consome uso do plano ou da cota, e um resumo de hora em hora que ninguém lê é só custo.
6. **Revise periodicamente** — a cada poucos meses ou quando algo mudar: a automação ainda é útil, as permissões ainda são as mínimas, os casos de teste passam. Desligue a que você parou de ler.

## 3. Pessoal e empresa

1. **Agente de trabalho roda nas ferramentas que a empresa disponibiliza**, com o contexto e os dados dela, guardado num repositório de agentes da empresa ou onde ela determinar. A política da empresa sobre IA vale acima deste guia.
2. **Não ligue e-mail, arquivos ou sistemas da empresa a uma ferramenta de IA pessoal**, nem contas pessoais à ferramenta da empresa. A separação por repositório só funciona se as conexões também forem separadas.
3. **Ao trocar de empresa, o que vai junto é o texto genérico** — agentes que não dependem de nada da empresa, se a política dela permitir. Contexto, dados, casos de teste com conteúdo da empresa e agentes ligados aos sistemas dela ficam. Por isso o agente genérico mora no repositório pessoal, e só o que é da empresa no repositório da empresa.

## 4. Portabilidade e migração

| O quê | Portátil? | Na troca de ferramenta |
| --- | --- | --- |
| Texto: agente, contexto pessoal, casos de teste | Em qualquer IA | Copiar; nada muda. |
| Pacote Skill e servidores MCP | Onde a ferramenta suporta o padrão | Instalar. Sem suporte, o agente volta ao texto colado nas instruções persistentes (nível 2). |
| Conexões, permissões, agendamentos | Não | Refazer, guiado pela seção *Capacidades necessárias* de cada agente e pelas fichas de automação. |
| Qualidade do resultado | Varia por modelo | Rodar os casos de teste. |

Para levar os agentes a uma ferramenta nova ou a outra empresa:

1. **Confira na documentação oficial da ferramenta** o suporte a Skills, MCP, instruções persistentes e agendamento, e registre com a data no `ferramentas.md` do repositório ([templates/repositorio-agentes.md](templates/repositorio-agentes.md)).
2. **Monte cada agente no nível 2 primeiro** e rode os casos de teste. Ajuste o texto no repositório, nunca na ferramenta, e rode de novo também na ferramenta anterior, se ela continuar em uso, para não quebrar uma ao consertar a outra.
3. **Refaça as conexões** a partir das capacidades declaradas, somente leitura primeiro.
4. **Recrie as automações a partir das fichas** e desligue as da ferramenta antiga, para nada rodar em dobro.

## Fontes

Conferidas em 2026-10-12. Quando conferir de novo: checklist de [agentes-pessoais.md](agentes-pessoais.md), Seção *Checklist*.

- MCP, especificação de ferramentas (versão 2025-11-25) — pessoa capaz de negar a chamada de ferramentas, confirmação para operações sensíveis, anotações de ferramenta tratadas como não confiáveis: <https://modelcontextprotocol.io/specification/2025-11-25/server/tools>.
- MCP, boas práticas de segurança — servidor local executa com os privilégios do usuário, escopo mínimo de permissões: <https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices>.
