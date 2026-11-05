# Crea la hoja del mes en el Excel de estadísticas copiando el formato de una hoja base.
# Uso:
#   .\escribir_excel.ps1 -Mes 'NOVIEMBRE 2026' -Base 'OCTUBRE 2026' -Datos 'C:\...\datos_noviembre_2026.json'
# JSON: { "cuentas": [ { "cuenta": "daimotorsmcbo", "nuevos": 368, "total": 10671, "contenido": 100,
#          "vis": 255429, "alc": 85179, "perfil": 4078, "inter": 2067, "google": 2069 }, ... ] }
# null = celda vacía. google null => engagement /2; google con valor => /3.
param(
    [Parameter(Mandatory)][string]$Mes,
    [Parameter(Mandatory)][string]$Base,
    [Parameter(Mandatory)][string]$Datos,
    [string]$Path = 'G:\Mi unidad\Marketing - OCG\Estadisticas Informe.xlsx'
)

$cuentas = (Get-Content $Datos -Raw -Encoding UTF8 | ConvertFrom-Json).cuentas
if ($cuentas.Count -ne 5) { throw "Se esperaban 5 cuentas, llegaron $($cuentas.Count)" }

$backup = Join-Path (Split-Path $Path) ("Estadisticas Informe - backup {0:yyyy-MM-dd}.xlsx" -f (Get-Date))
Copy-Item $Path $backup -Force

$x = New-Object -ComObject Excel.Application
$x.Visible = $false
$x.DisplayAlerts = $false
$prevAutoFill = $x.AutoCorrect.AutoFillFormulasInLists
try {
    # Las filas de resultados son tabla: sin esto Excel propaga la última fórmula a toda la columna
    $x.AutoCorrect.AutoFillFormulasInLists = $false
    $wb = $x.Workbooks.Open($Path)
    if ($wb.ReadOnly) { throw 'Archivo abierto en otro lado (solo lectura)' }
    foreach ($s in $wb.Worksheets) { if ($s.Name -eq $Mes) { throw "Ya existe hoja $Mes" } }

    $src = $wb.Worksheets.Item($Base)
    $src.Copy([Type]::Missing, $wb.Worksheets.Item($wb.Worksheets.Count))
    $ws = $wb.Worksheets.Item($wb.Worksheets.Count)
    $ws.Name = $Mes
    $ws.Range('A1').Formula = "RELACION DE ESTADISTICAS DE CUENTAS $Mes"

    function Set-Cell($r, $c, $v) {
        $cell = $ws.Cells.Item($r, $c)
        if ($null -eq $v) { $null = $cell.ClearContents() }
        else { $cell.Formula = [string]$v }
    }

    for ($i = 0; $i -lt 5; $i++) {
        $d = $cuentas[$i]
        $rp = 5 + $i; $rm = 12 + $i; $rr = 19 + $i
        Set-Cell $rp 1 $d.cuenta; Set-Cell $rp 2 $d.nuevos; Set-Cell $rp 3 $d.total; Set-Cell $rp 4 $d.contenido
        Set-Cell $rm 1 $d.cuenta; Set-Cell $rm 2 $d.vis; Set-Cell $rm 3 $d.alc
        Set-Cell $rm 4 $d.perfil; Set-Cell $rm 5 $d.inter; Set-Cell $rm 6 $d.google
        Set-Cell $rr 1 $d.cuenta
        if ($null -ne $d.google) { $avg = "((D$rm+E$rm+F$rm)/3)" } else { $avg = "((D$rm+E$rm)/2)" }
        $ws.Cells.Item($rr, 2).Formula = "=B$rm/C$rm"
        $ws.Cells.Item($rr, 3).Formula = "=$avg/C$rp"
        $ws.Cells.Item($rr, 4).Formula = "=$avg/C$rm"
    }
    $x.CalculateFull()
    $wb.Save()

    for ($r = 18; $r -le 23; $r++) {
        '{0} | {1} | {2} | {3} | {4}' -f $ws.Cells.Item($r,1).Text, $ws.Cells.Item($r,2).Text,
            $ws.Cells.Item($r,3).Text, $ws.Cells.Item($r,4).Text, $ws.Cells.Item($r,3).Formula
    }
    "Backup: $backup"
    $wb.Close($false)
} finally {
    $x.AutoCorrect.AutoFillFormulasInLists = $prevAutoFill
    $x.Quit()
    [void][Runtime.InteropServices.Marshal]::ReleaseComObject($x)
}
