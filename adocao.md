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
- toda worktree nova também precisa de `git submodule update --init` ([practices/engenharia.md](practices/engenharia.md), Seção *Workflow de revisão*);
- o estado adotado é o que `git submodule status docs/guide` mostra; não o repita em outro arquivo, porque a cópia envelhece na primeira atualização.

**Alternativa por cópia** — só quando o projeto não usa Git ou não pode ter submódulo: copie o diretório para `docs/guide/` e registre no `AGENTS.md` o commit de origem (`git -C <clone-do-conjunto> rev-parse --short HEAD`). A cópia continua proibida de edição.

## 2. Projeto novo

**Conjunto mínimo:** o conjunto em `docs/guide/` e quatro documentos, nesta ordem, cada um a partir do seu template:

1. `ARCHITECTURE.md` — mesmo esquelético; dá vocabulário ao resto. O que não está decidido vai em "Pontos não determinados"; estrutura planejada é legítima desde que rotulada como planejada.
2. `docs/workflow.md` — VCS, remoto, branch principal e de integração.
3. `AGENTS.md` — depois dos anteriores, porque índice só se escreve bem sobre o que já existe. Declara os domínios aplicáveis.
4. `README.md` — a apresentação para pessoas.

Nessa ordem toda referência entre documentos aponta para trás. Se alguma ferramenta de IA usada no projeto não lê `AGENTS.md`, crie o adaptador dela ([practices/ia.md](practices/ia.md), Seção *Arquivos de cada ferramenta*).

**Todo o resto nasce com o primeiro conteúdo real** — a primeira spec com a primeira funcionalidade não trivial, o primeiro ADR com a primeira decisão que atenda aos critérios do template, a primeira Skill quando um procedimento se repetir. Num repositório sem código é normal que a tabela de comandos do `AGENTS.md` esteja inteira marcada como `<a definir>`: documento obrigatório com pendências declaradas é o estado correto do dia zero ([manutencao.md](manutencao.md), Seção *Estado provisório*).

## 3. Projeto existente

Não pare o trabalho para documentar tudo: documentação retroativa em massa produz afirmação sem evidência.

1. Monte o conjunto (Seção *Montar o conjunto*).
2. Escreva o `AGENTS.md` com o que já é verificável hoje — comandos que você rodou, restrições que você conhece.
3. Levante o `ARCHITECTURE.md` a partir das fontes de evidência ([manutencao.md](manutencao.md), Seção *Fontes de evidência*), marcando o que o código não comprovar.
4. Escreva `docs/workflow.md` e ajuste o `README.md` existente, sem reescrever o que já está correto.
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
- Domínios aplicáveis a este projeto: <engenharia, ia, ...>.
- Não crie pastas vazias nem documentos opcionais.
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
