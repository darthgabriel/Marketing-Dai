// Presentación Black Friday 2026 para Gerencia - 3 diapositivas.
// Salida: black-friday-2026/entregables/Presentacion-Gerencia-BF2026.pptx
// Uso: node black-friday-2026/scripts/generar_presentacion.cjs
const path = require("path");
const pptxgen = require("pptxgenjs");
const { applyTheme } = require(process.env.PPTX_SKILL_DIR + "/scripts/apply_theme.js");

const OUT = path.join(__dirname, "..", "entregables", "Presentacion-Gerencia-BF2026.pptx");

const THEME = {
  name: "Black Friday 2026",
  headFontFace: "Arial",
  bodyFontFace: "Calibri",
  colors: {
    dk1: "111111", lt1: "FFFFFF", dk2: "262626", lt2: "F2F2F2",
    accent1: "F5B700", accent2: "002C5F", accent3: "8A1C2B", accent4: "4B5563",
    accent5: "9CA3AF", accent6: "16A34A", hlink: "002C5F", folHlink: "8A1C2B",
  },
};

(async () => {
  const pres = new pptxgen();
  pres.layout = "LAYOUT_WIDE"; // 13.33 x 7.5
  pres.title = "A la una, a las dos, de contado... · Black Friday 2026";
  pres.author = "Ing. Jose Paredes · Jefe IT y Marketing";
  pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
  const C = pres.SchemeColor;

  const footer = (dark) => [
    { text: { text: "Black Friday 2026 · Dai Motors · Yantai Motors · Uso interno de Gerencia",
      options: { x: 0.6, y: 7.0, w: 9, h: 0.3, fontSize: 10, color: dark ? C.accent5 : C.accent4, margin: 0 } } },
  ];
  const titlePh = (dark) => ({
    placeholder: {
      options: { name: "title", type: "title", x: 0.6, y: 0.75, w: 12.1, h: 1.0, fontSize: 34, bold: true, align: "left",
        color: dark ? C.background1 : C.text1, valign: "top", margin: 0, fontFace: THEME.headFontFace },
      text: "",
    },
  });
  const slideNum = (dark) => ({ x: 12.2, y: 7.0, w: 0.5, h: 0.3, fontSize: 10, color: dark ? C.accent5 : C.accent4, align: "right" });

  pres.defineSlideMaster({ title: "OSCURO", background: { color: THEME.colors.dk1 },
    objects: [titlePh(true), ...footer(true)], slideNumber: slideNum(true) });
  pres.defineSlideMaster({ title: "CLARO", background: { color: THEME.colors.lt1 },
    objects: [titlePh(false), ...footer(false)], slideNumber: slideNum(false) });

  const kicker = (s, text, dark) => s.addText(text, { x: 0.6, y: 0.4, w: 9, h: 0.3, fontSize: 13, bold: true,
    color: dark ? C.accent1 : C.accent4, charSpacing: 2, margin: 0, isTextBox: true, objectName: "Etiqueta" });

  // ---------- 1. Qué perseguimos ----------
  pres.addSection({ title: "Objetivos" });
  const s1 = pres.addSlide({ masterName: "OSCURO", sectionTitle: "Objetivos" });
  kicker(s1, "BLACK FRIDAY 2026 · VIERNES 27 DE NOVIEMBRE", true);
  s1.addText("A la una, a las dos, de contado...", { placeholder: "title" });
  s1.addText("Lo que perseguimos: vender, sumar clientes de contado y cuidar el precio del resto del inventario", { x: 0.6, y: 1.45, w: 12.1, h: 0.4, fontSize: 18,
    color: C.accent5, margin: 0, isTextBox: true, objectName: "Subtítulo objetivos" });

  const objs = [
    ["10", "unidades vendidas", "2 Accent y 2 Creta, 2 Tiggo 4 y 2 Himla, 2 Kaiyi X3 Pro. Cada una, al primero que la pague."],
    ["100%", "ventas de contado", "Todo lo que se venda el viernes entra de contado: caja inmediata, sin depender de aprobación bancaria."],
    ["BLACK", "lista propia de contado", "Clientes con pago verificado en Kommo. Base lista para diciembre."],
    ["0", "cambios en la lista de precios", "Solo bajan las unidades aprobadas. El resto del inventario mantiene su precio."],
  ];
  objs.forEach(([big, lab, t], i) => {
    const x = 0.6 + i * 3.08;
    s1.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y: 2.05, w: 2.85, h: 3.0, rectRadius: 0.12, fill: { color: C.text2 },
      line: { type: "none" }, objectName: `Objetivo ${i + 1}` });
    s1.addText(big, { x: x + 0.25, y: 2.25, w: 2.4, h: 0.85, fontSize: 44, bold: true, color: C.accent1, margin: 0,
      fontFace: THEME.headFontFace, isTextBox: true, objectName: `Cifra ${i + 1}` });
    s1.addText([
      { text: lab, options: { bold: true, fontSize: 16, color: C.background1, breakLine: true } },
      { text: t, options: { fontSize: 13, color: C.accent5 } },
    ], { x: x + 0.25, y: 3.15, w: 2.4, h: 1.75, valign: "top", margin: 0, paraSpaceAfter: 4, isTextBox: true,
      objectName: `Texto objetivo ${i + 1}` });
  });
  s1.addText("357$", { x: 0.6, y: 5.45, w: 2.2, h: 0.85, fontSize: 48, bold: true, color: C.background1, margin: 0,
    fontFace: THEME.headFontFace, isTextBox: true, objectName: "Medios" });
  s1.addText([
    { text: "Presupuesto de medios", options: { bold: true, fontSize: 16, color: C.background1, breakLine: true } },
    { text: "Pauta en Meta y WhatsApp masivo para las tres marcas. El costo del descuento se conoce antes de arrancar.", options: { fontSize: 13, color: C.accent5 } },
  ], { x: 2.9, y: 5.5, w: 9.8, h: 0.85, valign: "top", margin: 0, isTextBox: true, objectName: "Medios detalle" });
  s1.addNotes(
    "Este Black Friday persigue cuatro cosas.\n" +
    "1. Vender las diez unidades aprobadas: 2 Accent y 2 Creta, 2 Tiggo 4 y 2 Himla, 2 Kaiyi X3 Pro.\n" +
    "2. Que todo lo vendido ese viernes sea de contado: caja inmediata, sin depender de aprobación bancaria.\n" +
    "3. Construir una lista propia de clientes de contado (BLACK) que nos sirve para diciembre.\n" +
    "4. Hacerlo sin tocar la lista de precios: solo bajan las unidades aprobadas.\n" +
    "Presupuesto de medios: 357$."
  );

  // ---------- 2. Alineación ----------
  pres.addSection({ title: "Alineación" });
  const s2 = pres.addSlide({ masterName: "CLARO", sectionTitle: "Alineación" });
  kicker(s2, "POR QUÉ LA ESTRATEGIA ESTÁ ALINEADA", false);
  s2.addText("Lo que gana el cliente es lo que gana la empresa", { placeholder: "title" });

  const hdr = (t, fill, col) => ({ text: t, options: { bold: true, fontSize: 14, color: col, fill: { color: fill } } });
  const cell = (t, o = {}) => ({ text: t, options: { fontSize: 13, color: C.text1, ...o } });
  const rows = [
    [hdr("El cliente quiere", THEME.colors.dk1, C.background1), hdr("La campaña le da", THEME.colors.accent1, C.text1), hdr("La empresa gana", THEME.colors.dk1, C.background1)],
    [cell("Un descuento que pueda creer", { bold: true }), cell("Descuento real en unidades contadas, sin \"50%\" de mentira"), cell("Credibilidad, sin bajar el precio del resto del inventario")],
    [cell("Reglas claras", { bold: true }), cell("Bases publicadas: unidades contadas, solo contado, cada una al primero que pague"), cell("Asignación transparente y menos reclamos")],
    [cell("Tiempo para prepararse", { bold: true }), cell("Lista BLACK: recibe el precio 24 horas antes"), cell("Una base propia de clientes de contado")],
    [cell("No quedarse con las manos vacías", { bold: true }), cell("Obsequios o descuentos en otra unidad si se agotan las de Black Friday"), cell("Más ventas de contado ese viernes, no solo diez")],
    [cell("Contenido que entretenga, no publicidad", { bold: true }), cell("Un hilo por cuenta: humor, historia y números"), cell("Alcance con formatos que ya funcionan en el nicho")],
  ];
  s2.addTable(rows, { x: 0.6, y: 1.95, w: 12.1, colW: [3.4, 4.6, 4.1], rowH: [0.5, 0.72, 0.72, 0.72, 0.72, 0.72],
    border: { type: "solid", pt: 1, color: "E5E7EB" }, valign: "middle", margin: [4, 10, 4, 10], fontFace: THEME.bodyFontFace,
    objectName: "Tabla alineación" });
  s2.addText("Evidencia: en Instagram, los sketches y las cuentas regresivas de concesionarios (Venezuela y EE. UU.) superaron entre 4 y 63 veces la mediana de sus propias cuentas.",
    { x: 0.6, y: 6.45, w: 12.1, h: 0.35, fontSize: 12, italic: true, color: C.accent4, margin: 0, isTextBox: true, objectName: "Evidencia" });
  s2.addNotes(
    "La estrategia funciona porque cada cosa que le damos al cliente es también un beneficio para la empresa.\n" +
    "El público desconfía de los Black Friday de carros: por eso un descuento real en unidades contadas es más creíble que un 50%.\n" +
    "Las reglas claras evitan reclamos. La lista BLACK le da al cliente 24 horas para preparar el pago y a nosotros una base de contado.\n" +
    "Si se agotan, quien llegue tarde recibe obsequios o descuentos en otra unidad de contado: así el viernes vende más de diez.\n" +
    "El contenido se basa en lo que ya funciona en el nicho: sketches de concesionario y cuentas regresivas."
  );

  // ---------- 3. Ejecución y decisiones ----------
  pres.addSection({ title: "Decisiones" });
  const s3 = pres.addSlide({ masterName: "OSCURO", sectionTitle: "Decisiones" });
  kicker(s3, "CÓMO LO EJECUTAMOS · PENDIENTE ANTES DEL VIERNES 13", true);
  s3.addText("Cinco definiciones para arrancar el martes 17", { placeholder: "title" });

  const steps = [
    ["17 NOV", "Comenta BLACK"], ["23 NOV", "Se revelan las unidades"], ["26 NOV · 7 AM", "Precio a la lista"],
    ["27 NOV · 8 AM", "Precio público y venta"], ["2 DIC", "Reel de las entregas"],
  ];
  const stepW = 2.42;
  s3.addShape(pres.shapes.LINE, { x: 0.6 + stepW / 2, y: 2.15, w: stepW * 4, h: 0, line: { color: C.accent4, width: 2 },
    objectName: "Línea de tiempo" });
  steps.forEach(([d, h], i) => {
    const cx = 0.6 + i * stepW + stepW / 2;
    s3.addShape(pres.shapes.OVAL, { x: cx - 0.2, y: 1.95, w: 0.4, h: 0.4, fill: { color: (i === 2 || i === 3) ? C.accent1 : C.accent5 },
      line: { color: C.text1, width: 3 }, objectName: `Hito ${i + 1}` });
    s3.addText([
      { text: d, options: { bold: true, fontSize: 12, color: C.accent1, breakLine: true } },
      { text: h, options: { fontSize: 14, color: C.background1 } },
    ], { x: cx - stepW / 2 + 0.05, y: 2.5, w: stepW - 0.1, h: 0.7, align: "center", valign: "top", margin: 0,
      isTextBox: true, objectName: `Texto hito ${i + 1}` });
  });

  const dec = [
    ["Descuento sobre el precio final", "Un monto por modelo"],
    ["$200 adicionales", "$100 pauta Yantai + $100 WhatsApp masivo"],
    ["Regla", "Cada unidad, al primero que la pague de contado"],
    ["Medios de pago", "Para las piezas del viernes 20"],
    ["Si se agotan", "Obsequios o descuentos en otra unidad"],
  ];
  dec.forEach(([h, t], i) => {
    const y = 3.6 + i * 0.62;
    s3.addText(String(i + 1), { shape: pres.shapes.OVAL, x: 0.6, y, w: 0.42, h: 0.42, fill: { color: C.accent1 },
      color: C.text1, fontSize: 15, bold: true, align: "center", valign: "middle", margin: 0, objectName: `Decisión número ${i + 1}` });
    s3.addText([
      { text: h + "  ", options: { bold: true, fontSize: 15, color: C.background1 } },
      { text: t, options: { fontSize: 14, color: C.accent5 } },
    ], { x: 1.2, y: y - 0.02, w: 6.2, h: 0.46, valign: "middle", margin: 0, isTextBox: true, objectName: `Decisión ${i + 1}` });
  });

  s3.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: 7.8, y: 3.55, w: 4.9, h: 3.05, rectRadius: 0.12, fill: { color: C.text2 },
    line: { type: "none" }, objectName: "Panel presupuesto" });
  s3.addText([
    { text: "$157", options: { bold: true, fontSize: 28, color: C.background1 } },
    { text: " disponibles + ", options: { fontSize: 14, color: C.accent5 } },
    { text: "$200", options: { bold: true, fontSize: 28, color: C.accent1 } },
    { text: " por aprobar", options: { fontSize: 14, color: C.accent5 } },
  ], { x: 8.05, y: 3.75, w: 4.5, h: 0.6, margin: 0, isTextBox: true, objectName: "Presupuesto" });
  s3.addText([
    { text: "Total de medios: $357", options: { bold: true, fontSize: 15, color: C.background1, breakLine: true } },
    { text: "Hyundai $120 · Chery $107 · Yantai $130", options: { fontSize: 13, color: C.accent5, breakLine: true } },
    { text: " ", options: { fontSize: 8, breakLine: true } },
    { text: "Riesgo principal", options: { bold: true, fontSize: 15, color: C.accent1, breakLine: true } },
    { text: "El 84% de los clientes cotizados recientemente pidió financiamiento. La lista BLACK filtra contado desde el día 17.", options: { fontSize: 13, color: C.accent5 } },
  ], { x: 8.05, y: 4.45, w: 4.5, h: 2.0, valign: "top", margin: 0, isTextBox: true, objectName: "Total y riesgo" });
  s3.addNotes(
    "Así se ejecuta: el 17 abre la lista BLACK, el 23 se revelan las unidades, el 26 a las 7 am la lista recibe los precios, el 27 a las 8 am se publican y se vende, y el 2 dic mostramos las entregas.\n" +
    "Las unidades ya están aprobadas: 10 en total. Para arrancar el martes 17 faltan cinco definiciones antes del viernes 13:\n" +
    "1. Descuento sobre el precio final, un monto por modelo, solo en las unidades aprobadas. 2. $200 adicionales: $100 de pauta para Yantai ($40 y $60 solo si funciona) y $100 de WhatsApp masivo. 3. Cada unidad es del primero que la pague de contado. 4. Medios de pago aceptados. 5. Si se agotan, obsequios o descuentos en otra unidad.\n" +
    "Riesgo: el 84% de los clientes cotizados recientemente pidió financiamiento. Lo mitigamos filtrando contado en la lista desde el 17."
  );

  await pres.writeFile({ fileName: OUT });
  await applyTheme(OUT, THEME);
  console.log(OUT);
})();
