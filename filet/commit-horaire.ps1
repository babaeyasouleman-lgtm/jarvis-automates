# Filet du coffre Obsidian. Phase 1 du Plan Jarvis.
# Enregistre et pousse le coffre chaque heure.
# Ce script ne supprime jamais rien. Aucune commande de suppression.

$coffre  = 'C:\Obsidian\Second Brain'
$journal = 'C:\Obsidian\filet\journal.log'

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

Set-Location $coffre

# 1. Enregistrer ce qui a change
git add -A
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $horodatage = Get-Date -Format 'yyyy-MM-dd HH:mm'
    $nb = (git diff --cached --name-only | Measure-Object -Line).Lines
    git commit -q -m "Filet horaire $horodatage, $nb fichier(s)"
    if ($?) { Note "commit, $nb fichier(s)" } else { Note "ECHEC commit" }
}

# 2. Pousser, y compris les commits restes en arriere si le reseau etait coupe
$retard = git rev-list --count '@{u}..HEAD' 2>$null
if ($retard -and [int]$retard -gt 0) {
    git push -q origin main
    if ($?) { Note "pousse, $retard commit(s)" } else { Note "ECHEC push, $retard commit(s) en attente" }
}

# 3. Garder le journal court
if (Test-Path $journal) {
    $lignes = Get-Content $journal
    if ($lignes.Count -gt 500) {
        $lignes | Select-Object -Last 300 | Set-Content -Path $journal -Encoding utf8
    }
}
