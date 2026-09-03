<#
  Etape 1 de la verification : Word ouvre le document, le compte et l'exporte en PDF.

      powershell -ExecutionPolicy Bypass -File verifier.ps1 -Docx "C:\...\doc.docx"

  Qu'un document s'ouvre dans Word est la seule preuve solide qu'il n'est pas corrompu.
  Le PDF produit sert ensuite a apercu.ps1 pour le controle visuel.

  Ce script est volontairement ecrit "a plat", et il ne faut pas l'enrichir sans tester :

  1. PAS de $ErrorActionPreference = "Stop" autour du bloc Word. Si ExportAsFixedFormat
     echoue sous Stop, l'exception part dans le finally, ou $word.Quit() reste bloque sur
     une boite de dialogue invisible. Le script parait fige alors qu'il a juste rate
     l'export, et aucun message ne sort.
  2. PAS de creation de dossier avant d'ouvrir Word. Creer un dossier dans OneDrive juste
     avant declenche une synchronisation qui fait trainer l'export.
  3. PAS de rendu des pages ici. Word en COM et le moteur PDF de Windows en WinRT dans le
     meme processus PowerShell se bloquent mutuellement. C'est le role d'apercu.ps1.
  4. PAS d'export vers $env:TEMP : il vaut une forme courte 8.3 sur cette machine, du type
     C:\Users\ADMINI~1\..., que Word refuse. (Get-Item).FullName ne la rallonge pas.
  5. LE PIEGE PRINCIPAL : passer le chemin de sortie entre guillemets, "$tmpPdf" et non
     $tmpPdf. Une variable nue passee a une methode COM de Word est marshalee d'une facon
     que Word n'accepte pas, et ExportAsFixedFormat ne rend jamais la main. Le meme chemin
     ecrit en litteral fonctionne, ce qui rend le bug tres trompeur : on soupconne le
     chemin, le dossier, OneDrive, alors que c'est la forme de l'argument. L'interpolation
     force une chaine neuve et regle le probleme.
#>
param(
  [Parameter(Mandatory = $true)][string]$Docx,
  [string]$OutDir = ""
)

$Docx = (Resolve-Path $Docx).Path
$dossier = Split-Path $Docx
if (-not $OutDir) { $OutDir = Join-Path $dossier "_apercu" }
$tmpPdf = Join-Path $dossier "_verif_tmp.pdf"

# Une instance tuee de force laisse Word vouloir afficher son volet de recuperation au
# demarrage suivant, et ce volet bloque l'automatisation sans message.
Get-Process WINWORD -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Milliseconds 400
if (Test-Path $tmpPdf) { Remove-Item $tmpPdf -Force -ErrorAction SilentlyContinue }

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0
$doc = $word.Documents.Open($Docx, $false, $true)
"OUVERTURE OK  |  pages: {0}  |  mots: {1}" -f $doc.ComputeStatistics(2), $doc.ComputeStatistics(0)
$doc.ExportAsFixedFormat("$tmpPdf", 17)   # guillemets obligatoires, voir point 5. 17 = wdExportFormatPDF
$doc.Close($false)
$word.Quit()

# le dossier d'apercu se cree apres, une fois Word ferme
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
Move-Item $tmpPdf (Join-Path $OutDir "_verif.pdf") -Force
"PDF de controle: " + (Join-Path $OutDir "_verif.pdf")
