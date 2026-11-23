"""Storyboard para grabar: reel @yantaimotors lun 23 nov · "¿Acertaste?" · opción A "Un paso atrás desde la ventana" · 15 s.
La ventana del jueves ya se borró y no hay plástico: la toma 1 reusa el final del reel del jue 19 y la revelación es alejarse de la misma ventana, ya limpia.
Los textos van en edición, con letra naranja tipo marcador. Nadie en cámara: solo una mano y voz en off.
Salida: black-friday-2026/entregables/Storyboard-Yantai-Lun23.pdf
Uso: python black-friday-2026/scripts/generar_storyboard_yantai_lun23.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
COLOR = "#374151"
NARANJA = "#FF7A1A"

FONDO = '<rect width="1080" height="1920" fill="#0E2427"/>'
MARCO_VENTANA = ('<path d="M60 300 L1020 220 L1020 1500 L60 1560 Z" fill="#1C4A4F" stroke="#091A1C" stroke-width="40"/>'
                 '<path d="M120 380 Q500 330 980 290" stroke="#5FA3A8" stroke-width="10" opacity=".4" fill="none"/>')
PLASTICO = ''.join(f'<path d="M{x} {y} q60 -80 120 0 t120 10" stroke="#9CC9CC" stroke-width="5" fill="none" opacity=".45"/>'
                   for x, y in [(150, 700), (420, 900), (250, 1150), (600, 1250), (500, 600), (700, 1050)])


def mano(x, y, rot=0, marcador=False):
    m = (f'<rect x="-30" y="-230" width="34" height="170" rx="8" fill="#1B1B1B"/><rect x="-28" y="-250" width="30" height="30" fill="{NARANJA}"/>'
         if marcador else "")
    return (f'<g transform="translate({x} {y}) rotate({rot})">{m}'
            '<ellipse cx="0" cy="0" rx="120" ry="85" fill="#C98B62"/>'
            '<rect x="-70" y="40" width="140" height="300" rx="40" fill="#2B2B2B"/></g>')


def suv(x, y, s=1.0, plastico=False):
    p = PLASTICO.replace('stroke-width="5"', 'stroke-width="9"') if plastico else ""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M-420 0 L-410 -150 Q-380 -200 -300 -210 L-200 -330 Q-170 -360 -100 -360 L250 -360 Q320 -360 360 -300 '
            'L420 -190 Q440 -150 430 0 Z" fill="#C9D1D6"/>'
            '<path d="M-180 -210 L-110 -320 L60 -320 L60 -210 Z" fill="#26484C"/>'
            '<path d="M80 -210 L80 -320 L240 -320 Q290 -320 320 -270 L350 -210 Z" fill="#26484C"/>'
            f'{p}'
            '<circle cx="-250" cy="0" r="85" fill="#141414"/><circle cx="-250" cy="0" r="35" fill="#777"/>'
            '<circle cx="270" cy="0" r="85" fill="#141414"/><circle cx="270" cy="0" r="35" fill="#777"/></g>')


def card(texto, y=300, size=78):
    """Texto en pantalla, en edición, con letra tipo marcador naranja."""
    lineas = texto.split("|")
    out = ""
    for i, l in enumerate(lineas):
        out += (f'<text x="470" y="{y + size + i * int(size * 1.2)}" font-family="Segoe Print,Comic Sans MS,cursive" '
                f'font-size="{size}" font-weight="700" fill="{NARANJA}" text-anchor="middle" '
                f'stroke="#0E2427" stroke-width="3" paint-order="stroke">{l}</text>')
    return out


ZONA = '<rect x="0" y="230" width="850" height="1210" fill="none" stroke="#DC2626" stroke-width="5" stroke-dasharray="20 14" opacity=".7"/>'
ESCRITO = (f'<g font-family="Segoe Print,Comic Sans MS,cursive" font-size="120" fill="{NARANJA}" font-weight="700">'
           '<text x="170" y="760">1. TURBO</text><text x="170" y="960">2. CVT</text><text x="170" y="1160">3. 5</text></g>')

TOMAS = [
    dict(t="0:00-0:02", tipo="Reusar video del jue 19",
         ve='Los últimos 2 s del reel del jueves: la ventana escrita "1. TURBO · 2. CVT · 3. 5".',
         voz="¿Acertaste?", txt="¿ACERTASTE?",
         cam="No se graba: se corta del reel del jue 19.",
         svg=FONDO + MARCO_VENTANA + PLASTICO + ESCRITO + card("¿ACERTASTE?", 260, 96)),
    dict(t="0:02-0:05", tipo="Grabar",
         ve="Corte a la misma ventana, ya limpia. Primer plano del vidrio; la cámara empieza a alejarse despacio.",
         voz="Es la Kaiyi X3 Pro.", txt="KAIYI X3 PRO",
         cam="Arranca pegada a la ventana, en el mismo encuadre que el jueves, para que el corte se sienta continuo.",
         svg=FONDO + MARCO_VENTANA + '<path d="M700 520 l-70 160 M760 900 l-50 120" stroke="#9CC9CC" stroke-width="8" opacity=".5"/>'
             + '<path d="M520 1640 l0 120 M470 1710 l50 50 l50 -50" stroke="#fff" stroke-width="12" fill="none"/>'
             + card("KAIYI X3 PRO", 280, 92)),
    dict(t="0:05-0:07", tipo="Grabar",
         ve="La cámara termina de alejarse: la X3 Pro completa y la otra al lado.",
         voz="Y solo hay 2.", txt="SOLO 2",
         cam="Sigue el mismo movimiento de la toma 2, sin corte, hasta el plano abierto.",
         svg=FONDO + '<rect y="1300" width="1080" height="620" fill="#0A1B1D"/>'
             + suv(330, 1250, .62) + suv(780, 1330, .62) + card("SOLO 2", 300, 130)),
    dict(t="0:07-0:10", tipo="Grabar",
         ve="Recorrido rápido por las dos: frente, rin, costado.",
         voz="De contado, el viernes 27.", txt="DE CONTADO|VIERNES 27",
         cam="Cámara en mano, tres cortes de un segundo.",
         svg=FONDO + '<rect y="1300" width="1080" height="620" fill="#0A1B1D"/>' + suv(560, 1350, .95)
             + card("DE CONTADO|VIERNES 27", 300, 84)),
    dict(t="0:10-0:13", tipo="Grabar",
         ve="La mano abre la puerta trasera de una; se ven los asientos.",
         voz="El precio llega el jueves 26, solo a la lista.", txt="PRECIO|JUEVES 26",
         cam="Plano medio de la puerta, la mano entra por la derecha.",
         svg=FONDO + '<rect x="150" y="620" width="560" height="820" rx="30" fill="#C9D1D6"/>'
             '<rect x="200" y="680" width="460" height="340" rx="20" fill="#26484C"/>'
             '<rect x="260" y="1060" width="340" height="300" rx="30" fill="#3B3B3B"/>' + mano(780, 1060, 15)
             + card("PRECIO|JUEVES 26", 280, 84)),
    dict(t="0:13-0:15", tipo="Grabar",
         ve="Plano abierto de las dos. Corte a la placa final.",
         voz="Comenta BLACK si acertaste.", txt="COMENTA BLACK",
         cam="Plano abierto fijo, 2 s. Luego la placa negra del jueves.",
         svg=FONDO + '<rect y="1300" width="1080" height="620" fill="#0A1B1D"/>' + suv(330, 1250, .62) + suv(780, 1330, .62)
             + card("COMENTA|BLACK", 300, 110)),
]

STORIES = [
    ('Video: la cámara se aleja de la ventana y aparecen las dos', "Ahí están. ¿Acertaste?", ""),
    ("Foto de las dos X3 Pro de lado", "Kaiyi X3 Pro. Son 2.", ""),
    ("Foto del motor", "Turbo. Caja CVT.", ""),
    ("Foto de una de frente", "¿Vienes a verlas antes del viernes?", "Encuesta: Esta semana / El viernes"),
    ("Mapa o foto de la fachada", "Av. 8 Santa Rita con 82B y 83. Mañana: las reglas.", ""),
]

CSS = f"""
@page {{ size: Letter landscape; margin: 9mm 10mm }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 10.5px }}
.pg {{ break-after: page }} .pg:last-child {{ break-after: auto }}
.top {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 3px solid {COLOR}; padding-bottom: 4px; margin-bottom: 8px }}
.top b {{ font-size: 16px; color: {COLOR} }} .top span {{ color: #64748B; font-size: 10px }}
.row {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 9px }}
.f svg {{ width: 100%; aspect-ratio: 9/16; display: block; border: 2px solid #0B0B0F; border-radius: 10px }}
.f .tt {{ display: flex; justify-content: space-between; margin: 5px 0 2px; font-weight: 800; color: {COLOR}; font-size: 11.5px }}
.f .tag {{ display: inline-block; font-size: 9px; font-weight: 800; padding: 1px 6px; border-radius: 4px; background: #E5E7EB; margin-bottom: 3px }}
.f .tag.r {{ background: #FEF3C7; color: #92400E }}
.f p {{ margin: 2px 0; line-height: 1.28 }}
.f .v {{ background: #F1F5F9; border-left: 3px solid {NARANJA}; padding: 3px 5px; font-style: italic }}
.f .c {{ color: #475569; font-size: 9.5px }}
.leg {{ margin-top: 6px; color: #64748B; font-size: 9.5px }}
.two {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px }}
h3 {{ font-size: 12.5px; color: {COLOR}; margin: 8px 0 4px }}
table {{ width: 100%; border-collapse: collapse; font-size: 10.5px }}
th {{ background: #E2E8F0; text-align: left; padding: 3px 6px; font-size: 9.5px; text-transform: uppercase; width: 90px }}
td {{ border-bottom: 1px solid #E2E8F0; padding: 3px 6px; vertical-align: top }}
.st {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px }}
.st div {{ aspect-ratio: 9/16; border: 2px solid #CBD5E1; border-radius: 8px; padding: 8px; display: flex; flex-direction: column;
  justify-content: space-between; font-size: 10px; background: #1F2328; color: #fff }}
.st b {{ font-size: 12px }} .st i {{ color: #9CA3AF }} .st em {{ color: #FFD400; font-style: normal; font-weight: 700 }}
ul {{ padding-left: 14px }} li {{ margin: 2px 0 }}
"""


def tomas_html():
    out = ""
    for i, t in enumerate(TOMAS, 1):
        tag = f'<span class="tag{" r" if t["tipo"].startswith("Reusar") else ""}">{html.escape(t["tipo"])}</span>'
        out += (f'<div class="f"><svg viewBox="0 0 1080 1920">{t["svg"]}{ZONA}</svg>'
                f'<div class="tt"><span>Toma {i}</span><span>{t["t"]}</span></div>{tag}'
                f'<p><b>Se ve:</b> {html.escape(t["ve"])}</p><p class="v">“{html.escape(t["voz"])}”</p>'
                f'<p><b>Texto:</b> {html.escape(t["txt"].replace("|", " "))}</p>'
                f'<p class="c"><b>Cámara:</b> {html.escape(t["cam"])}</p></div>')
    return out


def stories_html():
    return "".join(f'<div><i>{i}. {html.escape(a)}</i><b>“{html.escape(b)}”</b><em>{html.escape(c)}</em></div>'
                   for i, (a, b, c) in enumerate(STORIES, 1))


DOC = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Storyboard Yantai lun 23</title>
<style>{CSS}</style></head><body>
<section class="pg">
  <div class="top"><b>Storyboard · Reel “¿Acertaste?” · @yantaimotors · Opción A: un paso atrás desde la ventana</b>
  <span>Lun 23 nov · 7:00 pm · 15 s · vertical 1080x1920 · PROPUESTA PARA REVISAR</span></div>
  <div class="row">{tomas_html()}</div>
  <p class="leg">Línea roja punteada: zona segura del texto. Los textos naranjas se ponen en edición (letra tipo marcador),
  no se escribe en la ventana. Dibujos de referencia de encuadre. Nadie en cámara: solo una mano y voz en off.</p>
</section>
<section class="pg">
  <div class="top"><b>Producción · Reel “¿Acertaste?”</b><span>Grabar vie 20 o lun 23 en la mañana · publicar lun 23, 7 pm</span></div>
  <div class="two">
    <div>
      <h3>Ficha</h3>
      <table>
        <tr><th>Sale</th><td>Nadie en cámara: una mano y voz en off</td></tr>
        <tr><th>Graba</th><td>Una persona, celular en vertical, a mano. Las tomas 2 y 3 son un solo movimiento hacia atrás</td></tr>
        <tr><th>Lugar</th><td>La misma ventana lateral de la X3 Pro del reel del jueves, y la otra X3 Pro al lado</td></tr>
        <tr><th>Reusar</th><td>Los últimos 2 s del reel del jue 19 (ventana escrita "1. TURBO · 2. CVT · 3. 5") para la toma 1</td></tr>
        <tr><th>Audio</th><td>Golpe seco justo cuando el plano abierto muestra las dos (toma 3)</td></tr>
        <tr><th>Edición</th><td>Mismo color que el jueves (verde azulado oscuro). Textos en naranja tipo marcador. Placa final del jueves
        cambiando "Muy pronto..." por "Kaiyi en Yantai Motors". Total 15 s</td></tr>
      </table>
      <h3>Checklist antes de grabar</h3>
      <ul>
        <li>Empezar la toma 2 en el mismo encuadre de la ventana que el jueves (mismo lado del carro, misma altura).</li>
        <li>Ensayar el paso atrás: lento al principio, más rápido al final. Grabarlo 2 o 3 veces.</li>
        <li>Las dos X3 Pro limpias y lado a lado para las tomas 3 y 6.</li>
        <li>Placas tapadas o fuera de cuadro si no se quieren mostrar.</li>
        <li>Pedir a quien editó el reel del jueves el archivo original, para cortar la toma 1 en buena calidad.</li>
      </ul>
    </div>
    <div>
      <h3>Stories del lun 23 · 5 frames</h3>
      <div class="st">{stories_html()}</div>
      <h3>Texto para decir (voz en off, seca)</h3>
      <table><tr><td>¿Acertaste?<br>Es la Kaiyi X3 Pro.<br>Y solo hay 2.<br>De contado, el viernes 27.<br>
      El precio llega el jueves 26, solo a la lista.<br>Comenta BLACK si acertaste.</td></tr></table>
      <h3>Pendiente</h3>
      <ul><li>Aprobar la opción A antes de pasarla al guion.</li>
      <li>Archivo original del reel del jue 19.</li></ul>
    </div>
  </div>
</section>
</body></html>"""

os.makedirs(OUT_DIR, exist_ok=True)
out_html = os.path.join(OUT_DIR, "Storyboard-Yantai-Lun23.html")
out_pdf = os.path.join(OUT_DIR, "Storyboard-Yantai-Lun23.pdf")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(DOC)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(out_pdf)
