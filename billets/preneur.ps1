# Le preneur de billets. Phase 8 du Plan Jarvis, 8 septembre 2026.
#
# Souleman demande un travail sur WhatsApp, l agent depose un billet dans
# 08 Billets, et ce script le fait prendre par Claude Code pendant que le PC
# est allume. Le billet revient en a valider, ou en bloque avec une question.
#
# C est un automate comme les autres : une consigne que le modele lit lui-meme,
# un lanceur court et sans accent, un journal qui dit ce qui a reellement
# tourne. Pour changer ce qu il fait, on modifie consigne.md. Ce script ne
# change que si la mecanique change.
#
# ----- Le deterministe d abord, le modele pour juger ------------------------
#
# Tout ce qui se calcule sans jugement se calcule ici : quel billet prendre,
# dans quel ordre, combien de fois il est deja passe, et la pose de l etat
# en cours qui empeche deux passages de se marcher dessus. Le modele ne recoit
# qu un chemin de fichier et une consigne. Un passage sans billet a prendre
# coute zero token et se termine en une seconde.
#
# ----- Ce qui l empeche de tourner, et pourquoi c est voulu -----------------
#
# Il saute quand le passage de nuit tient son verrou. Les deux puisent dans le
# meme quota d abonnement, et une collision est deja arrivee le 3 septembre
# 2026. Il saute aussi quand un git tourne deja dans le coffre. Dans les deux
# cas rien n est perdu : le billet est toujours a faire a l heure suivante.
#
# ----- L ordre de priorite, et le garde-fou --------------------------------
#
# Un billet en cours passe AVANT un billet a faire. Raison : en cours veut
# dire qu un passage precedent a ete interrompu, et reprendre vaut mieux que
# commencer autre chose en laissant un chantier ouvert. C est aussi ce qui
# rend le systeme auto-reparant : un passage qui meurt en cours de route est
# repris a l heure suivante sans intervention.
#
# Le garde-fou est passages.txt. Un billet qui a consomme cinq passages sans
# sortir de en cours n est plus pris : il resterait sinon a affamer tous les
# autres, indefiniment, en depensant du quota chaque heure. Il reste en cours,
# il apparait dans le digest de 8 h 30, et Souleman tranche.
#
# ----- Pourquoi l export a la fin ------------------------------------------
#
# L agent WhatsApp lit les billets dans son clone du cerveau, tire toutes les
# heures. Sans export apres un passage, un billet passe en bloque a 14 h ne
# serait visible de l agent que le lendemain matin, et repondre a une question
# prendrait deux jours. Avec, la boucle tient dans la journee.
#
# Aucun accent dans ce fichier, PowerShell 5.1 lit les .ps1 en ANSI. Les mots
# accentues viennent de mots.txt, lu en UTF-8.
#
# Lancement a la main :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\billets\preneur.ps1
# Voir quel billet serait pris, sans rien ecrire ni appeler le modele :
#   ... \preneur.ps1 -Sec

param(
    [switch]$Sec,
    [switch]$Manuel
)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre   = 'C:\Obsidian\Second Brain'
$base     = 'C:\Obsidian\billets'
$billets  = Join-Path $coffre '08 Billets'
$journal  = Join-Path $base 'journal.log'
$consigne = Join-Path $base 'consigne.md'
$contexte = Join-Path $base 'contexte.txt'
$motsTxt  = Join-Path $base 'mots.txt'
$passages = Join-Path $base 'passages.txt'
$verrou   = Join-Path $base 'verrou.txt'
$verrouPassage = 'C:\Obsidian\bibliothecaire\verrou.txt'
$captures = 'C:\Obsidian\captures\captures.ps1'
$export   = 'C:\Obsidian\cerveau\export.ps1'
$claude   = 'C:\Users\Administrator\.local\bin\claude.exe'
$modele   = 'opus'
$maxPassages   = 5
$verrouMinutes = 90
# -------------------------------------------------------------------------

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

# Le verrou n est jamais efface, seulement reecrit. Ce script ne supprime rien.
function Verrou-Lever {
    if (Test-Path $verrou) {
        $garde = @(Get-Content $verrou) | Where-Object { $_ -like 'debut=*' }
        Set-Content -Path $verrou -Value @($garde, "fin=$((Get-Date).ToString('o'))") -Encoding ascii
    }
}

function Fin($code) {
    Verrou-Lever
    exit $code
}

# Un verrou est-il tenu par quelqu un en ce moment ? Meme forme que celui du
# bibliothecaire : debut= rempli, fin= vide, et pas encore perime.
function Verrou-Tenu($chemin, $minutes) {
    if (-not (Test-Path $chemin)) { return $false }
    $v = @{}
    foreach ($l in (Get-Content $chemin)) {
        $i = $l.IndexOf('=')
        if ($i -gt 0) { $v[$l.Substring(0, $i)] = $l.Substring($i + 1).Trim() }
    }
    if (-not $v['debut'] -or $v['fin']) { return $false }
    try { $debut = [datetime]::Parse($v['debut']) } catch { return $false }
    return (((Get-Date) - $debut).TotalMinutes -lt $minutes)
}

# Ecriture UTF-8 SANS BOM, comme captures.ps1. Set-Content -Encoding utf8 en
# ajoute un sous PowerShell 5.1, et un BOM au milieu d une note du coffre est
# un caractere de plus que tout le monde lira comme du contenu.
function Set-Texte($chemin, $lignes, $crlf) {
    $fin = "`n"
    if ($crlf) { $fin = "`r`n" }
    [IO.File]::WriteAllText($chemin, (($lignes -join $fin) + $fin), (New-Object Text.UTF8Encoding($false)))
}

# La premiere cle etat: du frontmatter, remplacee. Rien d autre n est touche.
function Set-Etat($chemin, $valeur) {
    $brut = [IO.File]::ReadAllText($chemin)
    $crlf = $brut.Contains("`r`n")
    $lignes = @($brut -split "`r?`n")
    for ($i = 0; $i -lt $lignes.Count; $i++) {
        if ($lignes[$i] -match '^etat:\s*') { $lignes[$i] = 'etat: ' + $valeur; break }
    }
    Set-Texte $chemin $lignes $crlf
}

# 0. Verifications. Un chemin manquant s ecrit, il ne se devine pas.
if (-not (Test-Path $coffre))   { Note "ECHEC, coffre introuvable"; exit 1 }
if (-not (Test-Path $consigne)) { Note "ECHEC, consigne.md introuvable"; exit 1 }
if (-not (Test-Path $motsTxt))  { Note "ECHEC, mots.txt introuvable"; exit 1 }
if (-not (Test-Path $billets))  { Note "rien a prendre, 08 Billets n existe pas encore"; exit 0 }

$mots = @{}
foreach ($l in (Get-Content $motsTxt -Encoding UTF8)) {
    $t = $l.Trim()
    if (-not $t -or $t.StartsWith('#')) { continue }
    $i = $t.IndexOf('=')
    if ($i -lt 0) { continue }
    $mots[$t.Substring(0, $i).Trim()] = $t.Substring($i + 1).Trim()
}
foreach ($k in @('a_faire', 'en_cours')) {
    if (-not $mots.ContainsKey($k)) { Note "ECHEC, mots.txt sans la cle $k"; exit 1 }
}

# 1. Garde, le passage de nuit tourne. Meme quota, et deux Claude Code en
# parallele sur le meme coffre se disputeraient aussi git. On saute, sans
# rien marquer : le billet sera toujours la a l heure suivante.
if (-not $Sec -and (Verrou-Tenu $verrouPassage 180)) {
    Note "saute, le passage de nuit tient son verrou"
    exit 0
}

# 2. Garde, un preneur tourne deja. Un passage peut durer vingt minutes, la
# tache se declenche toutes les heures, mais une reprise manuelle pendant un
# passage automatique produirait deux modeles sur le meme billet.
if (-not $Sec) {
    if (Verrou-Tenu $verrou $verrouMinutes) {
        Note "saute, un preneur tourne deja"
        exit 0
    }
    Set-Content -Path $verrou -Value @("debut=$((Get-Date).ToString('o'))", "fin=") -Encoding ascii
}

# 3. Garde, un git tourne deja dans le coffre.
if (-not $Sec -and (Test-Path (Join-Path $coffre '.git\index.lock'))) {
    Note "saute, un autre git tourne deja dans le coffre"
    Fin 0
}

# 4. Deverser la boite aux lettres AVANT de choisir. Sans ca, une reponse
# ecrite sur WhatsApp il y a dix minutes n arriverait qu a la nuit, et
# repondre a une question couterait deux jours au lieu d une heure.
# captures.ps1 ne juge rien et n appelle aucun modele : le faire tourner ici
# ne coute que le tirage d un depot de deux megaoctets.
if (-not $Sec -and (Test-Path $captures)) {
    & powershell -ExecutionPolicy Bypass -File $captures
    Note "deversement de la boite, code $LASTEXITCODE"
}

# 5. Le pre-filtre. Deterministe, aucun token depense.
$compte = @{}
if (Test-Path $passages) {
    foreach ($l in (Get-Content $passages -Encoding ascii)) {
        $p = $l.Trim() -split '\s+'
        if ($p.Count -ge 2) { $compte[$p[0]] = [int]$p[1] }
    }
}

$enCours = @()
$aFaire  = @()
$affames = @()
foreach ($f in (Get-ChildItem -Path $billets -Filter '*.md' -File | Sort-Object Name)) {
    $id = ''
    $etat = ''
    $role = ''
    foreach ($l in (Get-Content $f.FullName -Encoding utf8 -TotalCount 20)) {
        if ($l -match '^billet:\s*(\S+)\s*$') { $id = $matches[1] }
        elseif ($l -match '^etat:\s*(.*)$')   { $etat = $matches[1].Trim() }
        elseif ($l -match '^role:\s*(.*)$')   { $role = $matches[1].Trim() }
    }
    if (-not $id) { continue }
    $n = 0
    if ($compte.ContainsKey($id)) { $n = $compte[$id] }
    $b = [pscustomobject]@{ Id = $id; Etat = $etat; Role = $role; Fichier = $f; Passages = $n }
    if ($n -ge $maxPassages) { $affames += $b; continue }
    if ($etat -eq $mots['en_cours'])   { $enCours += $b }
    elseif ($etat -eq $mots['a_faire']) { $aFaire += $b }
}

foreach ($b in $affames) {
    Note "ecarte, $($b.Passages) passages sans sortir : $($b.Id) $($b.Fichier.Name)"
}

$choisi = $null
if ($enCours.Count -gt 0)     { $choisi = $enCours[0] }
elseif ($aFaire.Count -gt 0)  { $choisi = $aFaire[0] }

if ($Sec) {
    Write-Output "en_cours=$($enCours.Count)  a_faire=$($aFaire.Count)  ecartes=$($affames.Count)"
    if ($choisi) { Write-Output "choisi=$($choisi.Id)  $($choisi.Fichier.Name)  [$($choisi.Etat)]  passage $($choisi.Passages + 1)" }
    else { Write-Output "choisi=aucun" }
    Note "mode sec, rien pris"
    exit 0
}

if ($null -eq $choisi) {
    Note "rien a prendre, $($aFaire.Count) a faire, $($enCours.Count) en cours"
    Fin 0
}

# 6. La prise. On pose en cours AVANT d appeler le modele : c est ce qui
# empeche deux passages de prendre le meme billet, et c est deterministe.
$passage = $choisi.Passages + 1
if ($choisi.Etat -ne $mots['en_cours']) { Set-Etat $choisi.Fichier.FullName $mots['en_cours'] }
$compte[$choisi.Id] = $passage
Set-Content -Path $passages -Value (@($compte.Keys | Sort-Object | ForEach-Object { "$_ $($compte[$_])" })) -Encoding ascii

Set-Content -Path $contexte -Encoding utf8 -Value @(
    "date=$((Get-Date).ToString('yyyy-MM-dd'))",
    "billet=$($choisi.Fichier.FullName)",
    "identifiant=$($choisi.Id)",
    "etat_avant=$($choisi.Etat)",
    "role=$($choisi.Role)",
    "passage=$passage"
)

Note "prend $($choisi.Id), $($choisi.Fichier.Name), passage $passage"
$chrono = [Diagnostics.Stopwatch]::StartNew()

Set-Location $coffre
$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele --output-format json
$code = $LASTEXITCODE
$chrono.Stop()
$duree = [math]::Round($chrono.Elapsed.TotalSeconds, 1)

if ($code -ne 0) {
    # Le billet reste en cours : il sera repris a l heure suivante, et le
    # compteur de passages empechera une boucle infinie.
    Note "ECHEC du passage, code $code, apres $duree s. Le billet reste en cours"
    if ($sortie) { Note "sortie : $sortie" }
    Fin 1
}

# La sortie est un objet JSON. num_turns dit si le billet a demande beaucoup
# d aller-retours, total_cost_usd est un equivalent et pas un debit : ce qui
# tourne ici passe sur le quota de l abonnement, pas sur la carte.
$brut = (@($sortie) -join "")
$dit = $brut
$j = $null
try { $j = $brut | ConvertFrom-Json } catch { $j = $null }
if ($j -and $null -ne $j.num_turns) {
    $dit = $j.result
    $equiv = [math]::Round($j.total_cost_usd, 2)
    Note ("mesure : {0} tours, entree {1}, cache lu {2}, sortie {3}, equivalent {4} USD" -f `
          $j.num_turns, $j.usage.input_tokens, $j.usage.cache_read_input_tokens, `
          $j.usage.output_tokens, $equiv)
    if ($j.is_error) { Note "ATTENTION, le modele signale une erreur, subtype $($j.subtype)" }
} else {
    Note "sortie illisible en json, texte brut conserve"
}
foreach ($l in @($dit -split "`n")) { if ($l.Trim()) { Note "dit : $($l.Trim())" } }

# 7. L etat reel apres le passage, relu sur le disque et pas cru sur parole.
$apres = ''
foreach ($l in (Get-Content $choisi.Fichier.FullName -Encoding utf8 -TotalCount 20)) {
    if ($l -match '^etat:\s*(.*)$') { $apres = $matches[1].Trim(); break }
}
Note "fin du passage en $duree s, $($choisi.Id) est $apres"

# Un billet sorti de en cours repart de zero : s il revient un jour, c est un
# travail neuf et pas la suite de celui-la.
if ($apres -ne $mots['en_cours']) {
    $compte.Remove($choisi.Id)
    Set-Content -Path $passages -Value (@($compte.Keys | Sort-Object | ForEach-Object { "$_ $($compte[$_])" })) -Encoding ascii
}

# 8. Filet, au cas ou il aurait oublie d enregistrer. Par chemin et jamais
# git add -A : Souleman peut avoir des choses en cours ailleurs dans le coffre.
& git add -- "08 Billets" 2>&1 | Out-Null
& git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    & git commit -q -m "Billet $($choisi.Id), enregistrement de secours" -- "08 Billets"
    if ($?) {
        $hash = (& git rev-parse --short HEAD).Trim()
        Note "commit de secours $hash, annuler avec git revert $hash"
    }
}

$retard = & git rev-list --count '@{u}..HEAD' 2>$null
if ($retard -and [int]$retard -gt 0) {
    & git push -q origin main 2>$null
    if ($?) { Note "pousse, $retard commit(s)" } else { Note "ECHEC push, $retard commit(s) en attente" }
}

# 9. L export du cerveau, pour que l agent WhatsApp voie le nouvel etat dans
# l heure au lieu du lendemain matin. Il ne juge rien et n appelle aucun
# modele. Un echec ici ne doit pas faire echouer le passage : le billet est
# deja ecrit dans le coffre, seul l affichage cote agent prend du retard.
if (Test-Path $export) {
    & powershell -ExecutionPolicy Bypass -File $export
    Note "export du cerveau, code $LASTEXITCODE"
}

# 10. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}

Verrou-Lever
