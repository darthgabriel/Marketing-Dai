"""Corte gerencial Special DAI - 1 hoja.
Salida: special-dai/entregables/Corte-Gerencial-Special-Dai-05nov.html + .pdf
Datos: CRM autoweb (leads creados y cotizaciones generadas 2-5 nov, solo Hyundai + Chery)
       + hoja "Presupuesto Special Dai" (Google Sheets, 4 nov).
Uso: python scripts/generar_corte_gerencial.py  (desde special-dai/)
"""
import base64
import io
import os
import subprocess

from PIL import Image

LOGO_DAI = r"C:\Users\DELL\Desktop\daiweb\public\img\logo-dai.png"
LOGO_CHERY = r"C:\Users\DELL\Desktop\autowebv26\public\img\logo-1-2.png"
OUT_HTML = os.path.join("entregables", "Corte-Gerencial-Special-Dai-05nov.html")
OUT_PDF = os.path.join("entregables", "Corte-Gerencial-Special-Dai-05nov.pdf")
CREDITO = "Ing. Jose Paredes · Jefe IT & Marketing"

# ---------------------------------------------------------------- DATOS (CRM, 5 nov media mañana)
# (día, leads H, leads C, cotizaciones H, cotizaciones C)
DIAS = [("Lun 2", 9, 7, 3, 3), ("Mar 3", 16, 10, 13, 4), ("Mié 4", 21, 15, 15, 6), ("Jue 5*", 2, 3, 3, 4)]
LEADS = {"H": 48, "C": 35}
COT = {"H": 34, "C": 17}
LEADS_COT = {"H": 32, "C": 15}          # leads nuevos con al menos 1 cotización
COT_BASE = {"H": 5.5, "C": 8.5}         # promedio cotizaciones Lun-Mié, 6 semanas previas
COT_LMW = {"H": 31, "C": 13}            # cotizaciones Lun-Mié esta semana
LEADS_LMW, LEADS_BASE = 78, 57
# Semana normal por marca (promedio Lun-Mié, 6 semanas 21 sep - 31 oct) vs esta semana Lun-Mié
NORMAL = {
    "H": {"leads": (46, 13.8), "cot": (31, 5.5), "pct": (65, 41),
          "plus": "Entran <b>3,3 veces más leads</b> que una semana normal y se cotiza 2 de cada 3."},
    "C": {"leads": (32, 43.0), "cot": (13, 8.5), "pct": (41, 22),
          "plus": "Entran <b>26% menos leads</b> que lo normal, pero se cotiza <b>el doble</b>: 41% vs 22%."},
}
MODELOS = {
    "H": [("Grand i10", 12), ("Creta", 8), ("Tucson", 8), ("Accent", 6)],
    "C": [("Arrizo 5 Pro", 9), ("Tiggo 2 Pro Max", 3), ("Tiggo 4 Pro Max", 3), ("Tiggo 7 / 9 Pro", 2)],
}
# Presupuesto (hoja Google, 4 nov)
GASTO, TOPE, DIRECTIVA, PAGADO, PEND = 4769.93, 7000, 4136, 3128.10, 1641.82
RUBROS = [  # (rubro, monto, color)
    ("Catering y café", 1146.53, "#0F172A"),
    ("Montaje: banderines y globos", 1007.60, "#334155"),
    ("Influencers", 950.00, "#D0021B"),
    ("Medios digitales: Meta, bulk WS, Siempre Mcbo", 775.00, "#0032C0"),
    ("Música en vivo y saxofonista", 660.00, "#7C3AED"),
    ("Impresos: pases, tabloides", 160.00, "#F59E0B"),
    ("Equipo: desayuno", 70.80, "#94A3B8"),
]


def logo_white(path):
    im = Image.open(path).convert("RGBA")
    im = im.crop(im.getbbox())
    white = Image.new("RGBA", im.size, (255, 255, 255, 255))
    white.putalpha(im.split()[-1])
    white.thumbnail((900, 900))
    buf = io.BytesIO()
    white.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def money(v):
    return "$" + f"{v:,.0f}".replace(",", ".")


def chart():
    """Barras agrupadas por día: leads (claro) y cotizaciones (sólido), apiladas H/C."""
    mx, h, y0 = 40, 112, 128
    out = []
    for i, (d, lh, lc, ch, cc) in enumerate(DIAS):
        x = 18 + i * 92
        for j, (a, b, op) in enumerate(((lh, lc, .35), (ch, cc, 1))):
            xx = x + j * 34
            ha, hb = a / mx * h, b / mx * h
            out.append(f'<rect x="{xx}" y="{y0-ha}" width="30" height="{ha}" fill="#0032C0" fill-opacity="{op}" rx="2"/>')
            out.append(f'<rect x="{xx}" y="{y0-ha-hb}" width="30" height="{hb}" fill="#D0021B" fill-opacity="{op}" rx="2"/>')
            out.append(f'<text x="{xx+15}" y="{y0-ha-hb-5}" text-anchor="middle" class="bv{"" if j else " lt"}">{a+b}</text>')
        out.append(f'<text x="{x+32}" y="{y0+15}" text-anchor="middle" class="bl">{d}</text>')
    return f'<svg viewBox="0 0 380 150" width="100%" style="max-height:150px">{"".join(out)}</svg>'


def brand(key, logo, color):
    pct = LEADS_COT[key] / LEADS[key]
    mult = COT_LMW[key] / COT_BASE[key]
    mx = MODELOS[key][0][1]
    rows = "".join(
        f'<div class="mrow"><span>{m}</span><div class="mbar"><i style="width:{n/mx*100:.0f}%"></i></div><b>{n}</b></div>'
        for m, n in MODELOS[key])
    def fmt(v):
        return f"{v:.0f}" if float(v).is_integer() or v >= 10 else f"{v:.1f}".replace(".", ",")
    cmp = "".join(
        f'<div class="cc"><b>{fmt(a)}{"%" if k == "pct" else ""}</b><small>vs {fmt(b)}{"%" if k == "pct" else ""}</small>'
        f'<small>{lbl}</small><em class="{"up" if a >= b else "dn"}">{"▲" if a >= b else "▼"} {abs(a/b-1)*100:.0f}%</em></div>'
        for k, lbl in (("leads", "leads"), ("cot", "cotizaciones"), ("pct", "cotizados"))
        for a, b in [NORMAL[key][k]])
    return f"""
  <div class="brand" style="--c:{color}">
    <div class="bhead"><img src="{logo}" class="blogo {key}"><span class="pill">×{f"{mult:.1f}".replace(".", ",")} vs semana normal</span></div>
    <div class="bnums">
      <div><b>{LEADS[key]}</b><span>leads creados</span></div>
      <div class="big"><b>{COT[key]}</b><span>cotizaciones</span></div>
      <div><b>{pct*100:.0f}%</b><span>leads cotizados</span></div>
    </div>
    <div class="cmp">
      <div class="ch">Lun–Mié · <b>esta semana</b> vs normal</div>
      {cmp}
    </div>
    <div class="plus"><i>+</i><span>{NORMAL[key]['plus']}</span></div>
    <div class="mods">{rows}</div>
  </div>"""


def budget():
    segs = "".join(f'<i style="width:{m/TOPE*100:.2f}%;background:{c}"></i>' for _, m, c in RUBROS)
    leg = "".join(
        f'<div class="rub"><i style="background:{c}"></i><span>{r}</span><b>{money(m)}</b><em>{m/GASTO*100:.0f}%</em></div>'
        for r, m, c in RUBROS)
    return f"""
    <div class="bud">
      <div class="budl">
        <div class="bigm">{money(GASTO)}<small> de {money(TOPE)}</small></div>
        <div class="stack">{segs}<span class="dmark" style="left:{DIRECTIVA/TOPE*100:.1f}%"><em>Directiva {money(DIRECTIVA)}</em></span></div>
        <div class="bkpis">
          <div><b>{money(PAGADO)}</b><span>pagado</span></div>
          <div><b style="color:#D0021B">{money(PEND)}</b><span>por pagar</span></div>
          <div><b>{money(TOPE-GASTO)}</b><span>disponible al tope</span></div>
          <div><b>{money(GASTO/sum(COT.values()))}</b><span>por cotización</span></div>
        </div>
      </div>
      <div class="rubs">{leg}</div>
    </div>"""


def build():
    dai, chery = logo_white(LOGO_DAI), logo_white(LOGO_CHERY)
    tl, tc = sum(LEADS.values()), sum(COT.values())
    cot_lmw, cot_base = sum(COT_LMW.values()), sum(COT_BASE.values())
    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>Corte Gerencial · Special Dai · 5 nov 2026</title>
<style>
@page {{ size: Letter; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: Inter, 'Segoe UI', Arial, sans-serif; color: #0F172A; width: 8.5in; height: 11in; overflow: hidden; position: relative;
  -webkit-print-color-adjust: exact; print-color-adjust: exact }}
.top {{ background: #0F172A; color: #fff; padding: 20px 34px 18px; position: relative; overflow: hidden }}
.top::after {{ content: ""; position: absolute; right: -70px; top: -70px; width: 280px; height: 280px; border-radius: 50%; background: radial-gradient(circle, rgba(208,2,27,.45), transparent 70%) }}
.top::before {{ content: ""; position: absolute; left: 30%; bottom: -140px; width: 320px; height: 320px; border-radius: 50%; background: radial-gradient(circle, rgba(0,50,192,.55), transparent 70%) }}
.row {{ display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 1 }}
.kicker {{ font-size: 9px; letter-spacing: .22em; text-transform: uppercase; color: #94A3B8; font-weight: 700 }}
.mark {{ font-size: 40px; font-weight: 300; margin-top: 6px; line-height: 1 }}
.mark s {{ color: #64748B; text-decoration: none; position: relative }}
.mark s::after {{ content: ""; position: absolute; left: -4px; right: -4px; top: 52%; height: 5px; background: #D0021B; transform: rotate(-4deg); border-radius: 2px }}
.mark b {{ font-weight: 900; margin-left: 8px }}
.sub {{ font-size: 11px; color: #CBD5E1; margin-top: 8px }}
.logos {{ display: flex; gap: 22px; align-items: center }}
.logos .dai {{ height: 46px }} .logos .chery {{ height: 42px }}
.sep {{ width: 1px; height: 40px; background: rgba(255,255,255,.25) }}
.hero {{ display: flex; gap: 26px; align-items: center; margin-top: 12px; position: relative; z-index: 1 }}
.hnum {{ flex: none; text-align: center; width: 150px; padding: 10px 0; border-radius: 16px; background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12) }}
.hnum b {{ display: block; font-size: 58px; font-weight: 900; line-height: 1 }}
.hnum span {{ font-size: 10px; letter-spacing: .14em; text-transform: uppercase; color: #FCA5A5; font-weight: 700 }}
.headline h1 {{ font-size: 25px; line-height: 1.15; font-weight: 800 }}
.headline h1 em {{ font-style: normal; color: #FCA5A5 }}
.headline p {{ font-size: 11.5px; color: #CBD5E1; margin-top: 8px; line-height: 1.5; max-width: 480px }}
.kpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 12px 34px 0 }}
.kpi {{ border: 1px solid #E2E8F0; border-radius: 10px; padding: 7px 12px }}
.kpi .l {{ font-size: 8.5px; letter-spacing: .14em; text-transform: uppercase; color: #64748B; font-weight: 700 }}
.kpi .v {{ font-size: 21px; font-weight: 900; margin-top: 2px }}
.kpi .d {{ font-size: 9.5px; color: #475569 }} .up {{ color: #16A34A }}
.sec {{ padding: 11px 34px 0 }}
.st {{ font-size: 9px; letter-spacing: .2em; text-transform: uppercase; font-weight: 800; display: flex; align-items: center; gap: 8px; margin-bottom: 8px }}
.st::before {{ content: ""; width: 18px; height: 2px; background: #D0021B }}
.brands {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px }}
.brand {{ background: var(--c); color: #fff; border-radius: 12px; padding: 12px 14px; position: relative; overflow: hidden }}
.brand::after {{ content: ""; position: absolute; right: -50px; top: -50px; width: 170px; height: 170px; border-radius: 50%; background: rgba(255,255,255,.08) }}
.bhead {{ display: flex; justify-content: space-between; align-items: center; height: 32px; position: relative; z-index: 1 }}
.blogo.H {{ height: 30px }} .blogo.C {{ height: 28px }}
.pill {{ font-size: 8.5px; font-weight: 800; letter-spacing: .06em; padding: 4px 9px; border-radius: 20px; background: #fff; color: var(--c) }}
.bnums {{ display: grid; grid-template-columns: 1fr 1.2fr 1fr; gap: 8px; margin-top: 7px; position: relative; z-index: 1 }}
.bnums div {{ background: rgba(0,0,0,.18); border-radius: 9px; padding: 5px 9px }}
.bnums .big {{ background: #fff; color: var(--c) }}
.bnums b {{ display: block; font-size: 21px; font-weight: 900; line-height: 1.05 }} .bnums .big b {{ font-size: 25px }}
.bnums span {{ font-size: 8px; text-transform: uppercase; letter-spacing: .1em; opacity: .85; font-weight: 700 }}
.cmp {{ margin-top: 8px; position: relative; z-index: 1; display: grid; grid-template-columns: repeat(3, 1fr); gap: 6px; border-top: 1px solid rgba(255,255,255,.22); padding-top: 6px }}
.cmp .ch {{ grid-column: 1 / -1; font-size: 8px; letter-spacing: .12em; text-transform: uppercase; opacity: .8; font-weight: 700 }}
.cc {{ background: rgba(0,0,0,.16); border-radius: 7px; padding: 4px 7px; display: flex; align-items: baseline; gap: 4px; flex-wrap: wrap }}
.cc b {{ font-size: 13px; font-weight: 900 }} .cc small {{ font-size: 9px; opacity: .75 }}
.cc span {{ display: none }}
.cc em {{ font-style: normal; font-size: 8px; font-weight: 800; margin-left: auto; background: rgba(255,255,255,.95); padding: 1px 5px; border-radius: 8px }}
.cc em.up {{ color: #15803D }} .cc em.dn {{ color: #B91C1C }}
.plus {{ display: flex; gap: 7px; align-items: center; margin-top: 7px; background: rgba(0,0,0,.2); border-radius: 8px; padding: 5px 8px; font-size: 9.5px; position: relative; z-index: 1 }}
.plus i {{ font-style: normal; font-weight: 900; width: 16px; height: 16px; border-radius: 50%; background: #fff; color: var(--c); display: grid; place-items: center; flex: none; font-size: 12px }}
.mods {{ margin-top: 6px; position: relative; z-index: 1 }}
.mrow {{ display: grid; grid-template-columns: 92px 1fr 22px; gap: 8px; align-items: center; font-size: 9px; margin-top: 2px }}
.mbar {{ height: 7px; border-radius: 4px; background: rgba(255,255,255,.18) }} .mbar i {{ display: block; height: 100%; border-radius: 4px; background: #fff }}
.mrow b {{ text-align: right }}
.two {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 18px }}
.bv {{ font: 800 10.5px 'Segoe UI', sans-serif; fill: #0F172A }} .bv.lt {{ fill: #64748B; font-weight: 600 }}
.bl {{ font: 600 10px 'Segoe UI', sans-serif; fill: #475569 }}
.legend {{ font-size: 8.5px; color: #475569; display: flex; gap: 10px; flex-wrap: wrap }}
.legend i {{ display: inline-block; width: 8px; height: 8px; border-radius: 2px; margin-right: 3px; vertical-align: -1px }}
.reads p {{ font-size: 9.5px; color: #334155; line-height: 1.4; padding: 4px 0 4px 11px; border-left: 3px solid #E2E8F0; margin-bottom: 6px }}
.reads p b {{ color: #0F172A }} .reads p.h {{ border-color: #0032C0 }} .reads p.c {{ border-color: #D0021B }}
.bud {{ display: grid; grid-template-columns: 1fr 1fr; gap: 18px; background: #F8FAFC; border-radius: 12px; padding: 10px 15px }}
.bigm {{ font-size: 28px; font-weight: 900 }} .bigm small {{ font-size: 12px; color: #64748B; font-weight: 600 }}
.stack {{ display: flex; height: 18px; border-radius: 9px; background: #E2E8F0; margin-top: 8px; position: relative }}
.stack i {{ display: block; height: 100% }} .stack i:first-child {{ border-radius: 9px 0 0 9px }}
.dmark {{ position: absolute; top: -5px; bottom: -5px; width: 2px; background: #F59E0B }}
.dmark em {{ position: absolute; top: 24px; left: -34px; width: 90px; font-size: 8.5px; font-style: normal; font-weight: 700; color: #B45309 }}
.bkpis {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; margin-top: 20px }}
.bkpis b {{ display: block; font-size: 13px; font-weight: 900 }} .bkpis span {{ font-size: 8px; color: #64748B; text-transform: uppercase; letter-spacing: .06em }}
.rub {{ display: grid; grid-template-columns: 10px 1fr 52px 26px; gap: 6px; align-items: center; font-size: 9px; padding: 2px 0; border-bottom: 1px solid #E2E8F0 }}
.rub i {{ width: 9px; height: 9px; border-radius: 2px }} .rub b {{ text-align: right }} .rub em {{ text-align: right; font-style: normal; color: #64748B; font-size: 8.5px }}
.foot {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 34px; background: #0F172A; color: #94A3B8; font-size: 8px; display: flex; justify-content: space-between; align-items: center }}
.foot .cr {{ text-align: right; color: #fff; font-size: 9px }} .foot .cr small {{ display: block; color: #94A3B8; font-size: 7.5px; letter-spacing: .14em; text-transform: uppercase }}
</style></head><body>

<div class="top">
  <div class="row">
    <div>
      <div class="kicker">Corte gerencial · día 4 de 6 · jueves 5 de noviembre 2026</div>
      <div class="mark">SPECIAL <s>DAYS</s><b>DAI</b></div>
      <div class="sub">Hyundai + Chery Maracaibo · 2 al 7 de noviembre · cierre sábado 7, 5 pm</div>
    </div>
    <div class="logos"><img class="dai" src="{dai}"><div class="sep"></div><img class="chery" src="{chery}"></div>
  </div>
</div>

<div class="kpis">
  <div class="kpi"><div class="l">Leads creados</div><div class="v">{tl}</div><div class="d"><b class="up">▲ {(LEADS_LMW/LEADS_BASE-1)*100:.0f}%</b> Lun–Mié vs {LEADS_BASE} normal</div></div>
  <div class="kpi"><div class="l">Cotizaciones</div><div class="v">{tc}</div><div class="d"><b class="up">×{f"{cot_lmw/cot_base:.1f}".replace(".", ",")}</b> Lun–Mié vs {cot_base:.0f} normal</div></div>
  <div class="kpi"><div class="l">Leads cotizados</div><div class="v">{sum(LEADS_COT.values())/tl*100:.0f}%</div><div class="d">{sum(LEADS_COT.values())} de {tl} con cotización</div></div>
  <div class="kpi"><div class="l">Cotizaciones por lead</div><div class="v">{f"{tc/tl:.2f}".replace(".", ",")}</div><div class="d">Hyundai {f"{COT['H']/LEADS['H']:.2f}".replace(".", ",")} · Chery {f"{COT['C']/LEADS['C']:.2f}".replace(".", ",")}</div></div>
</div>

<div class="sec">
  <div class="st">Por marca · leads y cotizaciones</div>
  <div class="brands">{brand('H', dai, '#0032C0')}{brand('C', chery, '#D0021B')}</div>
</div>

<div class="sec two">
  <div>
    <div class="st">Día a día</div>
    {chart()}
    <div class="legend"><span><i style="background:#0032C0;opacity:.35"></i><i style="background:#D0021B;opacity:.35"></i>leads</span>
      <span><i style="background:#0032C0"></i><i style="background:#D0021B"></i>cotizaciones</span><span>Hyundai abajo · Chery arriba · * jueves a media mañana</span></div>
  </div>
  <div class="reads">
    <div class="st">Lectura</div>
    <p class="h"><b>Hyundai cotiza con fuerza:</b> 34 cotizaciones, ×5,6 su semana normal. Tucson (8) y Accent (6), las unidades a mover, ya están en el tablero.</p>
    <p class="c"><b>Chery convierte mejor con menos:</b> los leads bajan 26% vs lo normal, pero se cotiza el doble. Aún hay 20 leads de la semana sin cotización.</p>
    <p><b>El miércoles fue el pico:</b> 36 leads y 21 cotizaciones en el día del media day.</p>
  </div>
</div>

<div class="sec">
  <div class="st">Presupuesto · lo que va</div>
  {budget()}
</div>

<div class="foot">
  <span><b style="color:#fff">Fuentes:</b> CRM autoweb · leads creados y cotizaciones generadas 2–5 nov 2026, solo Hyundai y Chery ·<br>
  hoja "Presupuesto Special Dai" (4 nov) · semana normal = 6–8 semanas previas, mismos días (Lun–Mié).</span>
  <span class="cr"><small>Elaborado por</small>{CREDITO}</span>
</div>
</body></html>"""
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)


def pdf():
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if os.path.exists(p):
            subprocess.run([p, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={os.path.abspath(OUT_PDF)}", os.path.abspath(OUT_HTML)], check=True)
            return


if __name__ == "__main__":
    build()
    pdf()
    print("OK", OUT_PDF)
