# fix-encoding.ps1
# Recovery de archivos UTF-8 corrompidos por PowerShell 5.1 Set-Content -Encoding UTF8
# El bug: PS5.1 lee con codepage ANSI (Windows-1252) y escribe con BOM,
# duplicando bytes de chars multi-byte.
#
# Uso:
#   powershell -ExecutionPolicy Bypass -File fix-encoding.ps1 -Path "file.html"

param(
  [Parameter(Mandatory=$true)][string]$Path
)

$bytes = [System.IO.File]::ReadAllBytes($path)
$out = New-Object System.Collections.Generic.List[byte]
$i = 0
while ($i -lt $bytes.Length) {
  $b  = $bytes[$i]
  $b1 = if ($i+1 -lt $bytes.Length) { $bytes[$i+1] } else { 0 }
  $b2 = if ($i+2 -lt $bytes.Length) { $bytes[$i+2] } else { 0 }
  $b3 = if ($i+3 -lt $bytes.Length) { $bytes[$i+3] } else { 0 }
  $b4 = if ($i+4 -lt $bytes.Length) { $bytes[$i+4] } else { 0 }
  $b5 = if ($i+5 -lt $bytes.Length) { $bytes[$i+5] } else { 0 }
  $b6 = if ($i+6 -lt $bytes.Length) { $bytes[$i+6] } else { 0 }
  $b7 = if ($i+7 -lt $bytes.Length) { $bytes[$i+7] } else { 0 }

  $matched = $false

  # Patrones de corrupcion: 2-byte UTF-8 en rango 0xA0-0xFF que se duplico a 4 bytes
  if ($b -eq 0xC3 -and $b1 -eq 0x83 -and $b2 -eq 0xC2) {
    $out.Add(0xC3); $out.Add($b3); $i += 4; $matched = $true
  }
  elseif ($b -eq 0xC3 -and $b1 -eq 0x82 -and $b2 -eq 0xC2) {
    $out.Add(0xC2); $out.Add($b3); $i += 4; $matched = $true
  }
  elseif ($b -eq 0xC2 -and $b1 -eq 0xC2 -and $b2 -eq 0xC2) {
    $out.Add(0xC2); $out.Add($b3); $i += 4; $matched = $true
  }

  # Patrones: 2-byte UTF-8 en rango 0x80-0x9F que se duplico a 5-7 bytes
  # U+0092 (0xC2 0x92) -> 0xC3 0x82 0xE2 0x80 0x99 -> 0xC2 0x92
  elseif ($b -eq 0xC3 -and $b1 -eq 0x82 -and $b2 -eq 0xE2 -and $b3 -eq 0x80 -and ($b4 -ge 0x98 -and $b4 -le 0x9D)) {
    $out.Add(0xC2); $out.Add($b2); $i += 5; $matched = $true
  }
  # U+0093 (0xC3 0x93) -> 0xC3 0x83 0xE2 0x80 0x9C -> 0xC3 0x93 (etc.)
  elseif ($b -eq 0xC3 -and $b1 -eq 0x83 -and $b2 -eq 0xE2 -and $b3 -eq 0x80 -and ($b4 -ge 0x98 -and $b4 -le 0x9D)) {
    $out.Add(0xC3); $out.Add($b2); $i += 5; $matched = $true
  }

  # U+219X arrows (0xE2 0x86 0x9X) -> 0xC3 0xA2 0xE2 0x80 0xA0 0xE2 0x80 0x9X -> 0xE2 0x86 0x9X
  elseif ($b -eq 0xC3 -and $b1 -eq 0xA2 -and $b2 -eq 0xE2 -and $b3 -eq 0x80 -and $b4 -eq 0xA0 -and $b5 -eq 0xE2 -and $b6 -eq 0x80 -and ($b7 -ge 0x98 -and $b7 -le 0x9D)) {
    $out.Add(0xE2); $out.Add(0x86); $out.Add($b7); $i += 8; $matched = $true
  }
  # U+201X (0xE2 0x80 0x9X) -> 0xC3 0xA2 0xE2 0x82 0xAC 0xE2 0x80 0x9X -> 0xE2 0x80 0x9X
  elseif ($b -eq 0xC3 -and $b1 -eq 0xA2 -and $b2 -eq 0xE2 -and $b3 -eq 0x82 -and $b4 -eq 0xAC -and $b5 -eq 0xE2 -and $b6 -eq 0x80 -and ($b7 -ge 0x98 -and $b7 -le 0x9D)) {
    $out.Add(0xE2); $out.Add(0x80); $out.Add($b7); $i += 8; $matched = $true
  }

  # Fixes especificos para chars concretos
  # U+00DC (Ü) -> U+00D3 (Ó) cuando deberia ser SECCIÓN
  elseif ($b -eq 0xC3 -and $b1 -eq 0x9C) {
    $out.Add(0xC3); $out.Add(0x93); $i += 2; $matched = $true
  }
  # U+00D8 (Ø) -> U+00D3 (Ó) cuando deberia ser DESEMPEÑO
  elseif ($b -eq 0xC3 -and $b1 -eq 0x98) {
    $out.Add(0xC3); $out.Add(0x93); $i += 2; $matched = $true
  }

  if (-not $matched) {
    $out.Add($b); $i++
  }
}

[System.IO.File]::WriteAllBytes($Path, $out.ToArray())
Write-Host "Fixed: $($out.Count) bytes written to $Path"
