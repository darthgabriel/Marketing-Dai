"""Genera el informe mensual de RRSS para gerencia (HTML -> PDF).

Uso:
    python generar_informe.py "NOVIEMBRE 2026" "OCTUBRE 2026" <narrativa.json>

Lee la hoja del mes y la del mes de comparación desde el Excel de
estadísticas, calcula indicadores con una sola regla para ambos meses
y exporta un PDF horizontal A4 con Edge en modo headless.
La narrativa (resumen, nota de comparación, inversión ADS) viene del JSON.
"""

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import openpyxl

EXCEL = Path(r"G:\Mi unidad\Marketing - OCG\Estadisticas Informe.xlsx")
OUT_DIR = Path(__file__).resolve().parent.parent / "informes"
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

CUENTAS = {
    "daimotorsmcbo": {"marca": "Dai Motors", "sub": "Hyundai", "color": "#0b2a63"},
    "cherymaracaibo": {"marca": "Dai Motors", "sub": "Chery", "color": "#111111"},
    "kyotomotorsmcbo": {"marca": "Kyoto Motors", "sub": "Mitsubishi", "color": "#9b0f1f"},
    "yantaimotors": {"marca": "Yantai Motors", "sub": "", "color": "#222222"},
    "karrymaracaibo": {"marca": "Karry", "sub": "Maracaibo", "color": "#13739e"},
}
ORDEN = list(CUENTAS)


# ---------- lectura ----------

def valor(v):
    """Convierte celdas tipo 98, '=98+16' o None en número."""
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):
        return v
    s = str(v).strip()
    if re.fullmatch(r"=?\s*[\d\s\+\-\.]+", s):
        return eval(s.lstrip("="), {"__builtins__": {}})
    return None


def leer_hoja(nombre):
    ws = openpyxl.load_workbook(EXCEL)[nombre]
    datos = {}
    seccion = None
    for fila in ws.iter_rows(values_only=True):
        a = (fila[0] or "")
        a = a.strip() if isinstance(a, str) else a
        if a in ("PUBLICO", "METRICAS", "RESULTADOS"):
            seccion = a
            continue
        if a not in CUENTAS:
            continue
        d = datos.setdefault(a, {})
        if seccion == "PUBLICO":
            d["nuevos"], d["total"], d["contenido"] = (valor(x) for x in fila[1:4])
        elif seccion == "METRICAS":
            d["vis"], d["alc"], d["perfil"], d["inter"], d["google"] = (valor(x) for x in fila[1:6])
    for d in datos.values():
        calcular(d)
    return datos


def calcular(d):
    partes = [d.get("perfil") or 0, d.get("inter") or 0]
    if d.get("google"):
        partes.append(d["google"])
    prom = sum(partes) / len(partes)
    d["frec"] = d["vis"] / d["alc"] if d.get("alc") else None
    d["eng_seg"] = prom / d["total"] if d.get("total") else None
    d["eng_cont"] = prom / d["alc"] if d.get("alc") else None


# ---------- formato ----------

def num(v, dec=0):
    if v is None:
        return "—"
    s = f"{v:,.{dec}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def usd(v, dec=0):
    return "—" if v is None else "$" + num(v, dec)


def pct(v, dec=1):
    return "—" if v is None else num(v * 100, dec) + "%"


def var(act, ant):
    """Variación relativa; None si no hay base."""
    if act is None or not ant:
        return None
    return act / ant - 1


def chip(v):
    if v is None:
        return '<span class="chip neu">s/d</span>'
    cls = "up" if v > 0.005 else "down" if v < -0.005 else "neu"
    flecha = "▲" if cls == "up" else "▼" if cls == "down" else "■"
    return f'<span class="chip {cls}">{flecha} {num(abs(v) * 100, 0)}%</span>'


# ---------- secciones ----------

def tarjeta(cuenta, act, ant):
    c = CUENTAS[cuenta]
    filas = [
        ("Nuevos seguidores", "nuevos", num),
        ("Total seguidores", "total", num),
        ("Contenido del mes", "contenido", num),
        ("Visualizaciones", "vis", num),
        ("Alcance", "alc", num),
        ("Visitas al perfil", "perfil", num),
        ("Interacciones", "inter", num),
        ("Visitas Google", "google", num),
        ("Inversión ADS", "ads", usd),
    ]
    cuerpo = "".join(
        f"<tr><td>{et}</td><td class='n'><b>{f(act.get(k))}</b></td>"
        f"<td class='n muted'>{f(ant.get(k))}</td><td class='n'>{chip(var(act.get(k), ant.get(k)))}</td></tr>"
        for et, k, f in filas
        if not (k == "google" and act.get(k) is None and ant.get(k) in (None, 0))
    )
    kpis = (
        f"<div class='kpi'><span>Frecuencia</span><b>{num(act['frec'], 2)}</b></div>"
        f"<div class='kpi'><span>Eng. seguidores</span><b>{pct(act['eng_seg'], 2)}</b></div>"
        f"<div class='kpi'><span>Eng. contenido</span><b>{pct(act['eng_cont'], 2)}</b></div>"
    )
    return (
        f"<section class='card' style='--brand:{c['color']}'>"
        f"<header><div><h3>{c['marca']}</h3><small>{c['sub']}</small></div>"
        f"<span class='handle'>@{cuenta}</span></header>"
        f"<table class='mt'><thead><tr><th></th><th class='n'>Mes</th><th class='n'>Comp.</th><th class='n'>Var.</th></tr></thead>"
        f"<tbody>{cuerpo}</tbody></table><div class='kpis'>{kpis}</div></section>"
    )


def construir(mes, mes_comp, act, ant, narrativa):
    for c in ORDEN:
        act[c]["ads"] = narrativa["inversion"].get(c, 0)
    tot = lambda d, k: sum((d[c].get(k) or 0) for c in ORDEN if c in d)
    por = lambda a, b, k=1: a / b * k if a and b else None
    resumen = [
        ("Nuevos seguidores", "nuevos"),
        ("Visualizaciones", "vis"),
        ("Alcance", "alc"),
        ("Interacciones", "inter"),
        ("Visitas al perfil", "perfil"),
        ("Piezas publicadas", "contenido"),
    ]
    tiles = "".join(
        f"<div class='tile'><span>{et}</span><b>{num(tot(act, k))}</b>"
        f"{chip(var(tot(act, k), tot(ant, k)))}<small>vs {num(tot(ant, k))} en {mes_comp.title()}</small></div>"
        for et, k in resumen
    ) + (
        f"<div class='tile'><span>Inversión ADS</span><b>{usd(tot(act, 'ads'))}</b>"
        f"<small>{sum(1 for c in ORDEN if act[c]['ads'])} cuentas con pauta</small></div>"
    )
    consolidado = "".join(
        f"<tr><td>@{c}</td><td class='n'>{num(act[c]['total'])}</td><td class='n'>{num(act[c]['nuevos'])}</td>"
        f"<td class='n'>{num(act[c]['vis'])}</td><td class='n'>{num(act[c]['alc'])}</td>"
        f"<td class='n'>{num(act[c]['inter'])}</td><td class='n'>{num(act[c]['frec'], 2)}</td>"
        f"<td class='n'>{pct(act[c]['eng_cont'], 2)}</td><td class='n'>{usd(act[c]['ads'])}</td>"
        f"<td class='n'>{usd(por(act[c]['ads'], act[c]['nuevos']), 2)}</td>"
        f"<td class='n'>{usd(por(act[c]['ads'], act[c]['alc'], 1000), 2)}</td></tr>"
        for c in ORDEN
    )
    tarjetas = [tarjeta(c, act[c], ant.get(c, {})) for c in ORDEN]
    leyenda = (
        f"<section class='card legend'><h4>Cómo leer las tarjetas</h4><ul>"
        f"<li><b>Mes</b>: {mes.title()} · <b>Comp.</b>: {mes_comp.title()} · <b>Var.</b>: variación porcentual.</li>"
        f"<li><b>Frecuencia</b>: veces que cada cuenta alcanzada vio el contenido.</li>"
        f"<li><b>Eng. seguidores</b>: respuesta promedio sobre el total de seguidores.</li>"
        f"<li><b>Eng. contenido</b>: respuesta promedio sobre las cuentas alcanzadas.</li>"
        f"<li><b>Inversión ADS</b>: pauta pagada en Meta durante el mes (USD).</li>"
        f"<li><b>s/d</b>: sin dato o sin base de comparación.</li></ul></section>"
    )


    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Informe RRSS {mes.title()}</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
<style>
@page {{ size: A4 landscape; margin: 0; }}
:root {{ --ink:#14181f; --muted:#667085; --line:#e4e7ec; --bg:#ffffff; --soft:#f4f6f9; --bar:#3b5b8c; --up:#0f7b4a; --down:#b42318; }}
* {{ box-sizing:border-box; }}
body {{ margin:0; font-family:Inter,Segoe UI,Arial,sans-serif; color:var(--ink); background:var(--bg); font-size:11px; }}
.page {{ width:297mm; height:210mm; padding:0; page-break-after:always; position:relative; overflow:hidden; }}
.top {{ background:#8a9099; color:#fff; display:flex; justify-content:space-between; align-items:center; padding:10mm 14mm 6mm; }}
.top h1 {{ margin:0; font-size:22px; letter-spacing:.5px; }} .top h2 {{ margin:0; font-size:30px; font-weight:800; }}
.body {{ padding:7mm 14mm; }}
.foot {{ position:absolute; bottom:0; left:0; right:0; height:6mm; background:#8a9099; }}
h3 {{ margin:0; font-size:15px; }} h4 {{ margin:0 0 6px; font-size:13px; }}
.muted {{ color:var(--muted); }} .n {{ text-align:right; font-variant-numeric:tabular-nums; }}
.lead {{ font-size:13px; line-height:1.5; max-width:250mm; margin:0 0 6mm; }}
.tiles {{ display:grid; grid-template-columns:repeat(7,1fr); gap:4mm; margin-bottom:6mm; }}
.tile {{ background:var(--soft); border-radius:8px; padding:4mm; display:flex; flex-direction:column; gap:3px; }}
.tile span {{ color:var(--muted); font-size:10px; text-transform:uppercase; letter-spacing:.4px; }}
.tile b {{ font-size:20px; }} .tile small {{ color:var(--muted); font-size:9px; }}
.chip {{ font-size:10px; font-weight:600; }} .chip.up {{ color:var(--up); }} .chip.down {{ color:var(--down); }} .chip.neu {{ color:var(--muted); }}
table {{ border-collapse:collapse; width:100%; }}
th {{ text-align:left; font-size:9.5px; color:var(--muted); text-transform:uppercase; font-weight:600; padding:4px 6px; border-bottom:1px solid var(--line); }}
td {{ padding:4px 6px; border-bottom:1px solid var(--line); }}
.grid2 {{ display:grid; grid-template-columns:1fr 1fr; gap:6mm; }}
.grid3 {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:5mm; }}
.card {{ border:1px solid var(--line); border-top:4px solid var(--brand); border-radius:8px; padding:4mm; }}
.card header {{ display:flex; justify-content:space-between; align-items:baseline; margin-bottom:3mm; }}
.card h3 {{ color:var(--brand); }} .card small {{ color:var(--muted); text-transform:uppercase; letter-spacing:1px; font-size:9px; }}
.handle {{ color:var(--muted); font-size:10px; }}
.mt td, .mt th {{ padding:3px 4px; font-size:10.5px; }}
.kpis {{ display:grid; grid-template-columns:repeat(3,1fr); gap:2mm; margin-top:3mm; }}
.kpi {{ background:var(--soft); border-radius:6px; padding:2.5mm; }} .kpi span {{ display:block; color:var(--muted); font-size:9px; text-transform:uppercase; }} .kpi b {{ font-size:15px; color:var(--brand); }}
.cards {{ padding-top:5mm; }}
.cards .grid3 {{ gap:4mm; }}
.cards .card {{ padding:3mm 3.5mm; }}
.cards .card header {{ margin-bottom:1.5mm; }}
.cards .card h3 {{ font-size:13px; }}
.cards .mt td, .cards .mt th {{ padding:1.6px 4px; font-size:9.5px; }}
.cards .kpis {{ margin-top:2mm; }}
.cards .kpi {{ padding:1.5mm 2mm; }} .cards .kpi span {{ font-size:8px; white-space:nowrap; }} .cards .kpi b {{ font-size:13px; }}
.legend {{ border-top-color:#c4c9d2; background:var(--soft); }} .legend ul {{ font-size:9.5px; line-height:1.45; }}
ul {{ margin:0; padding-left:16px; line-height:1.5; }} li {{ margin-bottom:3px; }}
.box {{ background:var(--soft); border-radius:8px; padding:4mm 5mm; }}
.notes {{ font-size:9.5px; color:var(--muted); line-height:1.45; }}
</style></head><body>

<div class="page"><div class="top"><h1>INFORME DE REDES SOCIALES · GERENCIA</h1><h2>{mes}</h2></div>
<div class="body">
<p class="lead">{narrativa['resumen']}</p>
<div class="tiles">{tiles}</div>
<h4>Consolidado por cuenta · Instagram</h4>
<table><thead><tr><th>Cuenta</th><th class="n">Seguidores</th><th class="n">Nuevos</th><th class="n">Visualizaciones</th><th class="n">Alcance</th><th class="n">Interacciones</th><th class="n">Frecuencia</th><th class="n">Eng. contenido</th><th class="n">Inversión ADS</th><th class="n">Costo / seg. nuevo</th><th class="n">Costo / 1.000 alcanzados</th></tr></thead>
<tbody>{consolidado}</tbody></table>
<p class="notes" style="margin-top:4mm">Comparación contra {mes_comp.title()} ({narrativa['nota_comparacion']}).</p>
</div><div class="foot"></div></div>

<div class="page"><div class="top"><h1>ESTADÍSTICAS POR CUENTA</h1><h2>{mes}</h2></div>
<div class="body cards"><div class="grid3">{"".join(tarjetas)}{leyenda}</div></div><div class="foot"></div></div>

</body></html>"""


def main():
    mes, mes_comp, narrativa_path = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    act, ant = leer_hoja(mes), leer_hoja(mes_comp)
    NARRATIVA = json.loads(narrativa_path.read_text(encoding="utf-8"))

    base = OUT_DIR / f"Informe RRSS {mes.title()}"
    html_path = base.with_suffix(".html")
    html_path.write_text(construir(mes, mes_comp, act, ant, NARRATIVA), encoding="utf-8")
    subprocess.run(
        [EDGE, "--headless", "--disable-gpu", "--no-pdf-header-footer",
         f"--print-to-pdf={base.with_suffix('.pdf')}", html_path.as_uri()],
        check=True, capture_output=True, timeout=120,
    )
    for c in ORDEN:
        a, b = act[c], ant.get(c, {})
        print(c, {k: (round(a[k], 4) if isinstance(a[k], float) else a[k]) for k in a},
              "| comp:", {k: b.get(k) for k in ("nuevos", "vis", "alc", "inter", "perfil")})
    print("PDF:", base.with_suffix(".pdf"))


if __name__ == "__main__":
    main()
