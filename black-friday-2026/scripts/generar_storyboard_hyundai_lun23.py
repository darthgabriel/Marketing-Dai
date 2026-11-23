"""Storyboard para grabar: reel @daimotorsmcbo lun 23 nov · "La revelación" · 15 s.
Cada toma en un cuadro 9:16 dibujado (qué se ve, dónde va el texto en pantalla), con tiempo, voz y notas de cámara.
Página 2: ficha de producción, carteles para imprimir, stories del día y checklist.
Salida: black-friday-2026/entregables/Storyboard-Hyundai-Lun23.pdf
Uso: python black-friday-2026/scripts/generar_storyboard_hyundai_lun23.py
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


def espalda(x, y, s=1.0, cartel="SÍGUEME", cw=300):
    """Alexis de espaldas, con un cartel pegado."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<circle cx="0" cy="-470" r="90" fill="#3B2F2A"/>'
            '<path d="M-190 300 L-170 -260 Q-150 -370 0 -375 Q150 -370 170 -260 L190 300 Z" fill="#1E293B"/>'
            '<rect x="-150" y="300" width="120" height="420" fill="#334155"/><rect x="30" y="300" width="120" height="420" fill="#334155"/>'
            f'<rect x="{-cw/2}" y="-230" width="{cw}" height="130" fill="#fff" stroke="#0B0B0F" stroke-width="8"/>'
            f'<text x="0" y="-145" font-family="Arial Black,Arial" font-weight="900" font-size="58" text-anchor="middle">{cartel}</text></g>')


def frente(x, y, s=1.0, cara="neutra"):
    """Alexis de frente (o volteado), con la expresión indicada."""
    cejas = ('<path d="M-55 -505 l35 -18 M20 -523 l35 18" stroke="#111" stroke-width="10"/>' if cara == "serio"
             else '<path d="M-55 -510 h35 M20 -510 h35" stroke="#111" stroke-width="10"/>')
    boca = ('<path d="M-30 -420 h60" stroke="#111" stroke-width="10"/>' if cara == "serio"
            else '<path d="M-30 -425 q30 25 60 0" stroke="#111" stroke-width="10" fill="none"/>')
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<circle cx="0" cy="-470" r="90" fill="#D9A57C"/><path d="M-90 -500 q90 -110 180 0" fill="#3B2F2A"/>'
            f'<circle cx="-35" cy="-475" r="9" fill="#111"/><circle cx="35" cy="-475" r="9" fill="#111"/>{cejas}{boca}'
            '<path d="M-190 300 L-170 -260 Q-150 -370 0 -375 Q150 -370 170 -260 L190 300 Z" fill="#1E293B"/>'
            '<rect x="-150" y="300" width="120" height="420" fill="#334155"/><rect x="30" y="300" width="120" height="420" fill="#334155"/></g>')


def carro(x, y, modelo, s=1.0, cartel=True):
    """Carro de frente con cartel SON 4 en el parabrisas."""
    c = ('<rect x="-75" y="-215" width="150" height="70" fill="#fff" stroke="#0B0B0F" stroke-width="5"/>'
         '<text x="0" y="-165" font-family="Arial Black,Arial" font-size="40" text-anchor="middle">SON 4</text>') if cartel else ""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<path d="M-200 0 L-190 -110 Q-170 -150 -130 -160 L-110 -250 Q-100 -280 -60 -280 L60 -280 Q100 -280 110 -250 '
            'L130 -160 Q170 -150 190 -110 L200 0 Z" fill="#B8C2CF"/>'
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

CUATRO = (carro(170, 1420, "ACCENT", .62) + carro(410, 1420, "ACCENT", .62) +
          carro(660, 1420, "CRETA", .62) + carro(905, 1420, "CRETA", .62))

TOMAS = [
    dict(t="0:00-0:03", cam="Cámara en mano, detrás de Alexis, a la altura del pecho. Camina hacia el fondo.",
         ve="Alexis camina con SÍGUEME en la espalda.", voz="Sigue a Alexis. Él te lleva a las cuatro.",
         txt="SIGUE A ALEXIS", svg=PISO + espalda(540, 1320, 1.0) + card("SIGUE A ALEXIS")),
    dict(t="0:03-0:05", cam="Paneo corto hacia la columna mientras Alexis sigue caminando.",
         ve="Pasan junto al cartel CASI pegado en una columna.", voz="(sin voz, solo música)", txt="CASI",
         svg=PISO + '<rect x="90" y="560" width="220" height="1000" fill="#C5CCD6"/>'
             '<rect x="105" y="900" width="190" height="110" fill="#fff" stroke="#0B0B0F" stroke-width="7"/>'
             '<text x="200" y="980" font-family="Arial Black,Arial" font-size="60" text-anchor="middle">CASI</text>'
             + espalda(720, 1420, .8) + card("CASI")),
    dict(t="0:05-0:09", cam="Alexis da un paso al lado y la cámara sigue de frente: plano abierto de las 4.",
         ve="Aparecen las 4 unidades en fila, cada una con SON 4 en el parabrisas.",
         voz="Dos Accent, dos Creta. El viernes 27 bajan.", txt="2 ACCENT · 2 CRETA",
         svg=PISO + CUATRO + espalda(1000, 1600, .55) + card("2 ACCENT · 2 CRETA", 330, 58)),
    dict(t="0:09-0:12", cam="Plano medio de Alexis. Se voltea, se mira el hombro, cara de “¿en serio?”.",
         ve="Alexis se da cuenta del cartel que tenía en la espalda.",
         voz="Precio el jueves, solo para la lista. Comenta BLACK.", txt="PRECIO EL JUEVES: LISTA BLACK",
         svg=PISO + carro(800, 1500, "CRETA", .7) + frente(420, 1380, 1.05, "serio") + card("PRECIO EL JUEVES:|LISTA BLACK", 300, 58)),
    dict(t="0:12-0:15", cam="Plano medio. Alexis se quita el cartel, lo voltea y lo pega en el parabrisas de una Creta.",
         ve="El cartel volteado dice CONTADO y queda pegado en una Creta.", voz="Hyundai en Dai Motors. Sigue a Alexis.",
         txt="HYUNDAI EN DAI MOTORS",
         svg=PISO + carro(640, 1500, "CRETA", .9, cartel=False)
             + '<rect x="520" y="1250" width="240" height="90" fill="#fff" stroke="#0B0B0F" stroke-width="6"/>'
               '<text x="640" y="1312" font-family="Arial Black,Arial" font-size="46" text-anchor="middle">CONTADO</text>'
             + frente(260, 1420, .9) + card("HYUNDAI EN|DAI MOTORS", 330, 60)),
]

STORIES = [
    ("Video de las 4 en fila", "Ya las conoces.", ""),
    ("Foto de los 2 Accent", "Dos Accent. {{versión}}.", ""),
    ("Foto de las 2 Creta, Alexis dentro de una", "Dos Creta. {{versión}}. Ven a verlas.", ""),
    ("Fondo blanco, letras de cartel", "¿Cuál te llevas?", "Encuesta: Accent / Creta"),
    ("Fondo blanco", "Mañana: las bases. Sin trampa.", ""),
]

CSS = f"""
@page {{ size: Letter landscape; margin: 9mm 10mm }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 11px }}
.pg {{ break-after: page }} .pg:last-child {{ break-after: auto }}
.top {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 3px solid {AZUL}; padding-bottom: 4px; margin-bottom: 8px }}
.top b {{ font-size: 16px; color: {AZUL} }} .top span {{ color: #64748B; font-size: 10px }}
.row {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px }}
.f svg {{ width: 100%; aspect-ratio: 9/16; display: block; border: 2px solid #0B0B0F; border-radius: 10px; background: #fff }}
.f .tt {{ display: flex; justify-content: space-between; margin: 5px 0 3px; font-weight: 800; color: {AZUL}; font-size: 12px }}
.f p {{ margin: 2px 0; line-height: 1.3 }}
.f .v {{ background: #F1F5F9; border-left: 3px solid {AZUL}; padding: 3px 5px; font-style: italic }}
.f .c {{ color: #475569; font-size: 10px }}
.leg {{ margin-top: 6px; color: #64748B; font-size: 9.5px }}
.two {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px }}
h3 {{ font-size: 12.5px; color: {AZUL}; margin: 8px 0 4px }}
table {{ width: 100%; border-collapse: collapse; font-size: 10.5px }}
th {{ background: #E2E8F0; text-align: left; padding: 3px 6px; font-size: 9.5px; text-transform: uppercase }}
td {{ border-bottom: 1px solid #E2E8F0; padding: 3px 6px; vertical-align: top }}
.carteles {{ display: flex; gap: 10px; flex-wrap: wrap }}
.cart {{ border: 4px solid #0B0B0F; padding: 8px 14px; font: 900 22px 'Arial Black', Arial; background: #fff }}
.cart small {{ display: block; font: 400 9px Arial; color: #64748B }}
.st {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px }}
.st div {{ aspect-ratio: 9/16; border: 2px solid #CBD5E1; border-radius: 8px; padding: 8px; display: flex; flex-direction: column;
  justify-content: space-between; font-size: 10px; background: #F8FAFC }}
.st b {{ font-size: 12px }} .st i {{ color: #64748B }} .st em {{ color: {AZUL}; font-style: normal; font-weight: 700 }}
ul {{ padding-left: 14px }} li {{ margin: 2px 0 }}
"""


def tomas_html():
    out = ""
    for i, t in enumerate(TOMAS, 1):
        svg = f'<svg viewBox="0 0 1080 1920">{t["svg"]}{ZONA}</svg>'
        out += (f'<div class="f">{svg}<div class="tt"><span>Toma {i}</span><span>{t["t"]}</span></div>'
                f'<p><b>Se ve:</b> {html.escape(t["ve"])}</p>'
                f'<p class="v">“{html.escape(t["voz"])}”</p>'
                f'<p><b>Texto:</b> {html.escape(t["txt"])}</p>'
                f'<p class="c"><b>Cámara:</b> {html.escape(t["cam"])}</p></div>')
    return out


def stories_html():
    return "".join(f'<div><i>{i}. {html.escape(a)}</i><b>“{html.escape(b)}”</b><em>{html.escape(c)}</em></div>'
                   for i, (a, b, c) in enumerate(STORIES, 1))


DOC = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Storyboard Hyundai lun 23</title>
<style>{CSS}</style></head><body>
<section class="pg">
  <div class="top"><b>Storyboard · Reel “La revelación” · @daimotorsmcbo</b><span>Lun 23 nov · 7:00 pm · 15 s · vertical 1080x1920</span></div>
  <div class="row">{tomas_html()}</div>
  <p class="leg">Línea roja punteada: zona segura. El texto en pantalla va dentro de ella; fuera la tapan el caption y los botones.
  Dibujos de referencia de encuadre, no de vestuario. Voz en off susurrada, la hace Alexis.</p>
</section>
<section class="pg">
  <div class="top"><b>Producción · Reel “La revelación”</b><span>Grabar vie 20 o lun 23 en la mañana · publicar lun 23, 7 pm</span></div>
  <div class="two">
    <div>
      <h3>Ficha</h3>
      <table>
        <tr><th>Sale</th><td>Alexis (también hace la voz en off susurrada)</td></tr>
        <tr><th>Graba</th><td>Un asesor, celular en vertical, cámara en mano siguiendo a Alexis</td></tr>
        <tr><th>Lugar</th><td>Entrada → pasillo → las 4 unidades en fila: Accent, Accent, Creta, Creta</td></tr>
        <tr><th>Audio</th><td>Música con ritmo de caminata. Golpe de sonido cuando aparecen las 4. Voz grabada aparte, sin eco</td></tr>
        <tr><th>Edición</th><td>Cámara en movimiento todo el tiempo. Subtítulos quemados. Texto en pantalla desde el frame 1</td></tr>
      </table>
      <h3>Carteles para imprimir (letra negra, fondo blanco)</h3>
      <div class="carteles">
        <div class="cart">SÍGUEME / CONTADO<small>espalda de Alexis · 1, impreso por los dos lados</small></div>
        <div class="cart">CASI<small>columna del pasillo · 1</small></div>
        <div class="cart">SON 4<small>parabrisas · 4 (uno por unidad)</small></div>
      </div>
      <h3>Checklist antes de grabar</h3>
      <ul>
        <li>Las 4 unidades limpias y en fila: Accent, Accent, Creta, Creta.</li>
        <li>Placas tapadas o fuera de cuadro si no se quieren mostrar.</li>
        <li>Pasillo despejado, sin clientes en cuadro sin permiso.</li>
        <li>Grabar 2 o 3 tomas de cada plano; la toma 3 es la más importante.</li>
        <li>Fotos para las stories: los 2 Accent, las 2 Creta con Alexis dentro de una.</li>
      </ul>
    </div>
    <div>
      <h3>Stories del lun 23 · 5 frames</h3>
      <div class="st">{stories_html()}</div>
      <h3>Texto para decir (Alexis, susurrado)</h3>
      <table><tr><td>Sigue a Alexis. Él te lleva a las cuatro.<br>Dos Accent, dos Creta. El viernes 27 bajan.<br>
      Precio el jueves, solo para la lista. Comenta BLACK.<br>Hyundai en Dai Motors. Sigue a Alexis.</td></tr></table>
      <h3>Pendiente</h3>
      <ul><li>Versión de cada modelo para las stories 2 y 3.</li>
      <li>Después del reel: DM a cada persona que vote en la encuesta, según el modelo que eligió.</li></ul>
    </div>
  </div>
</section>
</body></html>"""

os.makedirs(OUT_DIR, exist_ok=True)
out_html = os.path.join(OUT_DIR, "Storyboard-Hyundai-Lun23.html")
out_pdf = os.path.join(OUT_DIR, "Storyboard-Hyundai-Lun23.pdf")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(DOC)
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html],
               check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
print(out_pdf)
