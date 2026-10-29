# Domínio: sensores e testes

Cobre o que verifica uma mudança automaticamente: o conjunto mínimo de sensores, o que testar, como se escreve um teste que detecta defeito, como se organiza a suíte unitária e o que se exige dela no CI, e como pedir e revisar teste escrito por um agente. O que testar num firmware e a costura com o hardware estão em [testes-firmware.md](testes-firmware.md); a configuração da toolchain e do analisador, em [c-build-e-analise.md](c-build-e-analise.md); scripts, pipeline de CI e ambiente em que os sensores rodam sozinhos, em [ci.md](ci.md).

**Aplica-se a:** todo projeto.
**Leia quando:** for criar ou alterar teste ou sensor, decidir o que rodar antes de concluir uma mudança, ou pedir testes a um agente.

## 1. Conjunto mínimo de sensores

Uma **regra** orienta antes de agir; um **sensor** verifica depois, automaticamente, e detecta o erro que passou pela regra. Projeto que só tem regras depende de todo mundo lembrar de tudo.

Em ordem crescente de custo:

1. **Build** do módulo afetado.
2. **Teste direcionado** à mudança, ampliando para a suíte conforme o risco.
3. **Lint / análise estática** na configuração do próprio projeto.
4. **Documentação** — `python docs/guide/tools/verificar.py`: links, seções citadas, Skills e trechos repetidos entre arquivos.
5. **Varredura de segredos** antes do commit.

Regras de uso:

- os sensores existentes rodam antes de declarar a tarefa concluída, e quem executou informa quais rodou;
- sensor que não existe é registrado como verificação pendente, com o motivo — nunca simulado nem presumido aprovado;
- sensor que falha bloqueia a conclusão: corrigir ou relatar, não seguir adiante;
- **sensor que fecha o laço é o que o agente roda sozinho**: um comando, sem IDE, sem hardware, resposta em segundos. Validação que exige bancada, hardware ou o ambiente final é validação de pessoa — legítima, declarada no resumo, mas não substitui o sensor;
- onde o ambiente permitir, sensores rodam sozinhos (hook de pré-commit, CI — [ci.md](ci.md)). Sensor que depende de alguém lembrar é regra.

**Por que este é o item de maior retorno ao trabalhar com IA.** Sem sensor, o agente precisa acertar de primeira, e acertar de primeira é o que se compra com modelo caro e revisão longa. Com sensor, ele erra, vê o vermelho e corrige sozinho — e o modelo barato passa a bastar para a maior parte do trabalho. Não é preciso ter suíte completa para mudar de regime: um punhado de testes que rodam em segundos sobre a lógica que mais quebra já muda.

## 2. O que testar

**Comportamento novo ou alterado chega com teste na mesma mudança.** Toda mudança que cria ou altera comportamento testável — regra de negócio, cálculo, conversão, validação, análise de mensagem, máquina de estado — traz o teste junto, visto falhando antes de passar (Seção *Escrever um teste*). O que ficar sem teste é declarado no resumo da mudança, com o motivo. Teste deixado para depois raramente é escrito: a mudança seguinte já parte de código sem verificação, e quem revisa não tem como saber o que o código deveria fazer. Função sem comportamento próprio — repasse, acesso trivial — não pede teste; a regra é sobre comportamento, não sobre contagem de funções.

1. **Primeiro a lógica que mais quebra e é barata de testar**: regras de negócio, cálculo e conversão, validação de entrada, análise de mensagens, máquina de estado. É onde o teste pega o defeito que a validação manual deixa passar.
2. **O que depende do ambiente final** — hardware, tempo real, serviço externo — é validação manual, declarada como tal, nunca escondida atrás de "testado".
3. **Cobertura não é meta**: perseguir percentual produz teste que existe para contar. A meta é caso de erro e caso de limite cobertos onde uma falha custa caro.
4. **Todo defeito corrigido ganha um teste de regressão** que o reproduz, visto falhando antes da correção e passando depois. Defeito que escapou uma vez mostrou um caminho que a suíte não cobria; sem o teste, ele volta na próxima refatoração.
5. **Num projeto sem nenhum teste**, o caminho é: um comando que compile e rode a suíte; um módulo de lógica pura coberto de ponta a ponta; e daí em diante cada tarefa cobre a área que toca. Mutirão de testes produz suíte que ninguém entende. A escolha do arcabouço de teste é decisão do projeto, declarada no `AGENTS.md` e — por ser dependência nova — registrada conforme [engenharia.md](engenharia.md), Seção *Dependências*.

Em firmware, a ordem de retorno concreta e a costura com o hardware estão em [testes-firmware.md](testes-firmware.md).

## 3. Escrever um teste

1. **Um comportamento por teste**, com nome que diz a condição e o resultado esperado: `quadro_truncado_retorna_erro`, não `teste_uart_2`. O nome do teste que falhou é a primeira informação do diagnóstico.
2. **Vermelho antes de verde.** Todo teste novo roda ao menos uma vez contra o código sem a correção, e falha. Teste que nunca falhou não provou nada — é a falha mais comum em teste gerado por agente, e a mais fácil de não perceber.
3. **Caso de erro e de limite antes do caminho feliz.** O caminho feliz costuma já funcionar; é o resto que quebra em campo.
4. **Verifique efeito, não implementação**: o que a função devolveu, o estado observável pela interface pública, a chamada que chegou ao dublê. Teste que espia variável interna quebra em toda refatoração e não detecta defeito nenhum.
5. **Dublê só na fronteira**, e o mais simples que resolver. Um fake de vinte linhas que guarda o que foi enviado vale mais que um mock que verifica a ordem das chamadas.
6. **Determinístico**: sem relógio real, sem espera, sem dependência de ordem, sem valor aleatório de semente variável.
7. **Entrada realista, inclusive a inválida**: quadro cortado no meio, comprimento declarado maior que o recebido, valor fora da faixa, contador exatamente no ponto de estouro, buffer cheio. Onde o espaço de entrada for pequeno (um byte de comando, por exemplo), varra todos os valores em vez de escolher três.
8. **A falha diz o que houve** — esperado e obtido no texto da asserção. Falha que só diz "asserção falhou na linha 74" custa uma sessão de depuração por vez que aparece.

## 4. Testes unitários

1. **Teste unitário roda em milissegundos, sem disco, rede, hardware, relógio real nem outro processo.** O que toca nisso é teste de integração e fica em suíte separada (alvo ou rótulo próprio), para que a unitária continue rodando a cada mudança. Referência: a suíte unitária inteira responde em segundos; um teste que passa de ~100 ms está fazendo mais do que unidade.
2. **Estrutura preparar–agir–verificar, visível.** Três blocos separados, uma ação sob teste. Teste com várias ações e asserções intercaladas testa um roteiro: quando falha, não diz qual passo quebrou.
3. **Sem lógica no teste** — laço, condição, cálculo do valor esperado. Lógica no teste pode ter defeito próprio, e ninguém testa o teste. A exceção é a tabela de casos: a mesma regra com várias entradas vira uma tabela de entrada, esperado e nome do caso, percorrida por um laço sem condição; a falha mostra o nome da linha.
4. **Legibilidade antes de reaproveitamento.** Cada teste se lê sozinho, de cima a baixo, com os valores que importam à vista. Função auxiliar que monta entrada válida é bem-vinda — o teste altera só o campo que interessa —, mas preparação escondida em fixture compartilhada obriga a abrir três arquivos para entender uma falha.
5. **O arquivo de teste espelha o módulo**: `src/protocolo/quadro.c` → `tests/protocolo/test_quadro.c`. Quem altera o módulo acha o teste sem procurar, e módulo sem arquivo correspondente salta aos olhos na revisão.
6. **Teste novo é descoberto sozinho pelo build**, sem lista mantida à mão. Teste que depende de alguém registrá-lo numa lista é esquecido, compila, nunca roda e ninguém percebe.
7. **Código de teste é código de produção do sensor**: compila com os mesmos avisos tratados como erro, passa pela revisão e não fica comentado. Teste desativado segue [ci.md](ci.md), Seção *Quando fica vermelho*.

## 5. A suíte no CI

1. **Toda suíte automatizada roda no CI em todo push, inteira.** O teste direcionado basta para fechar o laço durante a tarefa; o CI roda tudo, porque é ele quem pega o efeito que a mudança teve longe de onde foi feita. Teste que só roda no PC de quem o escreveu não protege a mudança seguinte. Suíte longa demais para todo push segue [ci.md](ci.md), Seção *O pipeline*, item 4 — a unitária nunca está nesse caso.
2. **O comando do CI é o mesmo do PC** ([ci.md](ci.md), Seção *Scripts: uma etapa, um comando*). Suíte que só se roda pela IDE não entra no CI e não é sensor de agente.
3. **Zero testes executados é falha.** Filtro errado, diretório renomeado ou descoberta quebrada fazem o executor rodar nada e sair com sucesso — o falso verde mais silencioso que existe.
4. **No CI a suíte roda em ordem embaralhada ou em paralelo.** É o sensor da dependência de ordem entre testes, que de outro modo só aparece quando alguém acrescenta um teste no lugar errado.
5. **O resultado é publicado por teste** — relatório no formato que a plataforma mostra no PR/MR, mesmo quando falha —, para que o revisor veja qual comportamento quebrou sem abrir o log.
6. **Cobertura, quando medida, é informação para quem revisa, não porteiro.** Mostrar no PR/MR as linhas novas sem teste ajuda a revisão; exigir percentual produz o teste que existe para contar (Seção *O que testar*).

## 6. Pedir testes a um agente

Escrever testes é dos melhores usos de um agente: é trabalho volumoso, repetitivo e verificável. O que exige disciplina é a revisão, porque um teste ruim é pior que nenhum — ele dá confiança falsa e ninguém olha de novo.

**Ao escrever testes a pedido**, o agente segue este protocolo:

1. Antes de escrever, lista o que o módulo faz, quais entradas são inválidas ou de limite e onde está a fronteira com o que é externo (hardware, serviço, arquivo), e espera confirmação.
2. Não altera o código de produção na mesma tarefa: comportamento que parecer errado é relatado, não "consertado".
3. Prova que cada teste detecta defeito: quebra de propósito a função sob teste (inverte uma comparação, devolve constante, comenta uma linha), mostra o teste falhando, desfaz e mostra passando.
4. No resumo, aponta todo teste que continuou passando com a função quebrada.

**O que procurar ao revisar teste gerado por agente** — os modos de falha são específicos e se repetem:

- **Teste tautológico**: afirma o que o código faz hoje, inclusive o defeito. O antídoto é o teste de mutação manual do item 3 do protocolo acima. Teste que continua verde vai fora, não é corrigido.
- **Só caminho feliz**, com os casos de erro ausentes ou marcados como "não aplicável".
- **Dublê em tudo**: a suíte prova que as funções foram chamadas, não que o comportamento está certo.
- **Asserção frouxa** — "não é nulo", "não travou", "retornou algo".
- **A lógica reimplementada na asserção**: se o teste calcula o valor esperado do mesmo jeito que o código, os dois erram juntos e o teste passa.
- **Valor esperado copiado da saída atual.** O valor esperado vem da spec, do contrato no header ou da folha de dados — nunca do que o programa imprimiu.

**Teste não se ajusta para a mudança passar.** Se um sensor ficou vermelho, o defeito é do código até prova em contrário; alterar a asserção só é legítimo quando o comportamento esperado mudou de propósito, e então a alteração aparece no diff e no resumo da mudança, com o motivo.

**Código legado que vai ser alterado** recebe antes um teste de caracterização: ele captura o comportamento atual — sem afirmar que está certo — para que a refatoração prove que não mudou nada. Marque-o como caracterização, para que ninguém o leia como especificação.

## Checklist deste domínio

- [ ] Comportamento novo ou alterado tem teste na mesma mudança, ou a ausência está declarada no resumo com o motivo.
- [ ] Todo teste novo foi visto falhando antes de passar; defeito corrigido tem teste de regressão.
- [ ] Teste unitário não toca disco, rede, hardware nem relógio real, e não tem lógica além da tabela de casos.
- [ ] Teste novo é descoberto pelo build e roda no CI em todo push; a suíte vazia reprova.
- [ ] Há teste para caso de erro e de limite, não só para o caminho nominal.
- [ ] Nenhum teste verifica estado interno, depende de ordem, de relógio real ou de espera.
- [ ] Nenhuma asserção foi ajustada para acomodar o comportamento atual do código.
- [ ] Teste gerado por agente passou pela quebra proposital da função sob teste.
