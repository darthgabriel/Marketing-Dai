#!/usr/bin/env python3
"""Genera el brief de influencers del SPECIAL DAI en estilo 'Creative Brief' (tipo Nike).
Fuente de verdad: content/special-dai-brief-influencers.md
Salida: entregables/Special-Dai-Brief-Influencers.pdf (2 páginas)

Mejoras de diseño (ui-ux-pro-max):
- Estilo Swiss/editorial: grilla, alineación fuerte, numeración de secciones.
- Escala tipográfica modular consistente: 7.2 / 8.4 / 9.4 / 13.5 / 25 / 46.
- Contraste: texto principal #14181F (≈16:1), secundario #3D4451 (≈8.5:1),
  etiquetas #5A6270 (≈5.6:1). Nada de gris sobre gris.
- Line-height 1.5–1.6 en cuerpo (legibilidad).
- Sin emojis como iconos: círculos con iniciales (SVG-equivalent, print-safe).
"""
import subprocess, os

CSS = """
  @page { size: Letter; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html, body { background: #fff; color: #14181F; font-family: "IBM Plex Sans", system-ui, sans-serif; }
  .page { width: 8.5in; height: 11in; padding: 0.55in 0.62in 0.5in; position: relative; page-break-after: always; display: flex; flex-direction: column; }
  .page:last-child { page-break-after: auto; }

  /* ---- tipografía: escala modular 7.2 · 8.4 · 9.4 · 13.5 · 25 · 46 ---- */
  .hb-top { font-size: 12px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: ACCENT; }
  .wordmark { font-family: "Archivo Black", "IBM Plex Sans", sans-serif; font-size: 42px; letter-spacing: -1px; line-height: 1.02; margin: 2px 0 6px; }
  .wordmark .old { position: relative; color: #6B7280; }
  .wordmark .old::after { content: ""; position: absolute; left: -4px; right: -4px; top: 56%; height: 7px; background: #D0021B; transform: rotate(-5deg); }
  .wordmark .new { color: #14181F; }
  .tag { font-size: 9.4px; color: #3D4451; line-height: 1.5; max-width: 6.2in; margin-bottom: 12px; }

  .clientbox { border: 1.5px solid #14181F; padding: 9px 13px; font-size: 9px; line-height: 1.5; max-width: 4.4in; }
  .clientbox .lbl { font-size: 7.2px; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: ACCENT; }
  .clientbox .sep { border-top: 1px dashed #C4C9D2; margin: 7px 0; }

  /* ---- grilla de 2 columnas con divisor punteado (Swiss) ---- */
  .cols { display: grid; grid-template-columns: 1fr 1.5px 1fr; gap: 0 24px; margin-top: 16px; flex: 1 1 auto; }
  .dash { border-left: 2px dashed #C4C9D2; }
  .sec { margin-bottom: 16px; }
  .sec-h { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; }
  .ico { width: 22px; height: 22px; border-radius: 50%; background: ACCENT; color: #fff; display: inline-flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 700; flex: 0 0 22px; }
  .sec-h .n { font-size: 7.2px; font-weight: 700; letter-spacing: .18em; color: #5A6270; margin-left: auto; }
  .sec-h .t { font-size: 13.5px; font-weight: 700; letter-spacing: .1em; text-transform: uppercase; }
  .sec p { font-size: 9.4px; line-height: 1.55; color: #232A35; }
  .sec p + p { margin-top: 6px; }
  .sec ul, .sec ol { margin: 4px 0 0 15px; font-size: 9.4px; line-height: 1.55; color: #232A35; }
  .sec li { margin-bottom: 3px; }
  .sec ol { list-style: none; margin-left: 0; counter-reset: step; }
  .sec ol li { counter-increment: step; padding-left: 20px; position: relative; }
  .sec ol li::before { content: counter(step); position: absolute; left: 0; top: 1px; font-size: 7.2px; font-weight: 700; color: #fff; background: ACCENT; width: 13px; height: 13px; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

  .facts { display: flex; gap: 16px; margin-top: 8px; }
  .fact { text-align: center; flex: 1; }
  .fact .circ { width: 82px; height: 82px; border-radius: 50%; border: 2.5px solid ACCENT; margin: 0 auto 6px; display: flex; flex-direction: column; align-items: center; justify-content: center; }
  .fact .circ b { font-size: 23px; font-weight: 700; line-height: 1; }
  .fact .circ span { font-size: 6.5px; letter-spacing: .14em; text-transform: uppercase; color: #3D4451; margin-top: 3px; }
  .fact .cap { font-size: 8px; color: #3D4451; line-height: 1.35; }

  .taged { background: #F4F6F9; border-left: 3px solid #D0021B; padding: 8px 11px; font-size: 9.2px; line-height: 1.5; color: #232A35; margin-top: 8px; }
  .kw { font-family: Consolas, monospace; font-size: 8.2px; background: #EEF1F5; padding: 1.5px 5px; border-radius: 3px; color: #14181F; }
  table { width: 100%; border-collapse: collapse; font-size: 8.6px; margin-top: 7px; }
  th { text-align: left; font-size: 7.2px; letter-spacing: .14em; text-transform: uppercase; color: #5A6270; font-weight: 600; padding: 4.5px 0; border-bottom: 1.5px solid #14181F; }
  td { padding: 5px 0; border-bottom: 1px solid #E5E8EE; vertical-align: top; line-height: 1.4; color: #232A35; }
  .red { color: #D0021B; }
  .note { font-size: 8.4px; color: #3D4451; line-height: 1.5; margin-top: 8px; }

  .bottom { margin-top: auto; padding-top: 14px; }
  .bottom .rule { border-top: 2px dashed #C4C9D2; margin-bottom: 12px; }
  .hashtag { font-family: "Archivo Black", "IBM Plex Sans", sans-serif; font-size: 46px; letter-spacing: -1px; line-height: 1; color: #14181F; }
  .footer { position: absolute; right: 0.62in; bottom: 0.26in; font-size: 7px; letter-spacing: .16em; text-transform: uppercase; color: #8A919E; }
"""

ACC = "#0032C0"
FOOTER = "SPECIAL DAI · BRIEF INFLUENCERS · NOV 2026"

HEAD = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>Special Dai · Creative Brief · Influencers</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>"""

def page(n, content):
    css = CSS.replace("ACCENT", ACC)
    return (f'<section class="page">{content}'
            f'<div class="footer">SPECIAL DAI · {n}/2 · {FOOTER}</div></section>')

def sec(icon, title, num, inner):
    return (f'<div class="sec"><div class="sec-h"><span class="ico">{icon}</span>'
            f'<span class="t">{title}</span><span class="n">{num}</span></div>{inner}</div>')

def table_html(headers, rows):
    h = "".join(f"<th>{x}</th>" for x in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return f"<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>"

def header_block():
    return """
  <div class="hb-top">Brief creativo para</div>
  <div class="wordmark">SPECIAL <span class="old">DAYS</span> <span class="new">DAI</span></div>
  <div class="tag">Evento de ventas Dai Motors · Hyundai + Chery Maracaibo · del 2 al 7 de noviembre de 2026 · cierre sáb 7, 5 pm</div>
  <div class="clientbox">
    <span class="lbl">Cliente</span><br>
    <b>Dai Motors</b> — Concesionario autorizado Hyundai y Chery · Maracaibo, Zulia<br>
    <span style="color:#3D4451">@daimotorsmcbo · @cherymaracaibo</span>
    <div class="sep"></div>
    <span class="lbl">Preparado por</span><br>
    <b>Marketing Dai Motors</b><br>
    <span style="color:#3D4451">Contacto operativo: marketing Dai Motors</span>
  </div>"""

# ============================================================ PÁGINA 1
p1_left = sec("?", "El problema", "01", """
<p>Tres problemas resuelven el Special Dai.</p>
<ol>
<li><b>Otros concesionarios sin disponibilidad.</b> La resolución: tenemos 20 vehículos por marca en showroom y a lo que se vendan no se reponen.</li>
<li><b>Financiamiento percibido como difícil.</b> El comprador zuliano desconfía del concesionario y cree que el crédito es un calvario. El 60% del mercado compra a crédito.</li>
<li><b>Seis días de ventana.</b> Precios especiales solo del 2 al 7 de noviembre. Después de esa fecha los precios no vuelven.</li>
</ol>""") + sec("!", "El objetivo", "02", """
<p>Lo que el influencer debe lograr:</p>
<ul>
<li><b>Tráfico al showroom</b> con Pase Special Dai (cita el día del evento).</li>
<li><b>Mensajes al DM</b> con la keyword VIP.</li>
<li><b>Meta productiva:</b> 20 unidades por marca en showroom, no se reponen.</li>
<li><b>Top of mind</b> Dai Motors en el Zulia al cierre del 2026.</li>
</ul>""") + sec("Q", "Los datos", "03", """
<div class="facts">
  <div class="fact"><div class="circ"><b>6</b><span>días</span></div><div class="cap">Del 2 al 7 de noviembre</div></div>
  <div class="fact"><div class="circ"><b>20</b><span>por marca</span></div><div class="cap">Unidades en showroom. No se reponen</div></div>
  <div class="fact"><div class="circ"><b class="red">5pm</b><span>cierre</span></div><div class="cap">Sáb 7 nov · música en vivo desde 4 pm</div></div>
</div>""")

p1_right = sec("B", "El concepto", "04", """
<p>El evento se llama <b>SPECIAL DAI</b>: antes decía "SPECIAL <span style="text-decoration:line-through">DAYS</span>" y lo tachamos en rojo.
Es nombre propio del grupo, único y medible. El tachado es la identidad.</p>
<p>Seis días de precio especial sobre inventario real, asesoría de financiamiento en showroom y entrega express máxima de 3 días.
Dos concesionarios vecinos, Hyundai y Chery, una sola campaña. Cada colaboración es con una marca — <b>no se mezclan</b>.</p>
<div class="taged"><b>El cierre es especial:</b> sábado 7 de noviembre, desde las 4:00 pm — <b>música en vivo</b>, celebración y el último llamado. Cierra 5:00 pm. Después de esa hora los precios especiales mueren.</div>""") + sec("A", "El público", "05", """
<p><b>El comprador:</b> zulianos de 25 a 50 años que compran a crédito, desconfían de los concesionarios y quieren estrenar sin trabas.</p>
<p><b>En redes:</b> Hyundai — familias y emprendedores, humor zuliano y directo (9.830 seguidores). Chery — jóvenes 25–40 aspiracionales, primera SUV (13.000 seguidores).</p>
<p>El contenido del influencer debe verse real, no de catálogo: fotos del showroom, unidades reales, trato cercano.</p>""") + sec("M", "La mecánica", "06", """
<ol>
<li><b>Escribe VIP</b> al DM de la cuenta correspondiente.</li>
<li>Recibe tu <b>Pase Special Dai</b> el día del evento.</li>
<li>Llega al showroom, elige tu vehículo, reservas y <b>es tuyo con el descuento el mismo día</b>.</li>
</ol>""")

p1 = header_block() + f"""
  <div class="cols">
    <div>{p1_left}</div>
    <div class="dash"></div>
    <div>{p1_right}</div>
  </div>
  <div class="bottom">
    <div class="rule"></div>
    <div class="hashtag">#SpecialDai</div>
  </div>"""

# ============================================================ PÁGINA 2
p2_left = sec("R", "Los entregables", "07", table_html(["Entregable", "Detalle"], [
    ["Media day", "Recorrido por ambas zonas (Hyundai · Chery), lives y grabación vertical"],
    ["Reels", "9:16 · 1080×1920 · 8–20 s · subtítulos quemados · hook en los 2 primeros segundos"],
    ["Stories", "9:16 · 7 s por tarjeta · sticker de encuesta o contador"],
    ["Cierre", "Keyword VIP + mención del cierre sáb 7"],
    ["Música en vivo", "Presencia o cobertura del cierre con música en vivo"],
]) + """
<p class="note">Cada pieza se aprueba antes de publicar. Duda de precio, keyword o cuota → no se publica, se consulta.</p>""") + sec("P", "Prohibido", "08", """
<ul>
<li>Precios en el feed.</li>
<li>"Special Days" sin tachar en rojo.</li>
<li>Mostrar el showroom completo.</li>
<li>Inventar cuotas y/o precios.</li>
<li>Usar una keyword distinta a VIP.</li>
<li>Grabar clientes sin autorización escrita.</li>
</ul>""")

p2_right = sec("C", "Los conceptos", "09", """
<p>Seis conceptos. Uno por pieza. Nunca dos en el mismo contenido.</p>
""" + table_html(["Concepto", "Cómo se cuenta"], [
    ["<b>Precios especiales</b>", '"Hay un precio que solo existe del 2 al 7 de noviembre. Pregunta por él." (la cifra va en showroom)'],
    ["<b>Entrega express</b>", "Apruebas hoy, te lo llevas rápido. Cliente que compara y no decide. Solo a contado."],
    ["<b>Consignación de documentos</b>", "Verificamos tus documentos de financiamiento y te asesoramos."],
    ["<b>Asesoría en financiamiento</b>", "Te asesoramos con la inicial, cuotas y plazos que más se adapten a ti."],
    ["<b>Revelación del más vendido</b>", "Diremos cuál es el vehículo más vendido en 2026."],
    ["<b>Pocas unidades</b>", '"Lo que ves en el showroom es todo lo que hay."'],
]) + """
""") + sec("G", "Dirección creativa", "10", """
<p><b>Ángulo principal:</b> escasez real y precio que muere. No es "otra promoción": es un evento con fecha de cierre.</p>
<p><b>Mensaje clave:</b> 20 vehículos por marca, no se reponen. Después del sábado 7 a las 5 pm los precios especiales mueren.</p>
<p><b>Tono por cuenta:</b> Hyundai — cercano, humor zuliano, directo. Chery — aspiracional, emotivo, cercano. El influencer se suma al tono de la cuenta donde publique.</p>
<p><b>Referencia visual:</b> showroom real, unidades reales, sin catálogo. Vertical 9:16 siempre.</p>
""") + sec("S", "Las cuentas", "11", table_html(["", "Hyundai", "Chery"], [
    ["Cuenta", "@daimotorsmcbo", "@cherymaracaibo"],
    ["Seguidores", "9.830", "13.000"],
    ["Voz", "Cercano, emotivo", "Cercano, emotivo"],
    ["Keyword", '<span class="kw">VIP</span>', '<span class="kw">VIP</span>'],
]))

p2 = """
  <div class="hb-top">Brief creativo para</div>
  <div class="wordmark" style="font-size:30px"><span class="new">Ejecución del influencer</span></div>
  <div class="tag">Qué entregar, qué cuenta y qué no se puede hacer · mié 4 nov: media day en ambas zonas</div>
  <div class="cols">
    <div>""" + p2_left + """</div>
    <div class="dash"></div>
    <div>""" + p2_right + """</div>
  </div>
  <div class="bottom">
    <div class="rule"></div>
    <div class="hashtag" style="font-size:32px">#SpecialDai · 2–7 nov · cierra sáb 7, 5 pm</div>
  </div>"""

def build_html():
    css = CSS.replace("ACCENT", ACC)
    return (HEAD.format(css=css) + page(1, p1) + page(2, p2) + "</body></html>")

def render(html_path, pdf_path):
    browser = os.environ.get("CHROME_PATH")
    if not browser:
        for p in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                  r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"):
            if os.path.exists(p):
                browser = p
                break
    out = os.path.abspath(pdf_path)
    subprocess.run([browser, "--headless", "--disable-gpu", "--no-sandbox",
                    "--no-pdf-header-footer", f"--print-to-pdf={out}",
                    "file:///" + os.path.abspath(html_path).replace("\\", "/")],
                   check=True, capture_output=True, timeout=120)
    print(f"PDF: {out} ({os.path.getsize(out)/1024:.0f} KB)")

if __name__ == "__main__":
    html_path = os.path.join(os.path.dirname(__file__), "..", "entregables", "special-dai-brief-influencers.html")
    html_path = os.path.abspath(html_path)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(build_html())
    print("HTML:", html_path)
    render(html_path, os.path.join(os.path.dirname(html_path), "Special-Dai-Brief-Influencers.pdf"))
