"""Propuesta Black Friday 2026 para Gerencia - 3 hojas carta ("A la una, a las dos, de contado...").
Salida: black-friday-2026/entregables/Propuesta-Black-Friday-2026.html + .pdf
Datos: CRM autoweb Inventario Valorado (9 nov 2026), Corte de Cierre Special Dai (7 nov),
       Informe RRSS Octubre 2026.
Uso: python black-friday-2026/scripts/generar_propuesta.py
"""
import os
import subprocess

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(BASE, "entregables")
OUT_HTML = os.path.join(OUT_DIR, "Propuesta-Black-Friday-2026.html")
OUT_PDF = os.path.join(OUT_DIR, "Propuesta-Black-Friday-2026.pdf")
CREDITO = "Ing. Jose Paredes · Jefe IT & Marketing"

UNIDADES = [
    ("Hyundai en Dai Motors", "2 Accent + 2 Creta"),
    ("Chery en Dai Motors", "2 Tiggo 4 + 2 Himla"),
    ("Kaiyi en Yantai Motors", "2 Kaiyi X3 Pro"),
]
ADS = {"Hyundai": (20, 30, 35), "Chery": (18, 25, 29), "Yantai": (40, 25, 35)}
BULK = {"Hyundai": 35, "Chery": 35, "Yantai": 30}
FONDO_ADS, GASTO_SPECIAL = 157, 5057.34


def money(v):
    return "$" + f"{v:,.0f}".replace(",", ".")


def rows(data):
    return "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in data)


ads_tot = {k: sum(v) for k, v in ADS.items()}
ADS_T = sum(ads_tot.values())
BULK_T = sum(BULK.values())
MEDIOS = ADS_T + BULK_T
PEDIDO = MEDIOS - FONDO_ADS
assert (ADS_T, BULK_T, MEDIOS, PEDIDO) == (257, 100, 357, 200)
PCT_SPECIAL = round(MEDIOS / GASTO_SPECIAL * 100)

units = "".join(f'<div class="kpi"><span>{m}</span><b class="u">{n}</b></div>' for m, n in UNIDADES)
budget = rows([
    ["Meta Ads"] + [money(ads_tot[k]) for k in ADS] + [f"<b>{money(ADS_T)}</b>", f"{money(FONDO_ADS)} disponibles, $100 por aprobar"],
    ["Bulk WhatsApp"] + [money(BULK[k]) for k in ADS] + [f"<b>{money(BULK_T)}</b>", "Por aprobar"],
])
fases = rows(
    [n, f] + [money(ADS[k][i]) for k in ADS]
    for i, (n, f) in enumerate((("Expectativa", "17 al 22 nov"), ("Revelación", "23 al 26 nov"), ("Black Friday", "27 nov"))))
total_marca = "".join(f"<td><b>{money(ads_tot[k] + BULK[k])}</b></td>" for k in ADS)


def foot(n):
    return f'<footer><span>Elaborado por {CREDITO}</span><span>Uso interno de Gerencia</span><span>{n} de 3</span></footer>'


CSS = """
@page { size: Letter; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
html, body { font-family: 'Segoe UI', Arial, sans-serif; color: #0F172A; font-size: 11.6px; line-height: 1.42;
  -webkit-print-color-adjust: exact; print-color-adjust: exact }
.page { width: 8.5in; min-height: 10.96in; padding: .36in .42in .3in; display: flex; flex-direction: column; break-after: page }
.page:last-child { break-after: auto }
.hero { background: #0B0B0F; color: #fff; border-radius: 10px; padding: 18px 22px; display: flex; justify-content: space-between; align-items: flex-end }
.hero .k { font-size: 10px; letter-spacing: .14em; color: #F5C542; font-weight: 700 }
.hero h1 { font-size: 30px; line-height: 1.08; font-weight: 800; margin-top: 4px }
.hero .s { font-size: 11.5px; color: #CBD5E1; margin-top: 5px }
.hero .r { text-align: right; font-size: 10.5px; color: #CBD5E1; white-space: nowrap }
.hero .r b { color: #fff; font-size: 13px; display: block }
.top { display: flex; justify-content: space-between; align-items: baseline; border-bottom: 2px solid #0B0B0F; padding-bottom: 6px }
.top b { font-size: 14px; font-weight: 800 }
.top span { color: #64748B; font-size: 10px }
.lead { font-size: 15px; font-weight: 700; line-height: 1.3; margin: 14px 0 12px }
.lead em { font-style: normal; color: #D0021B }
.kpis { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px }
.kpi b.u { font-size: 16px; margin-top: 3px }
.kpi { border: 1px solid #E2E8F0; border-radius: 8px; padding: 9px 11px }
.kpi b { display: block; font-size: 22px; font-weight: 800; line-height: 1.1 }
.kpi span { color: #475569; font-size: 10px }
.kpi.d { background: #0B0B0F; border-color: #0B0B0F; color: #fff }
.kpi.d span { color: #CBD5E1 }
.kpi.d b { color: #F5C542 }
h2 { font-size: 12.5px; font-weight: 800; margin: 15px 0 6px; display: flex; gap: 7px; align-items: center }
h2 i { font-style: normal; background: #D0021B; color: #fff; width: 17px; height: 17px; border-radius: 4px; display: inline-flex; align-items: center; justify-content: center; font-size: 10px }
table { width: 100%; border-collapse: collapse; font-size: 11.2px }
th { background: #F1F5F9; text-align: left; padding: 5px 7px; font-size: 9.4px; color: #334155; font-weight: 700; text-transform: uppercase; letter-spacing: .03em }
td { padding: 5px 7px; border-bottom: 1px solid #E2E8F0; vertical-align: top }
td small { display: block; color: #64748B; font-size: 9.4px }
td .big { font-size: 15px; font-weight: 800; color: #D0021B }
tr.t td { background: #0B0B0F; color: #fff; border: 0 }
tr.rec td { background: #FEF9E7 }
ul { padding-left: 14px }
li { margin: 2.5px 0 }
.two { display: grid; grid-template-columns: 1fr 1fr; gap: 14px }
.note { color: #475569; font-size: 9.8px; margin-top: 6px }
.steps { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px }
.st { background: #F8FAFC; border-top: 3px solid #0B0B0F; padding: 6px 6px 7px; font-size: 9.5px; line-height: 1.3 }
.st b { display: block; font-size: 9.3px; color: #D0021B; margin-bottom: 2px }
.st.h { border-top-color: #D0021B; background: #FEF2F2 }
.reel { display: flex; align-items: center; gap: 6px; margin-bottom: 7px }
.card { flex: 1; background: #0B0B0F; color: #fff; text-align: center; border-radius: 4px; padding: 10px 5px; font-size: 10.5px; font-weight: 700; line-height: 1.2 }
.card small { display: block; color: #94A3B8; font-weight: 400; font-size: 8.6px; margin-top: 3px }
.card.f { background: #D0021B }
.card.f small { color: #FECACA }
.arr { color: #94A3B8; font-size: 12px }
.tl { display: grid; grid-template-columns: repeat(7, 1fr); gap: 4px }
.tl div { border-left: 3px solid #CBD5E1; padding: 2px 0 2px 6px; font-size: 9.4px; line-height: 1.25 }
.tl b { display: block; font-size: 10px }
.tl .x { border-left-color: #D0021B }
footer { margin-top: auto; padding-top: 9px; border-top: 1px solid #E2E8F0; display: flex; justify-content: space-between; color: #64748B; font-size: 8.8px }
"""

HTML = f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Propuesta Black Friday 2026</title><style>{CSS}</style></head><body>

<section class="page">
  <div class="hero">
    <div><div class="k">PROPUESTA PARA GERENCIA · BLACK FRIDAY 2026</div><h1>A LA UNA, A LAS DOS, DE CONTADO...</h1>
    <div class="s">Hyundai en Dai Motors · Chery en Dai Motors · Kaiyi en Yantai Motors</div></div>
    <div class="r"><b>Viernes 27 de noviembre</b>Solo contado · Actualizado 12 nov 2026</div>
  </div>
  <p class="lead">Diez unidades contadas, con descuento sobre el precio final, solo el viernes 27 y de contado. <em>Cada unidad es del primer cliente que la pague. Medios: {money(MEDIOS)}.</em></p>
  <div class="kpis">
    <div class="kpi"><b>10</b><span>unidades aprobadas en las tres cuentas</span></div>
    <div class="kpi"><b>{money(MEDIOS)}</b><span>medios: ads {money(ADS_T)} + bulk {money(BULK_T)}</span></div>
    <div class="kpi d"><b>{money(PEDIDO)}</b><span>presupuesto adicional a aprobar</span></div>  </div>

  <h2><i>1</i>Por qué unidades contadas y no toda la lista</h2>
  <ul>
    <li>Solo bajan las unidades aprobadas; el resto del inventario mantiene su precio.</li>
    <li>La escasez es verdadera: cada cuenta dice cuántas hay y muestra cuántas quedan.</li>
    <li>El costo del descuento se conoce antes de arrancar.</li>
  </ul>

  <h2><i>2</i>Unidades aprobadas</h2>
  <div class="kpis">{units}</div>
  <p class="note">Ventas confirma versión, color y placa de cada una y las bloquea en CRM antes del vie 13.</p>

  <h2><i>3</i>Decisiones pendientes</h2>
  <table><tr><th style="width:24px">#</th><th>Decisión</th><th>Recomendación</th></tr>{rows([
    ["1", "<b>Descuento por modelo</b>", "Un monto sobre el precio final para Accent, Creta, Tiggo 4, Himla y X3 Pro"],
    ["2", f"<b>Presupuesto adicional de {money(PEDIDO)}</b>", "Aprobar $100 de ads para Yantai y $100 de bulk WhatsApp"],
    ["3", "<b>Regla de asignación</b>", "Cada unidad, para el primer cliente que la pague de contado"],
    ["4", "<b>Medios de pago aceptados</b>", "Definirlos antes del vie 13: van en el carrusel del vie 20"],
    ["5", "<b>Si se agotan</b>", "Obsequios o descuentos en otra unidad, de contado, el mismo viernes"],
  ])}</table>
  {foot(1)}
</section>

<section class="page">
  <div class="top"><b>La oferta y cómo funciona</b><span>Black Friday 2026</span></div>

  <h2><i>4</i>Descuento, obsequios o ambos</h2>
  <table><tr><th>Opción</th><th>A favor</th><th>En contra</th></tr>
  <tr><td><b>A.</b> Descuento en las unidades aprobadas</td><td>Número claro para el gancho y la pauta</td><td>Costo directo en margen</td></tr>
  <tr><td><b>B.</b> Obsequios en las unidades aprobadas</td><td>Protege el precio; valor percibido mayor al costo</td><td>Gancho débil: "obsequio" no detiene el scroll</td></tr>
  <tr class="rec"><td><b>C. Descuento en las aprobadas + obsequios o descuentos en otras si se agotan · recomendada</b></td><td>Las unidades atraen; el plan B captura a quien llegue tarde</td><td>Hay que definir el paquete y su costo</td></tr></table>
  <p class="note">Las unidades se venden una sola vez: sin plan B, los demás leads de contado se pierden.</p>

  <h2><i>5</i>Mecánica</h2>
  <div class="steps">
    <div class="st"><b>Desde 17 nov</b>Cliente comenta o escribe BLACK y entra a la lista en Kommo</div>
    <div class="st"><b>17 al 26 nov</b>Asesor confirma que puede comprar de contado</div>
    <div class="st"><b>Lun 23</b>Se revelan las unidades, sin el precio. Bases publicadas</div>
    <div class="st"><b>Jue 26 · 7 am</b>La lista recibe los precios por WhatsApp: 24 h para preparar el pago</div>
    <div class="st"><b>Vie 27 · 8 am</b>Precios públicos en las 3 cuentas</div>
    <div class="st h"><b>Cada unidad</b>Para el primer cliente que la pague de contado; contador público de las que quedan</div>
    <div class="st"><b>Si se agotan</b>Obsequios o descuentos en otra unidad, de contado</div>
  </div>
  <p class="note">El mié 2 dic cada cuenta publica el reel de sus entregas. Sorteo descartado: exige validación legal y no garantiza un comprador calificado.</p>

  <h2><i>6</i>Referencia creativa: un hilo propio por cuenta</h2>
  <div class="reel">
    <div class="card">Algo grande viene<small>arranca la expectativa · 17 nov</small></div><span class="arr">›</span>
    <div class="card">Son 4 · Son 2<small>se dice cuántas hay</small></div><span class="arr">›</span>
    <div class="card">Precio a la lista<small>jue 26 · 7 am</small></div><span class="arr">›</span>
    <div class="card f">Quedan 4... 3... 2...<small>contador honesto · vie 27</small></div>
  </div>
  <table><tr><th>Cuenta</th><th>Hilo</th><th>Cierre</th></tr>{rows([
    ["<b>@daimotorsmcbo</b><br>2 Accent + 2 Creta", "Humor zuliano: Alexis, el asesor con el cartel en la espalda que nunca sabe qué dice. El viernes el cartel cuenta: QUEDAN 4", "Hyundai en Dai Motors"],
    ["<b>@cherymaracaibo</b><br>2 Tiggo 4 + 2 Himla", "Emotivo, sin broma: cuatro historias que todavía no empiezan, dos de familia y dos de trabajo", "Chery en Dai Motors"],
    ["<b>@yantaimotors</b><br>2 Kaiyi X3 Pro", "Directo, nadie en cámara: los números escritos con marcador en el vidrio. El primero es el 2", "Kaiyi en Yantai Motors"],
  ])}</table>
  <p class="note">Formato de carteles tomado de un Reel de @sephorauk de 15 segundos, grabado con celular: costo de producción cero. Guiones completos, día por día, en los PDF de guiones de cada cuenta.</p>
  {foot(2)}
</section>

<section class="page">
  <div class="top"><b>Presupuesto, metas y calendario</b><span>Black Friday 2026</span></div>

  <h2><i>7</i>Presupuesto de medios</h2>
  <table><tr><th>Línea</th><th>Hyundai</th><th>Chery</th><th>Yantai</th><th>Total</th><th>Estado</th></tr>{budget}
  <tr class="t"><td><b>Total</b></td>{total_marca}<td><b>{money(MEDIOS)}</b></td><td><b>Se piden {money(PEDIDO)}</b></td></tr></table>

  <div class="two">
    <div>
      <h2><i>8</i>Pauta por fase</h2>
      <table><tr><th>Fase</th><th>Fechas</th><th>Hyu.</th><th>Che.</th><th>Yan.</th></tr>{fases}</table>
      <h2><i>9</i>Metas propuestas</h2>
      <table><tr><th>Indicador</th><th>Hyu.</th><th>Che.</th><th>Yan.</th></tr>{rows([
        ["Unidades vendidas", "4 de 4", "4 de 4", "2 de 2"],
        ["Leads lun 23 a vie 27", "33<small>normal 20</small>", "71<small>normal 61</small>", "Por definir<small>sin línea base</small>"],
      ])}</table>
    </div>
    <div>
      <h2><i>10</i>Criterio de gasto</h2>
      <ul>
        <li><b>Hyundai recibe más que Chery:</b> la mediana de Reel de Chery fue 9 veces mayor (9.238 vs 1.036).</li>
        <li><b>Objetivo de pauta: mensajes.</b> Las visitas al perfil no miden conversación.</li>
        <li><b>Yantai en dos partes:</b> $40 en expectativa; los $60 de revelación y viernes solo si esos $40 generan conversaciones (se evalúa el dom 22). Su costo por 1.000 alcanzados es el más alto ($1,81 vs $1,17 y $0,75) y sus interacciones cayeron 73% en octubre.</li>
        <li><b>Bulk:</b> 500 a 2.000 entregas, a $0,05 a $0,20 cada una (estimado, sin cotizar).</li>
        <li><b>Primero la base caliente:</b> 169 leads recientes, incluidos 52 sin cotizar. Yantai usa su propia base.</li>
      </ul>
    </div>
  </div>

  <h2><i>11</i>Riesgos</h2>
  <table><tr><th>Riesgo</th><th>Mitigación</th></tr>{rows([
    ["Clientes recientes reclaman por el descuento", "Solo bajan las unidades aprobadas; el resto del inventario mantiene su precio"],
    ["Las unidades se van en minutos", "Obsequios o descuentos en otras unidades para quien llegue tarde"],
    ["Dos clientes pagan la misma unidad a la vez", 'Regla de pago escrita y publicada antes: qué cuenta como "pagó primero"'],
    ["El precio se filtra el jueves", "La venta abre solo el vie 27; la ventaja de la lista es preparar el pago"],
    ["Una unidad se vende antes del 27", "Bloquearlas en CRM antes del vie 13"],
    ["Contado reduce el público: 84% de los clientes cotizados recientemente incluyó financiamiento", "La lista filtra contado desde el 17 nov; el bulk prioriza clientes de contado"],
  ])}</table>

  <h2><i>12</i>Cronograma</h2>
  <div class="tl">
    <div class="x"><b>Jue 12 nov</b>Unidades aprobadas</div>
    <div><b>Vie 13</b>Descuentos, medios de pago, placas y bulk</div>
    <div><b>Lun 16</b>Grabación</div>
    <div><b>17 al 22</b>Expectativa</div>
    <div><b>23 al 26</b>Revelación de las unidades</div>
    <div class="x"><b>Vie 27</b>Black Friday, solo contado</div>
    <div><b>Lun 30 · Mié 2 dic</b>Cierre y entregas</div>
  </div>
  {foot(3)}
</section>
</body></html>"""

os.makedirs(OUT_DIR, exist_ok=True)
with open(OUT_HTML, "w", encoding="utf-8") as f:
    f.write(HTML)

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                f"--print-to-pdf={OUT_PDF}", OUT_HTML], check=True)
print(OUT_PDF)
