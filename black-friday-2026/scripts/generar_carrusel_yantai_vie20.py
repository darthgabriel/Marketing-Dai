"""Maqueta para producción: carrusel @yantaimotors vie 20 nov · "Checklist de contado" · 5 slides.
Sin fotos: fondo gris oscuro, letra blanca y casillas amarillas, como el marcador del vidrio.
Salida: black-friday-2026/entregables/carrusel-yantai-vie20/slide-1..5.png + Carrusel-Yantai-Vie20-Maqueta.pdf
(una página por slide, con el slide a la izquierda y sus textos para producción a la derecha).
Uso: python black-friday-2026/scripts/generar_carrusel_yantai_vie20.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entregables", "carrusel-yantai-vie20")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
GRIS, AMARILLO = "#1F2328", "#FFD400"
N = 5

CSS = f"""
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ background: {GRIS} }}
.s {{ width: 1080px; height: 1350px; position: relative; overflow: hidden; background: {GRIS}; color: #fff;
  font-family: 'Arial Black', 'Segoe UI Black', Arial, sans-serif }}
.n {{ position: absolute; top: 60px; right: 120px; font: 700 32px Arial, sans-serif; color: #9CA3AF }}
.h {{ position: absolute; bottom: 56px; left: 120px; font: 700 30px Arial, sans-serif; color: #9CA3AF }}
.logo {{ position: absolute; bottom: 56px; right: 120px; font: 700 30px Arial, sans-serif; color: {AMARILLO} }}
.k {{ position: absolute; top: 150px; left: 120px; font: 700 34px Arial, sans-serif; color: {AMARILLO}; letter-spacing: 2px }}
.t {{ position: absolute; left: 120px; right: 120px; top: 230px; font-size: 104px; line-height: 1.0 }}
.sub {{ position: absolute; left: 120px; right: 120px; font: 400 44px/1.3 Arial, sans-serif; color: #D1D5DB }}
.item {{ position: absolute; left: 120px; right: 120px; top: 470px; display: flex; gap: 48px; align-items: flex-start }}
.box {{ flex: none; width: 190px; height: 190px; border: 14px solid {AMARILLO}; border-radius: 10px; position: relative }}
.box.ok::after {{ content: ""; position: absolute; left: 38px; top: 6px; width: 60px; height: 115px;
  border-right: 22px solid {AMARILLO}; border-bottom: 22px solid {AMARILLO}; transform: rotate(40deg) }}
.item .txt {{ font-size: 88px; line-height: 1.02 }}
.prog {{ position: absolute; left: 120px; right: 120px; top: 760px; display: flex; gap: 18px }}
.prog i {{ flex: 1; height: 14px; border-radius: 7px; background: #4B5563 }}
.prog i.on {{ background: {AMARILLO} }}
.cta {{ font-size: 138px; line-height: .95; top: 300px }}
.dir {{ position: absolute; left: 120px; right: 120px; top: 640px; font: 700 46px/1.3 Arial, sans-serif; color: #fff }}
.dir b {{ color: {AMARILLO} }}
.lista {{ position: absolute; left: 120px; top: 610px; list-style: none }}
.lista li {{ display: flex; gap: 30px; align-items: center; font: 700 50px Arial, sans-serif; margin-bottom: 40px }}
.lista li span {{ width: 64px; height: 64px; border: 7px solid {AMARILLO}; border-radius: 6px; flex: none }}
"""


def marco(i, cuerpo):
    return (f'<section class="s">{cuerpo}<div class="n">{i}/{N}</div>'
            f'<div class="h">@yantaimotors</div><div class="logo">KAIYI · YANTAI MOTORS</div></section>')


def paso(i, k, texto, hechas):
    barras = "".join(f'<i class="{"on" if j < hechas else ""}"></i>' for j in range(3))
    return marco(i, f'''
<div class="k">CASILLA {k} DE 3</div>
<div class="item" style="top:300px"><div class="box ok"></div><div class="txt">{texto}</div></div>
<div class="prog">{barras}</div>''')


SLIDES = [
    marco(1, f'''
<div class="k">VIERNES 27 · SOLO CONTADO</div>
<div class="t" style="font-size:90px">CHECKLIST<br>PARA COMPRAR<br>DE CONTADO</div>
<ul class="lista"><li><span></span>Monto completo</li><li><span></span>Cédula y RIF</li><li><span></span>Lista BLACK</li></ul>
<div class="sub" style="top:1010px">Desliza y márcalas →</div>'''),
    paso(2, 1, "MONTO<br>COMPLETO<br>DISPONIBLE.", 1),
    paso(3, 2, "CÉDULA<br>Y RIF<br>VIGENTES.", 2),
    paso(4, 3, "ESTAR EN<br>LA LISTA<br>BLACK.", 3).replace(
        '<div class="prog">',
        '<div class="sub" style="top:620px">El precio te llega el <b style="color:#FFD400">jueves 26, 7 am</b>.</div><div class="prog" style="top:800px">'),
    marco(5, f'''
<div class="k">3 DE 3 · LISTO</div>
<div class="t cta">COMENTA<br>BLACK</div>
<div class="dir"><b>Kaiyi en Yantai Motors</b><br>Av. 8 Santa Rita con calles 82B y 83</div>'''),
]

TEXTOS = [
    ("Portada", "CHECKLIST PARA COMPRAR DE CONTADO",
     "Arriba: VIERNES 27 · SOLO CONTADO. Lista con 3 casillas vacías: Monto completo · Cédula y RIF · Lista BLACK. Abajo: Desliza y márcalas →"),
    ("Slide 2 · casilla 1", "MONTO COMPLETO DISPONIBLE.", "Arriba: CASILLA 1 DE 3. Casilla marcada y barra de progreso 1 de 3."),
    ("Slide 3 · casilla 2", "CÉDULA Y RIF VIGENTES.", "Arriba: CASILLA 2 DE 3. Casilla marcada y barra de progreso 2 de 3."),
    ("Slide 4 · casilla 3", "ESTAR EN LA LISTA BLACK.",
     "Arriba: CASILLA 3 DE 3. Debajo: El precio te llega el jueves 26, 7 am. Barra de progreso completa."),
    ("Cierre", "COMENTA BLACK", "Arriba: 3 DE 3 · LISTO. Debajo: Kaiyi en Yantai Motors · Av. 8 Santa Rita con calles 82B y 83."),
]
REGLAS = ("Reglas para todos: 1080x1350, fondo gris oscuro, letra blanca, casillas y detalles en amarillo (como el marcador "
          "del vidrio). Sin fotos y sin nadie en cámara. Número de slide arriba a la derecha, @yantaimotors abajo a la "
          "izquierda, \"KAIYI · YANTAI MOTORS\" abajo a la derecha. Texto a 120 px de los bordes. Si se puede, las casillas "
          "y el visto con trazo de marcador hecho a mano.")
FICHA_CSS = """
@page { size: Letter landscape; margin: 10mm 12mm }
* { box-sizing: border-box; margin: 0; padding: 0 }
body { font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 13px }
.p { display: flex; gap: 22px; height: 7.6in; break-after: page; align-items: flex-start }
.p:last-child { break-after: auto }
.p img { height: 7.4in; border: 1px solid #CBD5E1; border-radius: 6px }
.d { flex: 1 }
.d .k { color: #374151; font-weight: 800; font-size: 12px; letter-spacing: .08em; text-transform: uppercase }
.d h1 { font-size: 24px; margin: 4px 0 12px; color: #374151 }
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
for i, (nombre, tit, txt) in enumerate(TEXTOS, 1):
    img = "file:///" + os.path.join(OUT, f"slide-{i}.png").replace(os.sep, "/")
    paginas += (f'<section class="p"><img src="{img}"><div class="d"><div class="k">Carrusel vie 20 · @yantaimotors · {i}/{N}</div>'
                f'<h1>{nombre}</h1><table>'
                f'<tr><th>Titular</th><td class="big">{html.escape(tit)}</td></tr>'
                f'<tr><th>Resto del slide</th><td>{html.escape(txt)}</td></tr>'
                f'<tr><th>Foto</th><td>Ninguna: solo diseño</td></tr>'
                f'</table><p class="r">{html.escape(REGLAS)}</p></div></section>')
ficha = os.path.join(OUT, "ficha.html")
with open(ficha, "w", encoding="utf-8") as h:
    h.write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FICHA_CSS}</style></head><body>{paginas}</body></html>')
pdf = os.path.join(BASE, "entregables", "Carrusel-Yantai-Vie20-Maqueta.pdf")
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                f"--print-to-pdf={pdf}", ficha], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.remove(ficha)
print(OUT)
print(pdf)
