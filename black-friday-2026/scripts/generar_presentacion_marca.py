"""Presentación Black Friday 2026 para las marcas (Hyundai y Chery) - 2 hojas carta, sin montos.
Explica de qué va la campaña, las reglas y el calendario de la cuenta de cada marca.
Salida: black-friday-2026/entregables/Black-Friday-2026-Hyundai.pdf y Black-Friday-2026-Chery.pdf
Uso: python black-friday-2026/scripts/generar_presentacion_marca.py
"""
import os
import re
import subprocess

from generar_propuesta import CSS, rows

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

EXTRA_CSS = """
.cal td:first-child { white-space: nowrap; font-weight: 700; width: 92px }
.cal td:nth-child(2) { white-space: nowrap; color: #64748B; width: 72px }
.cal tr.x td { background: #FEF2F2 }
.cal tr.l td { color: #94A3B8; font-style: italic }
.rules { counter-reset: r; list-style: none; padding: 0; display: grid; grid-template-columns: 1fr 1fr; gap: 6px 14px }
.rules li { counter-increment: r; position: relative; padding-left: 26px; margin: 0 }
.rules li::before { content: counter(r); position: absolute; left: 0; top: 0; background: #0B0B0F; color: #fff;
  width: 18px; height: 18px; border-radius: 4px; font-size: 10px; font-weight: 700; display: flex; align-items: center; justify-content: center }
.steps { grid-template-columns: repeat(6, 1fr) }
"""

MARCAS = {
    "Hyundai": {
        "cuenta": "@daimotorsmcbo",
        "firma": "Hyundai en Dai Motors",
        "total": "4",
        "unidades": [("2", "Hyundai Accent"), ("2", "Hyundai Creta")],
        "hilo": "Humor zuliano con un personaje propio: Alexis, el asesor que lleva un cartel en la espalda y nunca sabe qué dice. "
                "El cartel anuncia lo que viene, se aparta para revelar las unidades y el viernes se convierte en el contador: QUEDAN 4, 3, 2...",
        "teaser": "El equipo de ventas, vestido de negro, se pone lentes oscuros y se forma frente al logo Hyundai: BLACK FRIDAY.",
        "cal": [
            ("Lun 16 nov", "7:00 pm", "Reel teaser", "El equipo de negro con lentes oscuros. Viernes 27, comenta BLACK."),
            ("Mar 17", "7:00 pm", "Reel", "Le pegan a Alexis un cartel en la espalda: algo viene el 27."),
            ("Mié 18", "", "Sin oferta", "Bajada de La Chinita: solo saludo."),
            ("Jue 19", "7:00 pm", "Reel", "El cliente que pide 50%: el descuento es real, pero no ese."),
            ("Vie 20", "7:00 pm", "Carrusel", "Lo que sirve y lo que no sirve para pagar de contado."),
            ("Sáb 21 · Dom 22", "", "Libre", ""),
            ("Lun 23", "7:00 pm", "Reel revelación", "Alexis se aparta y aparecen las 4 unidades: 2 Accent y 2 Creta. Sin precio."),
            ("Mar 24", "7:00 pm", "Carrusel", "Las bases, explicadas por Alexis. WhatsApp a la lista y a clientes recientes."),
            ("Mié 25", "7:00 pm", "Reel", "Alexis les habla a las cuatro. Último día para entrar a la lista."),
            ("Jue 26", "7:00 am", "WhatsApp", "La lista BLACK recibe los precios, antes que nadie."),
            ("Jue 26", "7:00 pm", "Reel", "Falta un día: la lista ya sabe el precio."),
            ("Vie 27", "8:00 am", "Reel + stories", "Precios públicos. Contador de unidades todo el día, solo con ventas confirmadas."),
            ("Sáb 28 · Dom 29", "", "Libre", ""),
            ("Lun 30", "7:00 pm", "Reel", "Cómo terminó: cuántas se vendieron."),
            ("Mié 2 dic", "7:00 pm", "Reel", "Las entregas, con los clientes que den su permiso."),
        ],
    },
    "Chery": {
        "cuenta": "@cherymaracaibo",
        "firma": "Chery en Dai Motors",
        "total": "4",
        "unidades": [("2", "Chery Tiggo 4"), ("2", "Chery Himla")],
        "hilo": "Emotivo y sin humor: \"Cuatro historias que todavía no empiezan\". Dos Tiggo 4 esperan su primera historia de familia "
                "y dos Himla su primera jornada de trabajo. Notas escritas a mano guían hasta ellas; en cámara solo salen manos, con voz en off. "
                "El viernes cada nota se marca VENDIDA cuando su historia empieza.",
        "teaser": "Asesores de negro con lentes oscuros se sientan al volante; en los lentes se lee BLACK FRIDAY.",
        "cal": [
            ("Lun 16 nov", "7:00 pm", "Reel teaser", "Todos de negro al volante, BLACK FRIDAY en los lentes. Viernes 27, comenta BLACK."),
            ("Mar 17", "7:00 pm", "Reel", "Una nota en la puerta: algo empieza el 27."),
            ("Mié 18", "", "Sin oferta", "Bajada de La Chinita: solo saludo."),
            ("Jue 19", "7:00 pm", "Reel", "El descuento que puedes creer: en carros, el 50% no existe."),
            ("Vie 20", "7:00 pm", "Carrusel", "El día que pagas tu carro completo: qué tener listo."),
            ("Sáb 21 · Dom 22", "", "Libre", ""),
            ("Lun 23", "7:00 pm", "Reel revelación", "Las notas guían hasta las 4 unidades: 2 Tiggo 4 y 2 Himla. Sin precio."),
            ("Mar 24", "7:00 pm", "Carrusel", "Lo que necesitas saber, sin letra pequeña. WhatsApp a la lista y a clientes recientes."),
            ("Mié 25", "7:00 pm", "Reel", "Las historias que escribieron los seguidores, pegadas en las unidades."),
            ("Jue 26", "7:00 am", "WhatsApp", "La lista BLACK recibe los precios, antes que nadie."),
            ("Jue 26", "7:00 pm", "Reel", "La noche antes: mañana, alguien estrena."),
            ("Vie 27", "8:00 am", "Reel + stories", "Precios públicos. Las notas se marcan VENDIDA solo con ventas confirmadas."),
            ("Sáb 28 · Dom 29", "", "Libre", ""),
            ("Lun 30", "7:00 pm", "Reel", "Cómo terminó: cuántas historias empezaron."),
            ("Mié 2 dic", "7:00 pm", "Reel", "Las primeras historias: entregas, con los clientes que den su permiso."),
        ],
    },
}

REGLAS = [
    "<b>Solo el viernes 27 de noviembre.</b> El descuento no aplica antes ni después.",
    "<b>Solo de contado.</b> Sin financiamiento ni cuotas en estas unidades.",
    "<b>Unidades contadas:</b> se dice cuántas hay y no se agregan más.",
    "<b>Descuento sobre el precio final</b>, definido por modelo. El resto del inventario mantiene su precio.",
    "<b>Cada unidad es del primer cliente que la pague.</b> La regla de pago se publica antes del viernes.",
    "<b>Lista BLACK:</b> quien comenta o escribe BLACK recibe el precio el jueves 26 a las 7 am, un día antes que el público.",
    "<b>Contador honesto:</b> el número de unidades que quedan solo cambia con una venta confirmada.",
    "<b>Si se agotan:</b> obsequios o descuentos en otra unidad, de contado, el mismo viernes.",
]


def html(marca, d):
    unidades = "".join(f'<div class="kpi"><b>{n}</b><span>{m}</span></div>' for n, m in d["unidades"])
    cal = ""
    for dia, hora, tipo, que in d["cal"]:
        cls = ' class="x"' if dia in ("Lun 23", "Vie 27") else (' class="l"' if tipo == "Libre" else "")
        cal += f"<tr{cls}><td>{dia}</td><td>{hora}</td><td><b>{tipo}</b></td><td>{que}</td></tr>"
    foot = lambda n: (f'<footer><span>Dai Motors · Marketing</span><span>Black Friday 2026 · {d["firma"]}</span>'
                      f'<span>{n} de 2</span></footer>')
    return f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Black Friday 2026 · {d["firma"]}</title><style>{CSS}{EXTRA_CSS}</style></head><body>

<section class="page">
  <div class="hero">
    <div><div class="k">BLACK FRIDAY 2026 · PRESENTACIÓN PARA {marca.upper()}</div><h1>A LA UNA, A LAS DOS, DE CONTADO...</h1>
    <div class="s">{d["firma"]} · Instagram {d["cuenta"]}</div></div>
    <div class="r"><b>Viernes 27 de noviembre</b>Solo contado</div>
  </div>
  <p class="lead">Unidades contadas de {marca}, con descuento sobre el precio final, solo el viernes 27 y de contado.
  <em>Cada unidad es del primer cliente que la pague.</em></p>
  <div class="kpis">
    <div class="kpi d"><b>{d["total"]}</b><span>unidades en la campaña</span></div>{unidades}
  </div>

  <h2><i>1</i>De qué se trata</h2>
  <ul>
    <li><b>Una oferta que se puede creer.</b> En lugar de "descuentos en todo", un número fijo de unidades con un descuento real y una fecha.</li>
    <li><b>Escasez verdadera.</b> Se dice cuántas hay y, el viernes, cuántas quedan. Nada de "últimas unidades" inventado.</li>
    <li><b>Primero los que se anotan.</b> La lista BLACK recibe el precio un día antes, para preparar el pago.</li>
    <li><b>El precio de la marca se cuida.</b> Solo bajan estas unidades; el resto del inventario no cambia.</li>
  </ul>

  <h2><i>2</i>Las reglas</h2>
  <ol class="rules">{"".join(f"<li>{r}</li>" for r in REGLAS)}</ol>

  <h2><i>3</i>Cómo funciona</h2>
  <div class="steps">
    <div class="st"><b>Desde lun 16</b>El cliente comenta o escribe BLACK y entra a la lista</div>
    <div class="st"><b>16 al 26 nov</b>Un asesor confirma que puede comprar de contado</div>
    <div class="st"><b>Lun 23</b>Se revelan las unidades, sin el precio</div>
    <div class="st"><b>Jue 26 · 7 am</b>La lista recibe los precios por WhatsApp</div>
    <div class="st h"><b>Vie 27 · 8 am</b>Precios públicos. Cada unidad, al primero que la pague</div>
    <div class="st"><b>Mié 2 dic</b>Reel de las entregas</div>
  </div>

  <h2><i>4</i>Línea creativa</h2>
  <table><tr><th style="width:110px">Pieza</th><th>Idea</th></tr>{rows([
    ["<b>Teaser</b><br><small>lun 16, ya grabado</small>", d["teaser"]],
    ["<b>Hilo de la campaña</b><br><small>mar 17 al mié 2 dic</small>", d["hilo"]],
    ["<b>Llamado</b>", "Siempre el mismo: comenta o escribe BLACK. Cierre de cada pieza: " + d["firma"] + "."],
  ])}</table>
  {foot(1)}
</section>

<section class="page">
  <div class="top"><b>Calendario en {d["cuenta"]}</b><span>Black Friday 2026 · {d["firma"]}</span></div>
  <table class="cal" style="margin-top:10px"><tr><th>Día</th><th>Hora</th><th>Formato</th><th>Qué se publica</th></tr>{cal}</table>
  <p class="note">Stories de lunes a viernes acompañan cada publicación: encuestas, cajas de preguntas y cuentas regresivas. Fines de semana sin publicaciones.</p>

  <h2><i>5</i>Lo que se definirá antes del arranque</h2>
  <ul>
    <li>Descuento por modelo y precio final de cada unidad.</li>
    <li>Versión y color de cada unidad.</li>
    <li>Medios de pago aceptados y regla de pago (qué cuenta como "pagó primero").</li>
    <li>Obsequios o descuentos para quien llegue cuando ya se agotaron.</li>
  </ul>
  {foot(2)}
</section>
</body></html>"""


os.makedirs(OUT_DIR, exist_ok=True)
for marca, d in MARCAS.items():
    doc = html(marca, d)
    assert not re.search(r"\$|\d+\s?%(?!\s*no existe)|USD|Special", doc.split("<body>")[1].replace("50%", "")), marca
    out_html = os.path.join(OUT_DIR, f"Black-Friday-2026-{marca}.html")
    out_pdf = os.path.join(OUT_DIR, f"Black-Friday-2026-{marca}.pdf")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                    f"--print-to-pdf={out_pdf}", out_html], check=True)
    print(out_pdf)
