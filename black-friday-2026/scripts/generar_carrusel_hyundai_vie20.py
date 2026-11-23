"""Maqueta para producción: carrusel @daimotorsmcbo vie 20 nov · "4 unidades, 1 sola condición" · 6 slides.
Las fotos van como recuadros con la indicación de qué foto va; el cartel SOLO CONTADO se dibuja para marcar
tamaño y posición. Entre el slide 1 y el 2 el cartel queda partido: "SOLO" | "CONTADO".
Salida: black-friday-2026/entregables/carrusel-hyundai-vie20/slide-1..6.png + Carrusel-Hyundai-Vie20-Maqueta.pdf
Uso: python black-friday-2026/scripts/generar_carrusel_hyundai_vie20.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "entregables", "carrusel-hyundai-vie20")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AZUL = "#002C5F"
N = 6

CSS = f"""
@page {{ size: 1080px 1350px; margin: 0 }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Arial Black', 'Segoe UI Black', Arial, sans-serif; color: #0B0B0F; background: #fff }}
.s {{ width: 1080px; height: 1350px; position: relative; overflow: hidden; background: #fff; break-after: page }}
.n {{ position: absolute; top: 60px; right: 120px; font: 700 32px Arial, sans-serif; color: #64748B }}
.h {{ position: absolute; bottom: 52px; left: 120px; font: 700 30px Arial, sans-serif; color: #64748B }}
.logo {{ position: absolute; bottom: 52px; right: 120px; font: 700 30px Arial, sans-serif; color: {AZUL} }}
.t {{ position: absolute; left: 120px; right: 120px; top: 150px; font-size: 92px; line-height: 1.0; letter-spacing: -1px }}
.t.m {{ font-size: 78px }}
.b {{ position: absolute; left: 120px; right: 120px; font: 400 40px/1.3 Arial, sans-serif; color: #1F2937 }}
.b b {{ font-weight: 800; color: #0B0B0F }}
.ph {{ position: absolute; left: 120px; right: 120px; bottom: 140px; background: #E5E7EB;
  border: 4px dashed #94A3B8; border-radius: 14px; overflow: hidden }}
.ph .lab {{ position: absolute; left: 16px; bottom: 16px; right: 16px; z-index: 2; background: rgba(255,255,255,.92); padding: 8px 12px; border-radius: 8px; font: 700 26px/1.25 Arial, sans-serif; color: #475569 }}
.ph .lab span {{ background: {AZUL}; color: #fff; padding: 3px 10px; border-radius: 6px; margin-right: 8px; font-size: 22px }}
.alexis {{ position: absolute; bottom: 0 }}
.cartel {{ position: absolute; z-index: 1; background: #fff; border: 5px solid #0B0B0F; display: flex; align-items: center;
  justify-content: center; font-size: 56px; white-space: nowrap; box-shadow: 0 6px 0 rgba(0,0,0,.15) }}
.ph-text {{ font-family: Arial, sans-serif }}
.var {{ background: #FEF08A; padding: 0 8px; border-radius: 6px; font-weight: 800 }}
.list {{ position: absolute; left: 120px; right: 120px; top: 340px; counter-reset: i; list-style: none }}
.list li {{ counter-increment: i; font: 700 46px/1.2 Arial, sans-serif; margin-bottom: 34px; padding-left: 96px; position: relative }}
.list li::before {{ content: counter(i); position: absolute; left: 0; top: -6px; width: 70px; height: 70px; border-radius: 12px;
  background: {AZUL}; color: #fff; font-size: 44px; display: flex; align-items: center; justify-content: center }}
.cta {{ font-size: 150px; line-height: .95 }}
.split {{ position: absolute; top: 0; height: 100%; width: 0; border-left: 6px dashed #DC2626 }}
.note {{ position: absolute; font: 700 24px Arial, sans-serif; color: #DC2626; background: #FEF2F2; padding: 6px 12px; border-radius: 8px }}
"""


def silueta(x, w=420, h=720, mini=False):
    """Alexis de espaldas, en silueta, para marcar posición. x es el borde izquierdo dentro del recuadro."""
    s = 0.45 if mini else 1
    w, h = int(w * s), int(h * s)
    return (f'<svg class="alexis" style="left:{x}px" width="{w}" height="{h}" viewBox="0 0 420 720">'
            '<circle cx="210" cy="95" r="80" fill="#334155"/>'
            '<path d="M40 720 L60 300 Q70 200 210 195 Q350 200 360 300 L380 720 Z" fill="#1E293B"/></svg>')


def cartel(x, y, texto, w=560, h=150, size=56):
    return f'<div class="cartel" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;font-size:{size}px">{texto}</div>'


def foto(alto, etiqueta, dentro):
    return (f'<div class="ph" style="height:{alto}px"><div class="lab"><span>FOTO</span>{html.escape(etiqueta)}</div>'
            f'{dentro}</div>')


def marco(i, cuerpo):
    return (f'<section class="s">{cuerpo}<div class="n">{i}/{N}</div>'
            f'<div class="h">@daimotorsmcbo</div><div class="logo">HYUNDAI · DAI MOTORS</div></section>')


# El recuadro de foto mide 840 de ancho (1080 - 2x120). Para que el cartel quede partido justo en el corte,
# en el slide 1 la foto se extiende hasta el borde derecho y en el slide 2 arranca desde el borde izquierdo.
CARTEL_W = 640
SLIDES = []

# 1 · Portada: se ve "SOLO", el resto del cartel se sale por la derecha.
SLIDES.append(marco(1, f'''
<div class="t">4 UNIDADES.<br>1 SOLA<br>CONDICIÓN.</div>
<div class="b" style="top:470px">Desliza: la tiene en la espalda. →</div>
<div class="ph" style="height:640px;right:0;border-right:0;border-radius:14px 0 0 14px">
  <div class="lab"><span>FOTO</span>Mitad izquierda de una foto horizontal: Alexis de espaldas, pegado al borde derecho</div>
  {silueta(750)}
  <div class="cartel" style="left:660px;top:260px;width:300px;height:150px;border-right:0;justify-content:flex-end;padding-right:14px">SOLO</div>
</div>
<div class="split" style="left:1074px"></div>
<div class="note" style="right:20px;top:560px">corte del slide →</div>
'''))

# 2 · Continúa la misma foto: "CONTADO" aparece al deslizar.
SLIDES.append(marco(2, f'''
<div class="t">SOLO DE<br>CONTADO</div>
<div class="b" style="top:360px">Las 4 del viernes 27 <b>no se financian</b>.<br>Ni cuotas, ni inicial, ni "te pago en enero".</div>
<div class="ph" style="height:640px;left:0;border-left:0;border-radius:0 14px 14px 0">
  <div class="lab" style="left:240px"><span>FOTO</span>Mitad derecha de la misma foto. Alexis mira por encima del hombro, sin entender</div>
  {silueta(-210)}
  <div class="cartel" style="left:0;top:260px;width:340px;height:150px;border-left:0;justify-content:flex-start;padding-left:14px">CONTADO</div>
</div>
<div class="split" style="left:0"></div>
'''))

# 3 · Por qué de contado.
SLIDES.append(marco(3, f'''
<div class="t">¿POR QUÉ DE<br>CONTADO?</div>
<div class="b" style="top:360px">Porque el descuento es para quien <b>paga completo</b>.<br>Pagas todo, pagas menos.</div>
{foto(620, "Alexis caminando de espaldas entre los carros; carros fuera de foco", silueta(210) + cartel(200, 280, "SOLO CONTADO", w=440, h=120, size=46))}
'''))

# 4 · Sin apartados: la regla de "quien pague primero", contada como consecuencia del contado.
SLIDES.append(marco(4, f'''
<div class="t m">SIN APARTADOS.<br>SIN RESERVAS.</div>
<div class="b" style="top:330px">Las 4 no se apartan.<br>Cada una es de quien <b>la pague completa primero</b>.</div>
{foto(560, "Alexis de espaldas frente a los carros, con los brazos abiertos como cerrando el paso", silueta(210) + cartel(200, 250, "SOLO CONTADO", w=440, h=120, size=46))}
'''))

# 5 · Resumen para guardar.
SLIDES.append(marco(5, f'''
<div class="t m">EL VIERNES 27,<br>EN 4 LÍNEAS</div>
<ol class="list">
  <li>Son 4 unidades.</li>
  <li>Solo de contado.</li>
  <li>Escribe BLACK: el precio te llega el jueves 26, 7 am.</li>
  <li>Cada una es de quien la pague primero.</li>
</ol>
<div class="ph" style="left:auto;width:300px;height:330px">
  <div class="lab" style="font-size:20px"><span>FOTO</span>Alexis pequeño, de espaldas</div>
  {silueta(70, mini=True)}{cartel(60, 170, "SOLO CONTADO", w=190, h=56, size=20)}
</div>
'''))

# 6 · Cierre.
SLIDES.append(marco(6, f'''
<div class="t cta">COMENTA<br>BLACK</div>
<div class="b" style="top:470px"><b>Hyundai en Dai Motors.</b></div>
{foto(620, "Alexis de espaldas, tapando los carros con el cuerpo", silueta(210) + cartel(200, 280, "SOLO CONTADO", w=440, h=120, size=46))}
'''))

# Textos de cada slide para producción: titular, texto, foto y cartel.
TEXTOS = [
    ("Portada", "4 UNIDADES. 1 SOLA CONDICIÓN.", "Desliza: la tiene en la espalda. →",
     "Mitad izquierda de una foto horizontal de Alexis de espaldas, pegado al borde derecho", "SOLO (la mitad del cartel)"),
    ("Slide 2", "SOLO DE CONTADO", 'Las 4 del viernes 27 no se financian. Ni cuotas, ni inicial, ni "te pago en enero".',
     "Mitad derecha de la misma foto. Alexis mira por encima del hombro, sin entender", "CONTADO (la otra mitad)"),
    ("Slide 3", "¿POR QUÉ DE CONTADO?", "Porque el descuento es para quien paga completo. Pagas todo, pagas menos.",
     "Alexis caminando de espaldas entre los carros; carros fuera de foco", "SOLO CONTADO"),
    ("Slide 4", "SIN APARTADOS. SIN RESERVAS.", "Las 4 no se apartan. Cada una es de quien la pague completa primero.",
     "Alexis de espaldas frente a los carros, con los brazos abiertos", "SOLO CONTADO"),
    ("Resumen", "EL VIERNES 27, EN 4 LÍNEAS",
     "1. Son 4 unidades. 2. Solo de contado. 3. Escribe BLACK: el precio te llega el jueves 26, 7 am. 4. Cada una es de quien la pague primero.",
     "Alexis pequeño, de espaldas, en una esquina", "SOLO CONTADO"),
    ("Cierre", "COMENTA BLACK", "Hyundai en Dai Motors.",
     "Alexis de espaldas, tapando los carros con el cuerpo", "SOLO CONTADO"),
]
FICHA_CSS = f"""
@page {{ size: Letter landscape; margin: 10mm 12mm }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 13px }}
.p {{ display: flex; gap: 22px; height: 7.6in; break-after: page; align-items: flex-start }}
.p:last-child {{ break-after: auto }}
.p img {{ height: 7.4in; border: 1px solid #CBD5E1; border-radius: 6px }}
.d {{ flex: 1 }}
.d .k {{ color: {AZUL}; font-weight: 800; font-size: 12px; letter-spacing: .08em; text-transform: uppercase }}
.d h1 {{ font-size: 24px; margin: 4px 0 12px; color: {AZUL} }}
.d table {{ width: 100%; border-collapse: collapse }}
.d th {{ text-align: left; width: 130px; vertical-align: top; padding: 9px 8px; background: #F1F5F9; font-size: 11px;
  text-transform: uppercase; color: #334155; border-bottom: 1px solid #E2E8F0 }}
.d td {{ padding: 9px 10px; border-bottom: 1px solid #E2E8F0; font-size: 15px; line-height: 1.4 }}
.d td.big {{ font-size: 20px; font-weight: 800 }}
.d .r {{ margin-top: 14px; font-size: 12px; color: #475569; line-height: 1.5 }}
"""
REGLAS = ("Reglas para todos: 1080x1350, fondo blanco, letras negras grandes. Número de slide arriba a la derecha, "
          "@daimotorsmcbo abajo a la izquierda, \"HYUNDAI · DAI MOTORS\" abajo a la derecha. Texto a 120 px de los bordes. "
          "El cartel SOLO CONTADO siempre del mismo tamaño y en el mismo lugar de la espalda de Alexis. "
          "Quitar la línea roja del corte en el diseño final.")


def doc(cuerpo):
    return f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{CSS}</style></head><body>{cuerpo}</body></html>'


os.makedirs(OUT, exist_ok=True)
for i, sl in enumerate(SLIDES, 1):
    f = os.path.join(OUT, f"slide-{i}.html")
    with open(f, "w", encoding="utf-8") as h:
        h.write(doc(sl))
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--window-size=1080,1350",
                    f"--screenshot={os.path.join(OUT, f'slide-{i}.png')}", f], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(f)

paginas = ""
for i, (nombre, tit, txt, fot, car) in enumerate(TEXTOS, 1):
    img = "file:///" + os.path.join(OUT, f"slide-{i}.png").replace(os.sep, "/")
    paginas += (f'<section class="p"><img src="{img}"><div class="d"><div class="k">Carrusel vie 20 · @daimotorsmcbo · {i}/{N}</div>'
                f'<h1>{nombre}</h1><table>'
                f'<tr><th>Titular</th><td class="big">{html.escape(tit)}</td></tr>'
                f'<tr><th>Texto</th><td>{html.escape(txt)}</td></tr>'
                f'<tr><th>Foto</th><td>{html.escape(fot)}</td></tr>'
                f'<tr><th>Cartel en la espalda</th><td>{html.escape(car)}</td></tr>'
                f'</table><p class="r">{html.escape(REGLAS)}</p></div></section>')
todo = os.path.join(OUT, "ficha.html")
with open(todo, "w", encoding="utf-8") as h:
    h.write(f'<!doctype html><html lang="es"><head><meta charset="utf-8"><style>{FICHA_CSS}</style></head><body>{paginas}</body></html>')
pdf = os.path.join(BASE, "entregables", "Carrusel-Hyundai-Vie20-Maqueta.pdf")
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--allow-file-access-from-files",
                f"--print-to-pdf={pdf}", todo], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
os.remove(todo)
print(OUT)
print(pdf)
