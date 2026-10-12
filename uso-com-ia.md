# Uso com IA — para quem conduz o trabalho

Este arquivo é para a pessoa que trabalha com um agente de IA, não para o agente: não está na tabela de roteamento do `PROJECT_GUIDE.md` e não é lido numa tarefa. As regras que o agente segue estão no `PROJECT_GUIDE.md` e em `practices/`; aqui ficam como conduzir a sessão, como revisar o que ele entrega e pedidos prontos.

## 1. Condução da sessão

Onde mais se ganha em custo e em qualidade não é no texto do harness: é em como a sessão é conduzida.

1. **Uma tarefa por sessão.** O contexto inteiro é reenviado a cada turno: numa sessão longa o custo cresce mais rápido que o trabalho feito, e a qualidade cai quando a janela se enche de tentativas antigas. Tarefa terminada, sessão nova.
2. **Aponte os arquivos.** Dizer o que ler é mais barato e mais preciso do que deixar o agente procurar; busca cega pela árvore é o gasto invisível de uma sessão.
3. **Isole investigação ampla** num contexto separado — subagente ou sessão auxiliar — que devolve conclusões e evidências, não a transcrição do que leu.
4. **Caminho errado não se corrige empilhando.** Se a abordagem se mostrou errada, volte ao último ponto bom ([practices/git.md](practices/git.md), Seção *Commit e rastreabilidade*) e recomece, levando no pedido o que você aprendeu. Tentativa descartada continua influenciando o agente enquanto estiver no contexto.
5. **O que é carregado em toda sessão fica estável durante a tarefa.** Alterar `AGENTS.md` ou o harness no meio do trabalho invalida o reaproveitamento de contexto e faz repagar tudo; mudança de harness é tarefa própria.
6. **O esforço caro vai onde ele paga.** Entender, planejar, escrever spec e revisar são onde a capacidade do modelo aparece; executar um plano aceito, com sensor verde ao fim de cada passo, exige bem menos. Projeto com sensores pode delegar a execução barata; projeto sem sensores paga o modelo caro em toda tarefa, porque acertar de primeira vira a única estratégia disponível ([practices/testes.md](practices/testes.md), Seção *Conjunto mínimo de sensores*).
7. **Uma tarefa da spec por sessão**, e não a spec inteira de uma vez: é o recorte que mantém o contexto pequeno, o diff revisável e o erro barato de desfazer.

## 2. Revisar o que o agente entrega

1. **Quem revisa responde pelo diff inteiro**; o fato de ter sido gerado por IA não reduz a responsabilidade.
2. **Delegue só o que dá para verificar** por sensor ou revisão barata. Sem critério de pronto, ou quando o erro não aparece na revisão, escreva a spec ([practices/specs.md](practices/specs.md)) ou mantenha a decisão com você.
3. **Teste gerado por agente tem modos de falha próprios**; a lista do que procurar está em [practices/testes.md](practices/testes.md), Seção *Pedir testes a um agente*.

## 3. Pedidos prontos

Ajuste o que está entre `<>`. Cada pedido só diz o que fazer agora; o protocolo que o agente segue está no arquivo citado. Os pedidos de adoção e de atualização do conjunto estão em [adocao.md](adocao.md).

Escrever testes:

```text
Escreva testes para <módulo>, seguindo docs/guide/practices/testes.md
(Seção "Pedir testes a um agente").
```

Rascunhar uma spec:

```text
Quero uma spec para: <o que precisa ser feito e por quê>. Siga
docs/guide/practices/specs.md (Seção "Criar uma spec") e o formato de
docs/guide/templates/spec.md. Não implemente nada.
```

Implementar uma tarefa de spec aprovada:

```text
Implemente a tarefa <n> de docs/specs/<nome>.md, seguindo
docs/guide/practices/specs.md (Seção "Seguir uma spec").
```
