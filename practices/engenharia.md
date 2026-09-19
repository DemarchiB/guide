# Domínio: engenharia e qualidade

Cobre como uma mudança é conduzida do início ao fim e o que se exige dela em qualquer projeto: incrementos verificáveis, segredos, dependências, submódulos, arquivos gerados e o resumo final. Branch, commit e integração estão em [git.md](git.md); sensores e testes, em [testes.md](testes.md); o que o agente observa a mais, em [ia.md](ia.md).

**Aplica-se a:** todo projeto.
**Leia quando:** for iniciar, conduzir ou encerrar uma mudança.

## 1. Processo de uma mudança

Vale para pessoa e agente.

1. **Entender**: objetivo e critério de sucesso, áreas afetadas, risco, se envolve código gerado, submódulo ou dependência externa, e quais validações existem. Leia o que se aplica à área e rastreie as interfaces afetadas.
2. **Planejar na medida da mudança**: mudança trivial vai direto; mudança não trivial ganha um plano antes da primeira edição ([ia.md](ia.md), Seção *Plano antes da primeira edição*); funcionalidade maior ganha spec ([specs.md](specs.md)).
3. **Implementar em incrementos verificáveis**: cada incremento é uma alteração coesa seguida do sensor mais barato que a verifica. Erro encontrado logo depois de uma alteração pequena tem causa óbvia; o mesmo erro depois de vinte alterações vira investigação. Mudança mínima, no estilo e nas abstrações existentes, sem refatoração não relacionada; ao mover arquivos, atualize todas as referências.
4. **Validar**: sensores do mais específico ao mais amplo ([testes.md](testes.md), Seção *Conjunto mínimo de sensores*); para mudança só documental, inspeção do diff e verificação de links. O que não puder ser executado é registrado com o motivo.
5. **Documentar**: uma passada, com o comportamento já estável e verificado ([../manutencao.md](../manutencao.md), Seção *Quando e como atualizar*).
6. **Encerrar com o resumo da mudança** (abaixo).

## 2. Resumo da mudança

Toda mudança termina com um resumo curto, escrito para quem vai revisar sem ter acompanhado o trabalho. É a resposta final do agente, a descrição do PR/MR e a base do corpo do commit — o mesmo texto, não três.

```markdown
**Principais mudanças**
- <o que mudou e por quê, em termos de comportamento, estrutura ou regra — não uma lista de arquivos>

**Decisões e suposições**
- <o que foi decidido ou suposto sem confirmação, para quem revisa validar; omita se não houver>

**Verificação**
- Executado: <comandos e resultado>
- Não executado: <o que faltou e por quê>

**Pendências e riscos**
- <o que ficou para depois, o que pode quebrar, o que foi visto fora do escopo; omita se não houver>

**Arquivos**
- Criados / alterados / movidos / removidos: <lista curta; em mudança grande, agrupe por pasta>
```

O resumo diz a verdade sobre o estado: o que não foi verificado aparece como não verificado, e o que ficou pela metade aparece como pendente. "Pronto" sem verificação declarada não é pronto.

## 3. Segredos e dados sensíveis

1. Credencial, chave, token, certificado privado ou dado pessoal nunca vão para o repositório — nem em código, configuração, spec, ADR, exemplo ou log colado num documento.
2. O `.gitignore` faz parte do harness: cobre no mínimo artefatos de build, dependências instaladas, configuração local de máquina ou IDE, arquivos de ambiente (`.env` e equivalentes) e saídas de ferramenta. Mantê-lo correto é parte da tarefa que introduz o arquivo local — e ele nunca justifica guardar um segredo real dentro da pasta do projeto.
3. Documentação cita o **nome** da variável ou parâmetro, nunca o valor.
4. Segredo que chegou ao histórico é **rotacionado**. Apagar num commit seguinte não desfaz a exposição: o valor continua no histórico e em todo clone.
5. Dado de produção (log real, dump, base de clientes) não entra no repositório; use dado sintético.

## 4. Dependências

**Dependência nova precisa ser necessária, confiável e ter versão fixada.** Nome incomum é verificado contra o registro oficial antes de instalar — typosquatting e pacote inventado por agente são o mesmo ataque. A introdução de uma dependência é decisão da pessoa, não do agente.

## 5. Modificações estruturais

Antes de mover ou dividir componentes: identifique a responsabilidade de cada área, mapeie dependências de entrada e saída, localize imports, scripts, configurações, pipelines e documentação afetados, verifique caminhos codificados, preserve compatibilidade ou declare a migração, e atualize o `ARCHITECTURE.md` se limites mudarem.

Evite: mover arquivos sem atualizar consumidores; criar camada sem responsabilidade própria; duplicar utilitários; reorganizar código apenas para acomodar uma IA ou uma IDE.

## 6. Submódulos e arquivos gerados

**Todo submódulo é projeto externo por padrão** — inclusive `docs/guide/`. Não altere código, configuração ou documentação dentro dele, não crie `AGENTS.md`, `ARCHITECTURE.md` ou Skills nele, não assuma permissão para enviar alterações, e documente só a interface que o projeto principal usa. Mudança num submódulo acontece apenas quando pedida explicitamente, como trabalho separado no repositório dele.

**Antes de editar um arquivo, determine se ele é gerado** (cabeçalho de geração, diretório de saída, regra de build). Havendo gerador: altere a fonte, execute o processo oficial, revise todas as saídas — inclusive remoções — e valide os consumidores. Não simule à mão a saída de um gerador indisponível; registre a limitação.

## Checklist deste domínio

- [ ] A mudança foi implementada em incrementos, cada um verificado pelo sensor mais barato que se aplica.
- [ ] Os sensores existentes foram executados e o resultado declarado; os ausentes viraram pendência, nunca "verificado manualmente" sem dizer como.
- [ ] Nenhum segredo, credencial ou dado de produção entrou no diff.
- [ ] Dependência nova foi decidida por uma pessoa, é verificável no registro oficial e tem versão fixada.
- [ ] Nenhum submódulo foi alterado sem pedido explícito; arquivo gerado foi alterado pela fonte.
- [ ] A mudança terminou com o resumo da Seção *Resumo da mudança*, incluindo o que não foi verificado.
