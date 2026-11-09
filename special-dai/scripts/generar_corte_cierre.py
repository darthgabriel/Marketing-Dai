"""Corte de cierre Special DAI - 1 hoja.
Salida: special-dai/entregables/Corte-Cierre-Special-Dai-07nov.html + .pdf
Datos: CRM autoweb (/api/leads y /api/leads/cotizaciones, 2-7 nov, solo Hyundai + Chery)
       + hoja "Presupuesto Special Dai" (Google Sheets, 9 nov).
Semana normal: promedio Lun-Sab de 6 semanas (21 sep - 31 oct).
Uso: python scripts/generar_corte_cierre.py  (desde special-dai/)
"""
import base64
import io
import os
import subprocess

from PIL import Image

LOGO_DAI = r"C:\Users\DELL\Desktop\daiweb\public\img\logo-dai.png"
LOGO_CHERY = os.path.join("assets", "logo-dai-chery.png")
OUT_HTML = os.path.join("entregables", "Corte-Cierre-Special-Dai-07nov.html")
OUT_PDF = os.path.join("entregables", "Corte-Cierre-Special-Dai-07nov.pdf")
CREDITO = "Ing. Jose Paredes · Jefe IT & Marketing"

# ---------------------------------------------------------------- DATOS (CRM, Lun 2 - Sab 7 nov)
# (dia, leads H, leads C, clientes cotizados H, clientes cotizados C)
# Cliente cotizado = telefono distinto con cotizacion; cuenta el dia de su primera cotizacion por marca
DIAS = [("Lun 2", 9, 7, 7, 6), ("Mar 3", 15, 11, 12, 7), ("Mié 4", 21, 15, 17, 9),
        ("Jue 5", 9, 13, 7, 7), ("Vie 6", 21, 30, 18, 23), ("Sáb 7", 14, 4, 12, 8)]
LEADS = {"H": 89, "C": 80}
COT = {"H": 73, "C": 60}                # clientes cotizados por marca
CLIENTES_TOTAL, CLIENTES_BASE = 124, 55.7  # sin repetir (9 clientes cotizaron ambas marcas)
LEADS_COT = {"H": 71, "C": 46}          # leads del evento con al menos 1 cotizacion
COT_BASE = {"H": 20.7, "C": 38.0}       # promedio clientes cotizados Lun-Sab, 6 semanas previas
LEADS_BASE = {"H": 24.3, "C": 73.3}
LEADS_COT_BASE = {"H": 17.0, "C": 30.5}
# Instagram, Meta Business Suite 2-7 nov: seguidores nuevos, cambio vs periodo anterior
SEGUIDORES = {"H": ("+1.271", "▲ 354%"), "C": ("+549", "▲ 36%")}
SEGUIDORES_TOTAL = {"H": "11.415", "C": "14.349"}  # Apify, perfil publico, 9 nov
PASES, PASES_IMPRESOS = 96, 200          # entregados entre las dos marcas (dato de Marketing, no mide asistencia)
CLIENTES_FINANCIAMIENTO = 104           # clientes con al menos una cotizacion financiada
NORMAL = {
    "H": {"leads": (89, 24.3), "cot": (73, 20.7), "pct": (80, 70),
          "plus": "Entraron <b>3,7 veces más leads</b> que una semana normal y se cotizaron 8 de cada 10."},
    "C": {"leads": (80, 73.3), "cot": (60, 38.0), "pct": (58, 42),
          "plus": "Con casi los mismos leads (<b>+9%</b>), los clientes cotizados subieron <b>58%</b>."},
}
MODELOS = {
    "H": [("Grand i10", 32), ("Accent", 25), ("Tucson", 18), ("Creta", 16)],
    "C": [("Arrizo 5 Pro", 24), ("Tiggo 2 Pro Max", 22), ("Tiggo 4 Pro Max", 17), ("Otros Chery", 6)],
}
# Meta Ads (CSV Administrador de anuncios, 10 oct - 8 nov): (anuncio, marca, impresiones, visitas al perfil, gasto, alcance)
# El alcance se suma por anuncio: no es unico, una persona puede contarse en varios anuncios
ADS = [
    ("Varios 1", "H", 15356, 462, 29.20, 9714), ("Historias Expectativa", "H", 11904, 293, 11.07, 9598),
    ("Influencer Diego", "H", 51025, 1528, 67.85, 35031), ("Historias Campaña", "H", 1846, 62, 1.60, 1432),
    ("Varios 1", "C", 5893, 174, 9.90, 4205), ("Historias Beatriz", "C", 33998, 1047, 48.14, 22571),
    ("Historias Expectativa", "C", 4267, 108, 5.88, 3852), ("Historias Campaña", "C", 25217, 489, 33.53, 15846),
    ("Reel Beatriz", "C", 36184, 523, 28.64, 25084),
]
INFLUENCERS = ("Influencer Diego", "Historias Beatriz", "Reel Beatriz")
# Presupuesto (hoja Google, 9 nov)
GASTO, TOPE, DIRECTIVA, PAGADO, PEND = 5057.34, 7000, 4136, 5058.51, 9.00
RUBROS = [  # (rubro, monto, color)
    ("Catering y café", 1433.94, "#0F172A"),
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
    mx, h, y0 = 56, 112, 128
    out = []
    for i, (d, lh, lc, ch, cc) in enumerate(DIAS):
        x = 6 + i * 63
        for j, (a, b, op) in enumerate(((lh, lc, .35), (ch, cc, 1))):
            xx = x + j * 25
            ha, hb = a / mx * h, b / mx * h
            out.append(f'<rect x="{xx}" y="{y0-ha}" width="23" height="{ha}" fill="#0032C0" fill-opacity="{op}" rx="2"/>')
            out.append(f'<rect x="{xx}" y="{y0-ha-hb}" width="23" height="{hb}" fill="#D0021B" fill-opacity="{op}" rx="2"/>')
            out.append(f'<text x="{xx+11.5}" y="{y0-ha-hb-5}" text-anchor="middle" class="bv{"" if j else " lt"}">{a+b}</text>')
        out.append(f'<text x="{x+24}" y="{y0+15}" text-anchor="middle" class="bl">{d}</text>')
    return f'<svg viewBox="0 0 380 150" width="100%" style="max-height:104px">{"".join(out)}</svg>'


def brand(key, logo, color):
    pct = LEADS_COT[key] / LEADS[key]
    mult = COT[key] / COT_BASE[key]
    mx = MODELOS[key][0][1]
    rows = "".join(
        f'<div class="mrow"><span>{m}</span><div class="mbar"><i style="width:{n/mx*100:.0f}%"></i></div><b>{n}</b></div>'
        for m, n in MODELOS[key])
    def fmt(v):
        return str(int(v + .5))

    def delta(k, a, b):
        if k == "pct":
            return f"+{a - b} pts"
        return f"{chr(9650) if a >= b else chr(9660)} {abs(a / b - 1) * 100:.0f}%"
    cmp = "".join(
        f'<div class="cc"><b>{fmt(a)}{"%" if k == "pct" else ""}</b><small>vs {fmt(b)}{"%" if k == "pct" else ""}</small>'
        f'<small>{lbl}</small><em class="{"up" if a >= b else "dn"}">{delta(k, a, b)}</em></div>'
        for k, lbl in (("leads", "leads"), ("cot", "clientes"), ("pct", "cotizados"))
        for a, b in [NORMAL[key][k]])
    return f"""
  <div class="brand" style="--c:{color}">
    <div class="bhead"><img src="{logo}" class="blogo {key}"><span class="pill">×{f"{mult:.1f}".replace(".", ",")} vs semana normal</span></div>
    <div class="bnums">
      <div><b>{LEADS[key]}</b><span>leads creados</span></div>
      <div class="big"><b>{COT[key]}</b><span>clientes cotizados</span></div>
      <div><b>{int(pct*100+.5+1e-6)}%</b><span>leads cotizados</span></div>
    </div>
    <div class="cmp">
      <div class="ch">Lun–Sáb · <b>evento</b> vs semana normal</div>
      {cmp}
    </div>
    <div class="plus"><i>+</i><span>{NORMAL[key]['plus']}</span></div>
    <div class="seg"><span>Seguidores IG</span><b class="tot">{SEGUIDORES_TOTAL[key]}</b><small>al 9 nov</small><b>{SEGUIDORES[key][0]}</b><em>{SEGUIDORES[key][1]} vs anterior</em></div>
    <div class="mods">{rows}</div>
  </div>"""


def n_es(v):
    return f"{v:,.0f}".replace(",", ".")


def ads():
    def tot(rows):
        return sum(r[2] for r in rows), sum(r[3] for r in rows), sum(r[4] for r in rows)
    imp, vis, gas = tot(ADS)
    alc = sum(r[5] for r in ADS)
    inf = [r for r in ADS if r[0] in INFLUENCERS]
    _, ivis, igas = tot(inf)
    fila = ""
    for key, nom, col in (("H", "Hyundai", "#7DA2FF"), ("C", "Chery", "#FF7A88")):
        i, v, g = tot([r for r in ADS if r[1] == key])
        fila += (f'<div class="adr"><b style="color:{col}">{nom}</b><span>{money(g)}</span><span>{n_es(sum(r[5] for r in ADS if r[1] == key))} alc.*</span><span>{n_es(i)} impr.</span>'
                 f'<span>{n_es(v)} visitas</span><span>' + f"${g/v:.3f}".replace(".", ",") + '</span></div>')
    return f"""
  <div class="ads">
    <div class="adk"><b>{money(gas)}</b><span>invertido</span></div>
    <div class="adk"><b>{n_es(alc)}*</b><span>alcance</span></div>
    <div class="adk"><b>{n_es(imp)}</b><span>impresiones</span></div>
    <div class="adk"><b>{n_es(vis)}</b><span>visitas al perfil</span></div>
    <div class="adk"><b>{f"${gas/vis:.2f}".replace(".", ",")}</b><span>por visita</span></div>
    <div class="adrs">{fila}<p>Los anuncios con influencers trajeron <b>{ivis/vis*100:.0f}% de las visitas</b> con {igas/gas*100:.0f}% del gasto. *Suma por anuncio: puede repetir personas.</p></div>
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
          <div><b>{money(TOPE-GASTO)}</b><span>disponible</span></div>
          <div><b>{money(GASTO/CLIENTES_TOTAL)}</b><span>por cliente</span></div>
        </div>
      </div>
      <div class="rubs">{leg}</div>
    </div>"""


def build():
    dai, chery = logo_white(LOGO_DAI), logo_white(LOGO_CHERY)
    tl, tc = sum(LEADS.values()), CLIENTES_TOTAL
    bl, bc = sum(LEADS_BASE.values()), CLIENTES_BASE
    lc, blc = sum(LEADS_COT.values()), sum(LEADS_COT_BASE.values())
    fin = CLIENTES_FINANCIAMIENTO
    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>Corte de Cierre · Special Dai · 7 nov 2026</title>
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
.sub {{ font-size: 11px; color: #CBD5E1; margin-top: 8px; white-space: nowrap }}
.logos {{ display: flex; gap: 16px; align-items: center; flex: none }}
.logos .dai {{ height: 40px }} .logos .chery {{ height: 40px }}
.sep {{ width: 1px; height: 40px; background: rgba(255,255,255,.25) }}
.hero {{ display: flex; gap: 26px; align-items: center; margin-top: 12px; position: relative; z-index: 1 }}
.hnum {{ flex: none; text-align: center; width: 150px; padding: 10px 0; border-radius: 16px; background: rgba(255,255,255,.06); border: 1px solid rgba(255,255,255,.12) }}
.hnum b {{ display: block; font-size: 58px; font-weight: 900; line-height: 1 }}
.hnum span {{ font-size: 10px; letter-spacing: .14em; text-transform: uppercase; color: #FCA5A5; font-weight: 700 }}
.headline h1 {{ font-size: 25px; line-height: 1.15; font-weight: 800 }}
.headline h1 em {{ font-style: normal; color: #FCA5A5 }}
.headline p {{ font-size: 11.5px; color: #CBD5E1; margin-top: 8px; line-height: 1.5; max-width: 480px }}
.kpis {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; padding: 12px 34px 0 }}
.kpi {{ border: 1px solid #E2E8F0; border-radius: 10px; padding: 7px 10px }}
.kpi .l {{ font-size: 7.5px; letter-spacing: .1em; text-transform: uppercase; color: #64748B; font-weight: 700 }}
.kpi .v {{ font-size: 21px; font-weight: 900; margin-top: 2px }}
.kpi .d {{ font-size: 8.5px; color: #475569 }} .up {{ color: #16A34A }}
.sec {{ padding: 11px 34px 0 }}
.st {{ font-size: 9px; letter-spacing: .2em; text-transform: uppercase; font-weight: 800; display: flex; align-items: center; gap: 8px; margin-bottom: 8px }}
.st::before {{ content: ""; width: 18px; height: 2px; background: #D0021B }}
.brands {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px }}
.brand {{ background: var(--c); color: #fff; border-radius: 12px; padding: 12px 14px; position: relative; overflow: hidden }}
.brand::after {{ content: ""; position: absolute; right: -50px; top: -50px; width: 170px; height: 170px; border-radius: 50%; background: rgba(255,255,255,.08) }}
.bhead {{ display: flex; justify-content: space-between; align-items: center; height: 32px; position: relative; z-index: 1 }}
.blogo.H {{ height: 30px }} .blogo.C {{ height: 30px }}
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
.seg {{ display: flex; align-items: center; gap: 8px; margin-top: 6px; position: relative; z-index: 1; font-size: 8px; text-transform: uppercase; letter-spacing: .08em; font-weight: 700 }}
.seg > * {{ white-space: nowrap }}
.seg b.tot {{ margin-left: 0 }} .seg small {{ font-size: 8px; font-weight: 600; text-transform: none; letter-spacing: 0; opacity: .8 }}
.seg b {{ font-size: 15px; font-weight: 900; letter-spacing: 0; margin-left: auto; text-transform: none }}
.seg em {{ font-style: normal; font-size: 8px; font-weight: 800; letter-spacing: 0; text-transform: none; background: #fff; color: #15803D; padding: 2px 6px; border-radius: 8px }}
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
.ads {{ display: grid; grid-template-columns: repeat(5, auto) 1fr; gap: 11px; align-items: center; background: #0F172A; color: #fff; border-radius: 12px; padding: 9px 15px }}
.adk b {{ display: block; font-size: 15px; font-weight: 900; line-height: 1.1 }} .adk span {{ font-size: 7.5px; text-transform: uppercase; letter-spacing: .08em; color: #94A3B8; font-weight: 700 }}
.adrs {{ border-left: 1px solid rgba(255,255,255,.2); padding-left: 10px }}
.adr {{ display: grid; grid-template-columns: 38px 26px 1fr 1fr 1fr 30px; gap: 4px; font-size: 7.5px; padding: 1px 0; white-space: nowrap }} .adr span {{ color: #CBD5E1 }}
.adrs p {{ font-size: 7.5px; color: #CBD5E1; margin-top: 3px }} .adrs p b {{ color: #fff }}
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
.foot .cr {{ white-space: nowrap; flex: none; margin-left: 14px; text-align: right; color: #fff; font-size: 9px }} .foot .cr small {{ display: block; color: #94A3B8; font-size: 7.5px; letter-spacing: .14em; text-transform: uppercase }}
</style></head><body>

<div class="top">
  <div class="row">
    <div>
      <div class="kicker">Corte de cierre · sábado 7 de noviembre 2026</div>
      <div class="mark">SPECIAL <s>DAYS</s><b>DAI</b></div>
      <div class="sub">Hyundai + Chery Maracaibo · Del lunes 2 al sábado 7 de noviembre 2026</div>
    </div>
    <div class="logos"><img class="dai" src="{dai}"><div class="sep"></div><img class="chery" src="{chery}"></div>
  </div>
</div>

<div class="kpis">
  <div class="kpi"><div class="l">Leads creados</div><div class="v">{tl}</div><div class="d"><b class="up">▲ {(tl/bl-1)*100:.0f}%</b> vs {bl:.0f} semana normal</div></div>
  <div class="kpi"><div class="l">Clientes cotizados</div><div class="v">{tc}</div><div class="d"><b class="up">×{f"{tc/bc:.1f}".replace(".", ",")}</b> vs {bc:.0f} semana normal</div></div>
  <div class="kpi"><div class="l">Leads cotizados</div><div class="v">{lc/tl*100:.0f}%</div><div class="d">{lc} de {tl} · normal {blc/bl*100:.0f}%</div></div>
  <div class="kpi"><div class="l">Con financiamiento</div><div class="v">{fin/tc*100:.0f}%</div><div class="d">{fin} de {tc} clientes</div></div>
  <div class="kpi"><div class="l">Pases entregados</div><div class="v">{PASES}</div><div class="d">de {PASES_IMPRESOS} · no equivale a visitas</div></div>
</div>

<div class="sec">
  <div class="st">Por marca · leads y clientes cotizados</div>
  <div class="brands">{brand('H', dai, '#0032C0')}{brand('C', chery, '#D0021B')}</div>
</div>

<div class="sec two">
  <div>
    <div class="st">Día a día</div>
    {chart()}
    <div class="legend"><span><i style="background:#0032C0;opacity:.35"></i><i style="background:#D0021B;opacity:.35"></i>leads</span>
      <span><i style="background:#0032C0"></i><i style="background:#D0021B"></i>clientes cotizados</span><span>Hyundai abajo · Chery arriba</span></div>
  </div>
  <div class="reads">
    <div class="st">Lectura</div>
    <p class="h"><b>Hyundai fue el gran salto:</b> 73 clientes cotizados, 3,5 veces su semana normal. Accent (25) y Tucson (18), las unidades a mover, entre los más pedidos.</p>
    <p class="c"><b>Chery cotizó mejor:</b> se cotizó el 58% de los leads, contra 42% normal. Quedaron 34 leads del evento sin cotización para seguimiento.</p>
    <p><b>El viernes fue el pico:</b> 51 leads y 41 clientes cotizados, a un día del cierre.</p>
  </div>
</div>

<div class="sec">
  <div class="st">Meta Ads · objetivo: visitas al perfil</div>
  {ads()}
</div>

<div class="sec">
  <div class="st">Presupuesto · cierre</div>
  {budget()}
</div>

<div class="foot">
  <span><b style="color:#fff">Fuentes:</b> CRM autoweb · leads y clientes cotizados 2–7 nov 2026, solo Hyundai y Chery (cliente sin repetir; 9 cotizaron ambas marcas y cuentan en cada una) ·<br>
  hoja "Presupuesto Special Dai" (9 nov) · Meta Ads y Business Suite · Apify (seguidores al 9 nov) · semana normal = promedio 6 semanas previas, Lun–Sáb.</span>
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
