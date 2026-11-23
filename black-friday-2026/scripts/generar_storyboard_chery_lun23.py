"""Storyboard para grabar: reel @cherymaracaibo lun 23 nov · "Te dije que eran 4" · 15 s · PROPUESTA.
Sigue al reel del jue 19: la asesora de blanco con lentes negros, en blanco y negro, revela las 4 unidades
(2 Tiggo 4 + 2 Himla) y dice las reglas: de contado, viernes 27, de quien pague primero, precio el jueves a la lista.
Salida: black-friday-2026/entregables/Storyboard-Chery-Lun23.pdf
Uso: python black-friday-2026/scripts/generar_storyboard_chery_lun23.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
VINO = "#8A1C2B"

FONDO = ('<rect width="1080" height="1920" fill="#D9D9D9"/><rect y="1250" width="1080" height="670" fill="#BDBDBD"/>'
         '<path d="M540 1250 L-200 1920 M540 1250 L1280 1920" stroke="#AAAAAA" stroke-width="6"/>')
BLUR = '<defs><filter id="bl"><feGaussianBlur stdDeviation="12"/></filter></defs>'


def asesora(x, y, s=1.0, lentes=True, texto_lentes="", apartada=False):
    """Asesora vestida de blanco, de frente. Lentes negros opcionales, con texto en los cristales."""
    lt = ""
    if lentes:
        lt = ('<rect x="-78" y="-500" width="66" height="40" rx="10" fill="#0B0B0B"/>'
              '<rect x="12" y="-500" width="66" height="40" rx="10" fill="#0B0B0B"/><path d="M-12 -485 h24" stroke="#0B0B0B" stroke-width="8"/>')
        if texto_lentes:
            lt += (f'<text x="0" y="-472" font-family="Arial Black,Arial" font-size="26" fill="#fff" text-anchor="middle" '
                   f'letter-spacing="2">{texto_lentes}</text>')
    else:
        lt = '<circle cx="-40" cy="-480" r="9" fill="#111"/><circle cx="40" cy="-480" r="9" fill="#111"/>'
    rot = ' rotate(-8)' if apartada else ''
    return (f'<g transform="translate({x} {y}) scale({s}){rot}">'
            '<path d="M-110 -470 Q-110 -600 0 -600 Q110 -600 110 -470 L120 -330 L-120 -330 Z" fill="#1A1A1A"/>'
            '<circle cx="0" cy="-470" r="88" fill="#A8A8A8"/>' + lt +
            '<path d="M-30 -425 q30 18 60 0" stroke="#333" stroke-width="7" fill="none"/>'
            '<path d="M-200 320 L-175 -260 Q-150 -365 0 -370 Q150 -365 175 -260 L200 320 Z" fill="#FAFAFA" stroke="#C8C8C8" stroke-width="5"/>'
            '<rect x="-150" y="320" width="120" height="420" fill="#F2F2F2" stroke="#C8C8C8" stroke-width="4"/>'
            '<rect x="30" y="320" width="120" height="420" fill="#F2F2F2" stroke="#C8C8C8" stroke-width="4"/></g>')


def tiggo(x, y, s=1.0, nota=True):
    n = ('<rect x="-80" y="-300" width="160" height="60" fill="#F4EDE1" stroke="#555" stroke-width="3"/>'
         '<text x="0" y="-262" font-family="Segoe Print,cursive" font-size="18" text-anchor="middle">SU PRIMERA HISTORIA</text>') if nota else ""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M-260 0 L-250 -140 Q-220 -190 -150 -200 L-90 -320 Q-70 -345 -20 -345 L170 -345 Q220 -345 250 -290 '
            'L270 -180 Q290 -140 280 0 Z" fill="#9E9E9E"/>'
            '<path d="M-80 -205 L-30 -315 L160 -315 L200 -205 Z" fill="#5E5E5E"/>' + n +
            '<circle cx="-150" cy="0" r="70" fill="#1A1A1A"/><circle cx="170" cy="0" r="70" fill="#1A1A1A"/>'
            '<text x="10" y="120" font-family="Arial" font-weight="700" font-size="44" fill="#444" text-anchor="middle">TIGGO 4</text></g>')


def himla(x, y, s=1.0, nota=True):
    n = ('<rect x="-170" y="-310" width="160" height="60" fill="#F4EDE1" stroke="#555" stroke-width="3"/>'
         '<text x="-90" y="-272" font-family="Segoe Print,cursive" font-size="18" text-anchor="middle">SU PRIMERA JORNADA</text>') if nota else ""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M-300 0 L-290 -150 Q-270 -190 -210 -200 L-160 -330 Q-140 -350 -100 -350 L40 -350 L60 -200 L300 -200 L310 0 Z" fill="#8E8E8E"/>'
            '<path d="M-180 -205 L-130 -320 L30 -320 L40 -205 Z" fill="#555"/>'
            '<path d="M70 -195 h230 v40 h-230 Z" fill="#777"/>' + n +
            '<circle cx="-190" cy="0" r="72" fill="#1A1A1A"/><circle cx="190" cy="0" r="72" fill="#1A1A1A"/>'
            '<text x="0" y="122" font-family="Arial" font-weight="700" font-size="44" fill="#444" text-anchor="middle">HIMLA</text></g>')


def card(texto, y=300, size=80):
    lineas = texto.split("|")
    return "".join(f'<text x="470" y="{y + size + i * int(size * 1.15)}" font-family="Arial Black,Arial" font-size="{size}" '
                   f'fill="#fff" stroke="#111" stroke-width="10" paint-order="stroke" text-anchor="middle" '
                   f'letter-spacing="2">{l}</text>' for i, l in enumerate(lineas))


ZONA = '<rect x="0" y="230" width="850" height="1210" fill="none" stroke="#DC2626" stroke-width="5" stroke-dasharray="20 14" opacity=".7"/>'
CUATRO = tiggo(200, 1430, .42) + tiggo(430, 1480, .42) + himla(670, 1430, .4) + himla(900, 1480, .4)

TOMAS = [
    dict(t="0:00-0:03", ve="Ella de frente, con los lentes puestos. Detrás, las cuatro unidades fuera de foco.",
         voz="Te dije que eran 4.", txt="TE DIJE: 4", cam="Plano medio, ella al centro, fondo desenfocado.",
         svg=FONDO + BLUR + f'<g filter="url(#bl)">{CUATRO}</g>' + asesora(540, 1300, 1.0) + card("TE DIJE: 4", 300, 100)),
    dict(t="0:03-0:05", ve="Se quita los lentes y da un paso al lado; el foco pasa a las cuatro.",
         voz="Estas son.", txt="CUATRO HISTORIAS", cam="Cambio de foco de ella a las unidades en el mismo movimiento.",
         svg=FONDO + CUATRO + asesora(950, 1500, .7, lentes=False, apartada=True) + card("CUATRO|HISTORIAS", 300, 86)),
    dict(t="0:05-0:08", ve="Camina junto a las dos Tiggo 4, con su nota en el parabrisas.",
         voz="Dos Tiggo 4, para la familia.", txt="2 TIGGO 4", cam="Cámara la acompaña de lado, despacio.",
         svg=FONDO + tiggo(420, 1420, .8) + tiggo(780, 1520, .55) + asesora(880, 1450, .6, lentes=False) + card("2 TIGGO 4", 300, 100)),
    dict(t="0:08-0:11", ve="Pasa junto a las dos Himla, con su nota en el parabrisas.",
         voz="Dos Himla, para el trabajo.", txt="2 HIMLA", cam="Mismo movimiento lateral, sin corte brusco.",
         svg=FONDO + himla(440, 1420, .75) + himla(800, 1520, .5) + asesora(150, 1480, .6, lentes=False) + card("2 HIMLA", 300, 100)),
    dict(t="0:11-0:13", ve="Se detiene frente a las cuatro, a cámara.", voz="De contado, el viernes 27.",
         txt="VIERNES 27 · CONTADO", cam="Plano abierto, ella al frente.",
         svg=FONDO + CUATRO + asesora(540, 1480, .75, lentes=False) + card("VIERNES 27|CONTADO", 300, 88)),
    dict(t="0:13-0:15", ve="Plano medio, seria, a cámara.", voz="Cada una, para quien la pague primero.",
         txt="QUIEN PAGUE PRIMERO", cam="Plano medio fijo.",
         svg=FONDO + BLUR + f'<g filter="url(#bl)">{CUATRO}</g>' + asesora(540, 1350, .95, lentes=False)
             + card("QUIEN PAGUE|PRIMERO", 300, 86)),
    dict(t="0:15-0:18", ve="Se vuelve a poner los lentes: en los cristales se lee BLACK. Corta a la placa negra.",
         voz="El jueves te mando el precio. Escríbeme BLACK.", txt="ESCRIBE BLACK",
         cam="Primer plano del rostro y los lentes. Placa: Black Friday · Dai Motors Chery.",
         svg='<rect width="1080" height="1920" fill="#CFCFCF"/>' + asesora(540, 1900, 2.2, texto_lentes="BLACK")
             + card("ESCRIBE|BLACK", 300, 100)),
]

STORIES = [
    ("Video: se quita los lentes y aparecen las cuatro", "Ya las conoces.", ""),
    ("Foto de las Tiggo 4", "Dos Tiggo 4. {{versión}}.", ""),
    ("Foto de las Himla con el platón a la vista", "Dos Himla. {{versión}}.", ""),
    ("La asesora a cámara", "¿Cuál es tu próxima historia?", "Encuesta: Familia (Tiggo 4) / Trabajo (Himla)"),
    ("Fondo negro, letras con contorno", "Mañana: todo lo que necesitas saber.", ""),
]

CSS = f"""
@page {{ size: Letter landscape; margin: 9mm 10mm }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 10px }}
.pg {{ break-after: page }} .pg:last-child {{ break-after: auto }}
.top {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 3px solid {VINO}; padding-bottom: 4px; margin-bottom: 8px }}
.top b {{ font-size: 15px; color: {VINO} }} .top span {{ color: #64748B; font-size: 10px }}
.row {{ display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px }}
.f svg {{ width: 100%; aspect-ratio: 9/16; display: block; border: 2px solid #0B0B0F; border-radius: 10px }}
.f .tt {{ display: flex; justify-content: space-between; margin: 5px 0 2px; font-weight: 800; color: {VINO}; font-size: 11px }}
.f p {{ margin: 2px 0; line-height: 1.26 }}
.f .v {{ background: #F1F5F9; border-left: 3px solid {VINO}; padding: 3px 5px; font-style: italic }}
.f .c {{ color: #475569; font-size: 9px }}
.leg {{ margin-top: 6px; color: #64748B; font-size: 9.5px }}
.two {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px }}
h3 {{ font-size: 12.5px; color: {VINO}; margin: 8px 0 4px }}
table {{ width: 100%; border-collapse: collapse; font-size: 10.5px }}
th {{ background: #E2E8F0; text-align: left; padding: 3px 6px; font-size: 9.5px; text-transform: uppercase; width: 90px }}
td {{ border-bottom: 1px solid #E2E8F0; padding: 3px 6px; vertical-align: top }}
.carteles {{ display: flex; gap: 10px; flex-wrap: wrap }}
.cart {{ border: 2px solid #555; padding: 8px 14px; font: 700 16px 'Segoe Print', cursive; background: #F4EDE1 }}
.cart small {{ display: block; font: 400 9px Arial; color: #64748B }}
.st {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px }}
.st div {{ aspect-ratio: 9/16; border: 2px solid #CBD5E1; border-radius: 8px; padding: 8px; display: flex; flex-direction: column;
  justify-content: space-between; font-size: 10px; background: #1A1A1A; color: #fff }}
.st b {{ font-size: 12px }} .st i {{ color: #9CA3AF }} .st em {{ color: #F4C2C2; font-style: normal; font-weight: 700 }}
ul {{ padding-left: 14px }} li {{ margin: 2px 0 }}
"""


def tomas_html():
    return "".join(
        f'<div class="f"><svg viewBox="0 0 1080 1920">{t["svg"]}{ZONA}</svg>'
        f'<div class="tt"><span>Toma {i}</span><span>{t["t"]}</span></div>'
        f'<p><b>Se ve:</b> {html.escape(t["ve"])}</p><p class="v">“{html.escape(t["voz"])}”</p>'
        f'<p><b>Texto:</b> {html.escape(t["txt"])}</p><p class="c"><b>Cámara:</b> {html.escape(t["cam"])}</p></div>'
        for i, t in enumerate(TOMAS, 1))


def stories_html():
    return "".join(f'<div><i>{i}. {html.escape(a)}</i><b>“{html.escape(b)}”</b><em>{html.escape(c)}</em></div>'
                   for i, (a, b, c) in enumerate(STORIES, 1))


DOC = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Storyboard Chery lun 23</title>
<style>{CSS}</style></head><body>
<section class="pg">
  <div class="top"><b>Storyboard · Reel “Te dije que eran 4” · @cherymaracaibo</b>
  <span>Lun 23 nov · 7:00 pm · 18 s · vertical 1080x1920 · PROPUESTA PARA REVISAR</span></div>
  <div class="row">{tomas_html()}</div>
  <p class="leg">Línea roja punteada: zona segura del texto. Todo en blanco y negro, como el teaser y el reel del jue 19: el vestido blanco
  y los lentes negros son lo que más resalta. Dibujos de referencia de encuadre, no de vestuario ni de modelos.</p>
</section>
<section class="pg">
  <div class="top"><b>Producción · Reel “Te dije que eran 4”</b><span>Grabar vie 20 o lun 23 en la mañana · publicar lun 23, 7 pm</span></div>
  <div class="two">
    <div>
      <h3>Ficha</h3>
      <table>
        <tr><th>Sale</th><td>La misma asesora del jue 19, vestida de blanco, con los mismos lentes negros. Habla a cámara</td></tr>
        <tr><th>Graba</th><td>Un asesor, celular en vertical a la altura de los ojos de ella; micrófono de solapa</td></tr>
        <tr><th>Lugar</th><td>Showroom: dos Tiggo 4 a un lado, dos Himla al otro, en fila</td></tr>
        <tr><th>Audio</th><td>La música del teaser, baja debajo de la voz. Golpe de sonido cuando el foco pasa a las cuatro (toma 2)</td></tr>
        <tr><th>Edición</th><td>Blanco y negro con contraste alto. Textos con las letras con contorno del teaser. Placa final:
        Black Friday · Dai Motors Chery. En la toma 7, "BLACK" en los cristales se agrega en edición</td></tr>
      </table>
      <h3>Notas para los parabrisas (papel crema, letra a mano)</h3>
      <div class="carteles">
        <div class="cart">SU PRIMERA HISTORIA<small>Tiggo 4 · 2</small></div>
        <div class="cart">SU PRIMERA JORNADA<small>Himla · 2</small></div>
      </div>
      <h3>Checklist antes de grabar</h3>
      <ul>
        <li>Mismo vestido blanco y mismos lentes que el jue 19.</li>
        <li>Las 4 unidades limpias, en fila, con su nota en el parabrisas.</li>
        <li>Placas tapadas o fuera de cuadro si no se quieren mostrar.</li>
        <li>Ensayar el cambio de foco de la toma 2 (tocar la pantalla del celular sobre las unidades).</li>
        <li>Grabar 2 o 3 tomas de cada plano. Fotos para las stories: las Tiggo 4 y las Himla con el platón a la vista.</li>
      </ul>
    </div>
    <div>
      <h3>Stories del lun 23 · 5 frames</h3>
      <div class="st">{stories_html()}</div>
      <h3>Texto para decir (ella, a cámara)</h3>
      <table><tr><td>Te dije que eran 4.<br>Estas son.<br>Dos Tiggo 4, para la familia.<br>Dos Himla, para el trabajo.<br>
      De contado, el viernes 27.<br>Cada una, para quien la pague primero.<br>El jueves te mando el precio. Escríbeme BLACK.</td></tr></table>
      <h3>Pendiente</h3>
      <ul><li>Confirmar que el reel del jue 19 se grabó con esta asesora.</li>
      <li>Versión de cada modelo para las stories 2 y 3.</li>
      <li>Aprobar esta versión antes de pasarla al guion.</li></ul>
    </div>
  </div>
</section>
</body></html>"""

os.makedirs(OUT_DIR, exist_ok=True)
out_html = os.path.join(OUT_DIR, "Storyboard-Chery-Lun23.html")
out_pdf = os.path.join(OUT_DIR, "Storyboard-Chery-Lun23.pdf")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(DOC)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(out_pdf)
