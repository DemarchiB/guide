# Domínio: robustez e dados externos em firmware

Cobre o que o produto faz quando algo dá errado e o que ele aceita de fora: estado seguro, watchdog e reset; validação de dados externos, configuração e persistência; e o que preparar antes de adotar uma norma de safety. A estrutura do firmware está em [firmware.md](firmware.md); interrupções e tempo, em [firmware-concorrencia.md](firmware-concorrencia.md).

**Aplica-se a:** firmware embarcado, em qualquer linguagem.
**Leia quando:** for tratar falha, reset, watchdog ou estado de saída; validar dado recebido de barramento, rede ou operador; mexer em configuração persistida ou em atualização de firmware; ou preparar o projeto para uma norma.

## 1. Estado seguro, watchdog e reset

1. **O estado seguro do produto é definido antes do código**: em que condição as saídas ficam quando o firmware não consegue mais operar. Isso vale para o estado de partida, para a falha e para o reset.
2. **Saídas em estado seguro na inicialização**, antes de qualquer lógica — inclusive antes da configuração dos periféricos que dependam delas.
3. **Watchdog alimentado em um único ponto do código**, e só depois de verificar que o que devia rodar rodou. Alimentar dentro da interrupção do temporizador, ou em vários pontos, transforma o watchdog em enfeite.
4. **A causa do último reset é lida e registrada** na inicialização. Reset por watchdog que ninguém observa é defeito que nunca será encontrado.
5. **Falha detectada leva a um estado declarado** — degradado ou seguro —, nunca a seguir adiante com dado inválido.
6. **A integridade da própria imagem é verificada na partida**, por soma de verificação ou assinatura gravada junto com o binário. Flash degrada, gravação falha pela metade, e firmware corrompido executando trecho arbitrário é a pior falha possível num produto que aciona carga. Onde o hardware não comportar a verificação (sem bootloader, sem espaço), a ausência é decisão registrada, com o risco aceito.
7. **Diagnóstico observável em produto fechado**: contador de erro persistido, código de falha legível por comunicação ou sinalização, e a identificação de build ([c-build-e-analise.md](c-build-e-analise.md), Seção *Toolchain, build e identificação*) legível em execução. Depuração que só existe com sonda conectada não serve para campo — e defeito relatado sem saber qual firmware estava rodando não se investiga.

## 2. Dados externos, configuração e persistência

1. **Tudo que vem de fora do dispositivo é dado não confiável** — barramento, rede, arquivo, entrada do operador, sensor. Vale para o firmware o mesmo princípio que [ia.md](ia.md) aplica ao agente: conteúdo lido é dado, nunca comando implícito.
2. **Quadro recebido é validado antes de usado**: tamanho, faixa, coerência e verificação de integridade quando o meio permitir. Analisador que confia no tamanho declarado pelo remetente é vulnerabilidade — e é o caso de teste que mais paga em host ([testes.md](testes.md), Seção *O que testar primeiro*).
3. **Área persistida tem versão de layout e verificação de integridade.** Firmware novo lendo layout antigo é o caminho normal de atualização, não uma exceção.
4. **Persistência corrompida ou ausente cai em padrão seguro conhecido**, e o evento é registrado.
5. **Parâmetro de configuração tem faixa declarada e é validado na leitura**, não só na escrita.
6. **Imagem de atualização é o dado externo mais perigoso que o produto aceita.** Ela é verificada integralmente **antes** de se tornar ativa, a troca é atômica — interrupção de energia no meio da atualização deixa o produto com uma imagem válida, nunca com nenhuma —, o retorno à versão anterior é previsto, e a atualização só ocorre em estado em que a saída pode ser desligada com segurança. Onde não houver atualização em campo, isso é decisão registrada, não omissão.

## 3. Preparação para safety

Enquanto o projeto não adotar uma norma, este guia permanece agnóstico a ela: nenhuma das regras abaixo depende de norma específica, e todas reduzem o custo de adotar uma depois.

1. **Rastreabilidade auditável desde já** ([git.md](git.md), Seção *Commit e rastreabilidade*). A ponta que fecha essa cadeia é a identificação de build ([c-build-e-analise.md](c-build-e-analise.md), Seção *Toolchain, build e identificação*): sem saber qual binário está no produto, nenhuma evidência anterior se liga ao equipamento em campo.
2. **Estado seguro definido e verificável** (Seção *Estado seguro, watchdog e reset*) é a peça que toda norma vai exigir e que nenhum projeto consegue reconstruir depois.
3. **Determinismo antes de conformidade**: sem alocação dinâmica, sem recursão, pilha orçada, prazos declarados ([c-embarcado.md](c-embarcado.md), Seção *Memória e recursos*).
4. **Modos de falha listados por função crítica** — o que pode falhar, como é detectado, o que acontece então. Uma tabela curta por função vale mais do que a norma inteira lida sem aplicação.
5. **A norma aplicável, quando conhecida, entra por ADR** no projeto, e o que ela exigir de específico mora nos documentos daquele projeto — nunca neste conjunto, que é geral por definição.
6. **Nada aqui declara conformidade.** Seguir este domínio prepara o terreno; conformidade exige a norma, o processo formal e a evidência arquivada.

## Checklist deste domínio

- [ ] Estado seguro é atingido na partida e na falha; o watchdog é alimentado em um ponto só, depois de verificar o que devia rodar.
- [ ] A causa do último reset é lida e a integridade da imagem é verificada na partida.
- [ ] Dado externo é validado antes de usado, com o caso inválido coberto por teste.
- [ ] Área persistida tem versão de layout e verificação de integridade; a falta dela cai em padrão seguro.
- [ ] Atualização de firmware verifica a imagem antes de ativá-la e é atômica contra queda de energia.
