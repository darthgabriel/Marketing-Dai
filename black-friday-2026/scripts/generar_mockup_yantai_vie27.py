"""Mockup para ver: reel @yantaimotors vie 27 nov · 8:00 am · "Hoy cuesta menos" · imágenes + textos · 14.2 s.
Cada toma = foto/video real a grabar (recuadro de referencia) con su tarjeta de texto en pantalla.
Página 2: ficha de producción, lista de tomas, stories del viernes y checklist.
Salida: black-friday-2026/entregables/Mockup-Reel-Vie27-Precio-Yantai.pdf (+ .html)
Uso: python black-friday-2026/scripts/generar_mockup_yantai_vie27.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AZUL = "#002C5F"

# ---------- piezas de dibujo (viewBox 1080x1920) · fondo gris oscuro, tarjeta amarilla ----------
FONDO = '<rect width="1080" height="1920" fill="#23272B"/>'


def foto(x, y, w, h, etiqueta, sub="", icon=""):
    """Recuadro de la foto o video real que se graba para esa toma, con mini-diagrama de ejemplo."""
    base = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#2E3A40" stroke="#FFD84D" stroke-width="6" stroke-dasharray="26 18"/>'
            f'<text x="{x + w/2}" y="{y + h - 120}" font-family="Arial Black,Arial" font-size="44" fill="#FFD84D" text-anchor="middle">FOTO/VIDEO</text>'
            f'<text x="{x + w/2}" y="{y + h - 62}" font-family="Arial" font-weight="700" font-size="36" fill="#E8EDF1" text-anchor="middle">{etiqueta}</text>'
            + (f'<text x="{x + w/2}" y="{y + h - 20}" font-family="Arial" font-size="28" fill="#9FB0BA" text-anchor="middle">{sub}</text>' if sub else ""))
    return base + (f'<g transform="translate({x + w/2} {y + h/2 - 110})">{icon}</g>' if icon else "")


def icon_reloj(h="8:00", r=150):
    """Mini-diagrama: reloj de pared con la manecilla en la hora indicada."""
    if h == "8:00":
        hands = '<line x1="0" y1="0" x2="-106" y2="-61" stroke="#23272B" stroke-width="22" stroke-linecap="round"/><line x1="0" y1="0" x2="0" y2="-128" stroke="#23272B" stroke-width="18" stroke-linecap="round"/>'
    else:
        hands = '<line x1="0" y1="0" x2="0" y2="-128" stroke="#23272B" stroke-width="22" stroke-linecap="round"/>'
    return (f'<circle cx="0" cy="0" r="{r}" fill="#FFD84D" stroke="#23272B" stroke-width="12"/>'
            f'{hands}<circle cx="0" cy="0" r="16" fill="#23272B"/>'
            f'<text x="0" y="{r + 70}" font-family="Arial Black,Arial" font-size="52" fill="#FFD84D" text-anchor="middle">{h}</text>')


def icon_x3_side(r=1.0):
    """Mini-diagrama: perfil de la X3 Pro con tarjetón de precio."""
    return (f'<g transform="scale({r})">'
            '<path d="M-260 60 L-250 -20 Q-235 -55 -195 -63 L-175 -110 Q-165 -132 -130 -134 L40 -134 Q80 -132 95 -105 '
            'L115 -60 Q165 -50 185 -15 L195 60 Z" fill="#FFD84D"/>'
            '<path d="M-150 -58 L-138 -108 Q-132 -122 -108 -124 L30 -124 Q55 -122 66 -104 L80 -58 Z" fill="#23272B" opacity=".55"/>'
            '<circle cx="-150" cy="70" r="42" fill="#23272B"/><circle cx="130" cy="70" r="42" fill="#23272B"/>'
            '<rect x="30" y="-190" width="190" height="76" rx="8" fill="#fff" stroke="#23272B" stroke-width="6" transform="rotate(-3 125 -152)"/>'
            '<text x="125" y="-140" font-family="Arial Black,Arial" font-size="46" fill="#23272B" text-anchor="middle">${{ }}</text></g>')


def icon_dos(r=1.0):
    """Mini-diagrama: dos X3 Pro en fila con contador."""
    c = icon_x3_side(.62)
    return f'<g transform="translate(-170 20)">{c}</g><g transform="translate(190 40) scale(.8)">{c}</g>' \
           f'<rect x="-90" y="120" width="180" height="60" rx="8" fill="#FFD84D"/><text x="0" y="163" font-family="Arial Black,Arial" font-size="44" fill="#23272B" text-anchor="middle">QUEDAN 2</text>'


def icon_escritorio(r=1.0):
    """Mini-diagrama: escritorio con recibo y llaves."""
    return (f'<g transform="scale({r})">'
            '<rect x="-230" y="20" width="460" height="34" fill="#FFD84D"/>'
            '<rect x="-150" y="-70" width="180" height="90" rx="8" fill="#fff" stroke="#23272B" stroke-width="6" transform="rotate(-4 -60 -25)"/>'
            '<path d="M120 -30 l60 0 l0 -18 l24 0 l0 18 l14 0 l0 26 l-24 0 l0 12 l-74 0 Z" fill="#FFD84D" stroke="#23272B" stroke-width="6"/>'
            '<text x="0" y="-140" font-family="Arial Black,Arial" font-size="44" fill="#FFD84D" text-anchor="middle">RECIBO + LLAVES</text></g>')


def icon_fachada(r=1.0):
    """Mini-diagrama: fachada con portón y letrero."""
    return (f'<g transform="scale({r})">'
            '<rect x="-250" y="-140" width="500" height="240" fill="#FFD84D" opacity=".25"/>'
            '<rect x="-250" y="-140" width="500" height="70" fill="#FFD84D"/>'
            '<rect x="-190" y="-40" width="380" height="140" fill="#23272B" stroke="#FFD84D" stroke-width="8"/>'
            '<line x1="-190" y1="0" x2="190" y2="0" stroke="#FFD84D" stroke-width="10"/>'
            '<line x1="-190" y1="40" x2="190" y2="40" stroke="#FFD84D" stroke-width="10"/>'
            '<line x1="-190" y1="80" x2="190" y2="80" stroke="#FFD84D" stroke-width="10"/>'
            '<text x="0" y="-95" font-family="Arial Black,Arial" font-size="46" fill="#23272B" text-anchor="middle">SANTA RITA</text></g>')


def icon_placa(r=1.0):
    """Mini-diagrama: placa final, carro oscuro + marca."""
    return (f'<g transform="scale({r})">'
            '<rect x="-260" y="-150" width="520" height="300" rx="20" fill="#141C21" stroke="#FFD84D" stroke-width="8"/>'
            '<path d="M-170 80 L-160 20 Q-150 -10 -120 -18 L-105 -55 Q-98 -72 -72 -74 L70 -74 Q100 -72 112 -50 '
            'L128 -16 Q165 -8 178 22 L186 80 Z" fill="#3A4A55"/>'
            '<text x="0" y="-100" font-family="Arial Black,Arial" font-size="50" fill="#FFD84D" text-anchor="middle">KAIYI YANTAI MOTORS</text></g>')


def card(texto, y=1200, size=72):
    """Tarjeta de texto grande sobre la imagen, dentro de la zona segura."""
    lineas = texto.split("|")
    alto = 70 + int(size * 1.15) * len(lineas)
    t = "".join(f'<text x="470" y="{y + 40 + size + i * int(size * 1.15)}" font-family="Arial Black,Arial" font-size="{size}" '
                f'fill="#23272B" text-anchor="middle">{l}</text>' for i, l in enumerate(lineas))
    return f'<rect x="90" y="{y}" width="760" height="{alto}" rx="20" fill="#FFD84D"/>{t}'


ZONA = ('<rect x="0" y="230" width="850" height="1210" fill="none" stroke="#DC2626" stroke-width="5" stroke-dasharray="20 14" opacity=".6"/>')

TOMAS = [
    dict(t="0:00-0:02", cam="Foto del reloj de pared del showroom marcando las 8:00 en punto. Zoom lento hacia el reloj.",
         ve="El reloj del showroom marcando 8:00 en punto.",
         voz="“8 am: comienza el Black Friday.”", txt="8 AM · BLACK FRIDAY",
         svg=FONDO + foto(140, 380, 800, 1000, "RELOJ DE PARED A LAS 8:00", "encuadre cerrado · zoom lento", icon_reloj("8:00")) + card("8 AM:|BLACK FRIDAY")),
    dict(t="0:02-0:04", cam="Corte: lateral 3/4 de la X3 Pro con el tarjetón del precio en el parabrisas. La cámara entra despacio al precio.",
         ve="Lateral de la X3 Pro, de perfil, con el precio en tarjetón sobre el parabrisas.",
         voz="“Kaiyi X3 Pro: {{precio}}. De contado.”", txt="X3 PRO ${{ }} · CONTADO",
         svg=FONDO + foto(140, 380, 800, 1000, "LATERAL 3/4 X3 PRO", "tarjetón en el parabrisas", icon_x3_side()) + card("X3 PRO ${{ }}|DE CONTADO", 1160, 56)),
    dict(t="0:04-0:06", cam="Foto de las dos X3 Pro en fila con el tarjetón del contador a la vista.",
         ve="Las dos X3 Pro en fila, de frente o 3/4.",
         voz="“Contando: solo quedan 2.”", txt="SOLO QUEDAN 2",
         svg=FONDO + foto(140, 380, 800, 1000, "LAS DOS X3 PRO", "en fila · tarjetón del contador", icon_dos()) + card("SOLO|QUEDAN 2")),
    dict(t="0:06-0:08", cam="Foto de la fachada de Av. 8 Santa Rita con el portón.",
         ve="Fachada del showroom en Santa Rita.",
         voz="“Kaiyi Yantai Motors. Santa Rita.”", txt="SANTA RITA",
         svg=FONDO + foto(140, 380, 800, 1000, "FACHADA SANTA RITA", "Av. 8 con 82B y 83", icon_fachada()) + card("KAIYI YANTAI MOTORS|SANTA RITA", 1160, 52)),
    dict(t="0:08-0:10", cam="El mismo reloj de la toma 1: la manecilla avanza hacia las 6 en edición (o serie de fotos del reloj avanzando). Se sostiene 2 s.",
         ve="El reloj avanzando hasta las 6: se acaba el día.",
         voz="“Black Friday, hasta las 6.”", txt="HASTA LAS 6",
         svg=FONDO + foto(140, 380, 800, 1000, "RELOJ AVANZANDO A LAS 6:00", "manecilla en movimiento · edición", icon_reloj("6:00")) + card("BLACK FRIDAY|HASTA LAS 6")),
]

STORIES = [
    ("8:00 am · Reel compartido", "El precio ya salió.", ""),
    ("Cada venta confirmada", "Vendida una. Queda {{N}}.", "Actualizar el contador solo con venta confirmada"),
    ("12:00 m", "Disponible: {{N}}.", "Foto de las que quedan"),
    ("3:00 pm", "¿Viniste hoy?", "Encuesta: Sí / No pude"),
    ("5:00 pm", "Queda 1 hora.", "Última llamada"),
    ("6:00 pm", "Se acabó. Gracias, Santa Rita.", "Portón cerrándose"),
]

CSS = f"""
@page {{ size: Letter landscape; margin: 9mm 10mm }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 11px }}
.pg {{ break-after: page }} .pg:last-child {{ break-after: auto }}
.top {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 3px solid {AZUL}; padding-bottom: 4px; margin-bottom: 8px }}
.top b {{ font-size: 16px; color: {AZUL} }} .top span {{ color: #64748B; font-size: 10px }}
.row {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 6px }}
.f svg {{ width: 100%; aspect-ratio: 9/16; display: block; border: 2px solid #23272B; border-radius: 8px; background: #23272B }}
.f .tt {{ display: flex; justify-content: space-between; margin: 3px 0 2px; font-weight: 800; color: {AZUL}; font-size: 8px }}
.f p {{ margin: 1px 0; line-height: 1.2; font-size: 7.5px }}
.f .v {{ background: #F1F5F9; border-left: 3px solid #FFD84D; padding: 2px 4px; font-style: italic }}
.f .t {{ color: #101418; font-weight: 700; font-size: 9px }}
.leg {{ margin-top: 6px; color: #64748B; font-size: 9.5px }}
.two {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px }}
h3 {{ font-size: 12.5px; color: {AZUL}; margin: 8px 0 4px }}
table {{ width: 100%; border-collapse: collapse; font-size: 10px }}
th {{ background: #E2E8F0; text-align: left; padding: 2px 5px; font-size: 9px; text-transform: uppercase }}
td {{ border-bottom: 1px solid #E2E8F0; padding: 2px 5px; vertical-align: top }}
.carteles {{ display: flex; gap: 10px; flex-wrap: wrap }}
.cart {{ border: 3px solid #FFD84D; background: #23272B; color: #fff; padding: 6px 10px; font: 900 15px 'Arial Black', Arial }}
.cart small {{ display: block; font: 400 8.5px Arial; color: #94A3B8; font-weight: 400 }}
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
    return f'<table><tr><th>#</th><th>Se ve</th><th>Cámara / edición</th></tr>{filas}</table>'


DOC = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Mockup reel precio · Yantai · vie 27 · fotos + textos</title>
<style>{CSS}</style></head><body>
<section class="pg">
  <div class="top"><b>Mockup · Reel “8 y 6” · @yantaimotors · fotos + textos</b><span>Vie 27 nov · 8:00 am · 14.6 s · vertical 1080x1920</span></div>
  <div class="row">{tomas_html()}</div>
  <p class="leg">Los recuadros punteados son la foto o video real a grabar; la tarjeta amarilla es el texto grande en pantalla (dentro de la zona segura, línea roja).
  ${{ }} = precio real por confirmar. Sin marcadores en esta pieza: solo imágenes del carro real y textos grandes.</p>
</section>
<section class="pg">
  <div class="top"><b>Producción · Reel “8 y 6”</b><span>Fotografiar el jue 26 en la tarde · montar y publicar vie 27, 8:00 am</span></div>
  <div class="two">
    <div>
      <h3>Ficha</h3>
      <table>
        <tr><th>Sale</th><td>Nadie en cámara: fotos del carro real + tarjetas de texto. (Si hay asesor disponible, una foto suya junto a las unidades es ganancia: la gente mira gente)</td></tr>
        <tr><th>Graba</th><td>Un asesor con celular; trípode para las fotos fijas</td></tr>
        <tr><th>Lugar</th><td>Showroom de Av. 8 Santa Rita, luz encendida</td></tr>
        <tr><th>Edición</th><td>Corte seco por foto, zoom lento 5-8% por toma. Subtítulos quemados. Música baja opcional o nada: los cortes mandan</td></tr>
        <tr><th>Regla</th><td>El contador QUEDAN N solo se actualiza con venta confirmada. Nunca publicar “quedan pocas”</td></tr>
        <tr><th>Dato</th><td>1.5T turbo, 154 HP: confirmado en la ficha de la cuenta. Todo lo demás va con {{ }} hasta Gerencia</td></tr>
      </table>
      <h3>Fotos a capturar el jue 26 (8 en 20 minutos)</h3>
      <div class="carteles">
        <div class="cart">RELOJ 8:00<small>pared del showroom · y segunda foto con la manecilla en 6:00 (o portón al atardecer)</small></div>
        <div class="cart">LATERAL 3/4 + TARJETÓN<small>precio ${{ }} escrito en cartulina blanca, pegado al parabrisas · 1</small></div>
        <div class="cart">LAS DOS EN FILA<small>con contador QUEDAN 2 en tarjetón · 1</small></div>
        <div class="cart">ESCRITORIO DE VENTAS<small>recibo, lápiz y llaves listas · 1</small></div>
        <div class="cart">FACHADA<small>Santa Rita, con el portón · 1</small></div>
      </div>
      <h3>Texto para decir (voz en off seca, grabada aparte)</h3>
      <table><tr><td>8 am: comienza el Black Friday.<br>Kaiyi X3 Pro: {{precio}}. De contado.<br>Contando: solo quedan 2.<br>Kaiyi Yantai Motors. Santa Rita.<br>Black Friday, hasta las 6.</td></tr></table>
      <h3>Checklist antes de las 8:00 am</h3>
      <ul>
        <li>Precio real confirmado por Gerencia y escrito en el tarjetón.</li>
        <li>Las 7 fotos tomadas y montadas el jue 26; el reel ya montado y revisado antes de dormir.</li>
        <li>Tarjetón del precio legible en la foto lateral (contraste alto, letra gruesa).</li>
        <li>Contador QUEDAN 2 correcto en la foto 6; si se vende antes, remontar con el número nuevo.</li>
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
        <li>{{precio}} de la X3 Pro: decisión de Gerencia.</li>
        <li>Después de cada venta: story del contador corregido + DM a la lista BLACK con las que quedan.</li>
        <li>A las 6 pm: story de cierre aunque no se hayan vendido.</li>
      </ul>
    </div>
  </div>
</section>
</body></html>"""

os.makedirs(OUT_DIR, exist_ok=True)
out_html = os.path.join(OUT_DIR, "Mockup-Reel-Vie27-Precio-Yantai.html")
out_pdf = os.path.join(OUT_DIR, "Mockup-Reel-Vie27-Precio-Yantai.pdf")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(DOC)
try:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    out_pdf = None
print(out_pdf or out_html)
