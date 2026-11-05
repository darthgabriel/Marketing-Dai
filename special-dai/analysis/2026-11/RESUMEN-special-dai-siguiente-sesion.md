# SPECIAL DAI · Resumen de sesión para continuidad
**Evento: Dai Motors · Hyundai + Chery Maracaibo · 2–7 nov 2026 (lun a sáb; domingo 8 NO viable)**
Generado: 22 oct 2026 · sesión de planificación y ejecución del plan de evento.

---

## 1 · Qué se hizo esta sesión

1. Análisis de **specialdays.es** (modelo Optima Marketing): evento de 2–4 días, solo con cita, stock limitado, precios solo en evento, precampaña T-3 semanas → se adaptó a Dai Motors.
2. Extracción de datos reales (todo en `context/datos/2026-10-22/`):
   - **Apify** 20 Reels por cuenta → `cherymaracaibo-reels.json`, `daimotorsmcbo-reels.json`.
   - **CRM autoweb** (192.168.100.2:3000, requiere login; usuario lo deja abierto en Playwright) → `crm-inventario-valorado-raw.json` (170 unidades, DOM extraído) → parseado con `parse_crm.py` → `crm-inventario-valorado.json` + resumen.
   - **Instagram público** vía Playwright: perfiles seguidores.
   - **websearch**: mercado Cavenez.
3. Dos playbooks escritos, aprobados y convertidos a PDF (Chrome headless vía `scripts/generar_special_dai.py`):
   - `analysis/2026-11/daimotorsmcbo-plan-special-dai.md` → `entregables/Noviembre-daimotorsmcbo-special-dai-plan1.pdf` (Plan 1, acento azul)
   - `analysis/2026-11/cherymaracaibo-plan-special-dai.md` → `entregables/Noviembre-cherymaracaibo-special-dai-plan2.pdf` (Plan 2, acento rojo)
   - HTML fuente en `entregables/special-dai-*.html`. Para regenerar: `python scripts/generar_special_dai.py`.

## 2 · Números clave (todos verificados, 22 oct 2026)

| | @daimotorsmcbo (Hyundai) | @cherymaracaibo (Chery) |
|---|---|---|
| Seguidores | 9.830 | **13.000** |
| Mediana de Reel (últimos 20) | 1.036 | **9.238 (9×)** |
| Mejor Reel | 193.218 (10K Nature) | 372.988 (Arrizo colores, 10.366 coment.) |
| Ritmo | 2,1/sem | 1,1/sem |
| Físicos en piso | **39** · $1.026.675 | **35** · $824.830 |
| En tránsito | 44 | 48 (+2 Karry) |
| Meta evento (propuesta) | **12 uds** (ritmo 3,9/sem) | **10 uds** (sin línea base — pendiente Gerencia) |

- Unidades viejas: Accent AO712OA **190 d** · Tiggo 4 Pro Max negra AO767HA **360 d**.
- Unidad nuevo hallazgo: **pickup Chery Himla D/C 2.4L** ×3 en piso → pieza de evento.
- Tucson: 9 uds, 2 vendidas en 61 días → foco de venta Hyundai.
- Mercado: 43.470 uds ene–sep 2026 (superó todo 2025), meta 50.000 · JAC 14.893 vs Hyundai 1.246 (ene–ago).
- Ambas cuentas mismo RIF J-30355833-0. **Benchmark interno del grupo, no competidores.**

## 3 · Decisiones cerradas con el usuario

- **Nombre: SPECIAL DAI** — logo: ~~DAYS~~ tachado → **DAI**. Hashtag `#SpecialDai`. Pase = "Pase Special Dai".
- **Evento simultáneo** las dos marcas, 2–7 nov, mismo showroom (zona Hyundai tech / zona Chery roja-blanca LED). **Domingo 8 fuera por design** (decisión explícita, anotada en ambos docs).
- **Presupuesto $3.500 por marca, TODO el evento incluido.** Distribución final:

| Línea | Hyundai | Chery |
|---|---|---|
| Catering + bebidas (50%) — $350/día × 6 + $300 café/hielo/vasos, compartido | $1.200 | $1.200 |
| Montaje (50%) — 4 banderines × $70 = $280 + inflables, alfombra, LED | $780 | $780 |
| **Bulk WhatsApp** | $477 | $505 |
| Tabloides glase QR+precio ×$7/uds | $273 (39) | $245 (35) |
| Papelería (50% de $400) · Regalos (50% de $400) | $200 · $200 | $200 · $200 |
| Promotora | 1 × 6 días | 1 × 6 días |
| Pauta Meta | **$200** | **$200** |
| Contingencia | $50 | $50 |

- **APARTE del presupuesto por marca (externos):** **Alfredo Comedia $750 + redes $300 → Hyundai** · **Susy Calderón $400 + redes $300 → Chery** · Siempre Maracaibo **>$300/cuenta** (costo externo, usuario lo confirmó como aparte) · **pantallas >$400/día** (fuera, >$2.400/evento) · alianza bancaria pendiente.
- Nombres no usados (baratos descartados): Beatriz Elena $150, Luipalour $100 (TikTok $350 por confirmar), Angelina Conté $80, Andria $600, Diego+Juanpi $600, María Nava $1.000.
- **Bulk WhatsApp:** cobro por entregado desde jul 2025, ~$0,05–0,20 LatAm. 2 toques: invitación T-7 (26 oct) + recordatorio T-1 (1 nov). ~2.400–10.000 entregas con el presupuesto. Plantilla Meta + opt-in. Cotizar 2 proveedores antes 25 oct. Base = reporte clientes Kommo.
- Pauta cayó de $3.500 → $200/cuenta a petición del usuario; el funnel ahora es bulk WS + orgánico.
- WhatsApp keywords: Hyundai `VIP I10 ACCENT TUCSON CRETA` · Chery `VIP TIGGO ARRIZO PICKUP`. Todo a Kommo (CRM), historial existente en Chery: "Escribe ARRIZO/TEAM/DECRETO/FAMILIA al 0414-6582009".
- Media day con influencers: mié 4 nov, recorrido ambas zonas, lives.
- Regla heredada: cuotas $ solo tras confirmar con entidad financiera; precio i10 $21.000 solo con unidades reales; nada de política.

## 4 · Línea de contenido (en ambos docs, pág 3)

- **Precampaña 22 oct–1 nov:** 10 piezas por cuenta — anuncio misterio (mié 22), Pase VIP (jue 23), modelo destacado (lun 26), 20 segundos asesor (mar 27), flujo WhatsApp (mié 28), Kilómetro Cero / pickup (jue 29), Tucson 9 / Tiggo 360 d (vie 30), montaje (sáb 31), dom 1 solo stories.
- **Evento 2–7 nov:** Reel diario 10–11 am — apertura, bloques por modelo (mar 3 mejor día), test drive (mié 4), entregas contador (jue 5), "Quedan X" del CRM (vie 6), cierre "precios mueren 5 pm" (sáb 7). Stories diarias.
- **Post-evento 9–11 nov:** "Lo que quedó", relance Kommo, se retoma grilla «Kilómetro Cero» (Hyundai) / piso 4 Reels/sem (Chery).

## 5 · Pendientes vivos

1. **Audiencia Chery** por edad/ciudad — requiere login Meta Business Suite.
2. **Línea base de ventas Chery** (60 días) — reporte de Gerencia.
3. **TikTok Chery** — no extraído.
4. **Base de clientes Kommo** para dimensionar el bulk exacto.
5. Cotizar bulk (2 proveedores) antes 25 oct · cotizar promotora · confirmar aliados bancarios y cuotas publicables · confirmar fecha de entrega de Alfredo/Susy.
6. Meta de Pases VIP por campaña — definir con base Kommo (24 oct).
7. Montaje: acción #4 de ambos docs (alfombra, inflables, banderines, LED; pantallas solo con costo externo aprobado).
8. CRM: verificar fecha de llegada de unidades en tránsito (lote "P. NOVIEMBRE" etc.) — si llegan antes del 2 nov, amplían stock del evento.

## 6 · Archivos

```
analysis/2026-11/daimotorsmcbo-plan-special-dai.md   Plan 1 (fuente)
analysis/2026-11/cherymaracaibo-plan-special-dai.md  Plan 2 (fuente)
entregables/Noviembre-daimotorsmcbo-special-dai-plan1.pdf
entregables/Noviembre-cherymaracaibo-special-dai-plan2.pdf
entregables/special-dai-{hyundai,chery}.html
scripts/generar_special_dai.py      regenera HTML+PDF
context/datos/2026-10-22/           Apify + CRM crudos + parse_crm.py + resumen_reels.py
.opencode/skills/dealer-diagnostico/ skill base (apify_instagram.py, render_pdf.py, formato.md)
analysis/2026-10/daimotorsmcbo-diagnostico-y-plan.md  diagnóstico previo (Hyundai, 13 oct)
```
