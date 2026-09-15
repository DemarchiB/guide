# Prática: Skills e adaptadores de ferramentas de IA

Cobre procedimentos reutilizáveis, Skills, subagentes e arquivos que uma ferramenta específica precisa para consumir as instruções canônicas. O trabalho normal do agente está em [ia.md](ia.md); este arquivo só é lido quando o workflow de ferramenta se aplica.

**Aplica-se a:** todo projeto que mantém Skills, subagentes ou adaptadores de ferramenta de IA.
**Leia quando:** for criar, usar ou manter uma Skill ou subagente, configurar uma ferramenta de IA, ou revisar um adaptador.

## 1. Skills: criar, usar e manter

Uma **Skill** é um procedimento reutilizável — por exemplo, revisar uma mudança, corrigir um defeito, analisar memória ou preparar uma liberação. Só `name` e `description` ficam disponíveis para o acionamento; o corpo é carregado quando a tarefa pede. Formato: [template de Skill](../templates/skill.md) e especificação [Agent Skills](https://agentskills.io/specification).

1. **Crie a Skill a partir de um procedimento já executado**, não de um procedimento ideal imaginado. Registre o que precisou ser explicado ou corrigido.
2. **Aponte para as regras, não as repita.** O procedimento manda aplicar os checklists dos domínios; não copia seu conteúdo.
3. **Torne determinístico o que puder ser script**, em vez de deixar o agente reinterpretar cada passo.
4. **Teste o acionamento** numa sessão nova com um pedido que deve ativar a Skill e outro parecido que não deve.
5. **Use a Skill quando o pedido corresponder a ela**; não improvise outro procedimento nem repita seu corpo no prompt.
6. **Mantenha-a junto com o procedimento.** Mudança de comando, caminho, ferramenta ou ordem exige atualizar a Skill; desvio recorrente é defeito a corrigir.
7. **Remova Skills sem uso** ou cujo procedimento o agente execute bem sem instrução; cada `description` custa contexto na descoberta.
8. **Rode `python docs/guide/tools/verificar.py`** depois de criar, renomear ou alterar uma Skill ou adaptador.

## 2. Adaptadores de ferramenta

O repositório tem uma fonte de instruções (`AGENTS.md`) e um lugar canônico para Skills (`.agents/skills/`). Ferramenta que não consome esses formatos recebe um adaptador somente se estiver em uso; regra do projeto nunca fica apenas no adaptador.

1. Prefira, nesta ordem: configuração apontando para a fonte canônica; arquivo da ferramenta que inclui a fonte; link simbólico quando sobreviver ao clone; stub textual como último recurso.
2. Stub de Skill repete somente `name` e `description` da Skill canônica e aponta o corpo para `.agents/skills/<nome>/SKILL.md`. O verificador confere a igualdade.
3. Subagente é adaptador quando o isolamento importar — por exemplo, revisão sem escrita ou investigação que consumiria o contexto principal — e segue a Skill correspondente.
4. Regra por caminho é ponteiro para o domínio aplicável, nunca cópia dele.
5. Configuração que muda o que o agente pode executar é versionada e revisada como código: comandos permitidos/negados, integrações e diretórios. Segredos nessa configuração seguem [engenharia.md](engenharia.md), Seção *Segredos e dados sensíveis*; documenta-se o nome da variável, nunca o valor.

## Checklist deste guia

- [ ] A Skill nasceu de procedimento observado, tem acionamento testado e descreve um critério de conclusão.
- [ ] O corpo aponta para regras canônicas sem copiá-las.
- [ ] O adaptador só existe para ferramenta em uso e referencia a fonte correta.
- [ ] `python docs/guide/tools/verificar.py` passou.
- [ ] Configuração de permissão está versionada sem segredo.
