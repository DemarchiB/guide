# Adoção

Cobre como um projeto passa a usar este conjunto: como montá-lo, quais documentos nascem no dia zero e em que ordem, como um projeto existente adota sem parar o trabalho, e como o projeto recebe atualizações do conjunto depois. Manter a documentação no dia a dia é assunto de [manutencao.md](manutencao.md).

**Leia este arquivo quando:** for criar um projeto do zero, adotar o conjunto num projeto existente, ou atualizar a versão do conjunto que um projeto usa.

## 1. Montar o conjunto

A forma padrão é **submódulo** em `docs/guide/`: o commit fixado é o estado adotado, a atualização é um comando, e editar o conjunto por engano dentro do projeto fica visível no `git status`.

```sh
git submodule add https://github.com/DemarchiB/guide.git docs/guide
git commit -m "Adota convenções de projeto em docs/guide"
```

Consequências que o projeto precisa conhecer:

- quem clona usa `git clone --recurse-submodules`, ou roda `git submodule update --init` depois — sem isso `docs/guide/` fica vazio e o agente trabalha sem as convenções;
- toda worktree nova também precisa de `git submodule update --init` ([practices/git.md](practices/git.md), Seção *Branch e revisão*);
- o estado adotado é o que `git submodule status docs/guide` mostra; não o repita em outro arquivo, porque a cópia envelhece na primeira atualização.

**Alternativa por cópia** — só quando o projeto não usa Git ou não pode ter submódulo: copie o diretório para `docs/guide/` e registre no `AGENTS.md` o commit de origem (`git -C <clone-do-conjunto> rev-parse --short HEAD`). A cópia continua proibida de edição.

## 2. Projeto novo

**Conjunto mínimo:** o conjunto em `docs/guide/` e três documentos, nesta ordem, cada um a partir do seu template:

1. `ARCHITECTURE.md` — mesmo esquelético; dá vocabulário ao resto. O que não está decidido vai em "Pontos não determinados"; estrutura planejada é legítima desde que rotulada como planejada.
2. `AGENTS.md` — depois do anterior, porque índice só se escreve bem sobre o que já existe. Declara os domínios aplicáveis e, na seção *Fluxo*, o branch base e como o trabalho do agente é entregue ([practices/git.md](practices/git.md), Seção *Agente em sessão local*) — são os fatos que o agente precisa em toda tarefa e não descobre sozinho.
3. `README.md` — a apresentação para pessoas.

`docs/workflow.md` **não** nasce no dia zero; os critérios para ele aparecer estão em `templates/workflow.md`.

Nessa ordem toda referência entre documentos aponta para trás. Se alguma ferramenta de IA usada no projeto não lê `AGENTS.md`, crie o adaptador dela ([practices/ia-harness.md](practices/ia-harness.md), Seção *Adaptadores de ferramenta*).

**O primeiro sensor é parte da adoção, não um passo futuro.** Antes de delegar implementação a um agente, o projeto precisa de pelo menos uma verificação que o próprio agente rode sozinho — nem que seja só o build por linha de comando. Sem isso ele não tem como saber se acertou, e todo erro volta para a revisão ou para a bancada ([practices/testes.md](practices/testes.md), Seção *Conjunto mínimo de sensores*). O que existe e o que falta vai na tabela de comandos do `AGENTS.md`, com o que falta marcado.

**Todo o resto nasce com o primeiro conteúdo real** — a primeira spec com a primeira funcionalidade não trivial, o primeiro ADR com a primeira decisão que atenda aos critérios do template, a primeira Skill quando um procedimento se repetir. Num repositório sem código é normal que a tabela de comandos do `AGENTS.md` esteja inteira marcada como `<a definir>`: documento obrigatório com pendências declaradas é o estado correto do dia zero ([manutencao.md](manutencao.md), Seção *Estado provisório*).

## 3. Projeto existente

Não pare o trabalho para documentar tudo: documentação retroativa em massa produz afirmação sem evidência.

1. Monte o conjunto (Seção *Montar o conjunto*).
2. Escreva o `AGENTS.md` com o que já é verificável hoje — comandos que você rodou, restrições que você conhece.
3. Levante o `ARCHITECTURE.md` a partir das fontes de evidência ([manutencao.md](manutencao.md), Seção *Fontes de evidência*), marcando o que o código não comprovar.
4. Ajuste o `README.md` existente, sem reescrever o que já está correto; escreva `docs/workflow.md` só se o fluxo não couber na seção *Fluxo* do `AGENTS.md`.
5. Registre como ADR só as decisões que ainda governam o código e que alguém questionaria.

Daí em diante, cada tarefa que tocar uma área documenta aquela área. A cobertura cresce pelo uso, não por mutirão.

## 4. Pedido pronto para um agente

Para delegar a adoção, use este pedido como está (ajuste apenas o que está entre `<>`):

```text
Adote as convenções montadas em docs/guide/ neste repositório, seguindo
docs/guide/adocao.md (Seção "<Projeto novo | Projeto existente>").
- Crie apenas os documentos obrigatórios, na ordem indicada, cada um a partir
  do seu template em docs/guide/templates/.
- Use somente fatos verificáveis no repositório; o resto entra marcado como
  <a definir> ou <a verificar: motivo>. Não invente comandos.
- Domínios aplicáveis a este projeto: <engenharia, git, ia, testes, ...>.
- Não crie pastas vazias nem documentos opcionais; não crie docs/workflow.md.
- Na seção Fluxo do AGENTS.md entram só dois fatos: o branch base e se você
  commita. Pergunte-me os dois; não deduza nenhum deles nem acrescente linhas.
- Antes de criar qualquer arquivo, liste o que vai criar e o que não encontrou
  evidência para preencher; espere minha confirmação.
- Trabalhe numa branch docs/adocao-convencoes e não faça merge.
Ao terminar, liste os arquivos criados, as pendências marcadas e os comandos
que você executou para verificar o que documentou.
```

## 5. Atualizar o conjunto num projeto

Quando o conjunto muda, o projeto **reavalia** — não necessariamente atualiza.

```sh
git -C docs/guide fetch
git -C docs/guide log --format='%h %s%n%(trailers:key=Impacto-adocao)' HEAD..origin/main   # o que mudou e o que fazer
git -C docs/guide diff HEAD..origin/main                                                   # o detalhe
git submodule update --remote docs/guide                                                   # se decidir atualizar
```

Cada linha `Impacto-adocao` é uma ação que o projeto precisa aplicar (`manutencao-do-conjunto.md`, Seção *Identificação e propagação*). Atualize num commit próprio, aplicando essas ações na mesma mudança. Ficar no estado atual é decisão legítima; se for deliberada e duradoura, registre o motivo numa linha do `AGENTS.md`.

O que costuma precisar de ajuste no projeto é o que **aponta** para o conjunto: a lista de domínios aplicáveis e as citações de arquivo e seção no `AGENTS.md`, no `docs/workflow.md`, nas Skills e nos adaptadores de ferramenta. O conteúdo do projeto em si não muda.

### Pedido pronto para um agente

Use este pedido depois de rodar `git submodule update --remote docs/guide`. O `<hash-antigo>` é o commit que o projeto tinha antes da atualização: ele aparece como a linha `-Subproject commit ...` em `git diff docs/guide`, ainda não commitada.

```text
O submódulo docs/guide foi atualizado. Traga este projeto para o estado novo,
seguindo docs/guide/adocao.md (Seção "Atualizar o conjunto num projeto").

1. Liste o que mudou e o que ele exige:
   git -C docs/guide log --format='%h %s%n%(trailers:key=Impacto-adocao)' <hash-antigo>..HEAD
2. Para cada linha Impacto-adocao, aplique a ação nos documentos DESTE projeto.
3. Verifique, além disso, se continuam corretos no projeto:
   - a lista de domínios aplicáveis do AGENTS.md (nomes de arquivo em practices/);
   - toda citação de arquivo do conjunto e de título de seção dele, em
     AGENTS.md, docs/workflow.md, .agents/skills/ e adaptadores de ferramenta;
   - as seções que os templates do conjunto passaram a exigir.
   Use `grep -rn docs/guide .` e `grep -rn Seção .` para encontrá-las.
4. Não altere nada dentro de docs/guide/ — é submódulo.
5. Não invente conteúdo novo: só corrija ponteiros quebrados e o que o trailer
   pedir. O que exigir decisão minha, liste em vez de decidir.

Ao terminar, rode `python docs/guide/tools/verificar.py` e entregue o resumo
da mudança, com a lista do que precisa de decisão minha.
```
