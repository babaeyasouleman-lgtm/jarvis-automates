# Le deversement de la boite aux lettres. Phase 7 du Plan Jarvis, 8 septembre
# 2026, elargi aux billets a la phase 8 le meme jour.
#
# L agent WhatsApp ecrit dans sa boite aux lettres, sur son volume Railway,
# puis pousse dans un depot a lui, jarvis-captures. Ce script tire ce depot et
# range ce qu il y trouve. C est le PC qui ecrit dans le coffre, jamais l agent,
# et la phase 8 n a pas rouvert cette question.
#
# ----- Trois destinations, une seule ligne d adresse ------------------------
#
# La cle type: du frontmatter decide, et rien d autre :
#
#   type: capture          -> 00 Inbox. Le bibliothecaire range ensuite.
#   type: billet           -> 08 Billets, un fichier neuf. Le bibliothecaire
#                             n y touche jamais, c est dans sa consigne.
#   type: reponse-billet   -> ajoute sous la section Question du billet que
#                             la cle billet: designe, et si ce billet etait
#                             bloque, il repasse a faire.
#
# Une deuxieme boite aux lettres aurait voulu dire un deuxieme depot, un
# deuxieme clone, un deuxieme jeu de filets contre le doublon et un deuxieme
# endroit ou une panne reseau peut perdre quelque chose. Le tuyau de la phase 7
# transporte deja des fichiers texte identifies : il ne manquait qu une adresse.
#
# Il ne juge rien. Il n appelle aucun modele. Il tire, il copie, il enregistre.
# C est un cousin de cerveau\export.ps1, dans l autre sens, pas d un automate
# qui pense. Faire repasser un billet repondu de bloque a a faire n est pas un
# jugement : une question repondue ne bloque plus, c est mecanique.
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
$billets  = Join-Path $coffre '08 Billets'
# Le vocabulaire des billets vit avec le preneur, pas ici : deux copies d une
# liste de mots finissent par diverger, et celle-ci decide d un etat ecrit
# dans le coffre.
$motsTxt  = 'C:\Obsidian\billets\mots.txt'
$plafondDeposes = 2000
# -------------------------------------------------------------------------

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

# Un nom qui n ecrase rien. Ecraser serait la seule facon de perdre quelque
# chose ici, donc on suffixe, dans 00 Inbox comme dans 08 Billets.
function Get-NomLibre($dossier, $nom) {
    $cible = Join-Path $dossier $nom
    if (-not (Test-Path $cible)) { return $cible }
    $sansExt = [IO.Path]::GetFileNameWithoutExtension($nom)
    $n = 2
    while (Test-Path $cible) {
        $cible = Join-Path $dossier ("{0} ({1}).md" -f $sansExt, $n)
        $n = $n + 1
    }
    return $cible
}

# Le corps d un fichier de la boite, sans son frontmatter ni son titre de
# transport. La boite pose un titre sur tout ce qui la traverse, ce qui est
# juste pour une capture qui devient une note, et faux pour une reponse qui
# devient deux lignes dans une note existante : sans ce retrait, le titre
# atterrissait au milieu de la phrase de Souleman. Vu au premier passage de
# bout en bout, phase 8.
#
# Les retours a la ligne sont gardes. Une reponse d une ligne ne change pas,
# une reponse de trois paragraphes reste lisible au lieu de devenir un mur.
function Get-Corps($chemin) {
    $lignes = @(Get-Content $chemin -Encoding utf8)
    if ($lignes.Count -gt 0 -and $lignes[0].Trim() -eq '---') {
        $i = 1
        while ($i -lt $lignes.Count -and $lignes[$i].Trim() -ne '---') { $i = $i + 1 }
        if ($i + 1 -le $lignes.Count - 1) { $lignes = @($lignes[($i + 1)..($lignes.Count - 1)]) }
        else { $lignes = @() }
    }
    # Le titre de transport, et les lignes vides qui le suivent.
    while ($lignes.Count -gt 0 -and -not $lignes[0].Trim()) { $lignes = @($lignes[1..($lignes.Count - 1)]) }
    if ($lignes.Count -gt 0 -and $lignes[0] -match '^#\s+\S') {
        if ($lignes.Count -gt 1) { $lignes = @($lignes[1..($lignes.Count - 1)]) } else { $lignes = @() }
    }
    return (($lignes -join "`n").Trim())
}

# Le billet que designe un identifiant, ou $null. On cherche par la cle
# billet: du frontmatter et jamais par le nom du fichier : le nom peut etre
# renomme dans Obsidian, l identifiant ne bouge pas.
function Get-Billet($dossier, $id) {
    foreach ($f in (Get-ChildItem -Path $dossier -Filter '*.md' -File)) {
        foreach ($l in (Get-Content $f.FullName -Encoding utf8 -TotalCount 20)) {
            if ($l -match '^billet:\s*(\S+)\s*$' -and $matches[1] -eq $id) { return $f }
        }
    }
    return $null
}

# Ecriture UTF-8 SANS BOM. Set-Content -Encoding utf8 en ajoute un sous
# PowerShell 5.1, et un BOM pose au milieu d une note du coffre est un
# caractere de plus que le bibliothecaire lira comme du contenu.
function Set-Texte($chemin, $lignes, $crlf) {
    $fin = "`n"
    if ($crlf) { $fin = "`r`n" }
    [IO.File]::WriteAllText($chemin, (($lignes -join $fin) + $fin), (New-Object Text.UTF8Encoding($false)))
}

# Ajouter une reponse sous la section Question d un billet, et le debloquer.
# Retourne $true si le fichier a ete ecrit.
function Add-Reponse($fichier, $texte, $mots, $jour) {
    $brut = [IO.File]::ReadAllText($fichier.FullName)
    $crlf = $brut.Contains("`r`n")
    $lignes = @($brut -split "`r?`n")
    $marque = $mots['question']
    # La ligne vide de fin n est pas de la coquetterie : sans elle, le titre
    # de la section suivante se colle a la reponse et Obsidian ne le rend plus
    # comme un titre.
    $bloc = @('', ('**{0}, {1}** : {2}' -f $mots['reponse'], $jour, $texte), '')

    $debut = -1
    for ($i = 0; $i -lt $lignes.Count; $i++) {
        if ($lignes[$i].Trim() -eq $marque) { $debut = $i; break }
    }

    if ($debut -lt 0) {
        # Pas de section Question, par exemple un billet ecrit a la main. On
        # ajoute la section a la fin plutot que de perdre la reponse.
        $lignes = @($lignes) + @('', $marque) + $bloc
    } else {
        # La reponse se pose a la FIN de la section, avant le titre suivant :
        # les reponses successives se lisent alors dans l ordre.
        $fin = $lignes.Count
        for ($i = $debut + 1; $i -lt $lignes.Count; $i++) {
            if ($lignes[$i] -match '^##\s') { $fin = $i; break }
        }
        $avant = @($lignes[0..($fin - 1)])
        $apres = @()
        if ($fin -lt $lignes.Count) { $apres = @($lignes[$fin..($lignes.Count - 1)]) }
        $lignes = $avant + $bloc + $apres
    }

    # Une question repondue ne bloque plus. Ce n est pas un jugement, c est
    # mecanique, et c est ce qui fait que le preneur reprend le billet tout
    # seul au passage suivant sans que personne ne touche au coffre a la main.
    # Seule la premiere cle etat: compte, celle du frontmatter.
    for ($i = 0; $i -lt $lignes.Count; $i++) {
        if ($lignes[$i] -match '^etat:\s*(.*)$') {
            if ($matches[1].Trim() -eq $mots['bloque']) { $lignes[$i] = 'etat: ' + $mots['a_faire'] }
            break
        }
    }

    Set-Texte $fichier.FullName $lignes $crlf
    return $true
}

# 1. Verifications
if (-not (Test-Path $coffre)) { Note "ECHEC, coffre introuvable"; exit 1 }
if (-not (Test-Path $inbox))  { Note "ECHEC, 00 Inbox introuvable"; exit 1 }
if (-not (Test-Path $billets)) { New-Item -ItemType Directory -Path $billets -Force | Out-Null }

# 1 ter. Les mots accentues, lus a cote. PowerShell 5.1 lit ce script en ANSI,
# donc ils ne peuvent pas y vivre. Meme reflexe que liste-blanche.txt.
# Leur absence n empeche que les billets : une capture ordinaire n en a pas
# besoin, et il n y a aucune raison de la retenir pour ca.
$mots = @{}
if (Test-Path $motsTxt) {
    foreach ($l in (Get-Content $motsTxt -Encoding UTF8)) {
        $t = $l.Trim()
        if (-not $t -or $t.StartsWith('#')) { continue }
        $i = $t.IndexOf('=')
        if ($i -lt 0) { continue }
        $mots[$t.Substring(0, $i).Trim()] = $t.Substring($i + 1).Trim()
    }
}
$motsOk = $mots.ContainsKey('a_faire') -and $mots.ContainsKey('bloque') `
          -and $mots.ContainsKey('question') -and $mots.ContainsKey('reponse')
if (-not $motsOk) { Note "mots.txt absent ou incomplet, les billets attendront le passage suivant" }

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
    # type: dit ou va le fichier, billet: dit lequel il concerne quand c est
    # une reponse. On lit 20 lignes plutot que 12 depuis la phase 8 : l en-tete
    # d un billet porte neuf cles au lieu de quatre.
    $id = ''
    $type = 'capture'
    $vise = ''
    foreach ($l in (Get-Content $f.FullName -Encoding utf8 -TotalCount 20)) {
        if ($l -match '^capture:\s*(\S+)\s*$') { $id = $matches[1] }
        elseif ($l -match '^type:\s*(\S+)\s*$') { $type = $matches[1] }
        elseif ($l -match '^billet:\s*(\S+)\s*$') { $vise = $matches[1] }
    }
    if (-not $id) {
        Note "sans identifiant, ignore : $($f.Name)"
        continue
    }
    # Un billet arrive avant mots.txt : on le laisse dans le depot sans
    # l inscrire nulle part. Il repartira au passage suivant, entier.
    if (-not $motsOk -and ($type -eq 'billet' -or $type -eq 'reponse-billet')) {
        Note "billet retenu faute de mots.txt : $($f.Name)"
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
    $aDeverser += [pscustomobject]@{ Id = $id; Type = $type; Vise = $vise; Fichier = $f }
}

if ($Sec) {
    Write-Output "marqueur=$borne"
    Write-Output "deja=$($deja.Count)"
    Write-Output "a_deverser=$($aDeverser.Count)"
    foreach ($c in $aDeverser) { Write-Output "  $($c.Id)  [$($c.Type)]  $($c.Fichier.Name)" }
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
$jour = (Get-Date).ToString('yyyy-MM-dd')
foreach ($c in $aDeverser) {

    # Une reponse ne cree pas de fichier : elle en modifie un. C est le seul
    # cas ou ce script ecrit dans une note existante du coffre, et c est
    # borne a une section et a une cle.
    if ($c.Type -eq 'reponse-billet') {
        if (-not $c.Vise) {
            Note "reponse sans cible, deversee dans 00 Inbox : $($c.Fichier.Name)"
        } else {
            $cibleBillet = Get-Billet $billets $c.Vise
            if ($null -eq $cibleBillet) {
                # Le billet n existe pas encore ici, par exemple s il vient
                # d etre cree dans le meme lot et que l ordre a joue contre
                # nous. On ne marque rien : la reponse repartira au passage
                # suivant, quand le billet sera la. Rien n est perdu.
                Note "billet $($c.Vise) introuvable, la reponse repartira au passage suivant"
                continue
            }
            try {
                $texte = Get-Corps $c.Fichier.FullName
                Add-Reponse $cibleBillet $texte $mots $jour | Out-Null
                $copies = $copies + 1
                $reussis += $c.Id
                if ([string]::Compare($c.Id, $maxi, [StringComparison]::Ordinal) -gt 0) { $maxi = $c.Id }
                Note "reponse ajoutee a $($cibleBillet.Name), billet debloque"
            } catch {
                Note "ECHEC de la reponse pour $($c.Fichier.Name) : $($_.Exception.Message)"
            }
            continue
        }
    }

    # Une capture va dans 00 Inbox, un billet dans 08 Billets. Une reponse
    # orpheline retombe dans 00 Inbox : mieux vaut la voir le dimanche que la
    # perdre. C est la seule ligne de ce script qui ressemble a un choix, et
    # elle se lit dans une table.
    $dossier = $inbox
    if ($c.Type -eq 'billet') { $dossier = $billets }

    $cible = Get-NomLibre $dossier $c.Fichier.Name
    if ([IO.Path]::GetFileName($cible) -ne $c.Fichier.Name) {
        Note "nom deja pris, deverse sous $([IO.Path]::GetFileName($cible))"
    }
    try {
        Copy-Item -Path $c.Fichier.FullName -Destination $cible -ErrorAction Stop
        $copies = $copies + 1
        $reussis += $c.Id
        if ([string]::Compare($c.Id, $maxi, [StringComparison]::Ordinal) -gt 0) { $maxi = $c.Id }
        if ($c.Type -eq 'billet') { Note "billet ouvert : $([IO.Path]::GetFileName($cible))" }
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
& git add -- "00 Inbox" "08 Billets" 2>&1 | Out-Null
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    $aujourdhui = (Get-Date).ToString('yyyy-MM-dd')
    & git commit -q -m "Captures de l agent, $aujourdhui" -- "00 Inbox" "08 Billets"
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
