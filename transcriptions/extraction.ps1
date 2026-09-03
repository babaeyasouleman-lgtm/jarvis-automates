# L extracteur de transcriptions Claude Code. Phase 2 bis du Plan Jarvis.
# Il lit ce que Souleman a dit a Claude Code depuis le dernier passage,
# en tire les faits durables, et les depose dans 00 Inbox.
# Il ne range rien. Le bibliothecaire passe apres lui.
#
# Ce script ne supprime aucune transcription. Le pre-filtre non plus.
# Seul le dossier travail est vide a chaque passage, ce sont des copies.
#
# Aucun accent dans ce fichier, volontairement. PowerShell 5.1 lit les .ps1
# en ANSI et abimerait les accents. Tout le texte accentue vit dans
# consigne.md, que Claude lit lui-meme en UTF8.
#
# Lancement manuel :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\transcriptions\extraction.ps1
# Voir ce qui serait traite, sans appeler le modele :
#   ... \extraction.ps1 -Sec
# Rattrapage historique, un lot borne dans le temps :
#   ... \extraction.ps1 -Jusqu 2026-08-20T00:00:00.000Z
#
# Ce script ne pousse pas vers GitHub. Le filet horaire et le bibliothecaire
# s en chargent, et rien ne se perd entre deux.

param(
    [string]$Jusqu = '',
    [switch]$Sec
)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre    = 'C:\Obsidian\Second Brain'
$base      = 'C:\Obsidian\transcriptions'
$consigne  = Join-Path $base 'consigne.md'
$prefiltre = Join-Path $base 'prefiltre.py'
$travail   = Join-Path $base 'travail'
$contexte  = Join-Path $base 'contexte.txt'
$marqueur  = Join-Path $base 'marqueur.txt'
$journal   = Join-Path $base 'journal.log'
$jourFait  = Join-Path $base 'dernier-jour.txt'
$claude    = 'C:\Users\Administrator\.local\bin\claude.exe'
$python    = 'C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe'
$modele    = 'sonnet'
# -------------------------------------------------------------------------

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

function Get-SemaineIso([datetime]$d) {
    $ci = [Globalization.CultureInfo]::InvariantCulture
    $jour = [int]$ci.Calendar.GetDayOfWeek($d)
    if ($jour -ge 1 -and $jour -le 3) { $d = $d.AddDays(3) }
    $n = $ci.Calendar.GetWeekOfYear($d, [Globalization.CalendarWeekRule]::FirstFourDayWeek, [DayOfWeek]::Monday)
    return "{0}-S{1:D2}" -f $d.Year, $n
}

$maintenant = Get-Date
$aujourdhui = $maintenant.ToString('yyyy-MM-dd')

# 1. Verifications
if (-not (Test-Path $python)) {
    $repli = (Get-Command python -ErrorAction SilentlyContinue)
    if ($repli) { $python = $repli.Source } else { Note "ECHEC, python introuvable"; exit 1 }
}
if (-not (Test-Path $prefiltre)) { Note "ECHEC, prefiltre.py introuvable"; exit 1 }
if (-not (Test-Path $consigne))  { Note "ECHEC, consigne.md introuvable"; exit 1 }
if (-not (Test-Path $coffre))    { Note "ECHEC, coffre introuvable"; exit 1 }
if (-not $Sec -and -not (Test-Path $claude)) { Note "ECHEC, claude.exe introuvable"; exit 1 }

# 1 bis. Garde, une extraction par jour.
# La tache reessaie toutes les 30 minutes tant qu Obsidian est ouvert. Sans
# ce garde, chaque reessai relancerait le modele des qu une nouvelle session
# existe, jusqu a 48 fois par jour.
# Le rattrapage historique avec -Jusqu est exempte, sinon on ne pourrait pas
# enchainer les lots dans la meme journee.
if (-not $Jusqu -and -not $Sec) {
    if ((Test-Path $jourFait) -and ((Get-Content $jourFait -TotalCount 1).Trim() -eq $aujourdhui)) {
        Note "saute, extraction deja faite aujourd hui"
        exit 0
    }
}

# 2. Le pre-filtre. Deterministe, aucun token depense ici.
$argsPy = @($prefiltre, $travail, $marqueur)
if ($Jusqu) { $argsPy += $Jusqu }
& $python @argsPy | Out-Null
if ($LASTEXITCODE -ne 0) { Note "ECHEC du pre-filtre, code $LASTEXITCODE"; exit 1 }

$resultat = Join-Path $travail 'resultat.txt'
if (-not (Test-Path $resultat)) { Note "ECHEC, le pre-filtre n a rien ecrit"; exit 1 }

$vals = @{}
foreach ($l in (Get-Content $resultat -Encoding utf8)) {
    if ($l -match '^([a-z]+)=(.*)$') { $vals[$matches[1]] = $matches[2] }
}
$sessions = [int]$vals['sessions']
$octets   = [int]$vals['octets']
$maxi     = $vals['maxi']

if ($sessions -eq 0) {
    Note "rien de neuf depuis $($vals['depuis'])"
    exit 0
}

$ko = [math]::Round($octets / 1024, 1)
Note "pre-filtre, $sessions session(s), $ko Ko a lire, depuis $($vals['depuis'])"

if ($Sec) {
    Note "mode sec, le modele n est pas appele"
    Write-Output "$sessions session(s), $ko Ko dans $travail"
    exit 0
}

# 3. Ce que l extracteur doit savoir, calcule ici et pas devine par lui
$semaine = Get-SemaineIso $maintenant
$lignes = @(
    "date=$aujourdhui",
    "semaine=$semaine",
    "sessions=$sessions"
)
Set-Content -Path $contexte -Value $lignes -Encoding utf8

# 4. Le passage
Set-Location $coffre
$avant = (git rev-parse --short HEAD).Trim()
Note "debut de l extraction, commit avant $avant, semaine $semaine"
$chrono = [Diagnostics.Stopwatch]::StartNew()

$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele
$code = $LASTEXITCODE
$chrono.Stop()
$duree = [math]::Round($chrono.Elapsed.TotalSeconds, 1)

if ($code -ne 0) {
    Note "ECHEC de l extraction, code $code, apres $duree s"
    if ($sortie) { Note "sortie : $sortie" }
    Note "marqueur inchange, les memes sessions seront relues au prochain passage"
    exit 1
}

foreach ($l in @($sortie)) { if ($l) { Note "dit : $l" } }

# 5. Filet, au cas ou il aurait oublie d enregistrer
git add -A 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Transcriptions, $aujourdhui, enregistrement de secours"
    Note "commit de secours, il avait laisse des choses non enregistrees"
}

$apres = (git rev-parse --short HEAD).Trim()
if ($apres -eq $avant) {
    Note "fin de l extraction en $duree s, rien depose"
} else {
    Note "fin de l extraction en $duree s, commit apres $apres, annuler avec git revert $apres"
}

# 6. Avancer le marqueur, seulement maintenant que le passage a reussi
Set-Content -Path $marqueur -Value $maxi -Encoding utf8
Note "marqueur avance a $maxi"

# 6 bis. Marquer la journee comme faite, pour les reessais du bibliothecaire.
# En ascii, volontairement : Set-Content -Encoding utf8 ajouterait un BOM que
# la comparaison ci-dessus lirait comme un caractere de plus.
Set-Content -Path $jourFait -Value $aujourdhui -Encoding ascii

# 7. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}
