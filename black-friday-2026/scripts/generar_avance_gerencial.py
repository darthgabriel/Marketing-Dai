"""Avance gerencial Black Friday 2026 · 1 hoja Letter · formato del corte gerencial Special DAI.
Salida: black-friday-2026/entregables/Avance-Gerencial-BlackFriday-25nov.html + .pdf
Datos: propuesta-gerencia.md · plan.md · guiones · CSV Ads Manager (26 oct-24 nov) · lista BLACK (25 nov)
Uso: python black-friday-2026/scripts/generar_avance_gerencial.py
"""
import base64
import io
import os
import subprocess

from PIL import Image

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_HTML = os.path.join(BASE, "entregables", "Avance-Gerencial-BlackFriday-25nov.html")
OUT_PDF = os.path.join(BASE, "entregables", "Avance-Gerencial-BlackFriday-25nov.pdf")
CREDITO = "Ing. Jose Paredes · Jefe IT & Marketing"

LOGO_DAI = r"C:\Users\DELL\Desktop\daiweb\public\img\logo-dai.png"
LOGO_CHERY = r"C:\Users\DELL\Desktop\autowebv26\public\img\logo-1-2.png"
LOGO_YANTAI = r"C:\Users\DELL\Desktop\marketing\.opencode\openwork\inbox\chat-attachments\ses_decc99786ffe8JnQzzO3sSTw7Q\93fc9cb9-8ac9-4173-af39-e5545bc308e8-yantai-motors 2.png"

# ---------------------------------------------------------------- DATOS (mié 25 nov, media mañana)
ADS = [  # (cuenta, gastado, presupuesto, visitas, CPM, impresiones, alcance, $/visita, frecuencia, color)
    ("Dai Motors", 56.14, 85, 1109, 1.97, 28454, 18662, 0.05, 1.52, "#0032C0"),
    ("Chery Maracaibo", 46.43, 72, 1089, 1.57, 29498, 18670, 0.04, 1.58, "#D0021B"),
    ("Yantai Motors", 60.44, 90, 1909, 0.95, 63317, 39497, 0.03, 1.60, "#7C3AED"),
]
SPENT, BUDGET = 163.01, 247
BULK = 100
BLACK = {"H": 47, "C": 23, "Y": 7}          # inscritos lista BLACK al mié 25
CUENTAS = [  # (key, nombre, handle, color, unidades, publicado, siguiente)
    ("H", "Hyundai en Dai Motors", "@daimotorsmcbo", "#0032C0", "2 Accent + 2 Tucson",
     "Reel 17 y 19 · carrusel 20 · revelación 23 · carrusel de bases 24",
     "Reel del viernes con los precios Accent y Tucson + bulk 2"),
    ("C", "Chery en Dai Motors", "@cherymaracaibo", "#D0021B", "2 Tiggo 4 + 2 Himla",
     "Reel 17 y 19 · carrusel 20 · revelación 23 · carrusel de bases 24",
     "Reel del viernes con los precios Tiggo 4 y Himla + bulk 2"),
    ("Y", "Kaiyi en Yantai Motors", "@yantaimotors", "#7C3AED", "2 Kaiyi X3 Pro",
     "Reel 17 y 19 · carrusel 20 · revelación 23 · carrusel de bases 24",
     "Reel del viernes “8 y 6” (armado, 5 tomas) + bulk 2"),
]
PUB_PIEZAS = 18      # expectativa + revelación completas, 6 piezas por cuenta


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


def meta_results():
    filas = ""
    for n, g, b, r, cpm, imp, alc, cr, fr, c in ADS:
        filas += f"""
      <div class="mr" style="--c:{c}">
        <div class="mhead"><b>{n}</b><span>{money(g)} de {money(b)}</span></div>
        <div class="mbar"><i style="width:{g / b * 100:.0f}%"></i></div>
        <div class="mst">
          <div><b>{imp:,}</b><span>impresiones</span></div>
          <div><b>{alc:,}</b><span>alcance</span></div>
          <div class="hot"><b>{r:,}</b><span>visitas de perfil</span></div>
          <div><b>${cr:.2f}</b><span>por visita</span></div>
          <div><b>${cpm:.2f}</b><span>CPM</span></div>
          <div><b>×{fr:.1f}</b><span>frecuencia</span></div>
        </div>
      </div>"""
    return f"""
    <div class="meta">
      {filas}
      <div class="mtot"><b>TOTAL · {money(SPENT)} de {money(BUDGET)}</b><span>121,269 impresiones · 76,829 alcance · 4,107 visitas a $0.04 ·
      {money(BUDGET - SPENT)} por gastar al viernes · bulk WhatsApp {money(BULK)} listo · calidad del anuncio sobre el promedio en las 3 cuentas</span></div>
    </div>"""


def account(key, name, handle, color, units, publicado, siguiente):
    return f"""
  <div class="acct" style="--c:{color}">
    <div class="ahead"><b>{name}</b><span class="pill">{handle}</span></div>
    <div class="anum">
      <div class="hot"><b>{BLACK[key]}</b><span>lista BLACK</span></div>
      <div><b>{units}</b><span>unidades</span></div>
      <div><b>{PUB_PIEZAS // 3}</b><span>piezas</span></div>
    </div>
    <div class="arow"><i>✓</i><span>{publicado}</span></div>
    <div class="arow"><i>→</i><span>{siguiente}</span></div>
  </div>"""


def build():
    dai, chery, yantai = logo_white(LOGO_DAI), logo_white(LOGO_CHERY), logo_white(LOGO_YANTAI)
    cards = "".join(account(*c) for c in CUENTAS)
    html = f"""<!DOCTYPE html><html lang="es"><head><meta charset="utf-8">
<title>Avance Gerencial · Black Friday 2026 · 25 nov</title>
<style>
@page {{ size: Letter; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: Inter, 'Segoe UI', Arial, sans-serif; color: #0F172A; width: 8.5in; height: 11in; overflow: hidden; position: relative;
  -webkit-print-color-adjust: exact; print-color-adjust: exact }}

/* ---------- header ---------- */
.top {{ background: #0F172A; color: #fff; padding: 14px 34px 12px; position: relative; overflow: hidden }}
.top::after {{ content: ""; position: absolute; right: -70px; top: -70px; width: 280px; height: 280px; border-radius: 50%;
  background: radial-gradient(circle, rgba(255,216,77,.30), transparent 70%) }}
.top::before {{ content: ""; position: absolute; left: 28%; bottom: -150px; width: 330px; height: 330px; border-radius: 50%;
  background: radial-gradient(circle, rgba(0,50,192,.55), transparent 70%) }}
.row {{ display: flex; justify-content: space-between; align-items: center; gap: 20px; position: relative; z-index: 1 }}
.kicker {{ font-size: 9px; letter-spacing: .2em; text-transform: uppercase; color: #94A3B8; font-weight: 700; white-space: nowrap }}
.mark {{ font-size: 30px; font-weight: 900; margin-top: 4px; line-height: 1; letter-spacing: .01em }}
.mark em {{ color: #FFD84D; font-style: normal }}
.sub {{ font-size: 10px; color: #CBD5E1; margin-top: 6px; line-height: 1.4 }}
.logos {{ display: flex; gap: 14px; align-items: center; flex: none }}
.logos img {{ display: block }}
.logos .dai {{ height: 34px }} .logos .chery {{ height: 30px }} .logos .yantai {{ height: 22px; max-width: 130px; object-fit: contain }}
.sep {{ width: 1px; height: 38px; background: rgba(255,255,255,.25); flex: none }}

/* ---------- kpis ---------- */
.kpis {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; padding: 16px 34px 0 }}
.kpi {{ border: 1px solid #E2E8F0; border-radius: 12px; padding: 11px 13px; background: #fff }}
.kpi .l {{ font-size: 8px; letter-spacing: .14em; text-transform: uppercase; color: #64748B; font-weight: 700; white-space: nowrap }}
.kpi .v {{ font-size: 22px; font-weight: 900; margin-top: 3px; line-height: 1.05 }}
.kpi .v small {{ font-size: 12px; color: #94A3B8; font-weight: 700 }}
.kpi .d {{ font-size: 8.5px; color: #475569; margin-top: 3px; line-height: 1.35 }}

/* ---------- secciones ---------- */
.sec {{ padding: 15px 34px 0 }}
.st {{ font-size: 9px; letter-spacing: .2em; text-transform: uppercase; font-weight: 800; display: flex; align-items: center; gap: 8px; margin-bottom: 7px }}
.st::before {{ content: ""; width: 18px; height: 2px; background: #FFD84D }}

/* ---------- tarjetas por cuenta ---------- */
.accts {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px }}
.acct {{ background: var(--c); color: #fff; border-radius: 14px; padding: 13px 14px; position: relative; overflow: hidden }}
.acct::after {{ content: ""; position: absolute; right: -55px; top: -55px; width: 160px; height: 160px; border-radius: 50%; background: rgba(255,255,255,.08) }}
.ahead {{ display: flex; justify-content: space-between; align-items: center; gap: 6px; position: relative; z-index: 1 }}
.ahead b {{ font-size: 11px; line-height: 1.25 }}
.pill {{ font-size: 7.5px; font-weight: 800; padding: 3px 8px; border-radius: 20px; background: #fff; color: var(--c); flex: none }}
.anum {{ display: grid; grid-template-columns: .9fr 1.35fr .8fr; gap: 6px; margin: 7px 0; position: relative; z-index: 1 }}
.anum div {{ background: rgba(0,0,0,.18); border-radius: 9px; padding: 5px 8px }}
.anum .hot {{ background: #fff; color: var(--c) }}
.anum b {{ display: block; font-size: 13px; font-weight: 900; line-height: 1.05 }}
.anum .hot b {{ font-size: 17px }}
.anum span {{ display: block; font-size: 6.5px; text-transform: uppercase; letter-spacing: .08em; opacity: .85; font-weight: 700; margin-top: 2px }}
.arow {{ display: flex; gap: 6px; margin-top: 4px; background: rgba(0,0,0,.20); border-radius: 8px; padding: 4px 7px; font-size: 7.5px; line-height: 1.3; position: relative; z-index: 1 }}
.arow:first-of-type {{ background: rgba(0,0,0,.20) }}
.arow i {{ font-style: normal; font-weight: 900; width: 14px; height: 14px; border-radius: 50%; background: #fff; color: var(--c);
  display: grid; place-items: center; flex: none; font-size: 9px; margin-top: 1px }}

/* ---------- dos columnas ---------- */
.two {{ display: grid; grid-template-columns: 1.02fr 1fr; gap: 18px; align-items: start }}
.meta {{ display: grid; gap: 7px }}
.mr {{ border: 1px solid #E2E8F0; border-radius: 12px; padding: 8px 11px; position: relative; background: #fff }}
.mr::before {{ content: ""; position: absolute; left: 0; top: 10px; bottom: 10px; width: 4px; border-radius: 0 2px 2px 0; background: var(--c) }}
.mhead {{ display: flex; justify-content: space-between; align-items: baseline; font-size: 9px }}
.mhead b {{ font-size: 11.5px; color: var(--c) }}
.mhead span {{ color: #64748B; font-weight: 700 }}
.mbar {{ height: 8px; border-radius: 4px; background: #E2E8F0; margin: 5px 0 6px }}
.mbar i {{ display: block; height: 100%; border-radius: 4px; background: var(--c) }}
.mst {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 5px }}
.mst div {{ background: #F8FAFC; border-radius: 8px; padding: 4px 6px; text-align: center }}
.mst .hot {{ background: var(--c) }} .mst .hot b, .mst .hot span {{ color: #fff }}
.mst b {{ display: block; font-size: 12px; font-weight: 900; line-height: 1.1 }}
.mst span {{ display: block; font-size: 6px; color: #64748B; text-transform: uppercase; letter-spacing: .05em; margin-top: 2px }}
.mst .hot span {{ color: rgba(255,255,255,.8) }}
.mtot {{ background: #0F172A; color: #E2E8F0; border-radius: 10px; padding: 6px 11px; font-size: 7.5px; line-height: 1.35 }}
.mtot b {{ font-size: 9.5px; color: #fff; margin-right: 6px }}
.reads p {{ font-size: 9px; color: #334155; line-height: 1.4; padding: 4px 0 4px 11px; border-left: 3px solid #E2E8F0; margin-bottom: 6px }}
.reads p b {{ color: #0F172A }}
.reads p.a {{ border-color: #FFD84D }} .reads p.b {{ border-color: #0032C0 }} .reads p.t {{ border-color: #7C3AED }} .reads p.r {{ border-color: #D0021B }}

/* ---------- hitos ---------- */
.next {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px }}
.nx {{ border: 1px solid #E2E8F0; border-radius: 12px; padding: 8px 12px; font-size: 8.5px; line-height: 1.4; background: #fff }}
.nx b {{ display: block; font-size: 9.5px; color: #0F172A }}
.nx em {{ font-style: normal; color: #64748B }}

/* ---------- footer ---------- */
.foot {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 34px; background: #0F172A; color: #94A3B8; font-size: 7.5px;
  display: flex; justify-content: space-between; align-items: center }}
.foot .cr {{ text-align: right; color: #fff; font-size: 9px }}
.foot .cr small {{ display: block; color: #94A3B8; font-size: 7px; letter-spacing: .14em; text-transform: uppercase }}
</style></head><body>

<div class="top">
  <div class="row">
    <div>
      <div class="kicker">Avance gerencial · mié 25 nov 2026 · 10:00 am</div>
      <div class="mark">BLACK <em>FRIDAY</em> 2026</div>
      <div class="sub">"A la una, a las dos, de contado..." · solo contado, viernes 27 · corte final el lunes 30</div>
    </div>
    <div class="logos"><img class="dai" src="{dai}"><div class="sep"></div><img class="chery" src="{chery}"><div class="sep"></div><img class="yantai" src="{yantai}"></div>
  </div>
</div>

<div class="kpis">
  <div class="kpi"><div class="l">Lista BLACK</div><div class="v" style="color:#B45309">77</div><div class="d">47 Dai · 23 Chery · 7 Yantai</div></div>
  <div class="kpi"><div class="l">Demanda vs unidades</div><div class="v" style="color:#15803D">7.7x</div><div class="d">77 inscritos para 10 unidades</div></div>
  <div class="kpi"><div class="l">Piezas publicadas</div><div class="v" style="color:#15803D">{PUB_PIEZAS}</div><div class="d">Expectativa y revelación completas · falta solo la del precio del viernes</div></div>
  <div class="kpi"><div class="l">Medios</div><div class="v">{money(BUDGET)}</div><div class="d">{money(SPENT)} en pauta activa · <b style="color:#15803D">{money(BUDGET - SPENT)} disponibles</b> · bulk {money(BULK)} listo</div></div>
  <div class="kpi"><div class="l">Unidades</div><div class="v">10</div><div class="d">2 Accent + 2 Tucson · 2 Tiggo 4 + 2 Himla · 2 Kaiyi X3 Pro</div></div>
</div>

<div class="sec">
  <div class="st">Por cuenta · qué va y qué sigue</div>
  <div class="accts">{cards}</div>
</div>

<div class="sec two">
  <div>
    <div class="st">Resultados en Meta · pauta "BlackFriday 1"</div>
    {meta_results()}
  </div>
  <div class="reads">
    <div class="st">Lectura</div>
    <p class="a"><b>La campaña llega completa al viernes:</b> revelación publicada, bases saliendo antes del jueves y el corte de resultados el lunes 30, como está planeado.</p>
    <p class="a"><b>Mañana 7 am el bulk 2 lleva los precios a la lista:</b> 77 inscritos reciben el precio por WhatsApp un día antes que nadie.</p>
    <p class="b"><b>La lista BLACK ya cubre la demanda:</b> 77 inscritos para 10 unidades (7.7 por unidad). Dai Motors (47) superó su meta de leads (33) con dos días por delante; Chery (23) la cierra con el bulk 2 y el reel del 26; Yantai suma 7 para sus 2 unidades.</p>
    <p class="b"><b>La pauta ya trabaja:</b> {money(SPENT)} de {money(BUDGET)} gastados; 4,107 visitas de perfil a $0.04 c/u, calidad de anuncio sobre el promedio en las 3 cuentas.</p>
    <p class="t"><b>La ola está a tiempo:</b> búsquedas de "black friday" en Venezuela suben 58% en 7 días y #blackfriday entró al top 10 de TikTok. El viernes 27 es el pico — y el contador honesto convierte cada venta del día en contenido.</p>
  </div>
</div>

<div class="sec">
  <div class="st">Próximos hitos</div>
  <div class="next">
    <div class="nx"><b>Jue 26 · 7:00 am</b>Bulk 2: precios a la lista BLACK<em> · 77 inscritos lo reciben primero</em></div>
    <div class="nx"><b>Vie 27 · 8:00 am</b>Reel del precio + venta solo contado<em> · pauta 8 am a 6 pm · stories con contador</em></div>
    <div class="nx"><b>Lun 30 · 7:00 pm</b>Reel de resultado + corte de cierre<em> · ventas, leads, gasto real vs presupuesto</em></div>
  </div>
</div>

<div class="foot">
  <span><b style="color:#fff">Fuentes:</b> black-friday-2026/propuesta-gerencia.md (12 nov) · .claude/instagram/plan.md · guiones por cuenta ·<br>
  Ads Manager: CSV "Jose-Paredes-Anuncios 26 oct-24 nov" · mockups de reel del viernes · tendencias (25 nov). Corte de resultados con CRM: lunes 30.</span>
  <span class="cr"><small>Elaborado por</small>{CREDITO}</span>
</div>
</body></html>"""
    os.makedirs(os.path.dirname(OUT_HTML), exist_ok=True)
    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write(html)


def pdf():
    for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
        if os.path.exists(p):
            subprocess.run([p, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                            f"--print-to-pdf={OUT_PDF}", OUT_HTML], check=True)
            return


if __name__ == "__main__":
    build()
    pdf()
    print("OK", OUT_PDF)
