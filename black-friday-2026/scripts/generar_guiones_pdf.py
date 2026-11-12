"""Guiones Black Friday 2026 en PDF para imprimir (carta horizontal).
Entrada: black-friday-2026/contenido-*.md
Salida:  black-friday-2026/entregables/Guiones-<cuenta>.pdf (+ .html)
Uso:     python black-friday-2026/scripts/generar_guiones_pdf.py
"""
import html
import os
import re
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

DOCS = [
    ("contenido-diario.md", "Guiones-BF2026-0-Indice", "Índice y calendario", "#0F172A"),
    ("contenido-hyundai.md", "Guiones-BF2026-1-Hyundai", "@daimotorsmcbo · Hyundai en Dai Motors", "#002C5F"),
    ("contenido-chery.md", "Guiones-BF2026-2-Chery", "@cherymaracaibo · Chery en Dai Motors", "#8A1C2B"),
    ("contenido-yantai.md", "Guiones-BF2026-3-Yantai", "@yantaimotors · Kaiyi en Yantai Motors", "#374151"),
]


def inline(t):
    t = html.escape(t, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    return t


def md_to_html(md):
    out, lines, i = [], md.splitlines(), 0
    first_h2 = True
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("```"):
            kind = ln[3:].strip()
            i += 1
            buf = []
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(html.escape(lines[i]))
                i += 1
            label = {"guion": "Texto para decir", "whatsapp": "Mensaje de WhatsApp"}.get(kind, "")
            out.append(f'<div class="code {kind}"><span>{label}</span><pre>' + "\n".join(buf) + "</pre></div>")
            i += 1
            continue
        if ln.startswith("|"):
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append(lines[i])
                i += 1
            cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
            head, body = cells[0], [r for r in cells[1:] if not re.fullmatch(r"[-: ]+", "".join(r))]
            t = "<table><thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead><tbody>"
            for r in body:
                cls = ' class="rec"' if r and r[0].startswith("**") else ""
                t += f"<tr{cls}>" + "".join(
                    f'<td class="t">{inline(c)}</td>' if re.fullmatch(r"\d:\d\d-\d:\d\d", c) else f"<td>{inline(c)}</td>"
                    for c in r) + "</tr>"
            out.append(t + "</tbody></table>")
            continue
        if ln.startswith("# "):
            out.append(f"<h1>{inline(ln[2:])}</h1>")
        elif ln.startswith("## "):
            cls = "" if first_h2 else ' class="nb"'
            first_h2 = False
            out.append(f"<h2{cls}>{inline(ln[3:])}</h2>")
        elif ln.startswith("### "):
            out.append(f"<h3>{inline(ln[4:])}</h3>")
        elif re.match(r"^- ", ln):
            buf = []
            while i < len(lines) and re.match(r"^- ", lines[i]):
                buf.append(f"<li>{inline(lines[i][2:])}</li>")
                i += 1
            out.append("<ul>" + "".join(buf) + "</ul>")
            continue
        elif re.match(r"^\d+\. ", ln):
            buf = []
            while i < len(lines) and re.match(r"^\d+\. ", lines[i]):
                buf.append(f"<li>{inline(re.sub(r'^\d+\. ', '', lines[i]))}</li>")
                i += 1
            out.append("<ol>" + "".join(buf) + "</ol>")
            continue
        elif ln.strip() == "---" or not ln.strip() or ln.startswith("**Texto para decir"):
            pass
        else:
            out.append(f"<p>{inline(ln)}</p>")
        i += 1
    return "\n".join(out)


CSS = """
@page { size: Letter landscape; margin: 12mm 13mm }
* { box-sizing: border-box }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 10.5px; line-height: 1.4; margin: 0 }
.top { display: flex; justify-content: space-between; border-bottom: 3px solid var(--c); padding-bottom: 4px; margin-bottom: 10px;
  font-size: 10px; color: #475569 }
.top b { color: var(--c); font-size: 11px }
h1 { font-size: 22px; color: var(--c); margin: 0 0 6px }
h2 { font-size: 16px; color: #fff; background: var(--c); padding: 6px 10px; border-radius: 4px; margin: 0 0 8px }
h2.nb { break-before: page }
h3 { font-size: 13px; color: var(--c); margin: 10px 0 4px }
p { margin: 3px 0 }
ul, ol { margin: 3px 0 6px 18px; padding: 0 }
table { width: 100%; border-collapse: collapse; margin: 4px 0 10px; break-inside: auto }
tr { break-inside: avoid }
th { background: #E2E8F0; text-align: left; padding: 4px 6px; font-size: 9.5px; text-transform: uppercase; letter-spacing: .02em }
td { border-bottom: 1px solid #E2E8F0; padding: 4px 6px; vertical-align: top }
tr.rec td { background: #F1F5F9 }
td.t { white-space: nowrap; font-variant-numeric: tabular-nums }
code { background: #FEF3C7; padding: 0 3px; border-radius: 2px; font-family: Consolas, monospace; font-size: 10px }
.code { border: 2px solid var(--c); border-radius: 6px; margin: 6px 0 10px; break-inside: avoid }
.code span { display: block; background: var(--c); color: #fff; font-size: 9.5px; font-weight: 700; padding: 3px 8px;
  text-transform: uppercase; letter-spacing: .04em }
.code pre { margin: 0; padding: 8px 12px; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; line-height: 1.6; white-space: pre-wrap }
.code.whatsapp { border-color: #16A34A } .code.whatsapp span { background: #16A34A }
.code.whatsapp pre { font-size: 11px }
"""


def build(src, name, title, color):
    md = open(os.path.join(BASE, src), encoding="utf-8").read()
    body = md_to_html(md)
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>{name}</title>
<style>:root {{ --c: {color} }}{CSS}</style></head><body>
<div class="top"><b>Black Friday 2026 · Guiones</b><span>{html.escape(title)}</span><span>Borrador · uso interno</span></div>
{body}
</body></html>"""
    out_html = os.path.join(OUT_DIR, name + ".html")
    out_pdf = os.path.join(OUT_DIR, name + ".pdf")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", out_html], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return out_pdf


if __name__ == "__main__":
    os.makedirs(OUT_DIR, exist_ok=True)
    for d in DOCS:
        print(build(*d))
