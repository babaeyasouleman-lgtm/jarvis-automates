# Le bibliothecaire du coffre Obsidian. Phase 2 du Plan Jarvis.
# Range 00 Inbox une fois par jour, enregistre avant et apres.
# Ce script ne supprime jamais rien. Aucune commande de suppression.
#
# Aucun accent dans ce fichier, volontairement. PowerShell 5.1 lit les .ps1
# en ANSI et abimerait les accents. Tout le texte accentue vit dans consigne.md,
# que Claude lit lui-meme en UTF8.
#
# Lancement manuel, en ignorant les deux gardes :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\bibliothecaire\passage.ps1 -Manuel

param([switch]$Manuel)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre   = 'C:\Obsidian\Second Brain'
$base     = 'C:\Obsidian\bibliothecaire'
$consigne = Join-Path $base 'consigne.md'
$contexte = Join-Path $base 'contexte.txt'
$marqueur = Join-Path $base 'dernier-passage.txt'
$journal  = Join-Path $base 'journal.log'
$compteur = Join-Path $base 'essais.txt'
$claude   = 'C:\Users\Administrator\.local\bin\claude.exe'
$modele   = 'opus'
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

# 0. La phase 2 bis, les transcriptions Claude Code.
# Elle depose dans 00 Inbox ce que le bibliothecaire rangera juste apres.
# Elle passe avant les deux gardes ci-dessous, volontairement : elle n ecrit
# que des fichiers neufs, donc Obsidian ouvert ne la gene pas. Son propre
# marqueur la rend idempotente, deux lancements le meme jour ne doublent rien.
$extraction = 'C:\Obsidian\transcriptions\extraction.ps1'
if (Test-Path $extraction) {
    & powershell -ExecutionPolicy Bypass -File $extraction
    Note "extraction des transcriptions, code $LASTEXITCODE"
} else {
    Note "extraction.ps1 introuvable, on passe directement au rangement"
}

# 1. Garde, deja passe aujourd hui
if (-not $Manuel) {
    if ((Test-Path $marqueur) -and ((Get-Content $marqueur -TotalCount 1).Trim() -eq $aujourdhui)) {
        Note "saute, deja passe aujourd hui"
        exit 0
    }
}

# 2. Garde, Obsidian ouvert. On attend et on reessaie au lieu d abandonner
# la journee, la tache se redeclenche toutes les 30 minutes.
# Soupape : apres 6 refus, soit trois heures d attente, on range quand meme.
# Sans elle, une journee ou Obsidian reste ouvert ne se rangerait jamais,
# et la boite se remplirait sans fin.
$refusMax = 6
if (-not $Manuel) {
    if (Get-Process Obsidian -ErrorAction SilentlyContinue) {
        $refus = 0
        if (Test-Path $compteur) {
            $c = ((Get-Content $compteur -TotalCount 1).Trim()) -split ' '
            if ($c[0] -eq $aujourdhui) { $refus = [int]$c[1] }
        }
        $refus = $refus + 1
        if ($refus -lt $refusMax) {
            Set-Content -Path $compteur -Value "$aujourdhui $refus" -Encoding ascii
            Note "Obsidian est ouvert, refus $refus sur $refusMax. Nouvel essai dans 30 minutes"
            exit 0
        }
        Note "Obsidian ouvert depuis $refus essais, on range quand meme"
    }
}

# 3. Verifications
if (-not (Test-Path $claude))   { Note "ECHEC, claude.exe introuvable"; exit 1 }
if (-not (Test-Path $consigne)) { Note "ECHEC, consigne.md introuvable"; exit 1 }
if (-not (Test-Path $coffre))   { Note "ECHEC, coffre introuvable"; exit 1 }

Set-Location $coffre

# 4. Enregistrer l etat avant le passage, pour que l annulation soit propre
git add -A 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Avant le bibliothecaire, $aujourdhui"
    Note "commit avant le passage"
}
$avant = (git rev-parse --short HEAD).Trim()

# 5. Ce que le bibliothecaire doit savoir, calcule ici et pas devine par lui
$semaine = Get-SemaineIso $maintenant
$jourSem = [int]$maintenant.DayOfWeek        # 0 dimanche, 1 lundi
$revue   = if ($jourSem -eq 0 -or $jourSem -eq 1) { 'oui' } else { 'non' }

$lignes = @(
    "date=$aujourdhui",
    "semaine=$semaine",
    "revue_hebdo=$revue",
    "commit_avant=$avant"
)
Set-Content -Path $contexte -Value $lignes -Encoding utf8

# 6. Le passage
Note "debut du passage, commit avant $avant, semaine $semaine, revue $revue"
$chrono = [Diagnostics.Stopwatch]::StartNew()

$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele
$code = $LASTEXITCODE
$chrono.Stop()

$duree = [math]::Round($chrono.Elapsed.TotalSeconds, 1)

if ($code -ne 0) {
    Note "ECHEC du passage, code $code, apres $duree s"
    if ($sortie) { Note "sortie : $sortie" }
    exit 1
}

foreach ($l in @($sortie)) { if ($l) { Note "dit : $l" } }

# 7. Filet de securite, au cas ou il aurait oublie d enregistrer
git add -A 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Bibliothecaire, $aujourdhui, enregistrement de secours"
    Note "commit de secours, il avait laisse des choses non enregistrees"
}

$apres = (git rev-parse --short HEAD).Trim()

if ($apres -eq $avant) {
    Note "fin du passage en $duree s, rien a ranger"
} else {
    Note "fin du passage en $duree s, commit apres $apres, annuler avec git revert $apres"
}

# 8. Pousser
$retard = git rev-list --count '@{u}..HEAD' 2>$null
if ($retard -and [int]$retard -gt 0) {
    git push -q origin main
    if ($?) { Note "pousse, $retard commit(s)" } else { Note "ECHEC push, $retard commit(s) en attente" }
}

# 9. Marquer la journee comme faite
Set-Content -Path $marqueur -Value $aujourdhui -Encoding utf8

# 10. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}
