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
# A egalite, l ordre est, depuis le 10 septembre 2026 :
#   1. une echeance dans les sept jours
#   2. la priorite de pole, livrer=1, entrer=2, tenir=3
#   3. l echeance
#   4. le nom de fichier
#
# Avant, c etait le nom de fichier seul, donc la date de creation, donc rien :
# un travail du pour demain passait derriere un billet sans date cree la
# veille. La regle des sept jours est generale et ne nomme aucun role : c est
# elle qui fait remonter Declic a l approche du 24 octobre sans lui donner de
# pole. Les poles viennent de _Equipe\Charte de l equipe.md.
#
# Deux etats ne sont JAMAIS pris : "bloque", qui attend Souleman, et
# "attente", qui attend un autre role. Les confondre ferait ranger une reponse
# de Souleman sous une question qui ne lui etait pas posee.
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
$archives = Join-Path $coffre '99 Archives\Billets'

# Le modele se choisit par le ROLE du billet, jamais ici. Opus pour ce que
# Souleman vend, une demo ou un livrable client. Sonnet pour la recherche, un
# brouillon, une relance, un rapport interne. Opus coute cinq fois Sonnet, et
# aller chercher une date limite sur le site d une ville n en vaut pas cinq.
# Table "quel modele pour quoi" du Plan Jarvis, appliquee le 10 septembre 2026.
$modeleVend      = 'opus'
$modeleReste     = 'sonnet'
$rolesQuiVendent = @('livraison', 'demo')

# Regle 5 du Plan Jarvis : aucun employe ne tourne sans plafond ecrit dans son
# lanceur. Il manquait. --max-budget-usd n existe qu avec --print, ce que ce
# script utilise deja. Un passage qui depasse s arrete, le billet reste en
# cours, et il repart au passage suivant.
$budgetPassage = 3.00
# Une demo de site lit une competence de 70 Ko, tire un site, trie des images
# et ecrit une page entiere : deux dollars sur Opus s arretent au milieu du
# build. Un passage coupe reprend au suivant grace au journal, mais trois
# passages pour une maquette de dix minutes, c est trois heures de PC. Un
# plafond par role, le defaut restant $budgetPassage. 10 septembre 2026.
# Releves a la demande de Souleman le 10 septembre 2026, avant le premier
# billet demo : sur l abonnement, ce chiffre n est pas une facture, c est un
# garde-fou contre un passage qui boucle et vide le quota de session.
$budgetParRole = @{
    'demo'      = 12.00
    'livraison' = 8.00
}
function Budget-Pour($role) {
    if ($role -and $budgetParRole.ContainsKey($role)) { return $budgetParRole[$role] }
    return $budgetPassage
}

# La priorite de pole. Elle sert a trancher quand deux billets se presentent
# au meme creneau. Avant, l ordre etait alphabetique par nom de fichier, donc
# arbitraire. Livrer passe avant Faire entrer parce qu il y a douze prospects
# demarches et zero site en ligne : vendre plus dans une machine qui ne livre
# pas, c est comme ca qu on perd des clients. Charte de l equipe.
# Declic n a pas de pole : c est son echeance qui le fait remonter.
$prioritePole = @{
    'livraison'  = 1
    'demo'       = 1
    'ventes'     = 2
    'marketing'  = 2
    'croissance' = 2
    'declic'     = 2
    'finances'   = 3
    'tech'       = 3
}
$prioriteParDefaut = 5

$maxPassages   = 5
$verrouMinutes = 90
$urgenceJours  = 7
$archiveJours  = 30
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

# Une cle du frontmatter, remplacee. Si elle n y est pas, elle est ajoutee
# juste avant le --- de fermeture. Rien d autre n est touche.
#
# L ajout n est pas un confort : un billet depose par l agent WhatsApp ne
# porte pas encore passages: ni etapes:, parce que le cote agent est refait
# dans une autre session. Le lanceur doit savoir ecrire dans les deux formes,
# l ancienne et la neuve, sans que personne ne migre quoi que ce soit.
function Set-Champ($chemin, $cle, $valeur) {
    $brut = [IO.File]::ReadAllText($chemin)
    $crlf = $brut.Contains("`r`n")
    $lignes = @($brut -split "`r?`n")
    if ($lignes.Count -lt 2 -or $lignes[0].Trim() -ne '---') { return }

    $ferme = -1
    for ($i = 1; $i -lt $lignes.Count; $i++) {
        if ($lignes[$i].Trim() -eq '---') { $ferme = $i; break }
    }
    if ($ferme -lt 0) { return }

    for ($i = 1; $i -lt $ferme; $i++) {
        if ($lignes[$i] -match ('^' + [regex]::Escape($cle) + ':\s*')) {
            $lignes[$i] = "${cle}: $valeur"
            Set-Texte $chemin $lignes $crlf
            return
        }
    }

    $avant = @($lignes[0..($ferme - 1)])
    $apres = @($lignes[$ferme..($lignes.Count - 1)])
    Set-Texte $chemin ($avant + @("${cle}: $valeur") + $apres) $crlf
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
foreach ($k in @('a_faire', 'en_cours', 'attente', 'bloque', 'fait', 'annule')) {
    if (-not $mots.ContainsKey($k)) { Note "ECHEC, mots.txt sans la cle $k"; exit 1 }
}

# Le modele suit le role du billet. Un role inconnu tombe sur Sonnet, ce qui
# est le sens sur : on ne depense pas cinq fois plus sur un role qu on n a pas
# prevu.
function Modele-Pour($role) {
    if ($rolesQuiVendent -contains $role) { return $modeleVend }
    return $modeleReste
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
$clos    = @()
$aujourdhui = (Get-Date).Date
foreach ($f in (Get-ChildItem -Path $billets -Filter '*.md' -File | Sort-Object Name)) {
    $id = ''
    $etat = ''
    $role = ''
    $ech  = ''
    $dem  = ''
    foreach ($l in (Get-Content $f.FullName -Encoding utf8 -TotalCount 25)) {
        if ($l -match '^billet:\s*(\S+)\s*$')    { $id = $matches[1] }
        elseif ($l -match '^etat:\s*(.*)$')      { $etat = $matches[1].Trim() }
        elseif ($l -match '^role:\s*(.*)$')      { $role = $matches[1].Trim() }
        elseif ($l -match '^echeance:\s*(.*)$')  { $ech = $matches[1].Trim() }
        elseif ($l -match '^demandeur:\s*(.*)$') { $dem = $matches[1].Trim() }
    }
    if (-not $id) { continue }

    # Un billet clos depuis assez longtemps part aux archives, plus bas.
    if ($etat -eq $mots['fait'] -or $etat -eq $mots['annule']) {
        if (($aujourdhui - $f.LastWriteTime.Date).TotalDays -ge $archiveJours) { $clos += $f }
        continue
    }

    # L echeance, en jours. Une echeance absente ou illisible vaut tres loin,
    # jamais tres proche : un billet sans date ne doit pas passer devant un
    # billet date, et une date mal ecrite ne doit pas se faire passer pour
    # urgente.
    $jours = 99999
    if ($ech) {
        try {
            $d = [datetime]::ParseExact($ech, 'yyyy-MM-dd', [Globalization.CultureInfo]::InvariantCulture)
            $jours = [int]($d.Date - $aujourdhui).TotalDays
        } catch { $jours = 99999 }
    }

    $pole = $prioriteParDefaut
    if ($role -and $prioritePole.ContainsKey($role)) { $pole = $prioritePole[$role] }

    # Une echeance dans les sept jours passe devant tous les poles. C est ce
    # qui fait remonter Declic sans lui donner de pole, et c est une regle
    # generale : ce qui est du cette semaine passe avant ce qui est important.
    # 0 trie avant 1, donc urgent en tete.
    $urgent = 1
    if ($jours -le $urgenceJours) { $urgent = 0 }

    $n = 0
    if ($compte.ContainsKey($id)) { $n = $compte[$id] }
    $b = [pscustomobject]@{
        Id         = $id
        Etat       = $etat
        Role       = $role
        Fichier    = $f
        NomFichier = $f.Name
        Passages   = $n
        Echeance   = $ech
        Jours      = $jours
        Pole       = $pole
        Urgent     = $urgent
        Demandeur  = $dem
    }
    if ($n -ge $maxPassages) { $affames += $b; continue }
    if ($etat -eq $mots['en_cours'])    { $enCours += $b }
    elseif ($etat -eq $mots['a_faire']) { $aFaire += $b }
    # Ni "bloque" ni "attente" ne sont jamais pris. Le premier attend
    # Souleman, le second attend un autre role.
}

foreach ($b in $affames) {
    Note "ecarte, $($b.Passages) passages sans sortir : $($b.Id) $($b.Fichier.Name)"
}

# Le compteur ne garde que ce qui est encore ouvert. Un billet annule ou fait
# avant d avoir termine un passage y laissait une ligne pour toujours, et
# passages.txt grossissait sans jamais servir. Le compteur ne sert qu a
# empecher une boucle sur un billet vivant.
$vivants = @{}
foreach ($b in ($enCours + $aFaire + $affames)) { $vivants[$b.Id] = $true }
$morts = @($compte.Keys | Where-Object { -not $vivants.ContainsKey($_) })
if ($morts.Count -gt 0) {
    foreach ($m in $morts) { $compte.Remove($m) }
    Set-Content -Path $passages -Value (@($compte.Keys | Sort-Object | ForEach-Object { "$_ $($compte[$_])" })) -Encoding ascii
    Note "$($morts.Count) compteur(s) retire(s), le billet n est plus ouvert"
}

# 5 bis. Les billets clos partent aux archives. Deterministe, aucun token.
#
# Pourquoi ce n est pas de la coquetterie : "08 Billets" est une racine
# entiere de cerveau\liste-blanche.txt, donc chaque billet part dans l export
# et pese sur le cout de CHAQUE question posee au cerveau. A cent billets par
# mois, rien n etant jamais supprime, le cerveau doublerait en trois mois, et
# "le cerveau qui grossit" est deja le premier risque de derapage du plan.
#
# "99 Archives" n est pas dans la liste blanche. Le billet quitte donc l export
# tout seul, sans qu on touche a la liste. Rien n est supprime, tout reste
# dans git, et le bibliothecaire n a toujours pas le droit d entrer ici.
if (-not $Sec -and $clos.Count -gt 0) {
    $bouges = 0
    foreach ($f in $clos) {
        $mois = $f.LastWriteTime.ToString('yyyy-MM')
        $dossier = Join-Path $archives $mois
        if (-not (Test-Path $dossier)) { New-Item -ItemType Directory -Path $dossier -Force | Out-Null }
        if (Test-Path (Join-Path $dossier $f.Name)) {
            Note "archive deja presente, laisse en place : $($f.Name)"
            continue
        }
        & git -C $coffre mv -- "08 Billets/$($f.Name)" "99 Archives/Billets/$mois/$($f.Name)" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) { $bouges++ } else { Note "ECHEC archivage de $($f.Name)" }
    }
    if ($bouges -gt 0) {
        & git -C $coffre commit -q -m "Archivage de $bouges billet(s) clos" 2>&1 | Out-Null
        Note "$bouges billet(s) clos archive(s) vers 99 Archives\Billets"
    }
}

# 5 ter. L ordre de prise. Tout deterministe, aucun token depense.
#
#   1. un billet en cours passe avant tout. Regle d origine, elle est bonne :
#      reprendre vaut mieux que commencer autre chose en laissant un chantier
#   2. puis une echeance dans les sept jours
#   3. puis la priorite de pole
#   4. puis l echeance
#   5. puis le nom de fichier, pour que deux passages identiques choisissent
#      le meme billet
#
# Avant le 10 septembre 2026, l ordre etait le nom de fichier, donc la date de
# creation, donc rien. Un travail du pour demain passait derriere un billet
# sans date cree la veille.
$enCours = @($enCours | Sort-Object Urgent, Pole, Jours, NomFichier)
$aFaire  = @($aFaire  | Sort-Object Urgent, Pole, Jours, NomFichier)

$choisi = $null
if ($enCours.Count -gt 0)     { $choisi = $enCours[0] }
elseif ($aFaire.Count -gt 0)  { $choisi = $aFaire[0] }

if ($Sec) {
    Write-Output "en_cours=$($enCours.Count)  a_faire=$($aFaire.Count)  ecartes=$($affames.Count)  clos_a_archiver=$($clos.Count)"
    if ($enCours.Count + $aFaire.Count -gt 0) {
        Write-Output "ordre de prise :"
        foreach ($b in ($enCours + $aFaire)) {
            $u = 'normal'
            if ($b.Urgent -eq 0) { $u = 'URGENT' }
            $e = $b.Echeance
            if (-not $e) { $e = 'sans date' }
            Write-Output ("  {0,-6}  pole {1}  {2,-11}  {3,-11}  {4,-9}  {5}" -f `
                $u, $b.Pole, $e, $b.Role, $b.Etat, $b.NomFichier)
        }
    }
    if ($choisi) {
        Write-Output ("choisi={0}  {1}  [{2}]  modele {3}  passage {4}" -f `
            $choisi.Id, $choisi.NomFichier, $choisi.Etat, (Modele-Pour $choisi.Role), ($choisi.Passages + 1))
    }
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
if ($choisi.Etat -ne $mots['en_cours']) { Set-Champ $choisi.Fichier.FullName 'etat' $mots['en_cours'] }
$compte[$choisi.Id] = $passage
Set-Content -Path $passages -Value (@($compte.Keys | Sort-Object | ForEach-Object { "$_ $($compte[$_])" })) -Encoding ascii

# Le compteur est ecrit AUSSI dans le billet, et c est ce qui remplace la
# ligne cout: que le modele remplissait a la main. On demandait a un modele un
# chiffre que le lanceur connait exactement, ce que "le deterministe d abord"
# interdit. passages.txt reste le compteur vivant, nettoye quand un billet se
# ferme ; passages: est la trace qui survit a l archivage. Les deux sortent de
# la meme variable, ecrite au meme endroit : ils ne peuvent pas diverger.
Set-Champ $choisi.Fichier.FullName 'passages' $passage

$restant = 'sans echeance'
if ($choisi.Jours -lt 99999) { $restant = "$($choisi.Jours) jour(s)" }
$modele = Modele-Pour $choisi.Role

Set-Content -Path $contexte -Encoding utf8 -Value @(
    "date=$((Get-Date).ToString('yyyy-MM-dd'))",
    "billet=$($choisi.Fichier.FullName)",
    "identifiant=$($choisi.Id)",
    "etat_avant=$($choisi.Etat)",
    "role=$($choisi.Role)",
    "demandeur=$($choisi.Demandeur)",
    "echeance=$($choisi.Echeance)",
    "jours_restants=$restant",
    "passage=$passage",
    "passages_max=$maxPassages"
)

Note "prend $($choisi.Id), $($choisi.Fichier.Name), passage $passage"
$chrono = [Diagnostics.Stopwatch]::StartNew()

$budgetPassage = Budget-Pour $choisi.Role
Note "modele $modele pour le role '$($choisi.Role)', plafond $budgetPassage USD"

Set-Location $coffre
$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele --max-budget-usd $budgetPassage --output-format json
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
