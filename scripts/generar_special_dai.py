#!/usr/bin/env python3
"""Genera los HTML del evento SPECIAL DAI (Plan 1 Hyundai, Plan 2 Chery)
y los imprime a PDF con Chrome headless (mismo motor del diagnóstico original).

Salida:
  entregables/special-dai-hyundai.html + .pdf
  entregables/special-dai-chery.html + .pdf
"""
import subprocess, os, sys

CSS = """
  @page { size: Letter; margin: 0; }
  * { box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  html, body { background: #fff; color: #111; font-family: "IBM Plex Sans", "Segoe UI", system-ui, sans-serif; }
  .page { width: 8.5in; height: 11in; padding: 0.45in 0.55in 0.4in; position: relative; page-break-after: always; display: flex; flex-direction: column; }
  .page:last-child { page-break-after: auto; }
  .kicker { font-size: 8px; letter-spacing: .22em; text-transform: uppercase; color: #6b6b6b; display: flex; justify-content: space-between; }
  .kicker .brand { font-weight: 600; color: #111; }
  h1 { font-size: 26px; line-height: 1.12; font-weight: 600; letter-spacing: -0.5px; margin: 14px 0 6px; }
  .subtitle { font-size: 10px; color: #444; line-height: 1.45; max-width: 95%; }
  .section-label { font-size: 7.5px; letter-spacing: .2em; text-transform: uppercase; color: #8a8a8a; margin: 12px 0 6px; }
  .rule { height: 1px; background: #e2e2e2; margin: 4px 0 10px; }
  .kpis { display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; margin-top: 10px; }
  .kpi .num { font-size: 26px; font-weight: 600; letter-spacing: -1px; line-height: 1; }
  .kpi .cap { font-size: 8.5px; color: #555; margin-top: 4px; line-height: 1.3; }
  .kpi .delta { font-size: 8.5px; color: ACCENT; font-weight: 600; margin-top: 2px; }
  .accent { color: ACCENT; }
  table { width: 100%; border-collapse: collapse; font-size: 8.6px; }
  th { text-align: left; font-size: 7.3px; letter-spacing: .12em; text-transform: uppercase; color: #8a8a8a; font-weight: 500; padding: 4px 0; border-bottom: 1px solid #111; }
  td { padding: 4.5px 0; border-bottom: 1px solid #ececec; vertical-align: top; line-height: 1.32; }
  td.n, th.n { text-align: right; }
  .big { font-size: 15px; font-weight: 600; }
  .two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 22px; }
  .bar-row { display: flex; align-items: center; gap: 8px; font-size: 8.5px; margin-bottom: 4px; }
  .bar-row .lbl { flex: 0 0 52px; }
  .bar-row .pct { flex: 0 0 42px; text-align: right; }
  .bar { flex: 1 1 auto; height: 7px; background: #ededed; }
  .bar > span { display: block; height: 100%; background: ACCENT; }
  .read { font-size: 9px; color: #333; line-height: 1.45; margin-top: 7px; }
  .foda { display: grid; grid-template-columns: 1fr; gap: 0; }
  .note { font-size: 8px; color: #777; margin-top: 5px; }
  .box { border: 1.5px dashed #c9c9c9; padding: 9px 11px; font-size: 8.8px; color: #555; line-height: 1.45; }
  .taged { background: #f4f4f4; border-left: 3px solid ACCENT; padding: 7px 10px; font-size: 8.8px; line-height: 1.45; color: #222; }
  .tagbig { font-size: 8.8px; color: ACCENT; font-weight: 600; }
  .sources { font-size: 6.8px; color: #9a9a9a; line-height: 1.4; margin-top: auto; padding-top: 8px; }
  .footer { position: absolute; right: 0.55in; bottom: 0.26in; font-size: 7px; letter-spacing: .16em; text-transform: uppercase; color: #b0b0b0; }
  .strike { position: relative; color: #9a9a9a; }
  .strike::after { content: ""; position: absolute; left: -2px; right: -2px; top: 55%; height: 2px; background: ACCENT; transform: rotate(-6deg); }
"""

HEAD = """<!DOCTYPE html>
<html lang="es"><head><meta charset="utf-8">
<title>{titulo}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{css}</style></head><body>"""

def kpi(num, cap, delta=None):
    d = f'<div class="delta">{delta}</div>' if delta else ""
    return f'<div class="kpi"><div class="num">{num}</div><div class="cap">{cap}</div>{d}</div>'

def tabla(headers, rows, widths=None):
    th = "".join(f'<th{" class=&quot;n&quot;" if False else ""}' )
    return None

def table_html(headers, rows):
    h = "".join(f"<th>{x}</th>" for x in headers)
    body = "".join(
        "<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows
    )
    return f'<table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table>'

def page(b, n, content):
    css = CSS.replace("ACCENT", b["acento"])
    return (f'<section class="page"><div class="kicker"><span class="brand">{b["kicker"]}</span>'
            f'<span>SPECIAL DAI · {n}/4</span></div>{content}'
            f'<p class="sources">{b["fuentes_p"][n]}</p>'
            f'<div class="footer">{b["footer"]}</div></section>')

# ============================================================ PÁGINAS
def p1(b):
    k = b["k1"]
    c = f'''
  <h1>{b["t1a"]}<br>{b["t1b"]}</h1>
  <p class="subtitle">SPECIAL DAI · {b["plan"]} · evento de ventas 2–7 de noviembre de 2026 · Presentación a Gerencia y Marketing · Datos al 22 de octubre de 2026. <i>Documento gemelo: {b["gemelo"]}.</i></p>
  <div class="section-label">LA CUENTA HOY · 22 DE OCTUBRE DE 2026</div>
  <div class="kpis">{"".join(kpi(*x) for x in k)}</div>
  <p class="read"><b>Lectura:</b> {b["lectura1"]}</p>
  <div class="section-label">BENCHMARK INTERNO DEL GRUPO · NO SON COMPETIDORES</div><div class="rule"></div>
  {table_html(["", b["nombre"], "La otra cuenta del grupo"], b["bench"])}
  <p class="note">Ambas cuentas son de Dai Motors (mismo RIF J-30355833-0). Se comparan para asignar la pauta, no para competir.</p>
  <div class="section-label">QUÉ VENDE Y QUÉ NO EN LOS ÚLTIMOS 20 REELS</div><div class="rule"></div>
  <div class="two-col">
    <div><div class="read" style="font-weight:600;margin:0 0 6px">Funciona: {b["func_clave"]}</div>{table_html(["Reel", "Vistas", "MG", "C"], b["ganadoras"])}</div>
    <div><div class="read" style="font-weight:600;margin:0 0 6px">No funciona: {b["nofunc_clave"]}</div>{table_html(["Reel", "Vistas", "MG", "C"], b["perdedoras"])}</div>
  </div>
  <p class="read"><b>{b["frase_reels"]}</b></p>
  <div class="section-label">A QUIÉN LE HABLAMOS</div><div class="rule"></div>
  {b["audiencia"]}
  '''
    return page(b, 1, c)

def p2(b):
    c = f'''
  <h1 style="margin-top:10px">{b["t2"]}</h1>
  <div class="section-label">EL MERCADO EN CIFRAS · CIERRE DE SEPTIEMBRE 2026</div><div class="rule"></div>
  <div class="kpis">{kpi("43.470", "vehículos nuevos colocados ene–sep 2026: ya superó los 38.610 de TODO el 2025")}{kpi("50.000", "meta anual de Cavenez para 2026")}{kpi("14.893", "unidades JAC ene–ago: el líder absoluto del país")}{kpi("1.246", "unidades Hyundai a nivel nacional ene–ago", "lo local decide")}</div>
  <p class="read"><b>Lectura:</b> en 9 meses el país ya va 13% por encima de TODO 2025. {b["lectura2"]}</p>
  <div class="section-label">LO QUE HAY EN PISO PARA EL EVENTO · CRM AUTOWEB · INVENTARIO VALORADO DAI MOTORS S.A. · 22 OCT</div><div class="rule"></div>
  {table_html(["Modelo", "Físico disponible", "Días promedio", "Rango"], b["inv"])}
  <p class="note">{b["transito"]}</p>
  <div class="section-label">EL PROBLEMA QUE EL EVENTO RESUELVE</div><div class="rule"></div>
  <div class="two-col">{b["problema"]}</div>
  <p class="read"><b>{b["frase_inv"]}</b></p>
  '''
    return page(b, 2, c)

def p3(b):
    c = f'''
  <h1 style="margin-top:10px">Un evento. Dos marcas en el mismo piso. Todo simultáneo por diseño.</h1>
  <div class="taged"><b>SPECIAL DAI</b> — <span class="strike">DAYS</span> <b>DAI.</b> Del lunes 2 al sábado 7 de noviembre, showroom Bella Vista: {b["concepto"]} El <b>Pase Special Dai</b> es la llave de acceso preferente (unidad asegurada, financiamiento en sala, salta la fila). <b>Domingo 8 NO es viable:</b> tráfico familiar, piso muerto en Maracaibo. El evento muere el sábado a la tarde — y los precios mueren con él.</div>
  <div class="section-label">PRECAMPAÑA · 22 OCT – 1 NOV · "SE VIENE ALGO QUE NO HICIMOS NUNCA"</div><div class="rule"></div>
  {table_html(["Fecha", "Pieza", "Idea central"], b["pre"])}
  <p class="note">Cada pieza lleva WhatsApp con palabra clave y objetivo Meta = mensajes a WhatsApp. Domingo 1: solo stories (es el peor día de la semana: 4.101 vistas promedio en 41 días medidos).</p>
  <div class="section-label">SEMANA DEL EVENTO · 2–7 NOV · DIARIO, 10–11 AM, GRABADO EN VIVO</div><div class="rule"></div>
  {table_html(["Día", "Pieza", "Idea central"], b["evento"])}
  <p class="read">Stories diarias: entregas, bancos firmando, colas, montaje. <b>Mié 4: media day con microinfluencers</b> (un día para las dos marcas, lives en ambas cuentas, recorrido por las dos zonas).</p>
  <div class="section-label">POST-EVENTO · 9–11 NOV</div><div class="rule"></div>
  <p class="read" style="margin-top:0">{b["post"]}</p>
  '''
    return page(b, 3, c)

def p4(b):
    c = f'''
  <h1 style="margin-top:10px">{b["t4"]}</h1>
  <div class="two-col" style="margin-top:8px">
    <div>
      <div class="section-label" style="margin-top:0">PRESUPUESTO TOTAL DEL EVENTO · $3.500 {b["nombre_corto"]}</div><div class="rule"></div>
      {table_html(["Línea", "Monto", "%", "Detalle"], b["pauta"])}
      <p class="note">Costos compartidos divididos 50/50 (catering+bebidas, papelería, regalos, montaje). <b>APARTE del presupuesto por marca:</b> Alfredo Comedia $750 + redes $300 (Hyundai) · Susy Calderón $400 + redes $300 (Chery) · Siempre Maracaibo > $300 · pantallas > $400/día · alianza bancaria (pendiente).</p>
      <p class="note">Bulk WhatsApp: ~$0,05–0,20 por entregado (LatAm, desde julio 2025 se cobra por entregado, no por conversación). Con la línea de bulk de cada marca caben ~2.400–10.000 entregas — 2 toques por cliente: invitación T-7 y recordatorio T-1. Plantilla aprobada por Meta + opt-in. Base exacta: reporte de clientes de Kommo. Cotizar con 2 proveedores antes del 25 oct.</p>
      <div class="section-label">GRILLA «KILOMÉTRO CERO» VIGENTE</div><div class="rule"></div>
      {table_html(["Período", "Qué pasa"], b["grilla"])}
    </div>
    <div>
      <div class="section-label" style="margin-top:0">CÓMO LO VAMOS A MEDIR</div><div class="rule"></div>
      {table_html(["KPI", "Hoy (real)", "Meta evento", "Dueño"], b["medicion"])}
      <div class="box" style="margin-top:8px"><b>Reglas de publicación:</b> {b["reglas"]}</div>
    </div>
  </div>
  <div class="section-label">ACCIONES A SEGUIR</div><div class="rule"></div>
  {table_html(["#", "Acción", "Responsable", "Fecha"], b["acciones"])}
  <p class="note">{b["pendientes"]}</p>
  '''
    return page(b, 4, c)

# ============================================================ DATOS HYUNDAI
HY = {
    "acento": "#0032C0",
    "kicker": "DAI MOTORS · HYUNDAI MARACAIBO",
    "footer": "Dai Motors · Hyundai Maracaibo",
    "plan": "Plan 1 de 2",
    "gemelo": "Plan 2 — Chery Maracaibo (@cherymaracaibo)",
    "nombre": "Hyundai (@daimotorsmcbo)",
    "nombre_corto": "HYUNDAI",
    "t1a": "Octubre se tropezó a mitad de camino.",
    "t1b": "El evento del 2 al 7 es el rescate programado.",
    "k1": [
        ("9.830", "seguidores · la mayor de la plaza Hyundai (Instagram público, 22 oct)", "+22 netos desde 30 sep"),
        ("1.036", "vistas del Reel típico actual (mediana, 20 Reels Apify)"),
        ("193.218", "vistas del mejor Reel: «Lo natural también se mueve» (10K Nature, 29 sep)"),
        ("$1,03M", "inventario Hyundai en piso: 39 unidades a valor (CRM, 22 oct)"),
    ],
    "lectura1": "la audiencia existe (9.830) pero octubre no convirtió: 115 vistas el Reel del 21 de octubre. La respuesta no es publicar más — es cambiar el formato de venta: evento con fecha, cita y plazo cerrado.",
    "bench": [
        ["Seguidores", "<b>9.830</b>", "13.000 (@cherymaracaibo)"],
        ["Reel típico (mediana)", "<b>1.036</b>", "9.238 — 9× el nuestro"],
        ["Mejor Reel del período", "<b>193.218</b>", "372.988"],
        ["Ritmo de Reels", "<b>2,1/semana</b>", "1,1/semana"],
        ["Unidades físicas para el evento", "<b>39</b>", "35"],
    ],
    "func_clave": "persona en cámara + producto",
    "ganadoras": [
        ["«Lo natural también se mueve» (10K Nature)", "<b>193.218</b>", "289", "6"],
        ["«¿Solo 20 segundos para enamorarte del Accent?»", "<b>58.622</b>", "427", "<b>208</b>"],
        ["«Hay metas que se sienten el doble» (entrega)", "32.848", "248", "5"],
    ],
    "nofunc_clave": "emoción sin producto, piezas de archivo",
    "perdedoras": [
        ["«¿Listo para conocerla?» (Creta, 21 oct)", "<b>115</b>", "2", "0"],
        ["«El compañero fiel de mil historias»", "225", "8", "0"],
        ["#TBT Día del Comunicador", "472", "29", "3"],
    ],
    "frase_reels": "El Accent con asesor en cámara sacó 58.622 vistas y 208 comentarios. El TBT del mismo mes sacó 472. La diferencia es el formato, no la suerte.",
    "audiencia": '''<div class="two-col"><div>
      <div class="bar-row"><span class="lbl">35–44</span><div class="bar"><span style="width:70%"></span></div><span class="pct">35,0%</span></div>
      <div class="bar-row"><span class="lbl">45–54</span><div class="bar"><span style="width:50%"></span></div><span class="pct">25,0%</span></div>
      <div class="bar-row"><span class="lbl">25–34</span><div class="bar"><span style="width:41%"></span></div><span class="pct">20,5%</span></div>
      <div class="bar-row"><span class="lbl">55–64</span><div class="bar"><span style="width:22%"></span></div><span class="pct">11,1%</span></div>
      <div class="bar-row"><span class="lbl">18–24</span><div class="bar"><span style="width:8%"></span></div><span class="pct">4,0%</span></div>
      <div class="bar-row"><span class="lbl">65+</span><div class="bar"><span style="width:9%"></span></div><span class="pct">4,4%</span></div>
      <p class="read" style="margin-top:6px">61,2% hombres.</p></div>
      <div><p class="read" style="margin:0">Maracaibo <b>48,4%</b> · San Francisco <b>11,4%</b> · Cabimas 3,9% · Caracas 2,7% · C. Ojeda 2,4%. Venezuela 87,1% — Zulia ≈ 69%.</p>
      <p class="read"><b>Lectura:</b> hablamos con familias que deciden la compra del carro familiar — el 70% del mercado responde al crédito (Bera: «90% Provincial» = 73.020 vistas, la pieza más vista del país en septiembre).</p></div></div>''',
    "t2": "El mercado lleva 43.470 autos en 9 meses. Nosotros tenemos 39 Hyundai en piso.",
    "lectura2": "Hyundai mueve poco a nivel nacional: Maracaibo es la plaza donde la marca puede competir — y el evento es la palanca local.",
    "inv": [
        ["<b>Grand i10</b> (GL / GLS / MT GL / Sedán GLS)", "<b>15</b>", "30", "2–111"],
        ["<b>Accent</b> 1.5L A/T GLS", "<b>9</b>", "78", "72–<b>190</b>"],
        ["<b>Tucson</b> 2.0L AT 2WD GLS", "<b>9</b>", "40", "8–94"],
        ["<b>Creta</b> 1.5L A/T GLS", "<b>6</b>", "27", "2–56"],
        ["<b>Karry Truck</b> (industrial)", "1", "78", "78"],
        ["<b>TOTAL HYUNDAI</b>", "<b>39</b>", "", "<b>$1.026.675</b>"],
    ],
    "transito": "En tránsito (sin fecha garantizada para el evento): 44 Hyundai + 48 Chery + 2 Karry en planta, más 2 Karry en exhibición — según las bandas del propio reporte. El evento se juega con lo que ya está aquí.",
    "problema": '''<div><ul style="list-style:none">
      <li style="font-size:8.8px;line-height:1.45;margin-bottom:7px;padding-left:11px;position:relative"><span style="position:absolute;left:0;top:6px;width:4px;height:4px;background:#0032C0"></span><b>Tucson: 9 unidades, 2 vendidas en 61 días.</b> Sin empuje puntual quedan hasta enero. El evento es el empuje.</li>
      <li style="font-size:8.8px;line-height:1.45;margin-bottom:7px;padding-left:11px;position:relative"><span style="position:absolute;left:0;top:6px;width:4px;height:4px;background:#0032C0"></span><b>Accent AO712OA: 190 días en piso</b> — su gemelo AO784WA tiene 156. La pieza del 27 oct los nombra; la mesa financiera del evento es el cierre.</li>
      <li style="font-size:8.8px;line-height:1.45;margin-bottom:7px;padding-left:11px;position:relative"><span style="position:absolute;left:0;top:6px;width:4px;height:4px;background:#0032C0"></span><b>Materia prima fresca: 32 de 39 unidades tienen menos de 60 días</b> (15 menos de 30). Solo 4 pasan de 90. El evento no vende chatarra.</li>
    </ul></div>
    <div><div class="box"><b>La semana del 2 al 7, por bloque de piso:</b><br>
    Lun 2 — apertura, todo el piso · Mar 3 — i10 (15) · Mié 4 — Tucson + Creta + test drive · Jue 5 — Accent (las blancas viejas, nombradas) · Vie 6 — últimas unidades del CRM · Sáb 7 — cierre.</div></div>''',
    "frase_inv": "39 unidades reales y $1,03 millones en piso. La semana del evento es la única con mecanismo probado para moverlas juntas.",
    "concepto": "los 39 Hyundai en zona tech corporativa y la mesa financiera en sala.",
    "pre": [
        ["<b>Mié 22</b>", "<b>Reel</b>", "Anuncio: «Del 2 al 7 de noviembre, Dai Motors hace algo que nunca hizo». Sin modelos, sin precio. Misterio + registro (piezas gemelas con la cuenta Chery, cortes distintos)"],
        ["<b>Jue 23</b>", "Carrusel 2 img", "<b>El Pase Special Dai</b>: qué da acceso (unidad asegurada, financiamiento en sala, salta la fila) y cómo conseguirlo"],
        ["Sáb 24", "Stories", "Countdown del evento"],
        ["<b>Lun 26</b>", "Carrusel 2 img", "<b>Grand i10 desde $21.000</b> + «asegúralo en el evento» — el único precio publicable de la plaza"],
        ["<b>Mar 27</b>", "<b>Reel</b>", "<b>20 segundos</b> — asesor Hyundai en cámara: qué va a pasar del 2 al 7 (el formato de las 58.622 vistas)"],
        ["Mié 28", "Reel corto", "El flujo real: click → WhatsApp <code>VIP</code> → asesor asigna tu hora"],
        ["<b>Jue 29</b>", "<b>Reel</b>", "<b>Kilómetro Cero</b> — entrega real con contador: «Esto pasa todos los días. Del 2 al 7, pasa más rápido»"],
        ["<b>Vie 30</b>", "Carrusel 2 img", "<b>Tucson: las 9 en el piso</b> — «La semana del 2 al 7 se mueven». El modelo más estancado se convierte en protagonista"],
        ["Sáb 31", "Stories + Reel", "«Mañana abre. El piso ya está» — grabación del montaje de la zona Hyundai"],
        ["Dom 1", "Stories", "Sin publicación fuerte — domingo no es viable ni para el evento ni para el contenido"],
    ],
    "evento": [
        ["<b>Lun 2</b>", "<b>Reel apertura</b>", "«Abrió. Todo el piso de Hyundai en un solo lugar» — colas reales, alfombra roja, mesa financiera lista"],
        ["<b>Mar 3</b> (mejor día: 7.486 vistas prom.)", "<b>Reel</b>", "Bloque i10: las 15 del piso + cuota calculada por DM"],
        ["<b>Mié 4</b>", "<b>Reel</b>", "<b>Test drive libre + banco aprobando en 15 minutos</b> — cliente real firmando (con permiso)"],
        ["<b>Jue 5</b>", "<b>Reel</b>", "<b>Kilómetro Cero en el evento</b>: entregas del día con contador de unidades"],
        ["<b>Vie 6</b>", "<b>Reel</b>", "«Quedan X» — número del CRM al cierre del jueves. Escasez real, no inventada"],
        ["<b>Sáb 7</b>", "<b>Reel cierre</b>", "«Último día. Los precios mueren hoy a las 5 pm» + relance a la lista VIP de no-asistidos"],
    ],
    "post": "<b>Lun 9:</b> «Lo que quedó» — inventario real por modelo. · <b>Relance Kommo</b> a todo lead que asistió sin comprar: cuota calculada del modelo que pidió. · <b>Mié 11:</b> se retoma la grilla «Kilómetro Cero» (13 oct–30 nov) con stock actualizado y chats con origen.",
    "t4": "$3.500 y 17 días de vuelo para cerrar la brecha 2,28× que el diagnóstico ya calculó.",
    "pauta": [
        ["<b>Catering + bebidas</b> (50%)", "<b>$1.200</b>", "34%", "$350/día × 6 días + $300 hielo/vasos/café (estación de café) = $2.400, mitad por marca"],
        ["<b>Montaje</b> (50%)", "<b>$780</b>", "22%", "4 banderines × $70 + inflables, alfombra roja (50%), LED zona Hyundai"],
        ["<b>Bulk WhatsApp</b>", "<b>$477</b>", "14%", "2 toques a la base de Kommo: invitación T-7 + recordatorio T-1. ~$0,05–0,20 por entregado"],
        ["<b>Tabloides glase</b>", "<b>$273</b>", "8%", "39 unidades × $7 = QR + precio por vehículo, una por auto"],
        ["Papelería (50%)", "$200", "6%", "$400 totales: Pases Special Dai, fichas, formularios"],
        ["Regalos (50%)", "$200", "6%", "$400 totales: bienvenida VIP + regalo de entrega"],
        ["Promotora", "$120", "3%", "1 por marca × 6 días (~$20/día tentativo)"],
        ["Pauta Meta", "$200", "6%", "mínimo vital: solo retargeting sobre interacción"],
        ["Contingencia", "$50", "1%", "reserva operativa"],
        ["<b>TOTAL</b>", "<b>$3.500</b>", "100%", ""],
    ],
    "grilla": [
        ["22 oct – 1 nov", "La grilla vigente se integra al funnel del evento (i10, Accent, Tucson, Kilómetro Cero)"],
        ["2 – 7 nov", "La grilla se suspende: la semana entera es el evento"],
        ["9 nov +", "Se retoma con stock actualizado y con data del evento"],
    ],
    "medicion": [
        ["Chats con palabra clave", "0", "100% con origen", "Ventas"],
        ["Pases Special Dai", "—", "meta por base Kommo (24 oct)", "Marketing"],
        ["Ventas en el evento", "3,9/sem (34 uds en 61 días ago–sep)", "<b>12 en el evento</b> (≈2,5× ritmo)", "Gerencia"],
        ["Reels del período", "2,1/sem", "<b>16 en 17 días</b> (9 pre + 7 evento)", "Marketing"],
        ["Reel típico (mediana)", "1.036", "≥ 3.000", "Marketing"],
        ["Tucson vendidas", "2 en 61 días", "≥ 3 en el evento", "Gerencia"],
    ],
    "reglas": "las cuotas en dólares se publican solo después de confirmarlas con cada entidad financiera. El precio del Grand i10 ($21.000) solo se comunica mientras haya unidades reales del modelo.",
    "acciones": [
        ["1", "Logo SPECIAL DAI (DAYS tachado → DAI) + arquitectura de zona Hyundai", "Marketing", "23 oct"],
        ["2", "Landing de registro + integración Kommo + automático de WhatsApp", "Marketing", "23 oct"],
        ["3", "Confirmar mesa financiera y cuotas publicables por entidad", "Ventas", "24 oct"],
        ["4", "Confirmar plan físico del showroom (inflables, alfombra, banderines, LED). Pantallas solo con aprobación de costo externo", "Operaciones", "24 oct"],
        ["5", "Confirmar y agendar Alfredo Comedia ($750, externo) — 3 historias + 1 Reel", "Marketing", "24 oct"],
        ["6", "Cotizar bulk WhatsApp (2 proveedores) y activar pauta $200 (retargeting)", "Marketing", "25 oct"],
        ["7", "Montar showroom completo", "Operaciones", "1 nov"],
        ["8", "Briefing diario 8:30 am de precampaña y evento", "Gerencia + Ventas", "diaria"],
        ["9", "Tablero de cierre: resultados reales vs. metas", "Gerencia", "9 nov"],
    ],
    "pendientes": "Metas propuestas desde ritmos reales medidos — la decisión final es de Gerencia.",
    "fuentes_p": {
        1: "Fuentes: Instagram público @daimotorsmcbo (22 oct 2026) · Apify/instagram-reel-scraper (20 Reels, 22 oct) · Meta Business Suite via diagnóstico 13 oct 2026.",
        2: "Fuentes: Cavenez via DFSK Venezuela y Motum Magazine (oct 2026) · CRM autoweb, Inventario Valorado Dai Motors S.A. (22 oct 2026) · diagnóstico 13 oct 2026.",
        3: "Fuente: grilla «Kilómetro Cero» 13 oct 2026 · rendimiento por día (Meta Business Suite, 286 días) · Apify (22 oct).",
        4: "Fuentes: CRM y Apify del 22 oct 2026 · diagnóstico 13 oct 2026 · Cavenez (oct 2026). Metas propuestas desde ritmos reales — corte final por Gerencia.",
    },
}

# ============================================================ DATOS CHERY
CH = {
    "acento": "#D0021B",
    "kicker": "DAI MOTORS · CHERY MARACAIBO",
    "footer": "Dai Motors · Chery Maracaibo",
    "plan": "Plan 2 de 2",
    "gemelo": "Plan 1 — Hyundai Maracaibo (@daimotorsmcbo)",
    "nombre": "Chery (@cherymaracaibo)",
    "nombre_corto": "CHERY",
    "t1a": "La cuenta Chery vuela en alcance y frena en el ritmo.",
    "t1b": "El evento convierte alcance en contratos firmados.",
    "k1": [
        ("13.000", "seguidores · primera medición real de la cuenta (Instagram, 22 oct)"),
        ("9.238", "vistas del Reel típico (mediana, 20 Reels Apify)", "9× la mediana de Hyundai"),
        ("372.988", "vistas del mejor Reel: «Lo único difícil va a ser elegir el color» (Arrizo, 25 sep) · 10.366 comentarios"),
        ("$824.830", "inventario Chery en piso: 35 unidades a valor (CRM, 22 oct)"),
    ],
    "lectura1": "cuando la cuenta muestra producto con persona y opción concreta, desprende alcance — 10.366 comentarios en un Reel son intención de compra, no casualidad. Pero publica 1,1 Reels/semana: el volumen no acompaña la fórmula. El evento la obliga a publicar en serie con la misma fórmula y destino claro (cita).",
    "bench": [
        ["Seguidores", "<b>13.000</b>", "9.830 (@daimotorsmcbo)"],
        ["Reel típico (mediana)", "<b>9.238</b>", "1.036"],
        ["Mejor Reel del período", "<b>372.988</b>", "193.218"],
        ["Ritmo de Reels", "<b>1,1/semana</b>", "2,1/semana"],
        ["Unidades físicas para el evento", "<b>35</b>", "39"],
    ],
    "func_clave": "producto con decisión concreta (color, versión, sonido)",
    "ganadoras": [
        ["«Lo único difícil va a ser elegir el color…» (Arrizo 5 Pro, 25 sep)", "<b>372.988</b>", "5.709", "<b>10.366</b>"],
        ["«¡Lujo y tecnología al alcance de tus manos!» (Arrizo, 14 sep)", "<b>117.795</b>", "1.268", "2.360"],
        ["«¿Ya conoces todo lo que la Tiggo 2 Pro Max tiene…?» (16 jul)", "<b>81.173</b>", "411", "845"],
    ],
    "nofunc_clave": "taller y cotidianidad",
    "perdedoras": [
        ["«Un día en nuestro taller de servicio» (20 oct)", "<b>306</b>", "5", "0"],
        ["Entregas inolvidables (16 oct)", "1.463", "38", "1"],
        ["«Asiento trasero desordenado» (28 sep)", "2.088", "7", "0"],
    ],
    "frase_reels": "La cuenta ya pregunta «Escribe ARRIZO / TEAM / DECRETO / FAMILIA» al 0414-6582009. Special Dai no cambia esa costumbre: la centraliza en un canal medible (Kommo).",
    "audiencia": '<div class="box">Pendiente: audiencia por edad, sexo y ciudad de @cherymaracaibo — requiere login de Meta Business Suite (se marca en «Pendientes»). La geografía base (Maracaibo + Zulia) es la misma del showroom; los cortes exactos se cargan al confirmar el acceso.</div>',
    "t2": "Chery no aparece en el top de marcas del país. El piso de Maracaibo puede cambiar esa conversación.",
    "lectura2": "JAC demostró que una marca china puede dominar el mercado con volumen. Chery compite por ese espacio: su cuenta local ya lidera el alcance del grupo Dai — sin sistema comercial detrás. El evento es ese sistema.",
    "inv": [
        ["<b>Tiggo 2 Pro Max</b> 1.5L AT", "<b>10</b>", "40", "20–74"],
        ["<b>Tiggo 4 Pro Max</b>", "<b>9</b>", "101", "20–<b>360</b>"],
        ["<b>Arrizo 5 Pro</b> (10 AT + 2 MT)", "<b>12</b>", "43", "23–78"],
        ["<b>Pickup Chery Himla D/C</b> 2.4L MT (2027)", "<b>3</b>", "32", "27–36"],
        ["<b>Tiggo 9</b>", "<b>1</b>", "78", "78"],
        ["<b>TOTAL CHERY</b>", "<b>35</b>", "", "<b>$824.830</b>"],
    ],
    "transito": "En tránsito (sin fecha garantizada para el evento): 48 Chery — 19 Arrizo, 11 Tiggo 2, 5 Tiggo 4, 4 Tiggo 7 Pro Max 2027, 2 Tiggo 8, 1 Tiggo 9, 6 Himla. También 44 Hyundai y 2 Karry (ver Plan 1). El evento se juega con las 35 que ya están aquí.",
    "problema": '''<div><ul style="list-style:none">
      <li style="font-size:8.8px;line-height:1.45;margin-bottom:7px;padding-left:11px;position:relative"><span style="position:absolute;left:0;top:6px;width:4px;height:4px;background:#D0021B"></span><b>Tiggo 4 Pro Max: 9 unidades, 101 días promedio, la más vieja con 360 días</b> (negra, placa AO767HA). El modelo más pedido y el más estancado — la contradicción que solo un evento con fecha resuelve.</li>
      <li style="font-size:8.8px;line-height:1.45;margin-bottom:7px;padding-left:11px;position:relative"><span style="position:absolute;left:0;top:6px;width:4px;height:4px;background:#D0021B"></span><b>Arrizo 5 Pro: 12 unidades</b> y su Reel hizo 372.988 vistas con 10.366 comentarios. Demanda comprobada, sin cierre.</li>
      <li style="font-size:8.8px;line-height:1.45;margin-bottom:7px;padding-left:11px;position:relative"><span style="position:absolute;left:0;top:6px;width:4px;height:4px;background:#D0021B"></span><b>La pickup Chery (Himla): 3 unidades de 32 días.</b> Producto nuevo del piso: el evento es su estreno público con test drive. <b>Tiggo 9: 1 unidad</b> — "única unidad" con fecha.</li>
    </ul></div>
    <div><div class="box"><b>La semana del 2 al 7, por bloque de piso:</b><br>
    Lun 2 — apertura, las 35 Chery · Mar 3 — Tiggo 2 + Tiggo 4 (19 SUV) · Mié 4 — test drive de la pickup · Jue 5 — Arrizo: los 6 colores · Vie 6 — últimas del CRM · Sáb 7 — cierre.</div></div>''',
    "frase_inv": "35 unidades reales y $824.830 en piso, con 24 de 35 frescas (menos de 60 días). La urgencia es verdadera: lo del evento es lo que existe hoy.",
    "concepto": "los 35 Chery en zona roja y blanca (LED temático, música ambiente, escritorio minimalista).",
    "pre": [
        ["<b>Mié 22</b>", "<b>Reel</b>", "Anuncio: «Del 2 al 7 de noviembre, algo que Dai Motors nunca hizo». Sin modelos, sin precio. Misterio + registro (piezas gemelas con la cuenta Hyundai, cortes distintos)"],
        ["<b>Jue 23</b>", "Carrusel 2 img", "<b>El Pase Special Dai</b>: qué da acceso (unidad asegurada, financiamiento en sala, salta la fila) y cómo conseguirlo"],
        ["Sáb 24", "Stories", "Countdown del evento"],
        ["<b>Lun 26</b>", "Carrusel 2 img", "<b>Arrizo 5 Pro: los 6 colores, el mismo precio</b> — el formato del Reel de 372.988 vistas, ahora con fecha en la mano"],
        ["<b>Mar 27</b>", "<b>Reel</b>", "<b>20 segundos</b> — asesor Chery en cámara: qué va a pasar del 2 al 7"],
        ["Mié 28", "Reel corto", "El flujo real: click → WhatsApp <code>VIP</code> → tu hora asignada con asesor"],
        ["<b>Jue 29</b>", "<b>Reel</b>", "<b>La pickup Chery en el piso</b> — 3 unidades: «la pickup ya está aquí, y ahora le pusimos fecha»"],
        ["<b>Vie 30</b>", "Carrusel 2 img", "<b>Tiggo 4 Pro Max: la unidad con 360 días</b> — nombrada y visible, con las 9 del grupo. «Alguien la está esperando»"],
        ["Sáb 31", "Stories + Reel", "«Mañana abre. La zona roja ya está» — grabación del montaje"],
        ["Dom 1", "Stories", "Sin publicación fuerte — domingo no es viable ni para el evento ni para el contenido"],
    ],
    "evento": [
        ["<b>Lun 2</b>", "<b>Reel apertura</b>", "«Abrió. La zona roja de Dai Motors se encendió» — colas reales, las 35 Chery juntas"],
        ["<b>Mar 3</b> (mejor día de la semana)", "<b>Reel</b>", "Bloque Tiggo 2 + Tiggo 4: las 19 SUV pequeñas juntas + cuota calculada por DM"],
        ["<b>Mié 4</b>", "<b>Reel</b>", "<b>Test drive de la pickup en el evento</b> + banco aprobando en 15 min — media day con microinfluencers (lives en ambas cuentas)"],
        ["<b>Jue 5</b>", "<b>Reel</b>", "<b>Arrizo: los 6 colores en el evento</b> — el formato ganador (372.988) con urgencia de fecha"],
        ["<b>Vie 6</b>", "<b>Reel</b>", "«Quedan X» — número del CRM al cierre del jueves. Escasez real, no inventada"],
        ["<b>Sáb 7</b>", "<b>Reel cierre</b>", "«Último día. Los precios mueren hoy a las 5 pm» + relance a la lista VIP de no-asistidos"],
    ],
    "post": "<b>Lun 9:</b> «Lo que quedó» — inventario real por modelo. · <b>Relance Kommo</b> a todo lead sin venta: cuota calculada del modelo que pidió. · <b>Mié 11:</b> la cuenta no puede volver a 1,1 Reels/semana — la semana de cadencia diaria demostró funcionar y el nuevo piso es 4/semana.",
    "t4": "$3.500 y 17 días de vuelo. Primera vez que Chery vende con sistema.",
    "pauta": [
        ["<b>Catering + bebidas</b> (50%)", "<b>$1.200</b>", "34%", "$350/día × 6 días + $300 hielo/vasos/café (estación de café) = $2.400, mitad por marca"],
        ["<b>Montaje</b> (50%)", "<b>$780</b>", "22%", "4 banderines × $70 + inflables, alfombra roja (50%), LED rojo/blanco zona Chery"],
        ["<b>Bulk WhatsApp</b>", "<b>$505</b>", "14%", "2 toques a la base de Kommo: invitación T-7 + recordatorio T-1. ~$0,05–0,20 por entregado"],
        ["<b>Tabloides glase</b>", "<b>$245</b>", "7%", "35 unidades × $7 = QR + precio por vehículo, una por auto"],
        ["Papelería (50%)", "$200", "6%", "$400 totales: Pases Special Dai, fichas, formularios"],
        ["Regalos (50%)", "$200", "6%", "$400 totales: bienvenida VIP + regalo de entrega"],
        ["Promotora", "$120", "3%", "1 por marca × 6 días (~$20/día tentativo)"],
        ["Pauta Meta", "$200", "6%", "mínimo vital: solo retargeting sobre interacción"],
        ["Contingencia", "$50", "1%", "reserva operativa"],
        ["<b>TOTAL</b>", "<b>$3.500</b>", "100%", ""],
    ],
    "grilla": [
        ["22 oct – 1 nov", "La cuenta publica 9 piezas de precampaña — su mayor cadencia del año"],
        ["2 – 7 nov", "Una pieza diaria en vivo desde el evento"],
        ["9 nov +", "Piso de 4 Reels/semana: la cadencia no baja después de demostrar que funciona"],
    ],
    "medicion": [
        ["Chats con palabra clave", "sin registro", "100% con origen", "Ventas"],
        ["Pases Special Dai", "—", "meta por base Kommo (24 oct)", "Marketing"],
        ["Ventas en el evento", "sin línea base (requiere Gerencia)", "<b>10 en el evento</b> — propuesta", "Gerencia"],
        ["Reels del período", "1,1/sem", "<b>16 en 17 días</b> (9 pre + 7 evento)", "Marketing"],
        ["Reel típico (mediana)", "9.238", "mantener ≥ 9.000", "Marketing"],
        ["Tiggo 4 Pro Max vendidas", "ritmo no medido", "≥ 3 (incluye la de 360 días)", "Gerencia"],
    ],
    "reglas": "las cuotas en dólares se publican solo después de confirmarlas con cada entidad financiera. La pickup (Himla D/C) y el Tiggo 9 se comunican como «unidades limitadas», sin precio publicado.",
    "acciones": [
        ["1", "Logo SPECIAL DAI (DAYS tachado → DAI) + arquitectura de la zona Chery (rojo/blanco, LED)", "Marketing", "23 oct"],
        ["2", "Landing de registro + integración Kommo + automático de WhatsApp", "Marketing", "23 oct"],
        ["3", "Sincronizar mesa financiera (misma del Plan 1) con modelos Chery", "Ventas", "24 oct"],
        ["4", "Confirmar plan físico de la zona Chery", "Operaciones", "24 oct"],
        ["5", "Confirmar y agendar Susy Calderón ($400, externo) — campaña full", "Marketing", "24 oct"],
        ["6", "Cotizar bulk WhatsApp (2 proveedores) y activar pauta $200 (retargeting)", "Marketing", "25 oct"],
        ["7", "Montar la zona Chery completa", "Operaciones", "1 nov"],
        ["8", "Briefing diario 8:30 am (compartido con Hyundai)", "Gerencia + Ventas", "diaria"],
        ["9", "Tablero de cierre: resultados reales vs. metas", "Gerencia", "9 nov"],
    ],
    "pendientes": "<b>Pendientes:</b> (1) audiencia Chery por edad/ciudad — requiere login de Meta; (2) línea base de ventas Chery últimos 60 días — requiere Gerencia; (3) TikTok Chery — no extraído aún. Sin esos datos la meta de unidades es propuesta, no cálculo de ritmo.",
    "fuentes_p": {
        1: "Fuentes: Instagram público @cherymaracaibo (22 oct 2026) · Apify/instagram-reel-scraper (20 Reels, 22 oct) · contexto de marca 2026 (context/cherymaracaibo.md).",
        2: "Fuentes: Cavenez via DFSK Venezuela y Motum Magazine (oct 2026) · CRM autoweb, Inventario Valorado Dai Motors S.A. (22 oct 2026) · Apify (22 oct).",
        3: "Fuente: fórmula de contenido medida (Reels top, 22 oct) · operación compartida del Plan 1.",
        4: "Fuentes: CRM y Apify del 22 oct 2026 · Cavenez (oct 2026) · contexto de marca. Metas propuestas — corte final por Gerencia.",
    },
}

# ============================================================ BUILD
def build_html(b, fname):
    css = CSS.replace("ACCENT", b["acento"])
    html = (HEAD.format(titulo=f"SPECIAL DAI · {b['nombre']}", css=css)
            + p1(b) + p2(b) + p3(b) + p4(b) + "</body></html>")
    path = os.path.join("entregables", fname)
    os.makedirs("entregables", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML:", path)
    return os.path.abspath(path)

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
    for b, f, pdf in ((HY, "special-dai-hyundai.html", "entregables/Noviembre-daimotorsmcbo-special-dai-plan1.pdf"),
                      (CH, "special-dai-chery.html", "entregables/Noviembre-cherymaracaibo-special-dai-plan2.pdf")):
        html = build_html(b, f)
        render(html, pdf)
