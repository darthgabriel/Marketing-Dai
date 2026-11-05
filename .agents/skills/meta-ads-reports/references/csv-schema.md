# CSV Schema — Meta Ads Manager Exports

Meta Ads Manager exporta dos CSVs por defecto al pedir un reporte de performance. Ambos vienen en español con encoding UTF-8 (a veces con BOM, a veces sin).

## Archivo 1: `*Anuncios*.csv` (granularidad: anuncio)

Una fila por cada combinación anuncio × día. El agente debe agregar a nivel anuncio.

### Columnas requeridas

| Columna | Tipo | Notas |
|---------|------|-------|
| `Inicio del informe` | date | `YYYY-MM-DD` |
| `Fin del informe` | date | `YYYY-MM-DD` |
| `Nombre del anuncio` | string | Nombre que el advertiser puso en el ad |
| `Entrega del anuncio` | enum | `active` / `not_delivering` / `inactive` / `recently_completed` |
| `Nombre del conjunto de anuncios` | string | FK al CSV de conjuntos |
| `Puja` | number | Bid amount en USD |
| `Tipo de puja` | enum | `ABSOLUTE_OCPM`, `CPC`, `CPM`, etc. |
| `Presupuesto del conjunto de anuncios` | number | Diario, USD |
| `Tipo de presupuesto del conjunto de anuncios` | enum | `Diario` / `Vitalicio` |
| `Último cambio significativo` | datetime | ISO 8601 con offset |
| `Configuración de atribución` | string | ej: `"1 día tras clic"` |
| `Impresiones` | int | Total served |
| `Alcance` | int | Cuentas únicas |
| `Resultados` | int | Según evento de optimización |
| `Indicador de resultado` | string | ej: `profile_visit_view`, `lead`, `purchase` |
| `Clasificación de calidad` | enum | `Por encima del promedio` / `Promedio` / `Por debajo del promedio` / `-` |
| `Clasificación del porcentaje de interacción` | enum | mismo enum que calidad |
| `Costo por mil cuentas de Meta alcanzadas (USD)` | number | |
| `CPM (costo por mil impresiones) (USD)` | number | |
| `Costo por resultados` | number | El "CPL" del advertiser |
| `Importe gastado (USD)` | number | |
| `Finalización` | date | `YYYY-MM-DD` o vacío |

### Normalización común

Los headers en español pueden tener tildes o caracteres rotos. Antes de procesar:

```python
import pandas as pd
df = pd.read_csv("Anuncios.csv", encoding="utf-8-sig")  # tolera BOM
df.columns = df.columns.str.strip().str.lower()
```

### Detección del evento de optimización

```python
evento = df["indicador de resultado"].iloc[0]
# Mapear a término humano en el reporte:
evento_label = {
    "profile_visit_view": "visitas al perfil",
    "lead": "leads",
    "purchase": "compras",
    "offsite_conversion.fb_pixel_purchase": "compras (pixel)",
}.get(evento, evento)
```

## Archivo 2: `*Conjuntos*.csv` (granularidad: ad set)

Misma estructura pero una fila por ad set por día. Útil para validar los totales y para análisis de presupuesto.

### Columnas clave

- `Nombre del conjunto de anuncios` — ad set name
- `Presupuesto del conjunto de anuncios` — cap diario
- `Importe gastado (USD)` — real spend (puede ser < budget por underspend)
- `Impresiones`, `Alcance`, `Resultados` — mismos campos

## Validaciones de calidad de datos

Antes de calcular KPIs, verificar:

1. **Consistencia de fechas**: `Inicio del informe` debe coincidir entre ambos CSVs.
2. **Spend < Budget × días**: Si gastó más, es billing anomaly. Reportar.
3. **Impresiones > 0 ≠ Resultados > 0**: puede haber entregado sin conversiones (CTR 0%). No es error, es dato.
4. **Anuncios con 0 impresiones**: revisar si el投放 está activo o si se desactivó al crear.
5. **CPM extremo** (<$0.10 o >$50): puede ser error de tracking o audiencia muy nicho. Marcar.

## Diferencias entre exportes

Meta a veces actualiza el schema. Versiones comunes:

- **Legacy** (2020-2022): columnas en camelCase inglés
- **Current** (2023+): snake_case en español, comillas dobles, separador `,`
- **Custom date range**: aparecen dos filas header (rango + atributos)

Si el CSV tiene un header raro con metadata, saltar las primeras N líneas:

```python
df = pd.read_csv("file.csv", skiprows=2, encoding="utf-8-sig")
```

## Cálculos derivados (los que NO están en el CSV)

```python
# Frecuencia de impresión
freq = impressions / reach

# CTR (si el evento es profile_visit)
ctr_profile = results / impressions

# Conversión efectiva (si hay conversion event tracking)
# (no calcular sin datos del pixel — Meta no lo exporta aquí)
```

## Privacidad

Los CSVs NO contienen PII (no hay emails, teléfonos, nombres de usuarios). Solo métricas agregadas. Es seguro incluirlas en el reporte.
