# Convenções de projeto

Conjunto de convenções que os projetos adotam em `docs/guide/`, para que uma pessoa ou um agente de IA entre em qualquer um deles e saiba onde procurar, onde escrever e como trabalhar. Este repositório **não é um projeto**: é o que os projetos seguem.

> Chegou aqui por `docs/guide/README.md` dentro de um projeto? Este é o README do conjunto de convenções; o do projeto está na raiz dele.

## Por onde começar

| Você vai... | Leia |
| --- | --- |
| adotar o conjunto num projeto | [`adocao.md`](adocao.md) |
| trabalhar num projeto que já adotou | [`PROJECT_GUIDE.md`](PROJECT_GUIDE.md) — curto; diz o que mais ler |
| alterar **este** conjunto | [`manutencao-do-conjunto.md`](manutencao-do-conjunto.md) e [`AGENTS.md`](AGENTS.md) |

Adoção em uma linha (detalhes e consequências em `adocao.md`):

```sh
git submodule add https://github.com/DemarchiB/guide.git docs/guide
```

## Estrutura

```text
PROJECT_GUIDE.md            ponto de entrada: precedência, regras invioláveis, o que ler em cada tarefa
adocao.md                   montar o conjunto, documentos do dia zero, atualizar o conjunto num projeto
estrutura.md                onde cada informação mora no projeto
manutencao.md               como a documentação do projeto se mantém verdadeira
manutencao-do-conjunto.md   como este conjunto evolui
practices/                  domínios e guias de apoio carregados sob demanda
templates/                  um arquivo por documento que o projeto cria
tools/verificar.py          verificador: links, includes, seções citadas, Skills e gitlinks externos
```

Os arquivos de `practices/` são divididos pelo **gatilho de leitura**: cada tarefa carrega um arquivo pequeno, não um domínio inteiro. Só o `PROJECT_GUIDE.md` é lido em toda tarefa.

## Como evolui

Sem número de versão nem changelog: o estado adotado é o commit do submódulo, e cada commit que exige ação de quem já adotou traz um trailer `Impacto-adocao` dizendo qual. Detalhes em [`manutencao-do-conjunto.md`](manutencao-do-conjunto.md).

Conteúdo em português (pt-BR). Uso interno.
