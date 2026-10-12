# Domínio: testes em firmware

Cobre o que muda nos testes quando o código é firmware: a ordem de retorno do que testar, a costura que permite testar a lógica no PC sem o hardware e os sensores que o host dá junto. As regras gerais de sensores e de como escrever um teste estão em [testes.md](testes.md); a separação de camadas que habilita tudo isto, em [firmware.md](firmware.md), Seção *Camadas e portabilidade*; presets e flags, em [c-build-e-analise.md](c-build-e-analise.md).

**Aplica-se a:** firmware embarcado e código C para microcontrolador.
**Leia quando:** for decidir o que testar num firmware, abrir a costura entre lógica e hardware, montar o preset de teste em host ou testar código que depende de tempo.

## 1. O que testar primeiro

Em firmware o esforço não se distribui por igual. Na ordem de retorno:

1. **Lógica pura, sem hardware** — análise e montagem de quadros de protocolo, cálculo e conversão de unidade, validação de faixa, máquina de estado, filtro, buffer circular, verificação de integridade. É barata de testar e é onde estão os defeitos que o teste pega e a bancada não: quadro truncado, tamanho declarado maior que o buffer, estouro de contador, transição que ninguém exercitou.
2. **Módulos que tocam hardware por uma interface pequena**, com a costura aberta (Seção *A costura*).
3. **O que depende de tempo real, ruído elétrico ou do periférico em si** permanece validação em bancada, declarada conforme [testes.md](testes.md), Seção *O que testar*.

**Não se testa** a HAL do fabricante, o compilador, nem função de acesso trivial.

**Num projeto sem nenhum teste**, o primeiro passo é um preset de host que compile e rode ([c-build-e-analise.md](c-build-e-analise.md), Seção *Sensores da linguagem*); daí em diante, vale o caminho de [testes.md](testes.md), Seção *O que testar*.

## 2. A costura

**Costura** é a fronteira onde a implementação de hardware pode ser trocada por um dublê sem que a lógica saiba.

1. **Prefira substituição em tempo de link.** A aplicação chama `uart_enviar()`; existem dois arquivos que a implementam — um para o alvo, um dublê para o host — e o preset do build escolhe qual entra. Não custa nada em execução, não usa macro e não muda o código de produção.
2. **Ponteiro de função só quando a troca precisa acontecer em execução** — ele tem preço em análise ([../templates/modulo-c.md](../templates/modulo-c.md)).
3. **Compilação condicional não é costura.** `#if TESTE` espalhado pelo módulo cria dois códigos diferentes: o que você testa não é o que embarca.
4. **A base de tempo é a costura mais valiosa.** Com `agora_ms()` substituível, um teste de tempo limite de 30 segundos roda em microssegundos e verifica o instante exato da transição. Sem ela, o teste dorme — e teste que dorme ninguém roda.
5. **Módulo com estado tem função de reinicialização** chamada antes de cada teste. Teste que só passa numa ordem é defeito do teste, e some por conta própria quando alguém acrescenta outro.

## 3. Sensores que o host dá junto

Rodar a suíte em host com os sanitizers ligados ([c-build-e-analise.md](c-build-e-analise.md), Seção *Sensores da linguagem*) transforma cada teste também em detector de estouro de buffer e de comportamento indefinido — o defeito que no alvo aparece como travamento aleatório.

## Checklist deste domínio

- [ ] Lógica nova de aplicação tem teste em host, sem hardware.
- [ ] A costura é por substituição em tempo de link; nenhum `#if TESTE` entrou no código de produção.
- [ ] Código que depende de tempo usa a base de tempo substituível; nenhum teste dorme.
- [ ] Módulo com estado testado tem função de reinicialização chamada antes de cada teste.
- [ ] O que só se valida em bancada está declarado como tal no resumo da mudança.
