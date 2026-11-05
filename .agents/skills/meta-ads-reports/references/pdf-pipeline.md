# PDF Pipeline — HTML → PDF con Edge headless

Pipeline mínimo para convertir el HTML del reporte en un PDF A4 sin dependencias externas. Edge está preinstalado en Windows 10/11.

## Comando base

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$html = "C:\path\to\reporte.html"
$pdf  = "C:\path\to\reporte.pdf"

# Quitar PDF previo (Edge no sobrescribe limpio)
Remove-Item $pdf -ErrorAction SilentlyContinue

& $edge --headless --disable-gpu --no-sandbox `
  --print-to-pdf="$pdf" `
  --print-to-pdf-no-header `
  "file:///$($html -replace '\\','/')"
```

**Flags importantes:**
- `--headless` — sin ventana
- `--disable-gpu` — evita crash en sistemas sin GPU dedicada
- `--no-sandbox` — necesario en algunos entornos corporativos
- `--print-to-pdf` — destino
- `--print-to-pdf-no-header` — quita "URL / fecha" que Edge agrega por defecto

## Fallback multiplataforma

```bash
# macOS / Linux con Chrome instalado
google-chrome --headless --disable-gpu --no-sandbox \
  --print-to-pdf=output.pdf \
  "file:///path/to/reporte.html"

# O con wkhtmltopdf (más rápido pero menos fiel)
wkhtmltopdf --enable-local-file-access --print-media-type \
  reporte.html reporte.pdf
```

## @page rules en el HTML

Para que el PDF salga en A4 con márgenes controlados:

```css
@page {
  size: A4;
  margin: 0;  /* manejamos márgenes con padding en .page */
}

.page {
  width: 210mm;
  height: 297mm;
  padding: 22mm 20mm 20mm 20mm;
  page-break-after: always;
  overflow: hidden;
  position: relative;
}
```

El `overflow: hidden` + `height: 297mm` garantiza que cada sección sea exactamente una página, sin contenido cortado.

## Carga de fuentes

Las fuentes Google (Fraunces, Manrope, JetBrains Mono) se cargan vía CDN en el `<head>`:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght,SOFT@9..144,300..900,0..100&family=Manrope:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;600&display=swap" rel="stylesheet">
```

Edge headless **sí descarga** las fuentes si hay internet. Si el entorno no tiene red, hacer fallback a `system-ui` y avisar al usuario que el renderizado será inferior.

## Troubleshooting

### Encoding se corrompe al reescribir el HTML

**Síntoma**: Después de un `Set-Content -Encoding UTF8` en PowerShell 5.1, los caracteres especiales (`ó`, `á`, `€`, `—`) aparecen como `Ã³`, `Ã¡`, `â¬`, `Ã—`.

**Causa**: PowerShell 5.1 `Set-Content -Encoding UTF8` agrega BOM y usa code page ANSI (Windows-1252) para leer/escribir.

**Fix**: Usar .NET directamente, sin BOM:

```powershell
$path = "C:\path\to\file.html"
$content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
[System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))
```

Si el archivo ya está corrupto, reverso del patrón de corrupción (cada UTF-8 multi-byte fue duplicado):
- `0xC3 0xA2` (`â`) + `0xE2 0x82 0xAC` (`€`) + `0xE2 0x80 0x9X` = original `0xE2 0x86 0x9X` (flechas)
- `0xC3 0x83` (`Ã`) + `0xE2 0x80 0x9X` = original `0xC3 0x9X` (Ó, Ü, etc.)

Ver script de recuperación en `scripts/fix-encoding.ps1` si aplica.

### Edge muestra error de "task provider"

Es benigno. Es un warning de Chromium sobre task management. El PDF igual se genera. Filtrar con `2>&1 | Out-Null`.

### "PDF no generado" sin error

Verificar:
1. La ruta del HTML no tiene espacios sin escapar (usar `file:///` con forward slashes)
2. El PDF destino está en un directorio escribible
3. Edge no está abierto (cierra instancias)

### Gráficos SVG no aparecen

Verificar que el SVG tiene `viewBox` y `width/height` o `class` con dimensiones en CSS. SVG inline funciona mejor que `<img src=...>`.

### Tablas se cortan entre páginas

Si una tabla cruza el límite de página, usar `page-break-inside: avoid` en el `<tbody>` o dividir manualmente.

## Script de batch (múltiples reportes)

```powershell
$edge = "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
$sources = Get-ChildItem "C:\Reports\*.html"

foreach ($html in $sources) {
    $pdf = $html.FullName -replace '\.html$', '.pdf'
    Remove-Item $pdf -ErrorAction SilentlyContinue
    & $edge --headless --disable-gpu --no-sandbox `
        --print-to-pdf="$pdf" `
        --print-to-pdf-no-header `
        "file:///$($html.FullName -replace '\\','/')"
    Write-Host "$($html.Name) → $([math]::Round((Get-Item $pdf).Length/1KB,1)) KB"
}
```

## Tiempo de renderizado típico

- 5 páginas A4 con 1-2 charts SVG: **3-5 segundos**
- 7 páginas con 3-4 charts: **5-8 segundos**
- Edge headless reutiliza caché de fuentes, segundo reporte del mismo directorio es más rápido.

## Verificación post-render

Después de generar el PDF, validar:
1. **Page count**: `Get-Content $pdf -Encoding Byte` + regex para `/Count N` (requiere parser PDF).
2. **Tamaño razonable**: ~50KB por página promedio. <20KB = problema de fuentes.
3. **Apertura**: abrir en Edge/Acrobat/Chrome sin warnings.
