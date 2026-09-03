<#
Resize and recompress prospect images so the inlined single file stays email-friendly.

    powershell -File optimize.ps1 -Source assets -Out assets-opt

Uses System.Drawing on purpose: PIL/Pillow is not installed on this machine and must
not be installed for this workflow.

Gallery photos drop to -MaxEdge (640 default) since they display around 280px tall.
The hero keeps up to -HeroMaxEdge. Any file whose recompressed version comes out
LARGER than the original is left as the original instead.
#>
param(
  [string]$Source = "assets",
  [string]$Out = "assets-opt",
  [int]$MaxEdge = 640,
  [int]$HeroMaxEdge = 1800,
  [int]$Quality = 78,
  [int]$HeroQuality = 82,
  # Comma-separated wildcards kept at HeroMaxEdge, e.g. "hero*.jpg,about.jpg".
  # A plain string (not string[]) because `powershell -File` cannot parse array args.
  [string]$HeroPattern = ""
)

Add-Type -AssemblyName System.Drawing

if (-not (Test-Path $Source)) { Write-Error "Source folder not found: $Source"; exit 1 }
New-Item -ItemType Directory -Force $Out | Out-Null

$jpegEncoder = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() |
               Where-Object { $_.MimeType -eq 'image/jpeg' }

function Convert-One($file, $maxEdge, $quality) {
  $img = [System.Drawing.Image]::FromFile($file.FullName)
  try {
    $ratio = [Math]::Min($maxEdge / $img.Width, $maxEdge / $img.Height)
    if ($ratio -gt 1) { $ratio = 1 }
    $nw = [int]($img.Width * $ratio); $nh = [int]($img.Height * $ratio)

    $bmp = New-Object System.Drawing.Bitmap($nw, $nh)
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.DrawImage($img, 0, 0, $nw, $nh)

    $ps = New-Object System.Drawing.Imaging.EncoderParameters(1)
    $ps.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter(
                     [System.Drawing.Imaging.Encoder]::Quality, [long]$quality)
    $dest = Join-Path $Out $file.Name
    $bmp.Save($dest, $jpegEncoder, $ps)
    $g.Dispose(); $bmp.Dispose()

    # Recompressing an already-optimized JPEG can grow it. Keep the smaller one.
    $after = (Get-Item $dest).Length
    if ($after -ge $file.Length) {
      Copy-Item $file.FullName $dest -Force
      Write-Output ("  {0,-52} kept original  {1,6:N0} KB" -f $file.Name, ($file.Length/1KB))
    } else {
      Write-Output ("  {0,-52} {1}x{2}  {3,6:N0} -> {4,-6:N0} KB" -f `
                    $file.Name, $nw, $nh, ($file.Length/1KB), ($after/1KB))
    }
  } finally { $img.Dispose() }
}

$heroPatterns = @()
if ($HeroPattern) {
  $heroPatterns = $HeroPattern.Split(',') | ForEach-Object { $_.Trim() } |
                  Where-Object { $_ -ne '' }
}

Write-Output "optimizing $Source -> $Out"
if ($heroPatterns.Count) { Write-Output ("full-size: " + ($heroPatterns -join ', ')) }
foreach ($f in Get-ChildItem "$Source\*" -Include *.jpg,*.jpeg) {
  $isFeature = $false
  foreach ($p in $heroPatterns) { if ($f.Name -like $p) { $isFeature = $true; break } }
  if ($isFeature) {
    Convert-One $f $HeroMaxEdge $HeroQuality
  } else {
    Convert-One $f $MaxEdge $Quality
  }
}

# SVGs copy through untouched.
foreach ($f in Get-ChildItem "$Source\*" -Include *.svg) {
  Copy-Item $f.FullName (Join-Path $Out $f.Name) -Force
  Write-Output ("  {0,-52} copied         {1,6:N0} KB" -f $f.Name, ($f.Length/1KB))
}

# PNGs need a decision, not a blind copy. Some sites serve their *photos* as PNG,
# which is enormous: one 308x310 photo came in at 184 KB. Copying those through
# produced a 0% saving and a 2.2 MB page. So: sample the alpha channel, report which
# PNGs are actually opaque, and flag them for JPEG conversion.
$convertible = @()
foreach ($f in Get-ChildItem "$Source\*" -Include *.png) {
  $bmp = New-Object System.Drawing.Bitmap($f.FullName)
  try {
    $transparent = $false
    $sx = [Math]::Max(1, [int]($bmp.Width / 50)); $sy = [Math]::Max(1, [int]($bmp.Height / 50))
    for ($x = 0; $x -lt $bmp.Width -and -not $transparent; $x += $sx) {
      for ($y = 0; $y -lt $bmp.Height; $y += $sy) {
        if ($bmp.GetPixel($x, $y).A -lt 250) { $transparent = $true; break }
      }
    }
    $centreOpaque = $bmp.GetPixel([int]($bmp.Width/2), [int]($bmp.Height/2)).A -ge 250
    $isPhoto = ($f.Length/1KB) -gt 40 -and $bmp.Width -gt 150
  } finally { $bmp.Dispose() }

  Copy-Item $f.FullName (Join-Path $Out $f.Name) -Force
  $note = if (-not $transparent -and $isPhoto) { "OPAQUE PHOTO -> convert to JPEG" }
          elseif ($transparent -and $centreOpaque -and $isPhoto) { "corner-only alpha -> JPEG if CSS clips it" }
          else { "keep as PNG" }
  if ($note -ne "keep as PNG") { $convertible += $f.Name }
  Write-Output ("  {0,-52} copied         {1,6:N0} KB  [{2}]" -f $f.Name, ($f.Length/1KB), $note)
}
if ($convertible.Count) {
  Write-Output ""
  Write-Output "ACTION NEEDED: these PNGs are photos and dominate the page weight."
  Write-Output "Convert them to JPEG, flattening onto the colour of their CSS container"
  Write-Output "(NOT always white: a portrait sitting on a navy panel needs the navy),"
  Write-Output "then update the src/data-full references in the HTML to the new .jpg names:"
  $convertible | ForEach-Object { Write-Output ("  - " + $_) }
}

$before = (Get-ChildItem "$Source\*" -File | Measure-Object -Property Length -Sum).Sum
$after  = (Get-ChildItem "$Out\*"    -File | Measure-Object -Property Length -Sum).Sum
Write-Output ""
Write-Output ("total: {0:N0} KB -> {1:N0} KB  ({2:N0}% smaller)" -f `
              ($before/1KB), ($after/1KB), ((1 - $after/$before) * 100))
