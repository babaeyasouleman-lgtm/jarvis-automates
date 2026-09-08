# Le deversement des captures. Phase 7 du Plan Jarvis, 8 septembre 2026.
#
# L agent WhatsApp ecrit ses captures dans sa boite aux lettres, sur son volume
# Railway, puis les pousse dans un depot a lui, jarvis-captures. Ce script les
# tire et les depose dans 00 Inbox. Le bibliothecaire range ensuite, comme il
# range les courriels et les reunions.
#
# Il ne juge rien. Il n appelle aucun modele. Il tire, il copie, il enregistre.
# C est un cousin de cerveau\export.ps1, dans l autre sens, pas d un automate
# qui pense.
#
# Le PC reste le seul ecrivain du coffre. L agent n a aucun jeton sur le depot
# du coffre, et ce script n en pousse aucun vers jarvis-captures : un seul
# ecrivain de chaque cote. C est toute la decision du 8 septembre 2026.
#
# Ce script ne supprime rien. Ni dans le coffre, ni dans le depot des captures.
# Une capture deversee reste dans jarvis-captures pour toujours ; ce qui
# l empeche de revenir n est pas une suppression, ce sont les deux filets.
#
# ----- Les deux filets contre le doublon, et lequel compte vraiment ---------
#
# deposes.txt porte les identifiants. C est LE filet : un identifiant vu ne
# revient jamais, meme si le marqueur recule. Le lanceur seul l ecrit, et
# seulement apres reussite.
#
# marqueur.txt porte l identifiant le plus recent deverse. Les identifiants
# sont horodates, donc ils se trient. Il sert a deux choses, pas a filtrer par
# lui-meme : redemarrer proprement si deposes.txt est perdu, et borner la
# taille de deposes.txt sans risque, puisque tout ce qui est plus vieux que le
# marqueur est deja couvert par lui.
#
# La regle exacte : on saute une capture si son identifiant est dans
# deposes.txt, OU s il est plus ancien que le marqueur alors que deposes.txt ne
# le connait pas, ce qui veut dire que deposes.txt a ete tronque.
#
# La limite connue de cette regle : une capture qui arriverait dans le depot
# APRES une plus recente, et absente de deposes.txt, serait refusee. Ca ne peut
# pas se produire en usage normal, parce que l agent pousse tout son lot d un
# coup et que l ordre est donc preserve. Ca ne se produirait qu apres une
# restauration du volume Railway depuis une sauvegarde. Le remede, ce jour-la :
# vider marqueur.txt, deposes.txt suffit a lui seul.
#
# Aucun accent dans ce fichier, PowerShell 5.1 lit les .ps1 en ANSI. Les titres
# accentues viennent du disque, lus en UTF-8.
#
# Lancement a la main :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\captures\captures.ps1
# Voir ce qui serait deverse, sans rien ecrire :
#   ... \captures.ps1 -Sec

param(
    [switch]$Sec
)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre   = 'C:\Obsidian\Second Brain'
$base     = 'C:\Obsidian\captures'
$depot    = Join-Path $base 'depot'
$journal  = Join-Path $base 'journal.log'
$marqueur = Join-Path $base 'marqueur.txt'
$deposes  = Join-Path $base 'deposes.txt'
$distant  = 'https://github.com/babaeyasouleman-lgtm/jarvis-captures.git'
$inbox    = Join-Path $coffre '00 Inbox'
$plafondDeposes = 2000
# -------------------------------------------------------------------------

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

# 1. Verifications
if (-not (Test-Path $coffre)) { Note "ECHEC, coffre introuvable"; exit 1 }
if (-not (Test-Path $inbox))  { Note "ECHEC, 00 Inbox introuvable"; exit 1 }

# 1 bis. Garde, un seul git a la fois dans le coffre. Le verrou de passage.ps1
# couvre l enchainement, pas un lancement a la main pendant que la tache
# Windows tourne. Ce n est pas un verrou complet, c est le meme reflexe que
# celui de export.ps1 : deux ecrivains sur un depot, jamais. Une relance
# suivante deversera, rien n est perdu.
if (-not $Sec -and (Test-Path (Join-Path $coffre '.git\index.lock'))) {
    Note "saute, un autre git tourne deja dans le coffre"
    exit 0
}

# 2. Le depot local des captures. Clone une seule fois, tire ensuite.
# Un echec de tirage n est pas une panne : on travaille sur ce qu on a deja,
# et les captures manquantes viendront au passage suivant. C est le meme
# raisonnement que le pull horaire du cerveau cote agent.
if (-not (Test-Path (Join-Path $depot '.git'))) {
    New-Item -ItemType Directory -Path $depot -Force | Out-Null
    & git clone -q $distant $depot 2>&1 | Out-Null
    if (-not (Test-Path (Join-Path $depot '.git'))) {
        Note "ECHEC, clone de jarvis-captures impossible. Le depot existe-t-il ?"
        exit 1
    }
    Note "depot clone dans $depot"
} else {
    & git -C $depot pull --ff-only -q 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) { Note "tirage echoue, on travaille sur la copie locale" }
}

$source = Join-Path $depot 'captures'
if (-not (Test-Path $source)) {
    Note "rien a deverser, le depot ne contient aucune capture"
    exit 0
}

# 3. Ce qui a deja ete deverse.
$deja = @{}
if (Test-Path $deposes) {
    foreach ($l in (Get-Content $deposes -Encoding utf8)) {
        $t = $l.Trim()
        if ($t) { $deja[$t] = $true }
    }
}
$borne = ''
if (Test-Path $marqueur) { $borne = (Get-Content $marqueur -TotalCount 1).Trim() }

# 4. Le tri. Rien n est ecrit ici, on decide seulement.
$aDeverser = @()
$sautes = 0
foreach ($f in (Get-ChildItem -Path $source -Filter '*.md' -File | Sort-Object Name)) {
    # L identifiant vit dans le frontmatter, ligne "capture:". C est lui qui
    # est stable, pas le nom du fichier : deux captures peuvent porter le meme
    # titre le meme jour.
    $id = ''
    foreach ($l in (Get-Content $f.FullName -Encoding utf8 -TotalCount 12)) {
        if ($l -match '^capture:\s*(\S+)\s*$') { $id = $matches[1]; break }
    }
    if (-not $id) {
        Note "sans identifiant, ignore : $($f.Name)"
        continue
    }
    if ($deja.ContainsKey($id)) { $sautes = $sautes + 1; continue }
    if ($borne -and ([string]::Compare($id, $borne, [StringComparison]::Ordinal) -le 0)) {
        # Plus vieux que le marqueur et absent de deposes.txt : deposes.txt a
        # ete tronque. Le marqueur prend le relais, sinon tout le depot
        # repartirait dans 00 Inbox a la premiere troncature.
        $sautes = $sautes + 1
        continue
    }
    $aDeverser += [pscustomobject]@{ Id = $id; Fichier = $f }
}

if ($Sec) {
    Write-Output "marqueur=$borne"
    Write-Output "deja=$($deja.Count)"
    Write-Output "a_deverser=$($aDeverser.Count)"
    foreach ($c in $aDeverser) { Write-Output "  $($c.Id)  $($c.Fichier.Name)" }
    Note "mode sec, rien deverse, marqueur inchange"
    exit 0
}

if ($aDeverser.Count -eq 0) {
    Note "rien de neuf, $sautes capture(s) deja vue(s)"
    exit 0
}

# 5. Le deversement. Copie, jamais deplacement : le depot garde l original.
# Un nom deja pris dans 00 Inbox recoit un suffixe plutot que d ecraser une
# note. Ecraser serait la seule facon de perdre quelque chose ici.
$copies = 0
$reussis = @()
$maxi = $borne
foreach ($c in $aDeverser) {
    $cible = Join-Path $inbox $c.Fichier.Name
    if (Test-Path $cible) {
        $sansExt = [IO.Path]::GetFileNameWithoutExtension($c.Fichier.Name)
        $n = 2
        while (Test-Path $cible) {
            $cible = Join-Path $inbox ("{0} ({1}).md" -f $sansExt, $n)
            $n = $n + 1
        }
        Note "nom deja pris, deverse sous $([IO.Path]::GetFileName($cible))"
    }
    try {
        Copy-Item -Path $c.Fichier.FullName -Destination $cible -ErrorAction Stop
        $copies = $copies + 1
        $reussis += $c.Id
        if ([string]::Compare($c.Id, $maxi, [StringComparison]::Ordinal) -gt 0) { $maxi = $c.Id }
    } catch {
        Note "ECHEC de copie pour $($c.Fichier.Name) : $($_.Exception.Message)"
    }
}

if ($copies -eq 0) {
    Note "aucune capture copiee, marqueur inchange"
    exit 1
}

# 6. Enregistrer, par chemin et pas avec git add -A. Le passage tourne pendant
# que Souleman peut avoir des choses en cours dans le coffre, et un git add -A
# les embarquerait dans un commit qui dit Captures.
Set-Location $coffre
& git add -- "00 Inbox" 2>&1 | Out-Null
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $aujourdhui = (Get-Date).ToString('yyyy-MM-dd')
    & git commit -q -m "Captures de l agent, $aujourdhui" -- "00 Inbox"
    if ($?) {
        $hash = (& git rev-parse --short HEAD).Trim()
        Note "$copies capture(s) deversee(s), commit $hash, annuler avec git revert $hash"
    } else {
        Note "ECHEC commit, marqueur inchange, les memes captures reviendront"
        exit 1
    }
} else {
    Note "$copies capture(s) copiee(s), rien a enregistrer cote git"
}

# 7. Les deux filets, avances seulement maintenant que le passage a reussi.
# deposes.txt d abord : c est lui qui compte. Le marqueur ensuite, et jamais
# au-dela de ce que deposes.txt porte, sinon une troncature perdrait des
# captures au lieu d en proteger.
Add-Content -Path $deposes -Value $reussis -Encoding ascii
Note "$($reussis.Count) identifiant(s) inscrits dans deposes.txt"

$tout = @(Get-Content $deposes -Encoding utf8 | Where-Object { $_.Trim() })
if ($tout.Count -gt $plafondDeposes) {
    $garde = $tout | Select-Object -Last ([int]($plafondDeposes / 2))
    Set-Content -Path $deposes -Value $garde -Encoding ascii
    Note "deposes.txt ramene a $($garde.Count) lignes, le marqueur couvre le reste"
}

Set-Content -Path $marqueur -Value $maxi -Encoding ascii
Note "marqueur avance a $maxi"

# 8. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}
