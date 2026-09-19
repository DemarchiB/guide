# Domínio: sensores e testes

Cobre o que verifica uma mudança automaticamente: o conjunto mínimo de sensores, o que vale a pena testar num firmware, como abrir a costura que torna o teste possível, como se escreve um teste que detecta defeito, e como pedir e revisar teste escrito por um agente. A configuração da toolchain e do analisador está em [c-build-e-analise.md](c-build-e-analise.md); a separação de camadas que habilita tudo isto, em [firmware.md](firmware.md), Seção *Camadas e portabilidade*.

**Aplica-se a:** todo projeto.
**Leia quando:** for criar ou alterar teste ou sensor, decidir o que rodar antes de concluir uma mudança, ou pedir testes a um agente.

## 1. Conjunto mínimo de sensores

Uma **regra** orienta antes de agir; um **sensor** verifica depois, automaticamente, e detecta o erro que passou pela regra. Projeto que só tem regras depende de todo mundo lembrar de tudo.

Em ordem crescente de custo:

1. **Build** do módulo afetado.
2. **Teste direcionado** à mudança, ampliando para a suíte conforme o risco.
3. **Lint / análise estática** na configuração do próprio projeto.
4. **Documentação** — `python docs/guide/tools/verificar.py`: links, includes, seções citadas, Skills e trechos repetidos entre arquivos.
5. **Varredura de segredos** antes do commit.

Regras de uso:

- os sensores existentes rodam **antes** de declarar a tarefa concluída, e quem executou informa quais rodou;
- sensor que não existe é registrado como verificação pendente, com o motivo — nunca simulado nem presumido aprovado;
- sensor que falha bloqueia a conclusão: corrigir ou relatar, não seguir adiante;
- **sensor que fecha o laço é o que o agente roda sozinho**: um comando, sem IDE, sem hardware, resposta em segundos. Validação que exige bancada é validação de pessoa — legítima, declarada no resumo, mas não substitui o sensor;
- onde o ambiente permitir, sensores rodam sozinhos (hook de pré-commit, CI). Sensor que depende de alguém lembrar é regra.

**Por que este é o item de maior retorno ao trabalhar com IA.** Sem sensor, o agente precisa acertar de primeira, e acertar de primeira é o que se compra com modelo caro e revisão longa. Com sensor, ele erra, vê o vermelho e corrige sozinho — e o modelo barato passa a bastar para a maior parte do trabalho. Não é preciso ter suíte completa para mudar de regime: um punhado de testes que rodam em segundos sobre a lógica que mais quebra já muda.

## 2. O que testar primeiro

Em firmware o esforço não se distribui por igual. Na ordem de retorno:

1. **Lógica pura, sem hardware** — análise e montagem de quadros de protocolo, cálculo e conversão de unidade, validação de faixa, máquina de estado, filtro, buffer circular, verificação de integridade. É barata de testar e é onde estão os defeitos que o teste pega e a bancada não: quadro truncado, tamanho declarado maior que o buffer, estouro de contador, transição que ninguém exercitou.
2. **Módulos que tocam hardware por uma interface pequena**, com a costura da Seção *A costura* aberta.
3. **O que depende de tempo real, ruído elétrico ou do periférico em si** permanece validação em bancada — declarada como tal, nunca escondida atrás de "testado".

**Não se testa** a HAL do fabricante, o compilador, nem função de acesso trivial. **Cobertura não é meta**: perseguir percentual produz teste que existe para contar. A meta é caso de erro e caso de limite cobertos onde uma falha custa uma visita ao campo.

**Num projeto sem nenhum teste**, o caminho é: um preset de host que compile e rode ([c-build-e-analise.md](c-build-e-analise.md), Seção *Sensores da linguagem*); um módulo de lógica pura coberto de ponta a ponta; e daí em diante cada tarefa cobre a área que toca. Mutirão de testes produz suíte que ninguém entende. A escolha do arcabouço de teste é decisão do projeto, declarada no `AGENTS.md` e — por ser dependência nova — registrada conforme [engenharia.md](engenharia.md), Seção *Dependências*.

## 3. A costura

**Costura** é a fronteira onde a implementação de hardware pode ser trocada por um dublê sem que a lógica saiba.

1. **Prefira substituição em tempo de link.** A aplicação chama `uart_enviar()`; existem dois arquivos que a implementam — um para o alvo, um dublê para o host — e o preset do build escolhe qual entra. Não custa nada em execução, não usa macro e não muda o código de produção.
2. **Ponteiro de função só quando a troca precisa acontecer em execução** — ele tem preço em análise ([../templates/modulo-c.md](../templates/modulo-c.md)).
3. **Compilação condicional não é costura.** `#if TESTE` espalhado pelo módulo cria dois códigos diferentes: o que você testa não é o que embarca.
4. **A base de tempo é a costura mais valiosa.** Com `agora_ms()` substituível, um teste de tempo limite de 30 segundos roda em microssegundos e verifica o instante exato da transição. Sem ela, o teste dorme — e teste que dorme ninguém roda.
5. **Módulo com estado tem função de reinicialização** chamada antes de cada teste. Teste que só passa numa ordem é defeito do teste, e some por conta própria quando alguém acrescenta outro.

## 4. Escrever um teste

1. **Um comportamento por teste**, com nome que diz a condição e o resultado esperado: `quadro_truncado_retorna_erro`, não `teste_uart_2`. O nome do teste que falhou é a primeira informação do diagnóstico.
2. **Vermelho antes de verde.** Todo teste novo roda ao menos uma vez contra o código sem a correção, e falha. Teste que nunca falhou não provou nada — é a falha mais comum em teste gerado por agente, e a mais fácil de não perceber.
3. **Caso de erro e de limite antes do caminho feliz.** O caminho feliz costuma já funcionar; é o resto que quebra em campo.
4. **Verifique efeito, não implementação**: o que a função devolveu, o estado observável pela interface pública, a chamada que chegou ao dublê. Teste que espia variável interna quebra em toda refatoração e não detecta defeito nenhum.
5. **Dublê só na fronteira**, e o mais simples que resolver. Um fake de vinte linhas que guarda o que foi enviado vale mais que um mock que verifica a ordem das chamadas.
6. **Determinístico**: sem relógio real, sem espera, sem dependência de ordem, sem valor aleatório de semente variável.
7. **Entrada realista, inclusive a inválida**: quadro cortado no meio, comprimento declarado maior que o recebido, valor fora da faixa, contador exatamente no ponto de estouro, buffer cheio.
8. **A falha diz o que houve** — esperado e obtido no texto da asserção. Falha que só diz "asserção falhou na linha 74" custa uma sessão de depuração por vez que aparece.

**Sensores baratos que o host dá junto**: rodar a suíte com os sanitizers ligados ([c-build-e-analise.md](c-build-e-analise.md), Seção *Sensores da linguagem*) transforma cada teste também em detector de estouro de buffer. Onde o espaço de entrada for pequeno (um byte de comando, por exemplo), varra todos os valores em vez de escolher três.

## 5. Pedir testes a um agente

Escrever testes é dos melhores usos de um agente: é trabalho volumoso, repetitivo e verificável. O que exige disciplina é a revisão, porque um teste ruim é pior que nenhum — ele dá confiança falsa e ninguém olha de novo.

Pedido pronto (ajuste o que está entre `<>`):

```text
Escreva testes em host para <módulo>, seguindo docs/guide/practices/testes.md.
- Antes de escrever, liste o que o módulo faz, quais entradas são inválidas ou
  de limite, e onde está a fronteira com o hardware. Espere minha confirmação.
- Um comportamento por teste; casos de erro e de limite antes do caminho feliz.
- Não altere o código de produção nesta tarefa. Se um comportamento parecer
  errado, relate — não "conserte".
- Depois de escrever, prove que cada teste detecta defeito: quebre a função sob
  teste de propósito, mostre o teste falhando, desfaça e mostre passando.
- No resumo, aponte todo teste que continuou passando com a função quebrada.
```

**O que procurar ao revisar teste gerado por agente** — os modos de falha são específicos e se repetem:

- **Teste tautológico**: afirma o que o código faz hoje, inclusive o defeito. O antídoto é o teste de mutação manual do pedido acima — quebre a função de propósito (inverta uma comparação, devolva constante, comente uma linha) e rode. Teste que continua verde vai fora, não é corrigido.
- **Só caminho feliz**, com os casos de erro ausentes ou marcados como "não aplicável".
- **Dublê em tudo**: a suíte prova que as funções foram chamadas, não que o comportamento está certo.
- **Asserção frouxa** — "não é nulo", "não travou", "retornou algo".
- **A lógica reimplementada na asserção**: se o teste calcula o valor esperado do mesmo jeito que o código, os dois erram juntos e o teste passa.
- **Valor esperado copiado da saída atual.** O valor esperado vem da spec, do contrato no header ou da folha de dados — nunca do que o programa imprimiu.

**Teste não se ajusta para a mudança passar.** Se um sensor ficou vermelho, o defeito é do código até prova em contrário; alterar a asserção só é legítimo quando o comportamento esperado mudou de propósito, e então a alteração aparece no diff e no resumo da mudança, com o motivo.

**Código legado que vai ser alterado** recebe antes um teste de caracterização: ele captura o comportamento atual — sem afirmar que está certo — para que a refatoração prove que não mudou nada. Marque-o como caracterização, para que ninguém o leia como especificação.

## Checklist deste domínio

- [ ] Todo teste novo foi visto falhando antes de passar.
- [ ] Há teste para caso de erro e de limite, não só para o caminho nominal.
- [ ] Nenhum teste verifica estado interno, depende de ordem, de relógio real ou de espera.
- [ ] Nenhuma asserção foi ajustada para acomodar o comportamento atual do código.
- [ ] Teste gerado por agente passou pela quebra proposital da função sob teste.
