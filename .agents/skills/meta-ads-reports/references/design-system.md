# Design System — "Editorial Deportivo de Lujo"

Sistema visual para informes de Meta Ads con estética premium automotive / business journalism. Inspirado en reportes anuales de Robb Report, Bloomberg Businessweek, y anuales de car magazines.

## NO usar

- Dashboards estilo SaaS (DataDog, Mixpanel, etc.)
- Glassmorphism, neumorfismo, gradientes morados
- Emojis en el reporte
- Iconografía densa (solo cuando aporta)
- Purple-on-white, blue-on-white, gradients genéricos
- Tipografías: Inter, Roboto, Arial, Space Grotesk (regla de oro del proyecto)

## Paleta cromática

Sistema de 9 tokens. Disciplina: **un solo acento cromático** (amber), todo lo demás es escala de gris cálido + un oxblood para warning.

```css
:root {
  /* Backgrounds (oscuros) */
  --ink:        #0E0D0B;  /* fondo principal, casi negro cálido */
  --ink-2:      #161412;  /* surface, ligeramente más claro */
  --ink-3:      #1F1C18;  /* bar track, hover */

  /* Hairlines */
  --hair:       #2A2622;  /* separadores principales */
  --hair-soft:  #1F1B17;  /* separadores secundarios */

  /* Foreground (claros) */
  --paper:      #EDE6D6;  /* texto principal, crema cálido */
  --paper-soft: #C9C2B0;  /* texto secundario */
  --mute:       #8C8675;  /* labels, captions */
  --mute-2:     #5C5749;  /* metadata, sub-labels */

  /* Acentos cromáticos (usar con disciplina) */
  --amber:      #C8954A;  /* ACCENT PRINCIPAL — números hero, highlights */
  --amber-soft: #8A6630;  /* gradiente stop para bars */
  --oxblood:    #B8472D;  /* solo para warning/loss */
  --sage:       #8FA876;  /* solo para success/positive */
}
```

### Reglas de uso

- **Amber**: máx 3-4 elementos por página. Si abunda, pierde jerarquía.
- **Sage**: solo `pill good`, `delta-up`, "éxito" callouts.
- **Oxblood**: solo `pill bad`, `delta-down`, errores, descontinuados.
- **Nunca** amber + sage juntos en un mismo componente (compiten).
- **Nunca** fondo `--paper` con texto `--ink` (invierte el sistema, rompe la jerarquía).

## Tipografía

Tres familias con roles estrictos. Cargadas vía Google Fonts CDN.

```css
--serif: 'Fraunces', 'Times New Roman', serif;
--sans:  'Manrope', system-ui, sans-serif;
--mono:  'JetBrains Mono', 'Courier New', monospace;
```

### Roles

| Familia | Uso | Tamaños comunes |
|---------|-----|-----------------|
| **Fraunces** | Display, títulos, citas, números hero | 14-56pt |
| **Manrope** | Cuerpo de párrafo, labels medianos | 8-10pt |
| **JetBrains Mono** | Datos tabulares, eyebrows, metadata, KPI units | 6.5-8pt |

### Fraunces en particular

Fraunces es variable con `opsz` (optical size) y `SOFT` (softness). Configurarla con `font-variation-settings`:

```css
/* Display (títulos grandes) */
font-variation-settings: "opsz" 144, "SOFT" 30;

/* Italic para acentos (la palabra clave del título) */
font-style: italic;
font-variation-settings: "opsz" 144, "SOFT" 60;
```

## Escala tipográfica

```
12pt → captions
14pt → subtítulos
22pt → títulos de sección
56pt → título portada (display)
```

Números hero (KPI cards): **26pt serif**. No más grande (domina la página).

## Componentes base

### KPI Card

```html
<div class="kpi">
  <div class="lbl">Visitas al perfil</div>
  <div class="val">13.833</div>
  <div class="sub">CTR visita 2.00%</div>
</div>
```

Layout: 4 cards en grid horizontal, separados por `border-right: 1px solid var(--hair)`. El label arriba en mono caps, el valor en serif 26pt, el sub-label en mono.

### Bar Chart (custom, sin libs)

```html
<div class="bar-row">
  <div class="lbl">YANTAI</div>
  <div class="bar-track">
    <div class="bar-fill" style="width: 100%;"></div>
  </div>
  <div class="val">335.327</div>
</div>
```

Grid: `22mm 1fr 22mm` (label / track / value). Fill con `linear-gradient(90deg, var(--amber-soft), var(--amber))`. Track con `--ink-2` + border `--hair-soft`. Alt fill para comparación: gradiente a `--mute`.

### Scatter Plot (SVG hand-crafted)

```html
<svg class="scatter-svg" viewBox="0 0 320 220" preserveAspectRatio="xMidYMid meet">
  <!-- grid lines, axis labels, then <circle> per ad with leader line + <text> label -->
</svg>
```

Importante: el eje Y NO debe empezar en 0 si los valores están concentrados (ej: CPL de $0.015 a $0.055). Usar escala con offset para que la variación sea visible.

### Pill (status badges)

```html
<span class="pill good">COMPLETADO</span>
<span class="pill warn">SUB-ESCALA</span>
<span class="pill bad">INACTIVO</span>
```

Border 1px del color semitransparente. Texto uppercase mono 6.5pt. Padding mínimo.

### Callout (insight boxed)

```html
<div class="callout">
  <div class="ct">Conclusión operativa</div>
  <p>...</p>
</div>
```

`border-left: 2px solid var(--amber)` + `background: linear-gradient(90deg, rgba(amber,0.04), transparent)`. Texto en serif italic.

## Espaciado

Sistema de 4mm / 5mm / 6mm / 8mm. Nunca usar valores arbitrarios.

```
4mm  → gap entre elementos hermanos
5mm  → padding interno de cards
6mm  → margin entre secciones
8mm  → margin entre sub-secciones
22mm → margin de página (header/footer)
20mm → padding lateral de página
```

## Páginas

- **A4 (210mm × 297mm)**
- Padding página: `22mm 20mm 20mm 20mm` (top, right, bottom, left)
- `page-break-after: always` en cada `<section class="page">`
- Top bar fija: nombre del informe + sección
- Footer: número de página en mono, brand centrado

## Background y textura

NO fondo sólido plano. Agregar profundidad con:

```css
.page {
  background:
    radial-gradient(ellipse at 20% 10%, rgba(200,149,74,0.04), transparent 50%),
    radial-gradient(ellipse at 90% 90%, rgba(184,71,45,0.03), transparent 50%),
    var(--ink);
}

.page::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image:
    repeating-linear-gradient(0deg, transparent 0, transparent 2px,
      rgba(237,230,214,0.008) 2px, rgba(237,230,214,0.008) 3px);
  pointer-events: none;
  opacity: 0.5;
}
```

El `::before` agrega una micro-textura tipo papel impreso, invisible pero perceptible al imprimir.

## Lo que diferencia este estilo de un dashboard genérico

1. **Sin íconos UI** (no hay "📊" ni "💡" ni "🚀")
2. **Números hero** en serif, no en sans
3. **Datos en mono** con `font-variant-numeric: tabular-nums`
4. **Tablas con hairline borders** (1px), no card-shadows
5. **Texto secundario en `--paper-soft`**, no en gris medio
6. **Una sola columna de charts** cuando son importantes, no grid 2×2
7. **Sección número** (`§ 01`) en mono, no bullet point
8. **Sección eyebrow** descriptivo en mono caps con letter-spacing
9. **Sin "Lorem ipsum"** ni placeholders visuales
10. **Citas en serif italic** — el único lugar donde se permite prosa larga

## Anti-patterns a evitar

```css
/* ❌ NUNCA */
background: linear-gradient(135deg, #667eea, #764ba2);
font-family: 'Inter', sans-serif;
box-shadow: 0 10px 30px rgba(0,0,0,0.3);
border-radius: 16px;

/* ✅ SIEMPRE */
background: var(--ink);
font-family: 'Fraunces', serif;
border: 1px solid var(--hair);
border-radius: 0;
```
