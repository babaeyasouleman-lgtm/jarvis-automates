# Export du cerveau. Phase 6 du Plan Jarvis, 8 septembre 2026.
#
# Il copie une partie du coffre vers un depot prive separe, jarvis-cerveau,
# que l agent WhatsApp tire toutes les heures pour repondre a mes questions.
#
# Il ne juge rien. Il ne fait aucun appel a un modele. Il copie et il pousse.
# C est un cousin de filet\commit-automates.ps1, pas d un automate qui pense.
#
# Ce qui part est decide par liste-blanche.txt, jamais par ce script.
# Un dossier absent de cette liste ne part pas, meme cree apres coup. C est
# tout l interet d une liste blanche : l oubli va dans le sens sur.
#
# Ce script ne supprime rien dans le coffre. Aucune commande de suppression ne
# vise C:\Obsidian\Second Brain. Il regenere en revanche son propre miroir,
# le dossier depot\, ou robocopy /MIR reflete la source : une note retiree du
# coffre disparait de l export, et un dossier retire de la liste blanche est
# retire du depot au passage suivant. Un miroir se refait en une commande.
#
# Aucun accent dans ce fichier, PowerShell 5.1 lit les .ps1 en ANSI. Les noms
# accentues du coffre viennent du disque ou de liste-blanche.txt, lu en UTF-8.
#
# Lancement a la main :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\cerveau\export.ps1

# ---------------------------------------------------------------- reglages
$coffre  = 'C:\Obsidian\Second Brain'
$base    = 'C:\Obsidian\cerveau'
$depot   = Join-Path $base 'depot'
$liste   = Join-Path $base 'liste-blanche.txt'
$journal = Join-Path $base 'journal.log'
$distant = 'https://github.com/babaeyasouleman-lgtm/jarvis-cerveau.git'
$python  = 'C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe'
$indexPy = 'C:\Obsidian\bibliothecaire\index.py'
$dossierDomaines = '03 Domaines'
# -------------------------------------------------------------------------

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

# 1. Lire la liste blanche. Sans elle, on ne devine pas : on s arrete.
if (-not (Test-Path $liste))  { Note "ECHEC, liste-blanche.txt introuvable, rien n est exporte"; exit 1 }
if (-not (Test-Path $coffre)) { Note "ECHEC, coffre introuvable"; exit 1 }

$racines  = @()
$domaines = @()
foreach ($l in (Get-Content $liste -Encoding UTF8)) {
    $t = $l.Trim()
    if (-not $t -or $t.StartsWith('#')) { continue }
    $i = $t.IndexOf('=')
    if ($i -lt 0) { continue }
    $cle = $t.Substring(0, $i).Trim()
    $val = $t.Substring($i + 1).Trim()
    if (-not $val) { continue }
    if ($cle -eq 'racine')  { $racines  += $val }
    if ($cle -eq 'domaine') { $domaines += $val }
}
if ($racines.Count -eq 0) { Note "ECHEC, aucune racine dans la liste blanche, rien n est exporte"; exit 1 }

# 2. Le depot local. Il est clone une seule fois, a la premiere execution.
if (-not (Test-Path (Join-Path $depot '.git'))) {
    New-Item -ItemType Directory -Path $depot -Force | Out-Null
    & git clone -q $distant $depot 2>&1 | Out-Null
    if (-not (Test-Path (Join-Path $depot '.git'))) { Note "ECHEC, clone de jarvis-cerveau impossible"; exit 1 }
    Note "depot clone dans $depot"
}

# 3. Ce que le coffre contient et qui ne part pas. Ecrit au journal pour que
# l oubli se voie : un dossier neuf reste sur le PC en silence sinon.
$ecartes = @()
foreach ($d in (Get-ChildItem -Path $coffre -Directory)) {
    if ($racines -notcontains $d.Name) { $ecartes += $d.Name }
}
if ($ecartes.Count -gt 0) { Note ("hors liste blanche, reste sur le PC : " + ($ecartes -join ', ')) }

# 4. La copie, une racine a la fois.
$exclusFichiers = @('*.local.*', '.env', '.env.*')
$copies = 0
foreach ($r in $racines) {
    $src = Join-Path $coffre $r
    $dst = Join-Path $depot $r
    if (-not (Test-Path $src)) { Note "absent du coffre, rien a exporter : $r"; continue }

    # Les sous-dossiers a exclure sont calcules, pas ecrits en dur : tout
    # sous-dossier de 03 Domaines absent de la liste blanche est exclu, y
    # compris un cree demain. "Moi" en fait partie et n y sera jamais ajoute.
    $exclusDossiers = @('.git', '.obsidian')
    if ($r -eq $dossierDomaines) {
        foreach ($sd in (Get-ChildItem -Path $src -Directory)) {
            if ($domaines -notcontains $sd.Name) {
                $exclusDossiers += $sd.FullName
                Note "domaine hors liste blanche, reste sur le PC : $r\$($sd.Name)"
            }
        }
    }

    & robocopy $src $dst /MIR /XD $exclusDossiers /XF $exclusFichiers /R:1 /W:1 /NFL /NDL /NJH /NJS /NP | Out-Null
    if ($LASTEXITCODE -ge 8) { Note "ECHEC robocopy $r, code $LASTEXITCODE"; exit 1 }
    $copies = $copies + 1
}

# 5. Retirer du miroir ce qui n est plus dans la liste blanche. Sans ca, un
# dossier retire de la liste resterait publie pour toujours.
foreach ($d in (Get-ChildItem -Path $depot -Directory)) {
    if ($d.Name -eq '.git') { continue }
    if ($racines -notcontains $d.Name) {
        Remove-Item -Path $d.FullName -Recurse -Force
        Note "retire du depot, il n est plus dans la liste blanche : $($d.Name)"
    }
}

# 6. Le garde. Ceinture apres les bretelles : on relit ce qui est reellement
# dans le miroir et on refuse de pousser si un seul fichier vient d ailleurs
# que de la liste blanche. Le coffre porte un dossier d immigration, des
# revenus et un couple. Une copie qui derape ne doit pas atteindre GitHub.
$intrus = @()
foreach ($f in (Get-ChildItem -Path $depot -Recurse -File)) {
    $rel = $f.FullName.Substring($depot.Length).TrimStart([char]92)
    if ($rel.StartsWith('.git')) { continue }
    $bouts = $rel -split [regex]::Escape([string][char]92)
    if ($bouts.Count -eq 1) { continue }
    if ($racines -notcontains $bouts[0]) { $intrus += $rel; continue }
    if ($bouts[0] -eq $dossierDomaines -and $bouts.Count -ge 2) {
        if ($domaines -notcontains $bouts[1]) { $intrus += $rel }
    }
}
if ($intrus.Count -gt 0) {
    Note "ECHEC du garde, $($intrus.Count) fichier(s) hors liste blanche dans le miroir. RIEN N EST POUSSE"
    foreach ($i in ($intrus | Select-Object -First 10)) { Note "  intrus : $i" }
    exit 1
}

# 7. La table des matieres. C est index.py du bibliothecaire, pointe sur le
# miroir au lieu du coffre : il produit alors la table de ce qui est exporte,
# et rien de plus. Aucun modele, une seconde, zero token.
$notes = 0
if (Test-Path $indexPy) {
    if (-not (Test-Path $python)) {
        $repli = Get-Command python -ErrorAction SilentlyContinue
        if ($repli) { $python = $repli.Source }
    }
    if (Test-Path $python) {
        & $python $indexPy $depot (Join-Path $depot 'index.txt') | Out-Null
        if ($LASTEXITCODE -eq 0) {
            $notes = (Get-Content (Join-Path $depot 'index.txt') -Encoding UTF8 | Measure-Object -Line).Lines
            Note "table des matieres, $notes notes"
        } else {
            Note "ECHEC de l index, code $LASTEXITCODE. On pousse quand meme, l agent le dira"
        }
    } else { Note "index saute, python introuvable" }
} else { Note "index.py introuvable, pas de table des matieres" }

# 8. La fraicheur. C est ce fichier, et pas la date d un commit, qui dit a
# l agent de quand date ce qu il lit. S il n est pas relu, l agent voit un
# export vieux et le dit : le silence n est jamais pris pour du frais.
$maintenant = Get-Date
Set-Content -Path (Join-Path $depot 'fraicheur.txt') -Encoding ascii -Value @(
    "export=$($maintenant.ToString('o'))",
    "notes=$notes"
)

# 9. Enregistrer et pousser.
# Garde : si un autre git tourne deja dans ce depot, on s arrete. Le cas se
# produit quand ce script est lance a la main pendant que la tache Windows
# le lance aussi. Ce n est pas un verrou complet, c est le meme reflexe que
# le verrou du bibliothecaire : deux ecrivains sur un depot, jamais.
if (Test-Path (Join-Path $depot '.git\index.lock')) {
    Note "saute, un autre git tourne deja dans le depot du cerveau"
    exit 0
}

Set-Location $depot
& git add -A 2>&1 | Out-Null
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $nb = (& git diff --cached --name-only | Measure-Object -Line).Lines
    & git commit -q -m ("Export du cerveau {0}, {1} note(s)" -f $maintenant.ToString('yyyy-MM-dd HH:mm'), $notes)
    if ($?) { Note "commit, $nb fichier(s)" } else { Note "ECHEC commit"; exit 1 }
} else {
    Note "rien a enregistrer"
}

$retard = & git rev-list --count '@{u}..HEAD' 2>$null
if (-not $retard) { $retard = & git rev-list --count HEAD 2>$null }
if ($retard -and [int]$retard -gt 0) {
    & git push -q -u origin HEAD 2>$null
    if ($?) { Note "pousse, $retard commit(s), $notes notes, $copies racine(s)" }
    else    { Note "ECHEC push, $retard commit(s) en attente" }
}

# 10. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 500) { $l | Select-Object -Last 300 | Set-Content -Path $journal -Encoding utf8 }
}
