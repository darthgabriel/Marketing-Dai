"""Maqueta para producción: carrusel @cherymaracaibo vie 20 nov · "El día que pagas tu carro completo" · 6 slides.
Fondo crema, letra serif, fechas con letra a mano. Las fotos van como recuadros con la indicación de qué foto va.
Salida: black-friday-2026/entregables/carrusel-chery-vie20/slide-1..6.png + Carrusel-Chery-Vie20-Maqueta.pdf
(una página por slide, con el slide a la izquierda y sus textos para producción a la derecha).
Uso: python black-friday-2026/scripts/generar_carrusel_chery_vie20.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entregables", "carrusel-chery-vie20")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
CREMA, VINO, TINTA = "#F4EDE1", "#8A1C2B", "#2B2320"
N = 6

CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ background: {CREMA} }}
.s {{ width: 1080px; height: 1350px; position: relative; overflow: hidden; background: {CREMA}; color: {TINTA};
  font-family: Georgia, 'Times New Roman', serif }}
.n {{ position: absolute; top: 60px; right: 120px; font: 400 30px Georgia, serif; color: #8C7B6B }}
.h {{ position: absolute; bottom: 56px; left: 120px; font: 400 28px Georgia, serif; color: #8C7B6B }}
.logo {{ position: absolute; bottom: 56px; right: 120px; font: 700 26px Arial, sans-serif; letter-spacing: 3px; color: {VINO} }}
.t {{ position: absolute; left: 120px; right: 120px; top: 150px; font-size: 76px; line-height: 1.12 }}
.mano {{ font-family: 'Segoe Print', 'Bradley Hand', 'Comic Sans MS', cursive; color: {VINO} }}
.ph {{ position: absolute; left: 120px; right: 120px; bottom: 140px; background: #E6DCCB; z-index: 0;
  border: 4px dashed #B8A78F; border-radius: 18px; overflow: hidden }}
.ph .lab {{ z-index: 2; position: absolute; left: 16px; bottom: 16px; right: 16px; background: rgba(255,255,255,.9); padding: 8px 12px;
  border-radius: 8px; font: 700 26px/1.25 Arial, sans-serif; color: #5B4B3D }}
.ph .lab span {{ background: {VINO}; color: #fff; padding: 3px 10px; border-radius: 6px; margin-right: 8px; font-size: 22px }}
.ph .ico {{ position: absolute; left: 0; right: 0; top: 38%; text-align: center; font: 400 120px Georgia, serif; color: #CBBBA3 }}
.cta {{ font-size: 120px; line-height: 1.0 }}
"""


def marco(i, cuerpo):
    return (f'<section class="s">{cuerpo}<div class="n">{i}/{N}</div>'
            f'<div class="h">@cherymaracaibo</div><div class="logo">CHERY · DAI MOTORS</div></section>')


# Referencias dibujadas de cada foto: le dicen a producción qué buscar y cómo encuadrarlo. No son la foto final.
MESA = ('<rect x="0" y="330" width="840" height="270" fill="#A9774E"/>'
        '<path d="M0 380 Q300 370 840 390 M0 450 Q420 440 840 460 M0 520 Q300 512 840 530" stroke="#8E5F3B" stroke-width="4" fill="none"/>'
        '<rect x="0" y="0" width="840" height="330" fill="#EADCC6"/>'
        '<circle cx="700" cy="80" r="130" fill="#FFE7B3" opacity=".7"/>')
PIEL, PIEL2 = "#D9A57C", "#C48A62"
ILUS = {
    1: MESA + '<g transform="rotate(-6 420 420)"><rect x="210" y="300" width="420" height="260" fill="#fff" stroke="#CBBBA3" stroke-width="3"/>'
          '<path d="M250 350h300M250 380h300M250 410h220" stroke="#D6CBBB" stroke-width="6"/>'
          '<path d="M260 500 q30 -40 50 0 t50 0 t40 -20 t60 10" stroke="#1F3A93" stroke-width="5" fill="none"/>'
          '<path d="M250 520h340" stroke="#8C7B6B" stroke-width="3" stroke-dasharray="8 6"/></g>'
          f'<ellipse cx="560" cy="430" rx="95" ry="58" fill="{PIEL}"/>'
          f'<rect x="590" y="400" width="250" height="90" rx="40" fill="#F4F1EA"/>'
          f'<path d="M480 445 q-20 10 -30 35" stroke="{PIEL2}" stroke-width="26" stroke-linecap="round" fill="none"/>'
          '<rect x="430" y="380" width="16" height="140" rx="6" fill="#2B2320" transform="rotate(35 438 450)"/>'
          f'<ellipse cx="200" cy="470" rx="80" ry="45" fill="{PIEL}" opacity=".9"/>',
    2: '<rect width="840" height="600" fill="#EADCC6"/>'
       '<rect x="170" y="60" width="500" height="480" rx="10" fill="#fff" stroke="#CBBBA3" stroke-width="3"/>'
       '<rect x="170" y="60" width="500" height="80" rx="10" fill="#8A1C2B"/>'
       '<text x="420" y="115" font-family="Georgia" font-size="40" fill="#fff" text-anchor="middle">NOVIEMBRE</text>'
       + "".join(f'<text x="{205+j*70}" y="{195+i*72}" font-family="Georgia" font-size="30" fill="#8C7B6B">{d}</text>'
                 for i in range(5) for j in range(7) for d in [i*7+j+1] if d <= 30)
       + '<ellipse cx="572" cy="401" rx="44" ry="36" fill="none" stroke="#C0392B" stroke-width="7" transform="rotate(-10 572 401)"/>'
       f'<ellipse cx="700" cy="500" rx="90" ry="55" fill="{PIEL}"/>'
       '<rect x="640" y="410" width="14" height="150" rx="6" fill="#C0392B" transform="rotate(-40 647 485)"/>',
    3: MESA + '<rect x="230" y="330" width="380" height="230" rx="6" fill="#F7F1E6" stroke="#CBBBA3" stroke-width="3" transform="rotate(-4 420 445)"/>'
          '<path d="M232 335 L420 450 L608 320" stroke="#CBBBA3" stroke-width="4" fill="none" transform="rotate(-4 420 445)"/>'
          '<circle cx="420" cy="452" r="22" fill="#8A1C2B"/>'
          '<rect x="640" y="400" width="120" height="70" rx="8" fill="#6B4B33" opacity=".5"/>',
    4: MESA + '<rect x="200" y="300" width="380" height="250" rx="8" fill="#E9D7A8" transform="rotate(-3 390 425)"/>'
          '<rect x="230" y="260" width="320" height="220" fill="#fff" stroke="#CBBBA3" stroke-width="3" transform="rotate(4 390 370)"/>'
          '<rect x="260" y="290" width="150" height="95" rx="8" fill="#DDE7F0" stroke="#9BB0C4" stroke-width="3"/>'
          '<circle cx="300" cy="330" r="22" fill="#9BB0C4"/><path d="M335 320h60M335 345h50" stroke="#9BB0C4" stroke-width="6"/>'
          '<text x="440" y="330" font-family="Arial" font-weight="700" font-size="34" fill="#5B4B3D">RIF</text>'
          '<path d="M440 360h80M440 385h70" stroke="#D6CBBB" stroke-width="6"/>'
          '<rect x="190" y="420" width="400" height="140" rx="8" fill="#D9C38E" transform="rotate(-3 390 490)"/>'
          '<text x="250" y="500" font-family="Arial" font-size="28" fill="#7A6640">Cédula · RIF</text>',
    5: MESA + '<rect x="320" y="250" width="200" height="330" rx="28" fill="#1C1C1E" transform="rotate(-8 420 415)"/>'
          '<rect x="335" y="275" width="170" height="270" rx="16" fill="#ECE5DD" transform="rotate(-8 420 415)"/>'
          '<g transform="rotate(-8 420 415)" filter="url(#b)"><rect x="350" y="300" width="120" height="40" rx="10" fill="#fff"/>'
          '<rect x="370" y="355" width="120" height="50" rx="10" fill="#DCF8C6"/><rect x="350" y="420" width="100" height="36" rx="10" fill="#fff"/></g>'
          '<rect x="335" y="275" width="170" height="36" fill="#075E54" transform="rotate(-8 420 415)"/>'
          '<rect x="600" y="430" width="110" height="80" rx="40" fill="#F4F1EA"/><rect x="690" y="440" width="30" height="40" rx="10" fill="#F4F1EA"/>',
    6: '<rect width="840" height="600" fill="#2F2A27"/>'
       '<g filter="url(#b2)"><path d="M120 420 Q200 250 520 230 L760 250 Q800 330 700 420 Z" fill="#E8E8E8"/>'
       '<path d="M200 380 Q260 300 480 290 L640 300 Q620 360 560 380 Z" fill="#AFC6D9"/>'
       '<circle cx="300" cy="350" r="45" fill="#FFF9E6"/><circle cx="560" cy="340" r="35" fill="#FFF9E6"/></g>'
       + "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#FFE7B3" opacity=".35"/>'
                 for x, y, r in [(90, 120, 40), (700, 110, 55), (430, 90, 30), (780, 520, 45), (60, 540, 35)]),
}
DEFS = ('<defs><filter id="b"><feGaussianBlur stdDeviation="5"/></filter>'
        '<filter id="b2"><feGaussianBlur stdDeviation="10"/></filter></defs>')


def foto(alto, etiqueta, n):
    svg = (f'<svg width="100%" height="100%" viewBox="0 0 840 600" preserveAspectRatio="xMidYMid slice" '
           f'style="position:absolute;inset:0">{DEFS}{ILUS[n]}</svg>')
    return (f'<div class="ph" style="height:{alto}px">{svg}'
            f'<div class="lab"><span>FOTO · REFERENCIA</span>{html.escape(etiqueta)}</div></div>')


TEXTOS = [
    ("Portada", "El día que pagas tu carro completo se siente distinto.", "Manos firmando, luz cálida", "&#9998;&#65038;"),
    ("Slide 2", "Nada pendiente. Solo una fecha que recordar.", "Calendario con el 27 marcado a mano", "27"),
    ("Slide 3", "Para que ese día salga bien, ten listo el monto completo.", "Sobre cerrado sobre la mesa de madera", "✉"),
    ("Slide 4", "Tus documentos al día: cédula y RIF vigentes.", "Carpeta con documentos", "▤"),
    ("Slide 5", "Si estás en la lista BLACK, el precio te llega el jueves 26. Un día para prepararte.", "Celular sobre la mesa", "☐"),
    ("Cierre", "Comenta BLACK. Chery en Dai Motors.", "Faro fuera de foco", "◯"),
]

SLIDES = [
    marco(1, '<div class="t" style="font-size:84px">El día que pagas tu carro <i>completo</i> se siente distinto.</div>'
          + foto(560, TEXTOS[0][2], 1)),
    marco(2, '<div class="t">Nada pendiente.<br>Solo una fecha que recordar: <span class="mano">el 27</span>.</div>'
          + foto(600, TEXTOS[1][2], 2)),
    marco(3, '<div class="t">Para que ese día salga bien, ten listo el <i>monto completo</i>.</div>'
          + foto(600, TEXTOS[2][2], 3)),
    marco(4, '<div class="t">Tus documentos al día:<br><span class="mano">cédula y RIF vigentes</span>.</div>'
          + foto(600, TEXTOS[3][2], 4)),
    marco(5, '<div class="t" style="font-size:68px">Si estás en la lista BLACK, el precio te llega el '
             '<span class="mano">jueves 26</span>.<br>Un día para prepararte.</div>'
          + foto(540, TEXTOS[4][2], 5)),
    marco(6, '<div class="t cta">Comenta<br><b style="color:#8A1C2B">BLACK</b></div>'
             '<div class="t" style="top:430px;font-size:48px">Chery en Dai Motors.</div>'
          + foto(600, TEXTOS[5][2], 6)),
]

REGLAS = ("Reglas para todos: 1080x1350, fondo crema, letra serif. Las fechas y los datos clave (el 27, cédula y RIF, "
          "jueves 26) con letra a mano en vino. Fotos cálidas, solo manos y objetos, nadie de frente. Número de slide "
          "arriba a la derecha, @cherymaracaibo abajo a la izquierda, \"CHERY · DAI MOTORS\" abajo a la derecha. "
          "Texto a 120 px de los bordes. Sin formas de pago.")
FICHA_CSS = """
@page { size: Letter landscape; margin: 10mm 12mm }
* { box-sizing: border-box; margin: 0; padding: 0 }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 13px }
.p { display: flex; gap: 22px; height: 7.6in; break-after: page; align-items: flex-start }
.p:last-child { break-after: auto }
.p img { height: 7.4in; border: 1px solid #CBD5E1; border-radius: 6px }
.d { flex: 1 }
.d .k { color: #8A1C2B; font-weight: 800; font-size: 12px; letter-spacing: .08em; text-transform: uppercase }
.d h1 { font-size: 24px; margin: 4px 0 12px; color: #8A1C2B }
.d table { width: 100%; border-collapse: collapse }
.d th { text-align: left; width: 130px; vertical-align: top; padding: 9px 8px; background: #F1F5F9; font-size: 11px;
  text-transform: uppercase; color: #334155; border-bottom: 1px solid #E2E8F0 }
.d td { padding: 9px 10px; border-bottom: 1px solid #E2E8F0; font-size: 15px; line-height: 1.4 }
.d td.big { font-size: 20px; font-weight: 800 }
.d .r { margin-top: 14px; font-size: 12px; color: #475569; line-height: 1.5 }
"""

os.makedirs(OUT, exist_ok=True)
for i, sl in enumerate(SLIDES, 1):
    f = os.path.join(OUT, f"slide-{i}.html")
    with open(f, "w", encoding="utf-8") as h:
        h.write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{sl}</body></html>')
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,1350",
                    f"--screenshot={os.path.join(OUT, f'slide-{i}.png')}", f], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f)

paginas = ""
for i, (nombre, txt, fot, _) in enumerate(TEXTOS, 1):
    img = "file:///" + os.path.join(OUT, f"slide-{i}.png").replace(os.sep, "/")
    paginas += (f'<section class="p"><img src="{img}"><div class="d"><div class="k">Carrusel vie 20 · @cherymaracaibo · {i}/{N}</div>'
                f'<h1>{nombre}</h1><table>'
                f'<tr><th>Texto</th><td class="big">{html.escape(txt)}</td></tr>'
                f'<tr><th>Foto</th><td>{html.escape(fot)}</td></tr>'
                f'</table><p class="r">{html.escape(REGLAS)}</p></div></section>')
ficha = os.path.join(OUT, "ficha.html")
with open(ficha, "w", encoding="utf-8") as h:
    h.write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FICHA_CSS}</style></head><body>{paginas}</body></html>')
pdf = os.path.join(BASE, "entregables", "Carrusel-Chery-Vie20-Maqueta.pdf")
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                f"--print-to-pdf={pdf}", ficha], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.remove(ficha)
print(OUT)
print(pdf)
