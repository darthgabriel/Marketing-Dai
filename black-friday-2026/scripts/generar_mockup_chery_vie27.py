"""Mockup para ver: reel @cherymaracaibo vie 27 nov · 8:00 am · "Los precios" · estilo serio luxury MIB · 18 s.
Cada toma en un cuadro 9:16 dibujado (qué se ve, dónde va el texto en pantalla), con tiempo, voz y notas de cámara.
Página 2: ficha de producción, notas para escribir, stories del viernes y checklist.
Salida: black-friday-2026/entregables/Mockup-Reel-Vie27-Precios-Chery.pdf (+ .html)
Uso: python black-friday-2026/scripts/generar_mockup_chery_vie27.py
"""
import html
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
AZUL = "#002C5F"

# ---------- piezas de dibujo (viewBox 1080x1920) · paleta negra + dorado ----------
PISO = ('<rect width="1080" height="1920" fill="#101014"/>'
        '<rect y="1150" width="1080" height="770" fill="#1C1C22"/>'
        '<path d="M540 1150 L-200 1920 M540 1150 L1280 1920 M540 1150 L300 1920 M540 1150 L780 1920" stroke="#2A2A32" stroke-width="6"/>'
        '<rect x="380" y="620" width="320" height="120" rx="10" fill="#23232B"/>'
        '<text x="540" y="698" font-family="Georgia,serif" font-weight="700" font-size="58" fill="#C9A227" text-anchor="middle">CHERY</text>')

LUZ = ('<path d="M540 0 L760 1150 L320 1150 Z" fill="#FFFFFF" opacity=".05"/>')


def agente(x, y, s=1.0, lentes=True, cam="caminando"):
    """La asesora de blanco con lentes negros: la firma de la cuenta, modo agente."""
    gafas = ('<rect x="-95" y="-500" width="190" height="52" rx="18" fill="#0B0B0F"/>'
             '<rect x="-8" y="-490" width="16" height="12" fill="#0B0B0F"/>') if lentes else (
        '<circle cx="-35" cy="-475" r="9" fill="#111"/><circle cx="35" cy="-475" r="9" fill="#111"/>'
        '<path d="M-55 -510 h35 M20 -510 h35" stroke="#111" stroke-width="10"/>')
    boca = '<path d="M-26 -420 h52" stroke="#111" stroke-width="9"/>'
    brazos = ('<rect x="-215" y="-240" width="55" height="380" rx="24" fill="#F3EFE6" transform="rotate(8 -188 -50)"/>'
              '<rect x="160" y="-240" width="55" height="380" rx="24" fill="#F3EFE6" transform="rotate(-8 188 -50)"/>') \
        if cam == "caminando" else ('<rect x="-245" y="-220" width="200" height="50" rx="24" fill="#F3EFE6" transform="rotate(-6 -145 -195)"/>')
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<circle cx="0" cy="-470" r="92" fill="#D9A57C"/><path d="M-92 -505 q92 -115 184 0" fill="#241B14"/>'
            f'{gafas}{boca}'
            '<path d="M-195 300 L-175 -260 Q-155 -375 0 -380 Q155 -375 175 -260 L195 300 Z" fill="#F3EFE6"/>'
            f'{brazos}'
            '<rect x="-150" y="300" width="120" height="420" fill="#23232B"/><rect x="30" y="300" width="120" height="420" fill="#23232B"/></g>')


def suv(x, y, modelo, s=1.0, color="#3A3A44"):
    """Tiggo 4 de frente en negro, con nota crema en el parabrisas."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<path d="M-200 0 L-190 -110 Q-170 -150 -130 -160 L-110 -250 Q-100 -280 -60 -280 L60 -280 Q100 -280 110 -250 '
            f'L130 -160 Q170 -150 190 -110 L200 0 Z" fill="{color}"/>'
            '<path d="M-100 -165 L-85 -255 L85 -255 L100 -165 Z" fill="#6E6E7A"/>'
            '<rect x="-75" y="-215" width="150" height="70" fill="#F7F1DF" stroke="#C9A227" stroke-width="5"/>'
            '<text x="0" y="-163" font-family="Georgia,serif" font-style="italic" font-size="36" text-anchor="middle">nota</text>'
            '<rect x="-180" y="-100" width="70" height="30" rx="8" fill="#C9A227" opacity=".7"/><rect x="110" y="-100" width="70" height="30" rx="8" fill="#C9A227" opacity=".7"/>'
            '<rect x="-190" y="-10" width="70" height="60" rx="10" fill="#000"/><rect x="120" y="-10" width="70" height="60" rx="10" fill="#000"/>'
            f'<text x="0" y="110" font-family="Georgia,serif" font-weight="700" font-size="44" fill="#C9A227" text-anchor="middle">{modelo}</text></g>')


def camioneta(x, y, modelo, s=1.0, color="#33333C"):
    """Himla (camioneta) de frente en negro, con nota crema en el parabrisas."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            f'<rect x="-20" y="-290" width="230" height="150" rx="18" fill="{color}"/>'
            f'<rect x="-40" y="-190" width="250" height="190" rx="14" fill="{color}"/>'
            f'<path d="M-180 -190 L-170 -250 Q-160 -285 -120 -288 L-40 -290 L-40 -160 Q-30 -150 -20 -150 L-40 -140 '
            f'L-185 -140 Z" fill="{color}"/>'
            '<path d="M-160 -200 L-152 -248 Q-146 -272 -112 -274 L-52 -274 L-52 -200 Z" fill="#6E6E7A"/>'
            '<rect x="-75" y="-215" width="115" height="70" fill="#F7F1DF" stroke="#C9A227" stroke-width="5"/>'
            '<text x="-17" y="-163" font-family="Georgia,serif" font-style="italic" font-size="36" text-anchor="middle">nota</text>'
            '<rect x="-170" y="-95" width="60" height="26" rx="8" fill="#C9A227" opacity=".7"/>'
            '<rect x="-180" y="-10" width="70" height="60" rx="10" fill="#000"/><rect x="120" y="-10" width="70" height="60" rx="10" fill="#000"/>'
            f'<text x="20" y="110" font-family="Georgia,serif" font-weight="700" font-size="44" fill="#C9A227" text-anchor="middle">{modelo}</text></g>')


def nota(x, y, s=1.0, linea1="TIGGO 4", precio=True):
    """Nota crema escrita a mano: la cara del precio al voltear."""
    cara = (f'<text x="0" y="25" font-family="Georgia,serif" font-style="italic" font-weight="700" font-size="60" fill="#3A2E1B" text-anchor="middle">${{ }}</text>'
            f'<text x="0" y="90" font-family="Georgia,serif" font-size="32" fill="#6B4F2A" text-anchor="middle">{linea1}</text>')
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<rect x="-190" y="-120" width="380" height="240" fill="#F7F1DF" stroke="#C9A227" stroke-width="6" transform="rotate(-2)"/>'
            '<rect x="-70" y="-138" width="140" height="36" fill="#C9A227" opacity=".45" transform="rotate(-2)"/>'
            f'{cara}</g>')


def carpeta(x, y, s=1.0):
    """Carpeta negra con broche dorado, medio abierta."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<rect x="-260" y="-160" width="520" height="330" rx="14" fill="#191920" stroke="#C9A227" stroke-width="6" transform="rotate(-2)"/>'
            '<rect x="-240" y="-180" width="480" height="310" rx="14" fill="#22222A" stroke="#C9A227" stroke-width="4" transform="rotate(3)"/>'
            '<rect x="-70" y="-20" width="140" height="26" rx="8" fill="#C9A227"/></g>')


def mano(x, y, s=1.0):
    """Mano sosteniendo el borde de la nota o carpeta."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<rect x="-30" y="0" width="60" height="330" rx="28" fill="#D9A57C"/>'
            '<circle cx="0" cy="-10" r="58" fill="#D9A57C"/>'
            '<circle cx="-24" cy="52" r="22" fill="#C8936B"/><circle cx="24" cy="52" r="22" fill="#C8936B"/>'
            '<circle cx="0" cy="20" r="24" fill="#C8936B"/></g>')


def llaves(x, y, s=1.0):
    """Llaves doradas sostenidas hacia cámara."""
    return (f'<g transform="translate({x} {y}) scale({s})">'
            '<circle cx="-60" cy="-40" r="46" fill="none" stroke="#C9A227" stroke-width="16"/>'
            '<rect x="-38" y="-18" width="150" height="22" rx="10" fill="#C9A227" transform="rotate(18)"/>'
            '<rect x="60" y="40" width="18" height="46" fill="#C9A227" transform="rotate(18)"/>'
            '<rect x="95" y="52" width="18" height="40" fill="#C9A227" transform="rotate(18)"/>'
            '<circle cx="40" cy="30" r="20" fill="none" stroke="#C9A227" stroke-width="12"/></g>')


def card(texto, y=330, size=64):
    """Texto en pantalla, dentro de la zona segura."""
    lineas = texto.split("|")
    alto = 70 + int(size * 1.15) * len(lineas)
    t = "".join(f'<text x="470" y="{y + 40 + size + i * int(size * 1.15)}" font-family="Georgia,serif" font-weight="700" font-size="{size}" '
                f'fill="#fff" text-anchor="middle">{l}</text>' for i, l in enumerate(lineas))
    return f'<rect x="90" y="{y}" width="760" height="{alto}" rx="16" fill="#0B0B0F" opacity=".85"/>{t}'


ZONA = ('<rect x="0" y="230" width="850" height="1210" fill="none" stroke="#DC2626" stroke-width="5" stroke-dasharray="20 14" opacity=".6"/>')

CUATRO = (suv(120, 1500, "TIGGO 4", .72) + suv(370, 1500, "TIGGO 4", .72) +
          camioneta(650, 1500, "HIMLA", .72) + camioneta(920, 1500, "HIMLA", .72))

TOMAS = [
    dict(t="0:00-0:03", cam="Plano entero: la asesora camina hacia cámara, decidida, con la carpeta negra. Las 4 unidades fuera de foco al fondo.",
         ve="La asesora de blanco con lentes negros camina hacia cámara con la carpeta. Showroom en penumbra.",
         voz="“Su Tiggo 4 tiene precio desde hoy. Caduca hoy.”", txt="PRECIO DESDE HOY",
         svg=PISO + LUZ + suv(180, 1500, "TIGGO 4", .5) + camioneta(880, 1500, "HIMLA", .5)
             + agente(540, 1330, 1.0) + carpeta(770, 1120, .55) + card("PRECIO DESDE HOY")),
    dict(t="0:03-0:05", cam="Primer plano: la carpeta se abre y sale la nota de la Tiggo 4 con el precio al frente.",
         ve="La nota crema de la Tiggo 4 con el precio escrito a mano, sobre la carpeta negra.",
         voz="“Tiggo 4, para la familia: {{precio Tiggo 4}}.”", txt="TIGGO 4 ${{ }}",
         svg=PISO + carpeta(540, 1100, 1.1) + nota(540, 850, 1.1, "TIGGO 4") + mano(940, 700) + card("TIGGO 4 ${{ }}")),
    dict(t="0:05-0:07", cam="Corte idéntico, la nota de la Himla. Mismo encuadre, misma mano.",
         ve="La nota crema de la Himla con el precio escrito a mano.",
         voz="“Himla, para el trabajo: {{precio Himla}}.”", txt="HIMLA ${{ }}",
         svg=PISO + carpeta(540, 1100, 1.1) + nota(540, 850, 1.1, "HIMLA") + mano(940, 700) + card("HIMLA ${{ }}")),
    dict(t="0:07-0:10", cam="Plano abierto: luz cenital sobre las cuatro unidades en fila, 2 + 2.",
         ve="Las cuatro en fila bajo un haz de luz: Tiggo 4, Tiggo 4, Himla, Himla.",
         voz="“Son 2 y 2, de contado, para quien pague primero. Hoy.”", txt="2 Y 2 · CONTADO",
         svg=PISO + LUZ + CUATRO + card("2 Y 2 · CONTADO", 330, 60)),
    dict(t="0:10-0:13", cam="Plano medio: la asesora a cámara se quita los lentes y extiende las llaves hacia el lente.",
         ve="La asesora ofrece las llaves hacia la cámara, seria. Nada de sonrisa: el gesto es la firma.",
         voz="“¡Tu sueño se cumple hoy!”", txt="TU SUEÑO SE CUMPLE HOY",
         svg=PISO + LUZ + agente(540, 1380, 1.05, lentes=False, cam="entrega") + llaves(760, 1080, .9)
             + card("TU SUEÑO|SE CUMPLE HOY", 300, 56)),
    dict(t="0:13-0:18", cam="Placa final: negro, logo y línea dorada. Se sostiene 2 s en silencio.",
         ve="Placa negra: CHERY EN DAI MOTORS, la línea dorada y las cuatro notas pegadas al vidrio.",
         voz="“Tienes hasta las 6 pm. Chery Dai Motors.”", txt="HASTA LAS 6 PM|CHERY DAI MOTORS",
         svg=PISO + CUATRO + card("HASTA LAS 6 PM|CHERY DAI MOTORS", 300, 56)),
]

STORIES = [
    ("8:00 am · Reel compartido", "El expediente abrió a las 8.", ""),
    ("Cada venta confirmada", "Asignación cumplida. Quedan {{N}}.", "Nota: VENDIDA"),
    ("12:00 m", "Estas esperan a su dueño.", "Foto de las que quedan"),
    ("3:00 pm", "¿Vino por la suya?", "Encuesta: Sí / Esta vez no"),
    ("Si se agotan", "Cuatro asignaciones cumplidas. Obsequios o descuentos en otra unidad hasta las {{hora cierre}}.", "Cuatro notas VENDIDA"),
    ("{{hora cierre}}", "El expediente se cierra. Gracias.", "La puerta del showroom cerrándose"),
]

CSS = f"""
@page {{ size: Letter landscape; margin: 9mm 10mm }}
* {{ box-sizing: border-box; margin: 0; padding: 0 }}
body {{ font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 11px }}
.pg {{ break-after: page }} .pg:last-child {{ break-after: auto }}
.top {{ display: flex; justify-content: space-between; align-items: baseline; border-bottom: 3px solid {AZUL}; padding-bottom: 4px; margin-bottom: 8px }}
.top b {{ font-size: 16px; color: {AZUL} }} .top span {{ color: #64748B; font-size: 10px }}
.row {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 8px }}
.f svg {{ width: 100%; aspect-ratio: 9/16; display: block; border: 2px solid #C9A227; border-radius: 10px; background: #101014 }}
.f .tt {{ display: flex; justify-content: space-between; margin: 4px 0 2px; font-weight: 800; color: {AZUL}; font-size: 10px }}
.f p {{ margin: 1px 0; line-height: 1.25; font-size: 9px }}
.f .v {{ background: #F5EFE3; border-left: 3px solid #C9A227; padding: 2px 4px; font-style: italic }}
.f .t {{ color: #3A2E1B; font-weight: 700; font-size: 9px }}
.leg {{ margin-top: 6px; color: #64748B; font-size: 9.5px }}
.two {{ display: grid; grid-template-columns: 1.1fr 1fr; gap: 16px }}
h3 {{ font-size: 12.5px; color: {AZUL}; margin: 8px 0 4px }}
table {{ width: 100%; border-collapse: collapse; font-size: 10.5px }}
th {{ background: #E8DFC9; text-align: left; padding: 3px 6px; font-size: 9.5px; text-transform: uppercase }}
td {{ border-bottom: 1px solid #E8DFC9; padding: 3px 6px; vertical-align: top }}
.carteles {{ display: flex; gap: 10px; flex-wrap: wrap }}
.cart {{ border: 2px solid #6B4F2A; background: #F7F1DF; padding: 8px 14px; font: 700 17px Georgia, serif; font-style: italic; color: #3A2E1B }}
.cart small {{ display: block; font: 400 9px Arial; color: #64748B; font-style: normal }}
.st {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 7px }}
.st div {{ border: 2px solid #E8DFC9; border-radius: 8px; padding: 6px; display: flex; flex-direction: column;
  justify-content: space-between; font-size: 9.5px; background: #FAF6EC; min-height: 66px }}
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


DOC = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><title>Mockup reel precios · Chery · vie 27 · luxury</title>
<style>{CSS}</style></head><body>
<section class="pg">
  <div class="top"><b>Mockup · Reel “Los precios” · @cherymaracaibo · estilo luxury MIB</b><span>Vie 27 nov · 8:00 am · 18 s · vertical 1080x1920</span></div>
  <div class="row">{tomas_html()}</div>
  <p class="leg">Línea roja punteada: zona segura. El texto en pantalla va dentro de ella; fuera lo tapan el caption y los botones.
  Dibujos de referencia de encuadre, no de vestuario. ${{ }} = precio real por confirmar, se escribe a mano en la nota.</p>
</section>
<section class="pg">
  <div class="top"><b>Producción · Reel “Los precios” · tono serio luxury</b><span>Grabar y montar el jue 26 en la tarde · publicar vie 27, 8:00 am</span></div>
  <div class="two">
    <div>
      <h3>Ficha</h3>
      <table>
        <tr><th>Sale</th><td>La asesora de blanco con lentes negros (la firma de la cuenta, modo agente) + sus manos</td></tr>
        <tr><th>Graba</th><td>Un asesor, celular en vertical, trípode. Luz baja controlada: cortinas a media luz, solo el haz sobre las unidades</td></tr>
        <tr><th>Lugar</th><td>Showroom oscuro, las 4 unidades en fila: 2 Tiggo 4 y 2 Himla</td></tr>
        <tr><th>Props</th><td>Carpeta negra con broche dorado, notas de papel crema escritas a mano (precio al frente al voltear), llaves doradas, lentes negros</td></tr>
        <tr><th>Audio</th><td>Voz en off grave, pausada, grabada aparte. Música de misión, grave y sin letra (estilo agencia secreta). Un tic-tac muy bajo bajo el precio. Silencio total en la placa final</td></tr>
        <tr><th>Regla</th><td>La nota VENDIDA solo se escribe con venta confirmada. Nunca publicar “quedan pocas”</td></tr>
        <tr><th>Tono</th><td>Serio, elegante, sin bromas. La asesora no sonríe: la confianza la da el gesto lento y la voz. Cero autobombo</td></tr>
      </table>
      <h3>Notas para escribir (papel crema, marcador negro)</h3>
      <div class="carteles">
        <div class="cart">TIGGO 4 / ${{ }}<small>2 notas · el precio al frente, se revela al abrir la carpeta</small></div>
        <div class="cart">HIMLA / ${{ }}<small>2 notas · mismo formato, misma letra</small></div>
        <div class="cart">VENDIDA<small>4 notas de repuesto · se escriben solo con venta confirmada</small></div>
      </div>
      <h3>Texto para decir (voz en off)</h3>
      <table><tr><td>Su Tiggo 4 tiene precio desde hoy.<br>Caduca hoy.<br>Tiggo 4, para la familia: {{precio Tiggo 4}}.<br>Himla, para el trabajo: {{precio Himla}}.<br>Son 2 y 2, de contado, para quien pague primero.<br>¡Tu sueño se cumple hoy!<br>Tienes hasta las 6 pm. Chery Dai Motors.</td></tr></table>
      <h3>Checklist antes de las 8:00 am</h3>
      <ul>
        <li>Precios reales confirmados por Gerencia y escritos en las notas.</li>
        <li>Showroom a media luz: el haz de luz sobre las 4 unidades, nada más encendido.</li>
        <li>Vestido blanco planchado y lentes negros limpios: son la firma del personaje.</li>
        <li>Carpeta negra, broche dorado y llaves con brillo (una pasada de paño).</li>
        <li>La toma 5 se graba 3 veces: extender las llaves sin sonreír, 2 s, sin parpadear.</li>
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
        <li>{{precio Tiggo 4}} y {{precio Himla}}: decisión de Gerencia.</li>
        <li>{{hora cierre}} del viernes: definir el horario de cierre del showroom.</li>
        <li>Después de cada venta: story de la nota VENDIDA + DM a la lista BLACK con las que quedan.</li>
      </ul>
    </div>
  </div>
</section>
</body></html>"""

os.makedirs(OUT_DIR, exist_ok=True)
out_html = os.path.join(OUT_DIR, "Mockup-Reel-Vie27-Precios-Chery.html")
out_pdf = os.path.join(OUT_DIR, "Mockup-Reel-Vie27-Precios-Chery.pdf")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(DOC)
try:
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", f"--print-to-pdf={out_pdf}", out_html],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
except FileNotFoundError:
    out_pdf = None
print(out_pdf or out_html)
