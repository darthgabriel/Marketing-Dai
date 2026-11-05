# Skill: meta-ads-reports

Generador de informes ejecutivos en PDF a partir de exports de Meta Ads Manager. Produce un reporte A4 con estética editorial premium listo para presentar a gerencia.

## Estructura

```
meta-ads-reports/
├── SKILL.md                          # Entry point, workflow completo
├── references/
│   ├── csv-schema.md                 # Schema de los CSV de Meta + validaciones
│   ├── design-system.md              # Tokens, tipografía, componentes
│   └── pdf-pipeline.md               # Edge headless → PDF, troubleshooting
├── templates/
│   └── report-base.html              # HTML 5-páginas con slots {{TOKEN}}
└── scripts/
    └── fix-encoding.ps1              # Recovery de PowerShell encoding corruption
```

## Quickstart

1. Copiar CSVs de Meta Ads a `sources/` (Anuncios + Conjuntos)
2. Copiar `templates/report-base.html` a `resultados/`
3. Reemplazar tokens `{{TOKEN}}` con datos del CSV
4. Renderizar:

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
& $edge --headless --disable-gpu --no-sandbox `
  --print-to-pdf="resultados\reporte.pdf" `
  --print-to-pdf-no-header `
  "file:///$((Resolve-Path 'resultados\reporte.html').Path -replace '\\','/')"
```

## Outputs

- **5 páginas A4** por defecto (portada + resumen + ad sets + top performers + cierre)
- Expansible a 7 con secciones opcionales (`Análisis de Creative` + `Plan Próximo Mes`)

## Lenguaje

Español rioplatense/neutro. Terminología técnica de media buying (CPM, CPL, OCPM, Quality Ranking, etc.). Sin jerga genérica de marketing.

Ver `SKILL.md` para el framework completo de análisis.
