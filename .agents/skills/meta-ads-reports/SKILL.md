---
name: meta-ads-reports
description: Use cuando el usuario pida analizar datos de campañas de Meta Ads (Facebook/Instagram), generar un informe ejecutivo en PDF para gerencia, o producir visualizaciones de performance publicitario (CPM, CPL, CTR, alcance, gasto). Activa también con frases como "informe de marketing", "reporte de campaña", "análisis de ads", "performance publicitario", "Meta Ads report", "Facebook Ads report", "anuncios de Facebook", "pauta digital" o cuando haya CSVs exportados de Meta Ads Manager en el directorio. Entrega: PDF A4 editorial premium con gráficos SVG hand-crafted, lenguaje técnico de media buying, y recomendaciones accionables para el próximo periodo. Aplica a cuentas B2C/B2B con optimización a cualquier evento (profile_visit, lead, purchase, etc.).
---

# Meta Ads Report Generator

Genera informes ejecutivos en PDF a partir de los CSV exportados de Meta Ads Manager. El skill está diseñado para que un agente produzca, en una sola sesión, un reporte A4 con estética editorial premium listo para presentar a gerencia.

## Cuándo usar este skill

- Hay CSVs de Meta Ads Manager en `sources/` o ruta similar (`*Anuncios*.csv` + `*Conjuntos*.csv`).
- El usuario pide "informe", "reporte", "análisis", "presentación a gerencia", "resultados de campaña".
- Hay un rango temporal definido (mes, quincena, periodo custom).
- El destinatario es alguien que NO maneja Ads Manager: necesita insights, no dashboards.

**No usar este skill si:**
- El usuario quiere un dashboard interactivo (usar herramienta de BI).
- Solo hay 1-2 anuncios o 1 día de datos (no hay patrón para analizar).
- El objetivo es presentar live, no imprimir/PDF.

## Inputs esperados

Dos CSVs de Meta Ads Manager exportados en español (encoding UTF-8 con BOM opcional):

1. **`*Anuncios*.csv`** — granularidad por anuncio (creative)
2. **`*Conjuntos*.csv`** — granularidad por ad set (campaña)

Ver schema completo en `references/csv-schema.md`. Si los archivos están en otro encoding o tienen headers distintos, normalizar primero.

## Outputs

- **PDF A4** en `resultados/` (o ruta indicada)
- **HTML fuente** editable para ajustes de último minuto
- **5 páginas por defecto**, expandible a 7 con secciones opcionales

## Workflow obligatorio

### 1. Validar datos
- Confirmar que `Inicio del informe` y `Fin del informe` cubren el periodo pedido.
- Contar ad sets y anuncios únicos.
- Verificar que hay resultados (algunos CSVs de campañas sin entrega vienen vacíos).
- Detectar automáticamente el evento de optimización desde `Indicador de resultado`.

### 2. Calcular KPIs en este orden

```
Nivel campaña:
  Gasto total         = SUM(Importe gastado)
  Impresiones         = SUM(Impresiones)
  Alcance único       = SUM(Alcance)  // nota: solapamiento entre ad sets
  Visitas/Resultados  = SUM(Resultados)
  CPM                 = (Gasto / Impresiones) × 1000
  CPCV / CPA / CPL    = Gasto / Resultados
  CTR                 = Resultados / Impresiones  // para profile_visit es ~2% benchmark
  Frecuencia imp.     = Impresiones / Alcance

Nivel ad set: mismos cálculos agrupados por "Nombre del conjunto de anuncios"
Nivel anuncio: mismos cálculos por "Nombre del anuncio"
```

### 3. Estructura del informe (5 páginas base)

| # | Página | Contenido obligatorio |
|---|--------|----------------------|
| 1 | **Portada** | Título editorial, periodo, folio, "Departamento de Marketing → Gerencia" |
| 2 | **Resumen Ejecutivo** | 4 KPIs hero, 3 insights narrativos, conclusión operativa |
| 3 | **Desempeño por Ad Set** | Bar chart impressions, bar chart CPL, tabla comparativa, lectura técnica |
| 4 | **Top Performers** | Top 10 anuncios + scatter plot costo × volumen |
| 5 | **Cierre & Decisiones** | One-liner, decisiones, calendario 4 semanas, firma |

Páginas opcionales (expandir a 7 si se justifica):
- 6: **Análisis de Creative** — taxonomía Tier 1/2/3, ranking de calidad, descontinuados
- 7: **Plan Próximo Mes** — reasignación presupuestaria, hipótesis, KPIs objetivo

### 4. Estética: "Editorial Deportivo de Lujo"

Inspirada en reportes anuales de revistas automotrices premium. NO usar dashboards genéricos ni estilo McKinsey/consultora.

**Tokens visuales (codificados en `references/design-system.md`):**
- Background ink-black `#0E0D0B`
- Acento burnt amber `#C8954A` (único color cromático, usado con disciplina)
- Tipografía: **Fraunces** (display serif) + **Manrope** (sans) + **JetBrains Mono** (datos)
- Hairlines `#2A2622`, papel `#EDE6D6`
- Sin gradientes morados, sin glassmorphism, sin emojis

### 5. Pipeline de renderizado

```
HTML (un archivo con @page A4 + 5-7 .page sections)
  → Edge headless --print-to-pdf
  → PDF A4 listo para imprimir/compartir
```

Comando exacto en `references/pdf-pipeline.md`. Edge resuelve en Windows sin dependencias. Para Mac/Linux usar `chrome --headless` o `wkhtmltopdf` como fallback.

### 6. Lenguaje técnico (siempre)

Usar terminología de media buying en español:
- CPM (costo por mil), CPCV (costo por visita al perfil), CPL (costo por lead), CPA (costo por adquisición)
- OCPM / ABSOLUTE_OCPM (tipo de puja)
- Quality Ranking, Engagement Rate Ranking
- Frequency / Frecuencia de impresión
- 1-day click / 1-day view (ventanas de atribución)
- Creative fatigue, ad rotation
- Lookalike audiences, interest stacking
- ABO (Ad Set Budget Optimization) vs CBO
- Breakdown por placement, device, demographic

**Evitar:** jerga de marketing genérica ("engagement", "awareness", "presencia de marca") sin cuantificar.

## Análisis obligatorio antes de redactar

Antes de escribir el reporte, el agente DEBE producir este diagnóstico (en su thinking, no en el output):

1. **¿Qué ad set lidera en CPL/CPA?**
2. **¿Cuál es el CPM más alto y por qué?** (compara con otros: audiencia cara vs creative fatigue vs placement)
3. **¿Qué % del tráfico viene del top 4 anuncios?** (>60% = alta concentración, riesgo)
4. **¿Hay calidad <Promedio en Meta Quality Ranking?** (creative necesita refresh)
5. **¿Qué formato/gancho está escalando?** (oferta directa, vacante, financiamiento, video)
6. **¿Qué anuncios están sub-entregados o con $0 gastado?** (revisar投放 / setup)
7. **¿Cuál es la tendencia de frequency?** (>3.5 = saturación)

## Principios de redacción

- **Densidad de números**: cada párrafo tiene al menos 1 cifra concreta.
- **Voz activa**: "Dai lidera en CPL" no "El CPL de Dai es liderado por".
- **Causa → efecto**: no solo reportar el número, explicar qué lo causa.
- **Recomendación accionable**: cada insight cierra con un "para julio →".
- **Sin fluff**: cero "es importante destacar que", "en conclusión", "vale la pena mencionar".
- **Bold para cifras clave** que el lector debe recordar.

## Plantilla HTML

Usar `templates/report-base.html` como punto de partida. Está estructurado con:
- CSS variables para design system
- Componentes reutilizables (`.kpi`, `.bar-row`, `.scatter-svg`, `.callout`, `.pill`)
- Slots marcados con `<!-- TODO: -->` para datos a sustituir
- @page A4 + page-break-after por sección

## Decisiones que requieren aprobación de gerencia

Toda recomendación presupuestaria se presenta como **decisión a aprobar**, no como orden ejecutada. Estructura estándar:

| # | Decisión | Impacto | Plazo |

## Guardrails

- **Nunca inventar datos.** Si el CSV no tiene un dato, omitir el análisis o marcar "no disponible".
- **No inflar positivos.** Si un ad set tuvo bajo desempeño, decirlo.
- **No proponer incremento de presupuesto sin justificación cuantitativa.** Y siempre como decisión, no como hecho.
- **No incluir PII de usuarios** (nombres, emails). Solo métricas agregadas.
- **Disclaimer implícito**: "basado en los datos exportados de Meta Ads al [fecha]. La atribución 1-day click no captura view-through conversions."

## Lista de verificación pre-entrega

- [ ] PDF abre correctamente en Acrobat Reader y Chrome
- [ ] Todos los números del PDF coinciden con los del CSV (revisar al menos 3 aleatorios)
- [ ] No hay "Lorem ipsum" ni placeholders
- [ ] Gráficos SVG renderizan (no aparecen como íconos rotos)
- [ ] Las decisiones están redactadas como "propuesta", no como "se hizo"
- [ ] Fechas en formato DD.MM.YYYY
- [ ] Moneda siempre "USD" con 2-4 decimales
- [ ] El idioma es español rioplatense/neutro, sin regionalismos

## Referencias

- `references/csv-schema.md` — columnas esperadas en los CSV de Meta Ads
- `references/design-system.md` — paleta, tipografía, componentes, espaciado
- `references/pdf-pipeline.md` — comando Edge, troubleshooting encoding
- `templates/report-base.html` — HTML base con 5 páginas, copiar y poblar
