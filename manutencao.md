# Manutenção documental

Cobre como a documentação de um projeto se mantém verdadeira: de onde vem o fato que ela registra, como se declara o que ainda não foi verificado, quando e como o texto é atualizado, e o que se confere ao terminar. Onde cada documento mora é assunto de [estrutura.md](estrutura.md); o processo de conduzir uma mudança é de [practices/engenharia.md](practices/engenharia.md).

**Leia este arquivo quando:** for documentar uma área a partir do código, revisar documentação existente, ou encerrar uma mudança que alterou a estrutura documental.

## 1. Princípios

1. **O repositório é a fonte de verdade.** Regra, arquitetura, comando e decisão vivem em arquivo versionado — nunca só em memória de agente, histórico de conversa, configuração de IDE ou arquivo local.
2. **A documentação reflete o projeto**; o projeto não é reorganizado para atender a uma ferramenta ou agente.
3. **Documentação desatualizada é instrução errada.** Para um agente, o que está escrito é o que vale; um documento velho faz mais estrago do que um documento ausente.
4. **Cada fato tem um dono.** O segundo lugar que precisa dele recebe um link, não uma segunda redação — duas redações divergem na primeira alteração.

## 2. Fontes de evidência

Antes de documentar ou alterar uma área, procure evidência nesta ordem:

1. código-fonte e interfaces públicas;
2. arquivos de build, dependências e configuração;
3. testes e validações executáveis;
4. documentação versionada e ADRs vigentes (considerando o `Status`);
5. scripts operacionais e automações;
6. comportamento observado e reproduzível.

Quando fontes divergirem: registre a divergência, determine qual fonte governa o comportamento atual, não atualize a documentação com uma conclusão não comprovada, e peça decisão quando a correção exigir conhecimento externo ao repositório.

## 3. Estado provisório

Nenhum documento fica bloqueado por falta de fato confirmado, e nenhum buraco é preenchido por suposição. O fato pendente é declarado na própria linha:

- `<a definir>` — ainda não há escolha feita;
- `<a verificar: motivo>` — há expectativa razoável, ainda não confirmada.

Comando que ninguém rodou entra como `<a verificar>`, nunca como oficial; comando que foi executado é documentado com diretório, pré-requisitos e efeitos colaterais quando relevantes, e nunca com credencial. A marcação sai na mesma mudança que confirma o fato.

**Seção sem conteúdo.** Seção prevista no template cujo conteúdo ainda não existe é **omitida** — o template continua dizendo onde ela entra quando o conteúdo surgir, e uma linha "nenhum até o momento" repetida em toda sessão de agente é custo sem informação. A exceção são campos que o template declara obrigatórios: esses ficam, com a marcação acima.

## 4. Quando e como atualizar

Atualize a documentação **na mesma mudança** que alterar: propósito ou escopo, comandos e pré-requisitos, arquitetura, limites ou dependências, comportamento especificado, workflows de Skills, formatos gerados, riscos e restrições.

**"Na mesma mudança" quer dizer no mesmo commit ou PR, não a cada edição.** Enquanto a implementação está em andamento o comportamento ainda muda: documentar a cada passo reescreve o mesmo texto várias vezes, gasta contexto e deixa um diff que não estabiliza. A documentação afetada é atualizada **uma vez, depois que o comportamento está implementado e verificado**, antes de encerrar. Durante o trabalho, o progresso vai para onde ele pertence — as tarefas da spec ou o plano, marcadas em marcos.

Duas exceções, ambas porque o documento é **entrada** do trabalho, não registro dele: a spec é escrita e aprovada antes de implementar; e, se a implementação mostrar que a spec está errada, o trabalho para e a spec é corrigida primeiro ([practices/specs.md](practices/specs.md), Seção *Seguir uma spec*).

Ao escrever ou revisar:

- remova o obsoleto, preserve o que continua correto, troque duplicação por link;
- diferencie fato, decisão e hipótese;
- escreva instrução concreta e verificável ("rode `cmake --build --preset debug`"), não intenção genérica ("garanta a qualidade");
- não escreva o que o agente descobre sozinho lendo a árvore ou o manifesto — visão geral do repositório em arquivo carregado em toda sessão aumenta custo sem melhorar resultado ([practices/ia-harness.md](practices/ia-harness.md), Seção *Harness e economia de contexto*);
- corte duplicação e adjetivo, nunca a justificativa de uma regra: regra sem porquê é contornada na primeira vez que incomoda.

## 5. Checklist de mudança documental

- [ ] Todo documento novo partiu do template, ou pertence a uma área sem template e cumpre o mínimo de `estrutura.md`, Seção *Áreas sem template*.
- [ ] `AGENTS.md` continua curto, declara os domínios aplicáveis e os desvios, e só lista comandos verificados.
- [ ] `ARCHITECTURE.md` continua de alto nível e único no projeto.
- [ ] Specs têm `Status`, requisitos com identificador único no projeto e critérios de aceite verificáveis.
- [ ] ADRs têm `Status` e `Data`; os superados apontam para o substituto e nenhum foi reescrito.
- [ ] Skills passam na verificação de frontmatter, e adaptadores de ferramenta não duplicam conteúdo.
- [ ] Links relativos resolvem — inclusive depois de mover arquivos (`python docs/guide/tools/verificar.py`).
- [ ] Fato não confirmado aparece com marcação de estado provisório.
- [ ] Nenhum arquivo de `docs/guide/` foi alterado e nenhuma cópia de template ficou solta no projeto.

## 6. Antipadrões

- Árvore preenchida: pasta, documento ou Skill criado para completar a estrutura.
- `AGENTS.md` longo, com visão geral do repositório, instrução genérica ou cópia de outros documentos.
- Arquivo de instrução de uma ferramenta específica com cópia do `AGENTS.md`, ou criado para ferramenta que ninguém usa no projeto.
- Comando hipotético apresentado como oficial; arquitetura baseada em suposição não marcada.
- Spec sem critério de aceite verificável; ADR para decisão trivial ou reversível; ADR reescrito em vez de substituído.
- A mesma regra escrita em dois lugares com redações diferentes.
- Fato específico de um projeto incorporado a um arquivo do conjunto.

## 7. Critério de sucesso

A documentação está adequada quando uma pessoa ou agente sem histórico prévio consegue, só com o repositório: localizar comandos reais e rodá-los; saber quais regras se aplicam e onde estão; encontrar specs, ADRs e planos distinguindo vigente de histórico; criar um documento novo no formato certo; saber quais verificações rodar e o que fazer quando falham; e concluir uma mudança sem depender de conhecimento privado.
