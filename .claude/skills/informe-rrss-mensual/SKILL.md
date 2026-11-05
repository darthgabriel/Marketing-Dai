---
name: informe-rrss-mensual
description: Informe mensual de estadísticas de Instagram de las cuentas OCG (daimotorsmcbo, cherymaracaibo, kyotomotorsmcbo, yantaimotors, karrymaracaibo). Extrae datos del mes anterior en Meta Business Suite, pide al usuario inversión ADS y visitas Google, crea la hoja del mes en el Excel "Estadisticas Informe.xlsx" y genera el PDF de 2 páginas para gerencia. Usar cuando pidan "estadísticas del mes", "informe RRSS", "informe para gerencia" o el cierre mensual de redes.
---

# Informe RRSS mensual (gerencia)

Mes a reportar = mes calendario anterior al día de hoy (ej. el 1 dic 2026 → NOVIEMBRE 2026).
Mes de comparación = hoja anterior existente en el Excel (normalmente el mes previo).

Archivos:
- Excel: `G:\Mi unidad\Marketing - OCG\Estadisticas Informe.xlsx` (hojas "MES AAAA" en mayúsculas)
- Carpeta de trabajo: `C:\Users\DELL\Desktop\marketing\estadisticas` (todo archivo de estadísticas va aquí)
  - `scripts\` → `escribir_excel.ps1`, `generar_informe.py`
  - `datos\` → `datos_<mes>_<año>.json`, `narrativa_<mes>_<año>.json`
  - `informes\` → `Informe RRSS <Mes Aaaa>.pdf` (y .html)
- Cómo extraer de Meta: `references/meta-extraccion.md` (leer antes del paso 2)

## 1. Pedir datos al usuario (una sola pregunta, al inicio)

Pedir juntos:
- **Inversión ADS (USD)** del mes por cuenta (las no indicadas = 0).
- **Visitas Google** (Google Business Profile) de daimotorsmcbo, cherymaracaibo y yantaimotors.

Kyoto y Karry no llevan Google → null. Seguir con el paso 2 mientras responde.

## 2. Extraer de Meta Business Suite

Navegador integrado; el usuario inicia sesión. Por cada cuenta, con `time_range=LAST_MONTH` y `platform=Instagram`:
nuevos seguidores, total seguidores, contenido del mes, visualizaciones (solo IG), alcance exacto (tooltip), visitas al perfil, interacciones.
Verificar el rango `1 <mes> - <último día>` en cada página.

Validar contra el mes anterior; si algo cambia >80% o parece de otra cuenta, avisar antes de seguir.

## 3. Escribir el Excel

Guardar datos en `estadisticas\datos\datos_<mes>_<año>.json` (ejemplo: `datos_octubre_2026.json`) (formato en la cabecera de `escribir_excel.ps1`, orden: dai, chery, kyoto, yantai, karry; null = vacío). Luego:

```powershell
$E = 'C:\Users\DELL\Desktop\marketing\estadisticas'
& "$E\scripts\escribir_excel.ps1" -Mes 'NOVIEMBRE 2026' -Base 'OCTUBRE 2026' -Datos "$E\datos\datos_noviembre_2026.json"
```

El script hace backup, copia el formato de la hoja base y escribe fórmulas: engagement ÷3 si hay Google, ÷2 si no.
Nunca usar openpyxl para escribir: el libro tiene gráfico, imagen y tablas que se pierden.
Si el Excel está abierto (solo lectura), pedir al usuario que lo cierre.

## 4. Narrativa y PDF

Crear `estadisticas\datos\narrativa_<mes>_<año>.json` (ejemplo: `narrativa_octubre_2026.json`):
```json
{
  "resumen": "2-3 frases con <b>cifras clave</b>: totales del grupo vs mes de comparación, cuenta líder y principal alerta.",
  "nota_comparacion": "fuente y aclaraciones (meses no registrados, etc.)",
  "inversion": {"daimotorsmcbo": 0, "cherymaracaibo": 0, "kyotomotorsmcbo": 0, "yantaimotors": 0, "karrymaracaibo": 0}
}
```
Calcular las cifras del resumen con los datos (no estimar). Luego:

```bash
cd "C:/Users/DELL/Desktop/marketing/estadisticas"
python scripts/generar_informe.py "NOVIEMBRE 2026" "OCTUBRE 2026" datos/narrativa_noviembre_2026.json
```

Formato acordado (no cambiar sin pedirlo): 2 páginas A4 horizontal.
1. Resumen ejecutivo, 7 indicadores (incluye Inversión ADS), consolidado con inversión, costo/seguidor nuevo y costo/1.000 alcanzados.
2. Las 5 tarjetas por cuenta (mes, comparación, variación, inversión) + recuadro "Cómo leer las tarjetas".
Sin página de gráficos ni de recomendaciones.

## 5. Verificar y entregar

- Screenshot del HTML con Edge (`--headless --screenshot --window-size=1123,1590`) y revisar que la página 2 no se corte.
- Contar páginas del PDF = 2.
- Enviar el PDF al usuario con resumen breve: totales, datos faltantes y supuestos.
