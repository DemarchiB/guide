# Template: scripts de etapa e pipeline de CI

**Quando usar:** ao criar os scripts que executam as etapas de verificação de um projeto, o pipeline de CI que os chama ou a imagem em que eles rodam. As regras são de [practices/ci.md](../practices/ci.md); este arquivo dá a forma.

**Papel:** ponto de partida para projeto em C com CMake, scripts em PowerShell 7 rodando em Windows e Linux e CI em contêiner Linux. Os nomes de preset, de imagem e de grupo são ilustrativos; o projeto ajusta e registra os comandos reais no `AGENTS.md` e o que roda no CI no `docs/workflow.md`.

**Convenções:**

1. **Um script por etapa em `scripts/`**, com o nome da etapa. O mesmo nome é o nome do job no pipeline — quem lê a falha no CI sabe qual comando rodar no PC. Nomes padronizados entre projetos: `build` (job `build-<alvo>`), `teste-host`, `analise`, `docs`, `segredos`, `liberar` (job `liberacao`) e `verificar`, que roda as etapas independentes juntas; estágios `verificar` e `liberar`. Etapa que não existir no projeto fica fora, não com outro nome.
2. **Todo script começa igual**: versão mínima declarada, parada na primeira falha, inclusive de comando externo. Sem isso, um `cmake` que falha no meio é seguido pelo próximo comando, e o script termina com sucesso.
3. **Cada etapa escreve em `build/<preset>`**, e o que ela entrega para outra etapa ou para quem diagnostica fica ali.
4. **A imagem é fixada por versão** em todos os jobs, e a mesma referência aparece no comando de reproduzir no PC.
5. **A exigência de pipeline verde para integrar é configurada na plataforma**: no GitLab, *Pipelines must succeed* nas verificações de merge e as branches protegidas; no GitHub, regra de proteção da branch com *Require status checks to pass*, marcando os jobs abaixo.

## Scripts

```text
scripts/
├── build.ps1        build de um preset do alvo: pwsh scripts/build.ps1 -Preset alvo-release
├── teste-host.ps1   build e testes do preset de host, com sanitizers
├── analise.ps1      analisador estático
└── verificar.ps1    roda as etapas independentes em paralelo, como o pipeline
```

`scripts/build.ps1`:

```powershell
#Requires -Version 7.4
param([Parameter(Mandatory)][string]$Preset)
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true   # comando externo com saída != 0 encerra o script

cmake --preset $Preset
cmake --build --preset $Preset --parallel
```

`scripts/teste-host.ps1`:

```powershell
#Requires -Version 7.4
$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $true

cmake --preset host-teste
cmake --build --preset host-teste --parallel
# O relatório JUnit é gravado no diretório de build do preset (build/host-teste).
# --no-tests=error: suíte vazia reprova; --schedule-random: expõe dependência de ordem.
ctest --preset host-teste --parallel --schedule-random --no-tests=error `
      --output-on-failure --output-junit relatorio-teste.xml
```

`scripts/verificar.ps1` — o equivalente local do pipeline:

```powershell
#Requires -Version 7.4
# Roda as etapas independentes em paralelo. Cada uma escreve no próprio diretório
# e no próprio log; nenhuma depende do que outra deixou.
$ErrorActionPreference = 'Stop'
$logs = Join-Path $PSScriptRoot '..' 'build' 'logs'
New-Item -ItemType Directory -Force -Path $logs | Out-Null

$etapas = @(
    @{ Nome = 'build-alvo'; Script = 'build.ps1'; Argumentos = @('-Preset', 'alvo-release') }
    @{ Nome = 'teste-host'; Script = 'teste-host.ps1'; Argumentos = @() }
    @{ Nome = 'analise';    Script = 'analise.ps1';    Argumentos = @() }
)

$resultados = $etapas | ForEach-Object -ThrottleLimit 4 -Parallel {
    $script = Join-Path $using:PSScriptRoot $_.Script
    $log = Join-Path $using:logs "$($_.Nome).log"
    $argumentos = $_.Argumentos
    pwsh -NoProfile -File $script @argumentos *> $log
    [pscustomobject]@{ Etapa = $_.Nome; Ok = ($LASTEXITCODE -eq 0); Log = $log }
}

$resultados | Format-Table -AutoSize
if ($resultados.Ok -contains $false) { exit 1 }
```

O `-ThrottleLimit` evita que as etapas disputem a CPU a ponto de ficarem mais lentas do que em série; cada uma já usa vários núcleos com `--parallel`.

## GitLab: `.gitlab-ci.yml`

```yaml
# Cada job chama um script; a lógica fica nos scripts.
default:
  image: registry.gitlab.com/<grupo>/imagem-build:1.4.0   # versão fixa, nunca latest
  interruptible: true          # push novo na mesma branch cancela o pipeline anterior

workflow:
  rules:
    - if: $CI_PIPELINE_SOURCE == "merge_request_event"
    - if: $CI_COMMIT_BRANCH && $CI_OPEN_MERGE_REQUESTS
      when: never              # branch com MR aberto: roda só o pipeline do MR
    - if: $CI_COMMIT_BRANCH    # todo push, em qualquer branch
    - if: $CI_COMMIT_TAG

variables:
  GIT_SUBMODULE_STRATEGY: recursive   # docs/guide é submódulo

stages: [verificar, liberar]

# Jobs do mesmo estágio rodam em paralelo e até o fim, mesmo que um falhe.
build-alvo:
  stage: verificar
  script: pwsh -File scripts/build.ps1 -Preset alvo-release
  artifacts:
    paths: [build/alvo-release/*.elf, build/alvo-release/*.hex, build/alvo-release/*.map]
    expire_in: 2 weeks

teste-host:
  stage: verificar
  script: pwsh -File scripts/teste-host.ps1
  artifacts:
    when: always               # o relatório interessa justamente quando falha
    reports:
      junit: build/host-teste/relatorio-teste.xml
    expire_in: 2 weeks

analise:
  stage: verificar
  script: pwsh -File scripts/analise.ps1

docs:
  stage: verificar
  script: python3 docs/guide/tools/verificar.py

# Só em tag; needs declara de quem depende e de onde vêm os artefatos.
liberacao:
  stage: liberar
  needs: [build-alvo, teste-host, analise, docs]
  rules:
    - if: $CI_COMMIT_TAG
  script: pwsh -File scripts/liberar.ps1
  artifacts:
    paths: [build/alvo-release/*.hex, build/alvo-release/*.map]
    expire_in: never
```

Repositório da imagem — gera e publica a imagem a cada tag (o runner precisa permitir Docker-in-Docker):

```yaml
publicar-imagem:
  image: docker:27
  services: [docker:27-dind]
  rules:
    - if: $CI_COMMIT_TAG
  script:
    - echo "$CI_REGISTRY_PASSWORD" | docker login -u "$CI_REGISTRY_USER" --password-stdin "$CI_REGISTRY"
    - docker build -t "$CI_REGISTRY_IMAGE:$CI_COMMIT_TAG" .
    - docker push "$CI_REGISTRY_IMAGE:$CI_COMMIT_TAG"
```

## GitHub: `.github/workflows/ci.yml`

```yaml
name: ci

on:
  push:            # todo push, em qualquer branch
  pull_request:

concurrency:       # push novo na mesma branch cancela a execução anterior
  group: ci-${{ github.ref }}
  cancel-in-progress: true

permissions:
  contents: read   # o token do job só lê o repositório

# Jobs sem needs rodam em paralelo e até o fim, mesmo que um falhe.
jobs:
  build-alvo:
    runs-on: ubuntu-24.04
    container: ghcr.io/<organizacao>/imagem-build:1.4.0   # versão fixa; a imagem precisa ter git
    steps:
      - uses: actions/checkout@v4
        with: { submodules: recursive }
      - run: pwsh -File scripts/build.ps1 -Preset alvo-release
      - uses: actions/upload-artifact@v4
        with:
          name: firmware
          path: |
            build/alvo-release/*.elf
            build/alvo-release/*.hex
            build/alvo-release/*.map
          retention-days: 14

  teste-host:
    runs-on: ubuntu-24.04
    container: ghcr.io/<organizacao>/imagem-build:1.4.0
    steps:
      - uses: actions/checkout@v4
        with: { submodules: recursive }
      - run: pwsh -File scripts/teste-host.ps1
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: relatorio-teste
          path: build/host-teste/relatorio-teste.xml
          retention-days: 14

  analise:
    runs-on: ubuntu-24.04
    container: ghcr.io/<organizacao>/imagem-build:1.4.0
    steps:
      - uses: actions/checkout@v4
        with: { submodules: recursive }
      - run: pwsh -File scripts/analise.ps1

  docs:
    runs-on: ubuntu-24.04
    container: ghcr.io/<organizacao>/imagem-build:1.4.0
    steps:
      - uses: actions/checkout@v4
        with: { submodules: recursive }
      - run: python3 docs/guide/tools/verificar.py
```

Com `push` e `pull_request` juntos, um PR aberto a partir de uma branch do próprio repositório roda duas vezes; é o custo de cobrir também o push sem PR. As ações de terceiros ficam fixadas por versão ou, onde a segurança importar, pelo SHA do commit.

## Imagem: `Dockerfile`

Ilustrativo: confira a versão e a soma publicadas pelo fornecedor antes de usar.

```dockerfile
# Versionado no repositório da imagem; a imagem é gerada por pipeline e publicada com tag.
FROM ubuntu:24.04

RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates curl git xz-utils \
        build-essential cmake ninja-build cppcheck python3 \
    && rm -rf /var/lib/apt/lists/*

# Toolchain do alvo: versão fixa e soma verificada.
ARG ARM_GNU_VERSAO=13.3.rel1
ARG ARM_GNU_SHA256=<sha256 publicado pela Arm>
ARG ARM_GNU_ARQUIVO=arm-gnu-toolchain-${ARM_GNU_VERSAO}-x86_64-arm-none-eabi
RUN curl -fsSLo /tmp/toolchain.tar.xz \
        https://developer.arm.com/-/media/Files/downloads/gnu/${ARM_GNU_VERSAO}/binrel/${ARM_GNU_ARQUIVO}.tar.xz \
    && echo "${ARM_GNU_SHA256}  /tmp/toolchain.tar.xz" | sha256sum -c - \
    && tar -xJf /tmp/toolchain.tar.xz -C /opt \
    && rm /tmp/toolchain.tar.xz
ENV PATH=/opt/${ARM_GNU_ARQUIVO}/bin:${PATH}

# PowerShell 7, para os mesmos scripts que rodam no Windows.
RUN curl -fsSLo /tmp/ms.deb https://packages.microsoft.com/config/ubuntu/24.04/packages-microsoft-prod.deb \
    && dpkg -i /tmp/ms.deb && rm /tmp/ms.deb \
    && apt-get update && apt-get install -y --no-install-recommends powershell \
    && rm -rf /var/lib/apt/lists/*
```

Reproduzir no PC o que o CI rodou, com a mesma imagem:

```sh
docker run --rm -v "${PWD}:/src" -w /src registry.gitlab.com/<grupo>/imagem-build:1.4.0 pwsh -File scripts/verificar.ps1
```
