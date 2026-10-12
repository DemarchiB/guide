# Template: contexto pessoal (`contexto/sobre-mim.md`)

**Quando criar:** ao montar o primeiro agente no nível 2 ([agentes-pessoais.md](../agentes-pessoais.md), Seção *Nível 2 — assistente com contexto*).

**Papel:** o que uma IA precisa saber sobre você para que qualquer agente acerte sem que você se repita. Escrito uma vez e colado nas instruções persistentes, depois das práticas gerais e antes do agente. Não descreve tarefa nenhuma: o que um agente faz fica no agente.

**Convenções:**

- **Curto — entre 150 e 400 palavras.** Cada linha vai em toda conversa, e contexto demais compete com a tarefa.
- **Só o que muda uma resposta.** O teste de cada linha: algum agente erraria sem isto? Biografia, gostos e histórico profissional quase nunca passam.
- **Pessoas por nome e papel, nada além.** "Ana — financeiro, aprova notas" ajuda a triar e-mails; telefone, endereço e opinião sobre a pessoa não entram.
- **Nunca entra:** senha, número de documento, dado de saúde, de finanças ou de família, endereço — pelo motivo de [agentes-pessoais.md](../agentes-pessoais.md), Seção *Nível 2 — assistente com contexto*.
- **Um contexto por repositório.** No repositório de uma empresa, o contexto é o profissional daquela empresa; no pessoal, nada que seja da empresa.

```markdown
# Sobre mim

## Papel
<Cargo e área; o que entrego; para quem.>

## Prioridades
<O que importa mais agora; o que pode esperar.>

## Como prefiro as respostas
<Idioma, tamanho, formato, tom. O que evitar.>

## Pessoas frequentes
- <Nome> — <papel na relação com você>

## Termos e siglas
- <Sigla> — <significado no seu contexto>
```

## Exemplo preenchido (ilustrativo)

```markdown
# Sobre mim

## Papel
Analista de compras numa indústria de médio porte. Negocio com fornecedores
e acompanho pedidos; não aprovo pagamentos.

## Prioridades
Pedidos atrasados da linha de produção primeiro; cotações novas podem
esperar até o fim do dia.

## Como prefiro as respostas
Português. Curtas, com o ponto principal na primeira frase. Listas só quando
há mais de três itens. Valores sempre em reais.

## Pessoas frequentes
- Ana — financeiro; aprova notas de serviço.
- Carlos — fornecedor principal de embalagens.

## Termos e siglas
- PC — pedido de compra.
- SLA — prazo de entrega combinado com o fornecedor.
```
