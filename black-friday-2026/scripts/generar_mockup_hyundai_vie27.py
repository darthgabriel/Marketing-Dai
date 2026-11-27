"""Mockup para ver: reel @daimotorsmcbo vie 27 nov · 8:00 am · "Abrió el Black Friday" · 14 s.
Cada toma en un cuadro 9:16 dibujado (qué se ve, dónde va el texto en pantalla), con tiempo, voz y notas de cámara.
Página 2: ficha de producción, carteles para imprimir, stories del viernes y checklist.
Salida: black-friday-2026/entregables/Mockup-Reel-Vie27-Precios-Hyundai.pdf (+ .html)
Uso: python black-friday-2026/scripts/generar_mockup_hyundai_vie27.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AZUL = "#002C5F"

# ---------- piezas de dibujo (viewBox 1080x1920) ----------
PISO = ('<rect width="1080" height="1920" fill="#EEF1F5"/>'
        '<rect y="1150" width="1080" height="770" fill="#DADFE6"/>'
        '<path d="M540 1150 L-200 1920 M540 1150 L1280 1920 M540 1150 L300 1920 M540 1150 L780 1920" stroke="#C5CCD6" stroke-width="6"/>'
        '<rect x="380" y="620" width="320" height="120" rx="10" fill="#C9D3E0"/>'
        '<text x="540" y="698" font-family="Arial" font-weight="700" font-size="60" fill="#002C5F" text-anchor="middle">HYUNDAI</text>')


def espalda(x, y, s=1.0, cartel="HOY", cw=300):
    """Alexis de espaldas, con un cartel pegado."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<circle cx="0" cy="-470" r="90" fill="#3B2F2A"/>'
            '<path d="M-190 300 L-170 -260 Q-150 -370 0 -375 Q150 -370 170 -260 L190 300 Z" fill="#1E293B"/>'
            '<rect x="-150" y="300" width="120" height="420" fill="#334155"/><rect x="30" y="300" width="120" height="420" fill="#334155"/>'
            f'<rect x="{-cw/2}" y="-230" width="{cw}" height="130" fill="#fff" stroke="#0B0B0F" stroke-width="8"/>'
            f'<text x="0" y="-145" font-family="Arial Black,Arial" font-weight="900" font-size="58" text-anchor="middle">{cartel}</text></g>')


def frente(x, y, s=1.0, cara="neutra"):
    """Alexis de frente, con la expresión indicada."""
    cejas = ('<path d="M-55 -505 l35 -18 M20 -523 l35 18" stroke="#111" stroke-width="10"/>' if cara == "serio"
             else '<path d="M-55 -510 h35 M20 -510 h35" stroke="#111" stroke-width="10"/>')
    boca = ('<path d="M-30 -420 h60" stroke="#111" stroke-width="10"/>' if cara == "serio"
            else '<path d="M-30 -425 q30 25 60 0" stroke="#111" stroke-width="10" fill="none"/>')
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<circle cx="0" cy="-470" r="90" fill="#D9A57C"/><path d="M-90 -500 q90 -110 180 0" fill="#3B2F2A"/>'
            f'<circle cx="-35" cy="-475" r="9" fill="#111"/><circle cx="35" cy="-475" r="9" fill="#111"/>{cejas}{boca}'
            '<path d="M-190 300 L-170 -260 Q-150 -370 0 -375 Q150 -370 170 -260 L190 300 Z" fill="#1E293B"/>'
            '<rect x="-150" y="300" width="120" height="420" fill="#334155"/><rect x="30" y="300" width="120" height="420" fill="#334155"/></g>')


def carro(x, y, modelo, s=1.0, cartel=True, color="#B8C2CF"):
    """Carro de frente, con o sin cartel en el parabrisas."""
    c = ('<rect x="-75" y="-215" width="150" height="70" fill="#fff" stroke="#0B0B0F" stroke-width="5"/>'
         '<text x="0" y="-165" font-family="Arial Black,Arial" font-size="40" text-anchor="middle">SON 4</text>') if cartel else ""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-200 0 L-190 -110 Q-170 -150 -130 -160 L-110 -250 Q-100 -280 -60 -280 L60 -280 Q100 -280 110 -250 '
            f'L130 -160 Q170 -150 190 -110 L200 0 Z" fill="{color}"/>'
            '<path d="M-100 -165 L-85 -255 L85 -255 L100 -165 Z" fill="#7F93AB"/>'
            f'{c}'
            '<rect x="-180" y="-100" width="70" height="30" rx="8" fill="#FFF7D6"/><rect x="110" y="-100" width="70" height="30" rx="8" fill="#FFF7D6"/>'
            '<rect x="-190" y="-10" width="70" height="60" rx="10" fill="#222"/><rect x="120" y="-10" width="70" height="60" rx="10" fill="#222"/>'
            f'<text x="0" y="110" font-family="Arial" font-weight="700" font-size="44" fill="#475569" text-anchor="middle">{modelo}</text></g>')


def card(texto, y=330, size=64):
    """Texto en pantalla, dentro de la zona segura. Usa | para partir en dos líneas."""
    lineas = texto.split("|")
    alto = 70 + int(size * 1.15) * len(lineas)
    t = "".join(f'<text x="470" y="{y + 40 + size + i * int(size * 1.15)}" font-family="Arial Black,Arial" font-size="{size}" '
                f'fill="#fff" text-anchor="middle">{l}</text>' for i, l in enumerate(lineas))
    return f'<rect x="90" y="{y}" width="760" height="{alto}" rx="16" fill="#0B0B0F" opacity=".88"/>{t}'


ZONA = ('<rect x="0" y="230" width="850" height="1210" fill="none" stroke="#DC2626" stroke-width="5" stroke-dasharray="20 14" opacity=".6"/>')

CUATRO = (carro(120, 1500, "ACCENT", .72) + carro(370, 1500, "ACCENT", .72) +
          carro(640, 1500, "TUCSON", .72, color="#9FB4C9") + carro(910, 1500, "TUCSON", .72, color="#9FB4C9"))

PANEL_PRECIOS = ('<rect x="330" y="1050" width="420" height="230" fill="#fff" stroke="#0B0B0F" stroke-width="8"/>'
                 '<text x="540" y="1140" font-family="Arial Black,Arial" font-size="52" text-anchor="middle">ACCENT ${{ }}</text>'
                 '<text x="540" y="1230" font-family="Arial Black,Arial" font-size="52" text-anchor="middle">TUCSON ${{ }}</text>')

MANO = ('<g><rect x="880" y="980" width="70" height="330" rx="30" fill="#D9A57C" transform="rotate(28 915 1145)"/>'
        '<circle cx="820" cy="960" r="52" fill="#D9A57C"/></g>')

RELOJ = ('<g transform="translate(540 960)">'
         '<circle cx="0" cy="0" r="330" fill="#fff" stroke="#0B0B0F" stroke-width="18"/>'
         '<circle cx="0" cy="0" r="290" fill="none" stroke="#DC2626" stroke-width="6" stroke-dasharray="8 30"/>'
         '<line x1="0" y1="0" x2="0" y2="-190" stroke="#0B0B0F" stroke-width="26" stroke-linecap="round"/>'
         '<line x1="0" y1="0" x2="150" y2="90" stroke="#0B0B0F" stroke-width="18" stroke-linecap="round"/>'
         '<circle cx="0" cy="0" r="26" fill="#DC2626"/></g>'
         '<text x="540" y="1420" font-family="Arial Black,Arial" font-size="64" fill="#475569" text-anchor="middle">8:00 AM</text>')

TOMAS = [
    dict(t="0:00-0:02", cam="Plano abierto fijo. La mano entra desde un lado y arranca el cartel HOY; Alexis trota hacia cámara.",
         ve="Alexis de espaldas frente a las 4 unidades, cartel HOY en la espalda. La mano se lo arranca y él trota.",
         voz="“Épale, te quedan 8 horas.”", txt="QUEDAN 8 HORAS",
         svg=PISO + CUATRO + espalda(540, 1250, 1.0, "HOY") + PANEL_PRECIOS + MANO + card("QUEDAN 8 HORAS")),
    dict(t="0:02-0:03", cam="Corte: la cámara barre el parabrisas de la Tucson de un lado al otro, rápido.",
         ve="La Tucson en plano cerrado con el precio en cartel sobre el parabrisas.",
         voz="“Tucson a {{precio Tucson}}.”", txt="TUCSON ${{ }}",
         svg=PISO + carro(540, 1350, "TUCSON", 1.15, color="#9FB4C9")
             + '<rect x="290" y="1075" width="500" height="110" fill="#fff" stroke="#0B0B0F" stroke-width="8"/>'
               '<text x="540" y="1155" font-family="Arial Black,Arial" font-size="62" text-anchor="middle">${{ }}</text>'
             + card("TUCSON ${{ }}")),
    dict(t="0:03-0:05", cam="Corte al Accent, mismo barrido rápido del parabrisas.",
         ve="El Accent en plano cerrado con el precio en cartel sobre el parabrisas.",
         voz="“Accent a {{precio Accent}}.”", txt="ACCENT ${{ }}",
         svg=PISO + carro(540, 1350, "ACCENT", 1.15)
             + '<rect x="290" y="1075" width="500" height="110" fill="#fff" stroke="#0B0B0F" stroke-width="8"/>'
               '<text x="540" y="1155" font-family="Arial Black,Arial" font-size="62" text-anchor="middle">${{ }}</text>'
             + card("ACCENT ${{ }}")),
    dict(t="0:05-0:08", cam="Corte: plano abierto fijo de las 4 unidades en fila, 2 Accent + 2 Tucson.",
         ve="Las cuatro en fila: Accent, Accent, Tucson, Tucson.",
         voz="“Son 2 y 2, de contado, del primero que pague.”", txt="2 Y 2 · CONTADO",
         svg=PISO + CUATRO + card("2 Y 2 · CONTADO", 330, 60)),
    dict(t="0:08-0:09", cam="Primer plano del reloj de pared del showroom, la manecilla grande marca la hora.",
         ve="El reloj del showroom marcando las 8:00.",
         voz="“Hasta las 6.”", txt="HOY HASTA 6 PM",
         svg=PISO + RELOJ + card("HOY HASTA 6 PM", 330, 60)),
    dict(t="0:09-0:11", cam="Plano medio: la mano le pega a Alexis el cartel QUEDAN 4; él se voltea y no ve nada.",
         ve="Alexis con el cartel QUEDAN 4 recién pegado, cara de no enterarse.",
         voz="“Y el que duerma, la pierde.”", txt="EL QUE DUERME,|LA PIERDE",
         svg=PISO + carro(820, 1500, "TUCSON", .65, color="#9FB4C9") + espalda(470, 1330, 1.05, "QUEDAN 4", cw=430) + MANO + card("EL QUE DUERME,|LA PIERDE", 300, 56)),
    dict(t="0:11-0:14", cam="Plano abierto de las 4 unidades; Alexis de frente a cámara, señalando el showroom.",
         ve="Alexis a cámara, las cuatro unidades detrás. El reloj vuelve de fondo.",
         voz="“Hyundai Dai Motors, ya el reloj comenzó.”", txt="HYUNDAI DAI MOTORS|EL RELOJ COMENZÓ",
         svg=PISO + CUATRO + frente(540, 1420, .95) + card("HYUNDAI DAI MOTORS|EL RELOJ COMENZÓ", 300, 52)),
]

STORIES = [
    ("8:00 am · Reel compartido", "Abrió. El reloj ya corrió.", ""),
    ("Cada venta confirmada", "Se fue un {{modelo}}. Quedan {{N}}.", "Cartel: QUEDAN 3, 2..."),
    ("12:00 m", "Esto es lo que queda.", "Foto del showroom"),
    ("3:00 pm", "¿Viniste hoy?", "Encuesta: Sí / No pude"),
    ("Si se agotan", "Se fueron las cuatro. Obsequios o descuentos en otra unidad hasta las 6 pm.", "Cartel AGOTADO"),
    ("6:00 pm", "Se acabó el reloj. Cerramos.", "Alexis sin carteles"),
]

CSS = f"""
@page {{ size: Letter landscape; margin: 9mm 10mm }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 11px }}
.pg {{ break-after: page }} .pg:last-child {{ break-after: auto }}
.top {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 3px solid {AZUL}; padding-bottom: 4px; margin-bottom: 8px }}
.top b {{ font-size: 16px; color: {AZUL} }} .top span {{ color: #64748B; font-size: 10px }}
.row {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 7px }}
.f svg {{ width: 100%; aspect-ratio: 9/16; display: block; border: 2px solid #0B0B0F; border-radius: 8px; background: #fff }}
.f .tt {{ display: flex; justify-content: space-between; margin: 4px 0 2px; font-weight: 800; color: {AZUL}; font-size: 9.5px }}
.f p {{ margin: 1px 0; line-height: 1.25; font-size: 8.5px }}
.f .v {{ background: #F1F5F9; border-left: 2px solid {AZUL}; padding: 2px 4px; font-style: italic }}
.f .t {{ color: #334155; font-weight: 700; font-size: 8.5px }}
.leg {{ margin-top: 6px; color: #64748B; font-size: 9.5px }}
.two {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px }}
h3 {{ font-size: 12.5px; color: {AZUL}; margin: 8px 0 4px }}
table {{ width: 100%; border-collapse: collapse; font-size: 10.5px }}
th {{ background: #E2E8F0; text-align: left; padding: 3px 6px; font-size: 9.5px; text-transform: uppercase }}
td {{ border-bottom: 1px solid #E2E8F0; padding: 3px 6px; vertical-align: top }}
.carteles {{ display: flex; gap: 10px; flex-wrap: wrap }}
.cart {{ border: 4px solid #0B0B0F; padding: 6px 12px; font: 900 19px 'Arial Black', Arial; background: #fff }}
.cart small {{ display: block; font: 400 8.5px Arial; color: #64748B }}
.st {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px }}
.st div {{ border: 2px solid #CBD5E1; border-radius: 8px; padding: 6px; display: flex; flex-direction: column;
  justify-content: space-between; font-size: 9.5px; background: #F8FAFC; min-height: 66px }}
.st b {{ font-size: 11px }} .st i {{ color: #64748B }} .st em {{ color: {AZUL}; font-style: normal; font-weight: 700 }}
ul {{ padding-left: 13px }} li {{ margin: 1px 0 }}
"""


def tomas_html():
    out = ""
    for i, t in enumerate(TOMAS, 1):
        svg = f'<svg viewBox="0 0 1080 1920">{t["svg"]}{ZONA}</svg>'
        out += (f'<div class="f">{svg}<div class="tt"><span>Toma {i}</span><span>{t["t"]}</span></div>'
                f'<p class="v">{html.escape(t["voz"])}</p>'
                f'<p class="t">{html.escape(t["txt"])}</p></div>')
    return out


def stories_html():
    return "".join(f'<div><i>{i}. {html.escape(a)}</i><b>“{html.escape(b)}”</b><em>{html.escape(c)}</em></div>'
                   for i, (a, b, c) in enumerate(STORIES, 1))


def detalle_html():
    filas = "".join(f'<tr><td><b>{i}</b> · {html.escape(t["t"])}</td><td>{html.escape(t["ve"])}</td>'
                    f'<td>{html.escape(t["cam"])}</td></tr>'
                    for i, t in enumerate(TOMAS, 1))
    return f'<table><tr><th>#</th><th>Se ve</th><th>Cámara</th></tr>{filas}</table>'


DOC = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Mockup reel Black Friday · Hyundai · vie 27</title>
<style>{CSS}</style></head><body>
<section class="pg">
  <div class="top"><b>Mockup · Reel “Abrió el Black Friday” · @daimotorsmcbo</b><span>Vie 27 nov · 8:00 am · 14 s · vertical 1080x1920</span></div>
  <div class="row">{tomas_html()}</div>
  <p class="leg">Línea roja punteada: zona segura. El texto en pantalla va dentro de ella; fuera lo tapan el caption y los botones.
  Dibujos de referencia de encuadre, no de vestuario. ${{ }} = precio real por confirmar, se escribe en la cartulina ese mismo día.</p>
</section>
<section class="pg">
  <div class="top"><b>Producción · Reel “Abrió el Black Friday”</b><span>Grabar y montar el jue 26 en la tarde · publicar vie 27, 8:00 am</span></div>
  <div class="two">
    <div>
      <h3>Ficha</h3>
      <table>
        <tr><th>Sale</th><td>Alexis y otro asesor</td></tr>
        <tr><th>Graba</th><td>Un tercero, celular en vertical, trípode</td></tr>
        <tr><th>Lugar</th><td>Showroom, frente a 2 Accent + 2 Tucson en fila</td></tr>
        <tr><th>Props</th><td>Cartulina HOY pegada sobre la de precios (se arranca en la toma 1), serie QUEDAN 4→AGOTADO, reloj de pared a la vista, marcador grueso</td></tr>
        <tr><th>Audio</th><td>Golpe seco al arrancar el cartel. Sin música en las tomas 2 y 3: los precios se escuchan limpios. Música desde la toma 4. Subtítulos quemados</td></tr>
        <tr><th>Regla</th><td>El contador QUEDAN N solo se cambia con venta confirmada. Nunca publicar “quedan pocas”</td></tr>
        <tr><th>⚠️</th><td>Tucson no está en las unidades aprobadas (era 2 Accent + 2 Creta): confirmar cambio con Gerencia antes de publicar precio</td></tr>
      </table>
      <h3>Carteles para imprimir (letra negra, fondo blanco)</h3>
      <div class="carteles">
        <div class="cart">HOY<small>espalda de Alexis, tapa la de precios · 1</small></div>
        <div class="cart">ACCENT ${{ }} · TUCSON ${{ }}<small>espalda de Alexis, debajo de HOY · escribir el precio a mano el vie 27 antes de las 8</small></div>
        <div class="cart">QUEDAN 4<small>espalda de Alexis · imprimir la serie 4-3-2-1 y AGOTADO, se van cambiando por venta confirmada</small></div>
      </div>
      <h3>Texto para decir</h3>
      <table><tr><td>Épale, te quedan 8 horas.<br>Tucson a {{precio Tucson}}.<br>Accent a {{precio Accent}}.<br>Son 2 y 2, de contado, del primero que pague.<br>Hasta las 6.<br>Y el que duerma, la pierde.<br>Hyundai Dai Motors, ya el reloj comenzó.</td></tr></table>
      <h3>Checklist antes de las 8:00 am</h3>
      <ul>
        <li>Precios reales confirmados por Gerencia y escritos en la cartulina (Accent y Tucson).</li>
        <li>Cambio Accent+Creta → Accent+Tucson aprobado por Gerencia.</li>
        <li>Las 4 unidades en fila, limpias, reloj de pared visible y con la hora correcta.</li>
        <li>Serie completa de carteles QUEDAN N + AGOTADO lista en la oficina.</li>
        <li>Grabar 2 o 3 repeticiones de la toma 1 (el cartel volando es el hook).</li>
        <li>Programar/publicar exactamente a las 8:00 am, ni un minuto antes.</li>
        <li>Historias del día cargadas: contador solo cambia con venta confirmada.</li>
      </ul>
    </div>
    <div>
      <h3>Detalle de tomas</h3>
      {detalle_html()}
      <h3>Stories del vie 27 · todo el día</h3>
      <div class="st">{stories_html()}</div>
      <h3>Pendiente</h3>
      <ul>
        <li>{{precio Accent}} y {{precio Tucson}}: decisión de Gerencia.</li>
        <li>Después de cada venta: story del cartel actualizado + DM a la lista BLACK con las que quedan.</li>
        <li>A las 6 pm: story de cierre aunque no se hayan vendido todas.</li>
      </ul>
    </div>
  </div>
</section>
</body></html>"""

os.makedirs(OUT_DIR, exist_ok=True)
out_html = os.path.join(OUT_DIR, "Mockup-Reel-Vie27-Precios-Hyundai.html")
out_pdf = os.path.join(OUT_DIR, "Mockup-Reel-Vie27-Precios-Hyundai.pdf")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(DOC)
try:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    out_pdf = None
print(out_pdf or out_html)
