<#
  Etape 2 de la verification : rend le PDF de controle en images, puis les assemble en une
  seule planche-contact a regarder.

      powershell -ExecutionPolicy Bypass -File apercu.ps1 -Dir "C:\...\_apercu"

  Doit tourner dans son propre processus, apres verifier.ps1. Word en COM et WinRT dans le
  meme processus se bloquent mutuellement.

  Pourquoi WinRT : Chrome headless ne rend PAS les PDF, la capture sort vide. Le moteur PDF
  de Windows le fait.
#>
param(
  [Parameter(Mandatory = $true)][string]$Dir,
  [string]$Pdf = "",
  [int]$Largeur = 700,
  [int]$Vignette = 300,
  [switch]$GarderPdf
)

$ErrorActionPreference = "Stop"
$Dir = (Resolve-Path $Dir).Path
if (-not $Pdf) { $Pdf = Join-Path $Dir "_verif.pdf" }
if (-not (Test-Path $Pdf)) { throw "PDF de controle introuvable: $Pdf. Lancer verifier.ps1 avant." }

# --- rendu des pages, via le moteur PDF de Windows ---
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Data.Pdf.PdfDocument, Windows.Data.Pdf, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.StorageFile, Windows.Storage, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.InMemoryRandomAccessStream, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null

$methods = [System.WindowsRuntimeSystemExtensions].GetMethods()
$asTaskOp = ($methods | Where-Object {
  $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
  $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1' })[0]
$asTaskAct = ($methods | Where-Object {
  $_.Name -eq 'AsTask' -and $_.GetParameters().Count -eq 1 -and
  $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncAction' })[0]

function Await($op, $type) {
  $t = $asTaskOp.MakeGenericMethod($type).Invoke($null, @($op)); $t.Wait(-1) | Out-Null; $t.Result
}

$file = Await ([Windows.Storage.StorageFile]::GetFileFromPathAsync($Pdf)) ([Windows.Storage.StorageFile])
$pdfDoc = Await ([Windows.Data.Pdf.PdfDocument]::LoadFromFileAsync($file)) ([Windows.Data.Pdf.PdfDocument])

Get-ChildItem (Join-Path $Dir "page-*.png") -ErrorAction SilentlyContinue | Remove-Item -Force
for ($i = 0; $i -lt $pdfDoc.PageCount; $i++) {
  $page = $pdfDoc.GetPage($i)
  $stream = New-Object Windows.Storage.Streams.InMemoryRandomAccessStream
  $opts = New-Object Windows.Data.Pdf.PdfPageRenderOptions
  $opts.DestinationWidth = [uint32]$Largeur
  $asTaskAct.Invoke($null, @($page.RenderToStreamAsync($stream, $opts))).Wait(-1) | Out-Null
  $reader = New-Object Windows.Storage.Streams.DataReader($stream.GetInputStreamAt(0))
  Await ($reader.LoadAsync([uint32]$stream.Size)) ([uint32]) | Out-Null
  $bytes = New-Object byte[] $stream.Size
  $reader.ReadBytes($bytes)
  [System.IO.File]::WriteAllBytes((Join-Path $Dir ("page-{0:D2}.png" -f ($i + 1))), $bytes)
  try { $page.Dispose() } catch {}
  try { $stream.Dispose() } catch {}
}

# --- planche-contact : une seule image a lire plutot que N ---
Add-Type -AssemblyName System.Drawing
$files = Get-ChildItem (Join-Path $Dir "page-*.png") | Sort-Object Name
$cw = $Vignette
$ch = [int]($Vignette * 1.294)
$bmp = New-Object System.Drawing.Bitmap(($cw * $files.Count + 10), ($ch + 24))
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear([System.Drawing.Color]::Gray)
$g.InterpolationMode = 'HighQualityBicubic'
$font = New-Object System.Drawing.Font('Arial', 10)
$i = 0
foreach ($f in $files) {
  $im = [System.Drawing.Image]::FromFile($f.FullName)
  $g.DrawImage($im, (New-Object System.Drawing.Rectangle(($i * ($cw + 4) + 3), 3, ($cw - 6), ($ch - 6))))
  $g.DrawString(("p." + ($i + 1)), $font, [System.Drawing.Brushes]::White, ($i * ($cw + 4) + 3), ($ch + 2))
  $im.Dispose(); $i++
}
$out = Join-Path $Dir "planche.png"
$bmp.Save($out, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()

"pages rendues: $($pdfDoc.PageCount)"
"planche: $out"
if (-not $GarderPdf) { Remove-Item $Pdf -Force -ErrorAction SilentlyContinue }
