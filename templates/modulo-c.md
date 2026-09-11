# Template: módulo em C (`<modulo>.h` + `<modulo>.c`)

**Quando usar** — o módulo tem **estado** e pode existir em mais de uma instância, ou pode vir a existir: um canal de comunicação, um eixo, um sensor, um temporizador de software, uma máquina de estado. O par de arquivos abaixo dá a esse módulo a forma de classe: atributos numa estrutura, operações com prefixo do módulo, e um ponteiro `me` para a instância como primeiro parâmetro.

**Quando não usar:**

- **Módulo sem estado** — conversão, tabela de consulta, cálculo puro. Ele é um conjunto de funções com prefixo; forçar uma estrutura vazia e um `me` que ninguém usa só acrescenta ruído.
- **Recurso físico único** (um periférico que existe uma vez no produto). O estado pode ser `static` no `.c`, com as operações sem `me`. Se houver chance real de virar dois, comece com instância — converter depois toca todos os chamadores.

**Convenções:**

1. **Um par de arquivos por módulo**, com o mesmo nome do tipo. Todo símbolo público leva o prefixo do módulo, e o projeto escolhe uma convenção de caixa e a mantém.
2. **`me` é o primeiro parâmetro**, sempre `<Tipo> *const me` — o ponteiro é constante, o objeto não. Nunca use `this`: é palavra reservada em C++ e quebra o dia em que o header for incluído de lá.
3. **Os campos da estrutura são privados por convenção.** Só as operações do próprio módulo os tocam; nenhum chamador acessa `objeto.campo` diretamente. C não impõe isso — a revisão impõe.
4. **Todo campo é documentado com unidade e faixa**, do mesmo modo que os parâmetros ([practices/c-embarcado.md](../practices/c-embarcado.md), Seção *Estrutura, nomes e interface*).
5. **O construtor valida e retorna erro.** `_init` verifica `me` e os parâmetros e devolve o tipo de erro do projeto; construtor `void` obriga o chamador a supor que deu certo.
6. **O destrutor só existe se tiver o que fazer** — levar saída a estado seguro, liberar um recurso de hardware, cancelar um temporizador. Sem alocação dinâmica ([practices/c-embarcado.md](../practices/c-embarcado.md), Seção *Memória e recursos*), `_deinit` vazio é ruído: remova-o em vez de mantê-lo por simetria.
7. **A guarda de inclusão não usa identificador reservado** — `MODULO_H`, nunca `__MODULO_H__` ([practices/c-embarcado.md](../practices/c-embarcado.md), Seção *Estrutura, nomes e interface*).
8. **Nada de `@version`, `@date` nem `@author` no cabeçalho do arquivo.** Envelhecem no primeiro commit que alguém esquece de atualizar, e a informação verdadeira já está no VCS e na identificação de build ([practices/c-build-e-analise.md](../practices/c-build-e-analise.md), Seção *Toolchain, build e identificação*). Cabeçalho registra o que não está no VCS: arquivo, responsabilidade e copyright.
9. **O header inclui só o que a interface precisa** e é incluível por C++ (`extern "C"`), para o teste em host. O que só a implementação usa fica no `.c`.

## Esqueleto

Os comentários de seção organizam a leitura de arquivos longos; em módulo pequeno, **remova as seções que ficarem vazias** — banner sem conteúdo é ruído que se repete em todo arquivo.

```c
/* ------------------------------- <modulo>.h ------------------------------- */
/**
 * @file <modulo>.h
 * @brief <responsabilidade do módulo, em uma linha>
 * @copyright <empresa> (c) <ano>
 */

#ifndef <MODULO>_H
#define <MODULO>_H

/* Includes ------------------------------------------------------------------*/
#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

/* Defines -------------------------------------------------------------------*/

/* Enums ---------------------------------------------------------------------*/

/* Typedefs ------------------------------------------------------------------*/

/** Atributos da classe. Campos privados por convenção: apenas as operações
 *  deste módulo os acessam. */
typedef struct {
    uint32_t <campo>;   /**< <significado, unidade e faixa> */
} <Modulo>;

/* Macros --------------------------------------------------------------------*/

/* Exported variables --------------------------------------------------------*/

/* Class' public operations (methods) declarations ---------------------------*/

/**
 * @brief  Construtor: deixa o objeto pronto para uso.
 * @param  me    Ponteiro para o objeto; não pode ser nulo.
 * @param  <par> <significado, unidade e faixa válida>
 * @pre    <condição que deve valer antes da chamada, ou "—">
 * @return <ERR>_OK, ou <ERR>_PARAM se algum argumento for inválido.
 */
<err_t> <Modulo>_init(<Modulo> *const me, <tipo> <par>);

/**
 * @brief  Destrutor: leva o objeto e o recurso associado a estado seguro.
 * @param  me Ponteiro para o objeto; não pode ser nulo.
 */
void <Modulo>_deinit(<Modulo> *const me);

#ifdef __cplusplus
}
#endif

#endif /* <MODULO>_H */
```

```c
/* ------------------------------- <modulo>.c ------------------------------- */
/**
 * @file <modulo>.c
 * @brief <responsabilidade do módulo, em uma linha>
 * @copyright <empresa> (c) <ano>
 */

/* Private includes ----------------------------------------------------------*/
#include "<modulo>/<modulo>.h"

/* Private defines -----------------------------------------------------------*/

/* Private enums -------------------------------------------------------------*/

/* Private typedefs ----------------------------------------------------------*/

/* Private macros ------------------------------------------------------------*/

/* Private variables ---------------------------------------------------------*/

/* Exported variables --------------------------------------------------------*/

/* Class' private operations (methods) declaration ---------------------------*/

/* Class' public operations (methods) definition -----------------------------*/

<err_t> <Modulo>_init(<Modulo> *const me, <tipo> <par>)
{
    if ((me == NULL) || (<par inválido>)) {
        return <ERR>_PARAM;
    }

    me-><campo> = <valor inicial>;

    return <ERR>_OK;
}

void <Modulo>_deinit(<Modulo> *const me)
{
    if (me == NULL) {
        return;
    }

    /* <estado seguro do recurso associado> */
}

/* Class' private operations (methods) definition ----------------------------*/
```

## Polimorfismo, quando ele se justifica

Operação virtual em C é uma tabela de ponteiros para função — `const`, portanto em flash — apontada pelo primeiro campo da estrutura base. A derivada declara a base como **primeiro membro**, o que torna o ponteiro para a derivada convertível para a base:

```c
typedef struct Sensor Sensor;

/** Tabela de operações virtuais; uma instância const por implementação. */
typedef struct {
    <err_t> (*ler)(Sensor *const me, int32_t *const valor_mv);
    void    (*desligar)(Sensor *const me);
} SensorVtbl;

struct Sensor {
    const SensorVtbl *vptr;   /* sempre o primeiro campo */
    uint8_t canal;
};

/* Despacho: a chamada que o código cliente usa. */
static inline <err_t> Sensor_ler(Sensor *const me, int32_t *const valor_mv)
{
    return me->vptr->ler(me, valor_mv);
}

/* Derivada: a base é o primeiro membro. */
typedef struct {
    Sensor base;
    uint16_t ganho;
} SensorNtc;
```

**Duas regras de uso, e elas importam mais do que o mecanismo:**

- **Só introduza a tabela virtual quando existirem duas implementações reais hoje.** Uma implementação atrás de despacho indireto é custo sem benefício, e "vai que um dia" não é evidência. Um dublê de teste conta como segunda implementação quando o despacho é o que permite testar o cliente em host sem o hardware — mas, se a troca em tempo de link resolve (outro `.c` no build de teste), ela é mais simples e não custa análise.
- **Ponteiro para função tem preço em análise.** Ele quebra o grafo de chamadas estático, e com ele a análise automática de profundidade de pilha e a rastreabilidade de qual código roda em qual caminho — exatamente o que uma norma de safety vai querer ver ([practices/firmware.md](../practices/firmware.md), Seção *Preparação para safety*). Onde o polimorfismo for usado em código crítico, a tabela é `const`, o conjunto de implementações é fechado e conhecido em tempo de compilação, e o `vptr` é verificado contra nulo antes do primeiro despacho.

## Exemplo preenchido (ilustrativo)

```c
/* ------------------------------- motor.h ---------------------------------- */
/**
 * @file motor.h
 * @brief Controle de um eixo: partida, parada e leitura de corrente.
 * @copyright <empresa> (c) 2026
 */

#ifndef MOTOR_H
#define MOTOR_H

#include <stdint.h>
#include <stdbool.h>

#include "erro/erro.h"

#ifdef __cplusplus
extern "C" {
#endif

typedef struct {
    uint8_t  canal;             /**< Canal de acionamento, 0 a 3. */
    uint16_t corrente_max_ma;   /**< Limite de corrente, em mA, 0 a 20000. */
    uint32_t partida_ms;        /**< Instante da última partida, base monotônica. */
    bool     ligado;            /**< Estado atual da saída. */
} Motor;

/**
 * @brief  Construtor: associa o objeto a um canal e define o limite de corrente.
 * @param  me              Ponteiro para o objeto; não pode ser nulo.
 * @param  canal           Canal de acionamento, 0 a 3.
 * @param  corrente_max_ma Limite de corrente em mA, 1 a 20000.
 * @pre    O canal já foi configurado pela camada de hardware.
 * @return ERRO_OK, ou ERRO_PARAM se algum argumento estiver fora da faixa.
 */
erro_t Motor_init(Motor *const me, uint8_t canal, uint16_t corrente_max_ma);

#ifdef __cplusplus
}
#endif

#endif /* MOTOR_H */
```

Repare no que o exemplo carrega e o esqueleto vazio não mostra: toda grandeza traz a unidade no nome, todo campo e todo parâmetro trazem a faixa, e a pré-condição diz o que precisa ter acontecido antes. É esse trio que transforma a regra "valide a entrada externa" em algo que dá para conferir numa revisão — e que, mais tarde, é a evidência que uma norma pede sem que ninguém tenha que reconstruí-la.
