#!/usr/bin/env python3
"""Sensor de documentação do conjunto de convenções.

Uso (da raiz do repositório):
    python tools/verificar.py              # no repositório do conjunto
    python docs/guide/tools/verificar.py   # num projeto que adotou o conjunto

Verifica:
  links     links relativos em Markdown apontam para arquivos existentes
            (blocos de código e código inline são ignorados);
  includes  diretivas #[[file:...]] apontam para arquivos existentes;
  skills    frontmatter de .agents/skills/*/SKILL.md segue a especificação
            Agent Skills; adaptadores em diretórios de ferramenta
            (.<ferramenta>/skills/<nome>/SKILL.md) têm name e description
            idênticos aos da Skill canônica, que precisa existir;
  secoes    (só no conjunto) toda citação "Seção *Título*" corresponde a um
            título existente.

Também informa, em caracteres, os arquivos permanentes e os AGENTS.md
condicionais encontrados por caminho. Gitlinks declarados em .gitmodules
ficam fora da varredura: são projetos externos, não documentação do
projeto consumidor.

Sai com código 1 se houver qualquer problema. Só biblioteca padrão, Python 3.8+.
"""

import argparse
import re
import sys
from pathlib import Path

IGNORAR_DIRS = {".git", "node_modules", "build", "out", "dist", ".venv", "venv", "__pycache__"}

LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^\)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
INCLUDE_RE = re.compile(r"#\[\[file:([^\]\r\n]+)\]\]")
INLINE_CODE_RE = re.compile(r"(`+)(.+?)\1")
SECAO_RE = re.compile(r"Seç(?:ão|ões)\s+\*([^*]+)\*")
TITULO_RE = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$")
NOME_SKILL_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def ler(caminho):
    return caminho.read_text(encoding="utf-8").replace("\r\n", "\n")


def normalizar_relativo(caminho):
    caminho = str(caminho).replace("\\", "/")
    while caminho.startswith("./"):
        caminho = caminho[2:]
    return caminho.rstrip("/")


def caminhos_gitlink(raiz):
    """Lê somente os caminhos de submódulos declarados no manifesto local."""
    manifesto = raiz / ".gitmodules"
    if not manifesto.is_file():
        return []
    caminhos = []
    for linha in ler(manifesto).split("\n"):
        m = re.match(r"^\s*path\s*=\s*(.+?)\s*$", linha)
        if m:
            caminhos.append(normalizar_relativo(m.group(1)))
    return caminhos


def ignorado(rel, caminhos):
    rel = normalizar_relativo(rel)
    return any(rel == caminho or rel.startswith(caminho + "/") for caminho in caminhos)


def arquivos_md(raiz, ignorar):
    ignorar = [normalizar_relativo(i) for i in ignorar]
    for p in sorted(raiz.rglob("*.md")):
        partes = set(p.relative_to(raiz).parts[:-1])
        if partes & IGNORAR_DIRS:
            continue
        rel = p.relative_to(raiz).as_posix()
        if ignorado(rel, ignorar):
            continue
        yield p


def linhas_fora_de_codigo(texto):
    """Gera (número, linha) fora de blocos cercados, sem o código inline."""
    cerca = None
    for n, linha in enumerate(texto.split("\n"), 1):
        m = re.match(r"^\s*(`{3,}|~{3,})", linha)
        if m:
            marca = m.group(1)
            if cerca is None:
                cerca = marca
            elif marca[0] == cerca[0] and len(marca) >= len(cerca):
                cerca = None
            continue
        if cerca is None:
            yield n, INLINE_CODE_RE.sub("", linha)


def verificar_links(raiz, ignorar):
    problemas = []
    for arq in arquivos_md(raiz, ignorar):
        for n, linha in linhas_fora_de_codigo(ler(arq)):
            for alvo in LINK_RE.findall(linha):
                if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", alvo) or alvo.startswith("#"):
                    continue  # URL externa, mailto:, âncora local
                caminho = alvo.split("#", 1)[0].split("?", 1)[0]
                if not caminho:
                    continue
                destino = (arq.parent / caminho).resolve()
                if not destino.exists():
                    problemas.append(f"{arq.relative_to(raiz).as_posix()}:{n}: link quebrado -> {alvo}")
    return problemas


def verificar_includes(raiz, ignorar):
    problemas = []
    for arq in arquivos_md(raiz, ignorar):
        for n, linha in enumerate(ler(arq).split("\n"), 1):
            for alvo in INCLUDE_RE.findall(linha):
                alvo = alvo.strip()
                destino = (arq.parent / alvo).resolve()
                if not destino.is_file():
                    problemas.append(
                        f"{arq.relative_to(raiz).as_posix()}:{n}: arquivo incluído não existe -> {alvo}"
                    )
    return problemas


def normalizar_titulo(t):
    t = re.sub(r"^\d+(\.\d+)*\.?\s+", "", t.strip())
    return t.replace("`", "").replace("*", "").strip().lower()


def verificar_secoes(raiz, ignorar):
    titulos = set()
    arquivos = list(arquivos_md(raiz, ignorar))
    for arq in arquivos:
        for _, linha in linhas_fora_de_codigo(ler(arq)):
            m = TITULO_RE.match(linha)
            if m:
                titulos.add(normalizar_titulo(m.group(1)))
    problemas = []
    for arq in arquivos:
        # inclui blocos de código: citação dentro de template também precisa existir
        for n, linha in enumerate(ler(arq).split("\n"), 1):
            for citado in SECAO_RE.findall(linha):
                if normalizar_titulo(citado) not in titulos:
                    problemas.append(
                        f"{arq.relative_to(raiz).as_posix()}:{n}: seção citada não existe -> *{citado}*"
                    )
    return problemas


def frontmatter(texto):
    if not texto.startswith("---\n"):
        return None
    fim = texto.find("\n---", 4)
    if fim < 0:
        return None
    campos, chave = {}, None
    for linha in texto[4:fim].split("\n"):
        m = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", linha)
        if m and not linha.startswith((" ", "\t")):
            chave, valor = m.group(1), m.group(2).strip()
            if valor in (">", "|", ">-", "|-", ""):
                valor = ""
            campos[chave] = valor.strip("\"'")
        elif chave and linha.startswith((" ", "\t")) and campos.get(chave) is not None:
            if not re.match(r"^\s+[A-Za-z0-9_-]+:", linha):  # continuação de texto, não submapa
                campos[chave] = (campos[chave] + " " + linha.strip()).strip()
    return campos


def validar_skill(arq, raiz):
    rel = arq.relative_to(raiz).as_posix()
    fm = frontmatter(ler(arq))
    if fm is None:
        return [f"{rel}: sem frontmatter YAML entre '---'"], None
    erros = []
    nome = fm.get("name", "")
    desc = fm.get("description", "")
    if not nome:
        erros.append(f"{rel}: campo 'name' ausente")
    elif len(nome) > 64 or not NOME_SKILL_RE.match(nome):
        erros.append(f"{rel}: 'name' inválido ({nome}): 1-64 caracteres, a-z, 0-9 e hífens simples")
    elif nome != arq.parent.name:
        erros.append(f"{rel}: 'name' ({nome}) difere do nome da pasta ({arq.parent.name})")
    if not desc:
        erros.append(f"{rel}: campo 'description' ausente")
    elif len(desc) > 1024:
        erros.append(f"{rel}: 'description' com {len(desc)} caracteres (máximo 1024)")
    if len(fm.get("compatibility", "")) > 500:
        erros.append(f"{rel}: 'compatibility' com mais de 500 caracteres")
    return erros, fm


def verificar_skills(raiz, ignorar):
    problemas, canonicas = [], {}
    base = raiz / ".agents" / "skills"
    if base.is_dir() and not ignorado(base.relative_to(raiz), ignorar):
        for arq in sorted(base.glob("*/SKILL.md")):
            if ignorado(arq.relative_to(raiz), ignorar):
                continue
            erros, fm = validar_skill(arq, raiz)
            problemas += erros
            if fm:
                canonicas[arq.parent.name] = fm
    for dir_ferramenta in sorted(raiz.glob(".*/skills")):
        if dir_ferramenta.parent.name == ".agents" or dir_ferramenta.parent.name in IGNORAR_DIRS:
            continue
        if dir_ferramenta.is_symlink() or ignorado(dir_ferramenta.relative_to(raiz), ignorar):
            continue
        for arq in sorted(dir_ferramenta.glob("*/SKILL.md")):
            if arq.parent.is_symlink() or ignorado(arq.relative_to(raiz), ignorar):
                continue
            erros, fm = validar_skill(arq, raiz)
            problemas += erros
            nome = arq.parent.name
            rel = arq.relative_to(raiz).as_posix()
            if nome not in canonicas:
                problemas.append(f"{rel}: Skill fora do local canônico; mova para .agents/skills/{nome}/")
            elif fm and (fm.get("name"), fm.get("description")) != (
                canonicas[nome].get("name"), canonicas[nome].get("description")
            ):
                problemas.append(f"{rel}: name/description diferem de .agents/skills/{nome}/SKILL.md")
    return problemas


def formatar_tamanhos(arquivos, raiz):
    return [f"  {len(ler(a)):>6} {a.relative_to(raiz).as_posix()}" for a in arquivos]


def tamanhos_sempre_carregados(raiz):
    alvos = []
    for candidato in (
        raiz / "PROJECT_GUIDE.md",
        raiz / "docs" / "guide" / "PROJECT_GUIDE.md",
        raiz / "AGENTS.md",
    ):
        if candidato.is_file() and candidato not in alvos:
            alvos.append(candidato)
    return formatar_tamanhos(alvos, raiz)


def tamanhos_agents_condicionais(raiz, ignorar):
    alvos = []
    for arq in arquivos_md(raiz, ignorar):
        rel = arq.relative_to(raiz).as_posix()
        if arq.name == "AGENTS.md" and rel != "AGENTS.md":
            alvos.append(arq)
    return formatar_tamanhos(alvos, raiz)


def main():
    ap = argparse.ArgumentParser(description="Sensor de documentação do conjunto de convenções.")
    ap.add_argument("raiz", nargs="?", default=".", help="raiz do repositório (padrão: diretório atual)")
    ap.add_argument("--ignorar", action="append", default=[], metavar="CAMINHO",
                    help="caminho relativo a ignorar na verificação de links (repetível)")
    args = ap.parse_args()
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if callable(reconfigure):
        reconfigure(errors="replace")  # console Windows sem UTF-8

    raiz = Path(args.raiz).resolve()
    ignorar = list(args.ignorar)
    for caminho in caminhos_gitlink(raiz):
        if caminho not in ignorar:
            ignorar.append(caminho)
    e_conjunto = (raiz / "PROJECT_GUIDE.md").is_file() and (raiz / "practices").is_dir()

    etapas = [
        ("links", verificar_links(raiz, ignorar)),
        ("includes", verificar_includes(raiz, ignorar)),
        ("skills", verificar_skills(raiz, ignorar)),
    ]
    if e_conjunto:
        etapas.append(("secoes", verificar_secoes(raiz, ignorar)))

    total = 0
    for nome, problemas in etapas:
        estado = "ok" if not problemas else f"{len(problemas)} problema(s)"
        print(f"[{nome}] {estado}")
        for p in problemas:
            print(f"  {p}")
        total += len(problemas)

    tamanhos = tamanhos_sempre_carregados(raiz)
    if tamanhos:
        print("[tamanho do que é carregado em toda sessão, em caracteres — informativo]")
        print("\n".join(tamanhos))
    condicionais = tamanhos_agents_condicionais(raiz, ignorar)
    if condicionais:
        print("[AGENTS condicionais por caminho, em caracteres — informativo]")
        print("\n".join(condicionais))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
