# Manutenção do próprio conjunto

Cobre o que só quem **edita este conjunto** precisa saber: que tipo de conteúdo cabe aqui e onde, quando um domínio novo se justifica e qual o seu formato, como decidir o tamanho e a divisão dos arquivos, e como uma alteração chega aos projetos que já adotaram. Nada aqui é lido para trabalhar num projeto.

**Leia este arquivo quando:** for acrescentar, dividir, mover ou remover conteúdo do conjunto, ou declarar o impacto de uma alteração.

## 1. Que conteúdo entra, e onde

| Tipo | Onde | Carregado |
| --- | --- | --- |
| Ponto de entrada: precedência, regras invioláveis, roteamento | `PROJECT_GUIDE.md` | em toda tarefa |
| Procedimento que atravessa projetos (adotar, estruturar, manter) | arquivo na raiz (`adocao.md`, `estrutura.md`, `manutencao.md`) | sob demanda |
| Prática de um assunto técnico | um arquivo em `practices/`, por gatilho de leitura | quando o projeto declara o domínio e a tarefa o toca |
| Formato de um documento ou arquivo de código recorrente | um arquivo por documento em `templates/` | ao criar aquele documento |
| Sensor reutilizável | `tools/`, só biblioteca padrão da linguagem, sem instalação | executado, não lido |
| Mapa arquitetural e limites de um projeto | `ARCHITECTURE.md` do projeto | quando a tarefa cruza componentes, interfaces, variantes ou dependências |

**Só entra o que vale para mais de um projeto.** Fato de um projeto — seu produto, seus comandos, a norma que ele adotou — mora nos documentos daquele projeto. Uma prática de linguagem ou plataforma (C embarcado, TypeScript, uma família de microcontroladores) é legítima aqui quando é o padrão de quem mantém o conjunto para todos os projetos daquele tipo; o domínio declara a quem se aplica e cada projeto decide se o adota.

## 2. Antes de criar um domínio ou template

Conteúdo novo nasce de repetição observada, não de lacuna percebida. Verifique nesta ordem:

1. **Já existe?** Procure no conjunto inteiro (`grep -ri`). Se for caso particular de regra existente, refine a existente.
2. **É um procedimento na voz de quem executa uma tarefa** (revisar, corrigir, liberar versão)? Então é Skill do projeto, que **aponta** para os domínios em vez de repetir suas regras.
3. **Vale só para um projeto?** Então é documento daquele projeto.
4. **Já foi praticado?** Convenção escrita antes do primeiro uso real é palpite com aparência de norma. Template, em especial, nasce quando o segundo documento real mostra a forma repetida.

Só o que sobrevive aos quatro entra. Não crie arquivo vazio "para o futuro".

## 3. Formato de um domínio

```markdown
# Domínio: <assunto>

<2-3 linhas: o que cobre e, explicitamente, o que fica de fora e onde está.>

**Aplica-se a:** <tipo de projeto — "todo projeto", "código C para microcontrolador">
**Leia quando:** <tarefas concretas que exigem este arquivo>

## 1. <Tema>

1. **<Regra acionável e verificável, em negrito.>** <Porquê em uma ou duas frases.>

## Checklist deste domínio

- [ ] <verificação que um revisor ou agente confere no diff>
```

Ao criar um domínio: acrescente a linha de tarefa na tabela *O que ler para cada tarefa* do `PROJECT_GUIDE.md` e o arquivo na lista *Domínios de prática*. Ao criar um template: acrescente-o ao catálogo de `estrutura.md` e, se ele muda onde algo é registrado, à tabela *Onde registrar uma informação*.

## 4. Custo de contexto e divisão de arquivos

O que custa não é o tamanho de um arquivo: é contexto lido sem necessidade. Um agente carrega o arquivo inteiro que a tabela de roteamento mandar ler — não existe "ler só a seção aplicável" —, e por isso **a unidade de divisão é o gatilho de leitura, não o assunto**. Dois critérios:

- **O que é lido em toda tarefa é o mínimo possível.** Vale para o `PROJECT_GUIDE.md` e, nos projetos, para o `AGENTS.md`. Cada acréscimo passa pelo teste: *uma tarefa típica sairia errada sem isto?* Se só algumas tarefas precisam, o conteúdo vai para um arquivo lido sob demanda e o ponto de entrada ganha, no máximo, uma linha de roteamento. `python tools/verificar.py` informa o tamanho desses arquivos para que o crescimento fique visível na revisão, sem reprovar nada.
- **O que é lido sob demanda é dividido por gatilho.** Um arquivo reúne o que uma tarefa precisa ler junto, e a linha da tabela de roteamento que leva até ele descreve uma tarefa real. **É sinal para dividir quando duas tarefas frequentes usam partes diferentes do mesmo arquivo** — mexer numa interrupção não precisa das regras de persistência, escrever código C não precisa das de configurar o build. É sinal para juntar quando dois arquivos são quase sempre lidos em conjunto.

Não há limite numérico de linhas, mas há uma referência prática: um domínio que passa de ~200 linhas quase sempre está atendendo a mais de um gatilho. Confira as linhas de roteamento que levam a ele; se forem tarefas distintas, divida por elas.

Nos dois casos, o que se corta primeiro é duplicação, exemplo redundante e adjetivo — nunca o porquê de uma regra, que é o que impede que ela seja contornada na primeira vez que incomodar.

## 5. Para onde vai um trecho que precisa sair

**O destino se escolhe pelo assunto, nunca por onde há menos texto.** Trecho empurrado para o arquivo mais curto não é encontrado por quem procura o assunto. Se nenhum arquivo existente é o dono, o trecho vira arquivo próprio e entra na tabela de roteamento do `PROJECT_GUIDE.md`.

**Uma regra tem um dono só.** O segundo lugar recebe um ponteiro — arquivo e **título** da seção, nunca só o número, que muda quando se insere uma seção. A exceção é o texto que um template contém para o projeto copiar: ali a repetição é conteúdo gerado, não regra duplicada.

## 6. Identificação e propagação

O estado que um projeto adotou é o commit do submódulo, e o que mudou desde então é o `git log` do conjunto (`adocao.md`, Seção *Atualizar o conjunto num projeto*). Não há número de versão nem arquivo de changelog: para um consumidor que fixa um commit, uma versão só acrescentaria um rótulo a manter em sincronia com o repositório.

O que o changelog daria — saber o que fazer ao atualizar — vem de um **trailer no commit**, escrito no momento em que a informação existe e impossível de divergir do diff que o acompanha. Todo commit que exige ação de quem já adotou — regra que mudou de sentido, caminho ou título de seção que mudou, arquivo renomeado ou removido — termina com um trailer por ação, em linhas seguidas no último parágrafo da mensagem:

```text
Impacto-adocao: trocar referências a practices/x.md, Seção "Y", por practices/z.md
Impacto-adocao: remover docs/index.md do projeto, se não tiver conteúdo próprio
```

Alteração que não obriga ninguém a nada não leva trailer. O nome sem acento é deliberado: trailers são filtráveis por ferramentas de linha de comando (`git log --format='%(trailers:key=Impacto-adocao)'`), e acento no nome da chave é fonte de erro de digitação e de codificação.

Commits são atômicos por assunto, como em qualquer projeto: mudança de sentido de regra não vai junto com reformatação.

## 7. Checklist de alteração do conjunto

- [ ] `python tools/verificar.py` passa: links e títulos de seção citados.
- [ ] A regra alterada tem um dono só; os outros arquivos apontam para ele.
- [ ] Nenhum fato específico de um projeto entrou.
- [ ] Arquivo novo, renomeado ou removido está refletido no `PROJECT_GUIDE.md`, em `estrutura.md` e no `README.md`.
- [ ] Cada arquivo alterado continua atendendo a um gatilho de leitura só.
- [ ] O commit tem um trailer `Impacto-adocao` para cada ação exigida de quem já adotou, quando aplicável.
