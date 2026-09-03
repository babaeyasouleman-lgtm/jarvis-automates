# Filet des automates. Entretien du Plan Jarvis, point 3.
# Sauvegarde chaque heure ce qui fait tourner l equipe et qui n est
# sous aucun git : les consignes et lanceurs de C:\Obsidian, les skills
# maison, les taches planifiees de l app, et la memoire Claude.
# Depot : C:\Obsidian, pousse vers babaeyasouleman-lgtm/jarvis-automates.
# Le coffre, C:\Obsidian\Second Brain, a son propre depot et est ignore ici.
#
# Ce script ne supprime rien hors du dossier miroir, qu il regenere.
# Aucun accent dans ce fichier, PowerShell 5.1 lit les .ps1 en ANSI.

$racine  = 'C:\Obsidian'
$miroir  = Join-Path $racine 'miroir'
$journal = Join-Path $racine 'filet\journal-automates.log'
$skills  = 'C:\Users\Administrator\.claude\skills'
$taches  = 'C:\Users\Administrator\.claude\scheduled-tasks'
$memoire = 'C:\Users\Administrator\.claude\projects\C--Users-Administrator-OneDrive-Bureau\memory'

# Les skills maison seulement. Les skills installes, gstack et autres,
# se reinstallent et pesent plus d un Go.
$skillsMaison = @('agent-vocal', 'devis', 'prospect-site', 'prospect-email', 'no-ai-slop')

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

# 1. Le miroir. /MIR reflete la source, /XD et /XF excluent ce qui ne
# doit jamais partir : dependances, caches, fichiers de cles.
$exclusDossiers = @('node_modules', '__pycache__', '.git')
$exclusFichiers = @('*.local.*', '.env', '.env.*', '*.pyc')
$sources = @()
foreach ($s in $skillsMaison) {
    $src = Join-Path $skills $s
    if (Test-Path $src) { $sources += @{ src = $src; dst = (Join-Path $miroir "skills\$s") } }
}
$sources += @{ src = $taches;  dst = (Join-Path $miroir 'scheduled-tasks') }
$sources += @{ src = $memoire; dst = (Join-Path $miroir 'memoire') }

foreach ($p in $sources) {
    & robocopy $p.src $p.dst /MIR /XD $exclusDossiers /XF $exclusFichiers /R:1 /W:1 /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { Note "ECHEC robocopy $($p.src), code $LASTEXITCODE" }
}

# 2. Enregistrer ce qui a change
Set-Location $racine
git add -A 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $horodatage = Get-Date -Format 'yyyy-MM-dd HH:mm'
    $nb = (git diff --cached --name-only | Measure-Object -Line).Lines
    git commit -q -m "Filet automates $horodatage, $nb fichier(s)"
    if ($?) { Note "commit, $nb fichier(s)" } else { Note "ECHEC commit" }
}

# 3. Pousser, si le depot distant existe. Tant qu il n existe pas sur
# GitHub, la poussee echoue et se retente a l heure suivante.
$retard = git rev-list --count '@{u}..HEAD' 2>$null
if (-not $retard) { $retard = git rev-list --count HEAD 2>$null }
if ($retard -and [int]$retard -gt 0) {
    git push -q -u origin main 2>$null
    if ($?) { Note "pousse, $retard commit(s)" } else { Note "ECHEC push, $retard commit(s) en attente. Le depot jarvis-automates existe-t-il sur GitHub ?" }
}

# 4. Garder le journal court
if (Test-Path $journal) {
    $lignes = Get-Content $journal
    if ($lignes.Count -gt 500) {
        $lignes | Select-Object -Last 300 | Set-Content -Path $journal -Encoding utf8
    }
}
