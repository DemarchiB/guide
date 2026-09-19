# Template: `README.md`

**Quando usar:** no dia zero de qualquer projeto. É um dos três documentos obrigatórios.

**Papel:** apresentar o projeto a pessoas e ferramentas pela primeira vez — propósito, pré-requisitos, caminho inicial de uso, links para a documentação detalhada. Não é inventário arquitetural.

**Convenções:** link para documento que ainda não existe fica fora do arquivo, em vez de virar link quebrado. Comando ainda não verificado entra com a marcação de estado provisório. Como o conjunto é submódulo, o primeiro comando de quem clona precisa trazê-lo.

````markdown
# <nome do projeto>

<Uma a três linhas: o que é e para quem serve.>

## Pré-requisitos
- <toolchain, versão, sistema operacional, hardware>

## Como começar
```
git clone --recurse-submodules <url>
<comando de configuração>
<comando de build>
<comando de execução ou teste>
```

## Documentação
- Arquitetura: [ARCHITECTURE.md](ARCHITECTURE.md)
- Instruções para agentes de IA: [AGENTS.md](AGENTS.md)
- Convenções de projeto: [docs/guide/PROJECT_GUIDE.md](docs/guide/PROJECT_GUIDE.md)
- Workflow de revisão: [docs/workflow.md](docs/workflow.md)  <omita se o projeto não tiver este arquivo>

## Licença
<licença ou "uso interno">
````
