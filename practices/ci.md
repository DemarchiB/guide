# Domínio: CI e automação de build

Cobre a automação dos sensores: os scripts que executam cada etapa, o paralelismo entre elas, o ambiente em que rodam, o pipeline de CI que as chama e o que fazer quando ele fica vermelho. Quais sensores existem e como se escreve um teste estão em [testes.md](testes.md); toolchain e presets de C, em [c-build-e-analise.md](c-build-e-analise.md); o papel do CI na revisão de PR/MR, em [git.md](git.md), Seção *Agente assíncrono e PR/MR*. Exemplos de scripts, pipeline para GitLab e GitHub e imagem estão em [templates/ci.md](../templates/ci.md).

**Aplica-se a:** todo projeto; o pipeline, a projeto com remoto que ofereça CI.
**Leia quando:** for criar ou alterar script de build, teste ou automação; introduzir CI num repositório que não tem; configurar pipeline de CI, hook ou a imagem em que o build roda; investigar CI lento ou vermelho.

## 1. Scripts: uma etapa, um comando

1. **Cada etapa é um script que roda sozinho, no PC e no runner** — build, teste em host, análise, verificação da documentação —, com uma responsabilidade, sem interação e com código de saída diferente de zero na falha. É o que torna a mesma verificação executável por pessoa, por agente e pelo CI; etapa que só existe no CI não se reproduz quando falha.
2. **O pipeline só chama scripts.** Lógica no arquivo de CI — laço, condição, cópia de arquivo, sequência de comandos — não roda no PC e diverge do script na primeira alteração. O arquivo de CI decide quando e onde; o script decide o quê.
3. **O script roda em todos os sistemas em que o projeto é usado.** Quem desenvolve em Windows e roda o CI em Linux escreve os scripts numa linguagem que roda nos dois — PowerShell 7 (`pwsh`) ou Python. `.bat` e `.cmd` só rodam em Windows; `.sh` exige camada extra nele. Dois scripts para a mesma etapa, um por sistema, divergem.
4. **Nada no script supõe o sistema**: caminho montado pela linguagem (`Join-Path`, `pathlib`), nunca com separador fixo; nome de arquivo com a caixa exata, porque o Linux distingue; final de linha fixado no `.gitattributes` ([git.md](git.md), Seção *Commit e rastreabilidade*).

## 2. Paralelismo

1. **Etapas independentes rodam em paralelo — no PC e no CI.** Build do alvo, teste em host, análise e verificação da documentação não dependem umas das outras: em série o tempo é a soma delas, em paralelo é a mais lenta. Um script que dispara as etapas independentes ao mesmo tempo no PC corresponde, uma a uma, aos jobs paralelos do pipeline.
2. **Paralelo exige isolamento.** Cada etapa escreve no próprio diretório (`build/<preset>`), sem arquivo temporário de nome fixo, porta fixa ou "a etapa B usa o que a A deixou ali". Estado compartilhado entre etapas paralelas produz falha intermitente, a mais cara de diagnosticar.
3. **Dependência real é declarada, não presumida pela ordem.** O que uma etapa consome de outra é passado como artefato e declarado no pipeline (`needs:`): a etapa começa assim que sua dependência termina, sem esperar um estágio inteiro.
4. **Paraleliza-se também dentro da etapa**: `cmake --build --parallel` e `ctest --parallel` usam todos os núcleos sem mudar o pipeline.

## 3. Ambiente: imagem com as ferramentas

1. **O job não instala ferramenta a cada execução.** Baixar uma toolchain de 1 GB em cada job custa minutos por job, multiplicados pelos jobs paralelos, e falha quando o servidor de origem falha. As ferramentas estáveis — toolchain, CMake, analisador, interpretador dos scripts — vêm numa imagem de contêiner.
2. **Ferramenta do build se instala por script, sem passo manual.** Só assim ela entra numa imagem; instalador gráfico ou ativação manual deixa o CI dependente de uma máquina preparada à mão. Ferramenta proprietária pede, além disso, saber onde a licença vale. A preferência por toolchain e analisador livres está em [c-build-e-analise.md](c-build-e-analise.md), Seção *Toolchain, build e identificação*.
3. **Imagem pronta e confiável primeiro.** Se uma imagem oficial ou mantida pela comunidade da ferramenta serve, ou serve com pouco acréscimo, ela é a base; imagem própria do zero só quando nenhuma servir.
4. **A imagem é fixada por versão ou digest, nunca `latest`.** Imagem que muda sem commit muda o compilador sem aviso: o build quebra sem alteração no código ou, pior, gera binário diferente do validado.
5. **Imagem própria é código**: o `Dockerfile` é versionado, a imagem é gerada por pipeline e publicada no registry da plataforma, com tag que identifica a versão das ferramentas. Download dentro do `Dockerfile` tem versão fixa e soma de verificação. Imagem montada à mão não se reproduz no dia em que for preciso trocar uma ferramenta.
6. **A mesma imagem roda no PC** para reproduzir uma falha do CI. Sem isso, "passa aqui e falha lá" vira investigação do ambiente em vez do código.
7. **Imagem para o que é estável, cache para o que muda.** Dependência que muda com frequência — pacote baixado pelo próprio build, por exemplo — vai no cache do CI, com chave derivada do arquivo que a fixa; na imagem, obrigaria a regenerá-la a cada mudança.

## 4. O pipeline

1. **Roda em todo push, em qualquer branch, e em todo PR/MR.** Defeito encontrado no push custa menos que o encontrado na revisão, e o agente assíncrono depende do CI como sensor ([git.md](git.md), Seção *Agente assíncrono e PR/MR*).
2. **Verde é obrigatório para integrar no tronco e nas branches de integração**, configurado na plataforma — merge só com pipeline verde, branch protegida —, não deixado à disciplina.
3. **Os jobs seguem a ordem e o conteúdo dos sensores** de [testes.md](testes.md), Seção *Conjunto mínimo de sensores*. Jobs independentes rodam até o fim mesmo que um deles falhe, para que um push mostre todos os vermelhos de uma vez; job que depende de um que falhou não roda.
4. **Rápido é requisito.** Referência: o pipeline de um push responde em até ~10 minutos. Pipeline lento é ignorado e acumula pushes na fila; o remédio está nas Seções *Paralelismo* e *Ambiente: imagem com as ferramentas*, não em rodar menos sensores. O que é longo demais para todo push — todas as variantes de build, suíte longa — roda agendado ou antes do merge, como declarado no `docs/workflow.md`.
5. **Push novo na mesma branch cancela o pipeline anterior dela**: o resultado do commit superado não interessa a ninguém e ocupa o runner.
6. **O job publica o que diagnostica a falha** — relatório de teste, log do analisador, mapa de memória —, como artefato com prazo de expiração. O binário de liberação é arquivado conforme [c-build-e-analise.md](c-build-e-analise.md), Seção *Toolchain, build e identificação*.
7. **O que o CI não cobre é declarado** no `docs/workflow.md` — gravação, bancada, ensaio com hardware —, para que verde não seja lido como "validado".
8. **Permissão mínima**: segredo só no job que precisa, como variável protegida da plataforma, nunca no arquivo de CI ([engenharia.md](engenharia.md), Seção *Segredos e dados sensíveis*); o token do job só com as permissões que ele usa.

## 5. Repositório sem CI

Introduzir CI é uma sequência de mudanças pequenas, cada uma verde e útil sozinha; não um projeto que só entrega no fim. Os nomes e a forma vêm de [templates/ci.md](../templates/ci.md), para que quem passa de um repositório a outro reconheça os scripts e os jobs.

1. **Primeiro os scripts, depois o pipeline.** Cada sensor que já existe vira um script em `scripts/` que roda no PC (Seção *Scripts: uma etapa, um comando*) — o primeiro costuma ser o da adoção ([adocao.md](../adocao.md)). Pipeline escrito antes dos scripts nasce com a lógica dentro do arquivo de CI e não se reproduz localmente.
2. **O primeiro pipeline roda só o que já passa** — tipicamente build e verificação da documentação — e entra já verde. Pipeline que nasce vermelho ensina a ignorar o vermelho desde o primeiro dia; sensor que ainda reprova o código existente espera, ou entra com catraca (item 5).
3. **Logo depois, o verde passa a ser exigido pela plataforma** (Seção *O pipeline*, item 2). Pipeline que não bloqueia nada é relatório que ninguém abre.
4. **Cada sensor novo entra no pipeline na mesma mudança que o cria.** A suíte de teste, o analisador, a varredura de segredos: o script e o job chegam juntos. Sensor que fica "para ligar no CI depois" só roda quando alguém lembra.
5. **Sensor com dívida entra com catraca, não desligado**: falha só no achado novo, e a dívida existente fica registrada e encolhe — mecanismo em [c-build-e-analise.md](c-build-e-analise.md), Seção *Adoção incremental*, válido para qualquer analisador. Esperar o código ficar limpo para ligar o sensor é esperar para sempre.
6. **Imagem própria só quando instalar no job passar a custar** (Seção *Ambiente: imagem com as ferramentas*). No começo, uma imagem pronta da ferramenta basta.
7. **Sem plataforma de CI, o script que roda todas as etapas é o pipeline** (`scripts/verificar.ps1` do template): roda antes de integrar, e o `docs/workflow.md` registra "CI: nenhum" e esse comando. Quando a plataforma chegar, cada etapa do script vira um job sem reescrever nada.
8. **O estado fica declarado**: a linha de CI da tabela de comandos do `AGENTS.md` e o `docs/workflow.md` dizem o que roda, onde e o que ainda falta, marcado como pendente — nunca omitido.

## 6. Quando fica vermelho

1. **Vermelho no tronco tem prioridade sobre trabalho novo**: tudo o que nasce dele herda a falha, e enquanto ele estiver vermelho nenhuma outra mudança pode provar que está certa.
2. **Rodar de novo até passar não é correção.** Falha intermitente é defeito — do teste, do script ou do código — e se investiga. Se não puder ser corrigida de imediato, o teste é isolado com o motivo registrado e uma pendência aberta, nunca apagado nem silenciado: teste intermitente ensina todos a ignorar o vermelho.
3. **Mudança no pipeline, num hook ou na imagem é mudança como outra qualquer**: vai numa branch, passa pelo próprio CI e pela revisão. Feita por agente, exige pedido explícito ([git.md](git.md), Seção *O que exige pedido explícito*).

## 7. Hook local

1. **Hook de pré-commit roda só o que leva segundos** — varredura de segredos, verificação da documentação, formatação; o CI roda tudo. Hook lento é contornado com `--no-verify` e deixa de existir na prática.
2. **O hook é versionado no repositório** e ativado por `core.hooksPath`, com o comando de ativação no `AGENTS.md`. Hook que cada pessoa copia à mão diverge entre máquinas.

## Checklist deste domínio

- [ ] Cada etapa nova ou alterada é um script que roda sozinho no PC e no runner; o arquivo de CI só o chama.
- [ ] Etapas que rodam em paralelo não compartilham diretório, arquivo temporário nem porta; dependências entre jobs estão declaradas.
- [ ] O job não baixa nem instala ferramenta estável; a imagem está fixada por versão ou digest.
- [ ] O pipeline roda em todo push e PR/MR, e o verde é exigido pela plataforma para integrar.
- [ ] Sensor novo entrou no pipeline na mesma mudança; sensor com dívida entrou com catraca, não desligado.
- [ ] Nenhum teste foi reexecutado até passar, apagado ou silenciado para deixar o pipeline verde.
- [ ] O que o CI não cobre está declarado no `docs/workflow.md`.
