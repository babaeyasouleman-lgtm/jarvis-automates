# Les reunions Fathom. Phase 4 bis du Plan Jarvis.
# Il prend le resume des rencontres de Souleman depuis le dernier passage et
# depose une capture par reunion dans 00 Inbox. Jamais la transcription.
#
# Il ne modifie rien dans Fathom, ne partage aucune reunion, n ecrit a
# personne. Il lit, il resume, il depose.
#
# Ce script ne supprime rien dans le coffre. Aucune commande de suppression
# ailleurs que sur ses propres fichiers de travail, qui sont des copies.
#
# Difference avec les trois autres automates, assumee et ecrite dans le plan :
# Fathom passe par un connecteur MCP, donc c est le modele qui appelle l outil
# et non un pre-filtre Python. Tout ce qui peut se calculer avant se calcule
# quand meme ici : le repertoire du coffre, la date de depart, les reunions
# deja vues, le plafond. list_meetings retourne deja le resume, donc un seul
# appel d outil suffit pour lister et resumer.
#
# Aucun accent dans ce fichier, volontairement. PowerShell 5.1 lit les .ps1
# en ANSI et abimerait les accents. Tout le texte accentue vit dans
# consigne.md, que Claude lit lui-meme en UTF8.
#
# Lancement manuel :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\reunions\reunions.ps1
# Voir le contexte qui serait donne au modele, sans l appeler :
#   ... \reunions.ps1 -Sec
# Attention, -Sec ne montre pas le tri des reunions, contrairement au mode sec
# de l extracteur et des courriels. La liste des reunions vit derriere le
# connecteur Fathom, et seul le modele peut l appeler. Le mode sec montre donc
# la date de depart, le plafond et les reunions deja vues, c est-a-dire tout
# ce qui se calcule sans reseau.
# Ignorer le garde du jour :
#   ... \reunions.ps1 -Manuel
# Premier passage sur une fenetre plus large que 30 jours :
#   ... \reunions.ps1 -Jours 90
#
# Ce script ne pousse pas vers GitHub. Le filet horaire et le bibliothecaire
# s en chargent, et rien ne se perd entre deux.

param(
    [switch]$Sec,
    [switch]$Manuel,
    [int]$Jours = 0,
    [int]$Plafond = 5
)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre    = 'C:\Obsidian\Second Brain'
$base      = 'C:\Obsidian\reunions'
$consigne  = Join-Path $base 'consigne.md'
$repPy     = Join-Path $base 'repertoire.py'
$travail   = Join-Path $base 'travail'
$contexte  = Join-Path $base 'contexte.txt'
$marqueur  = Join-Path $base 'marqueur.txt'
$deposes   = Join-Path $base 'deposes.txt'
$journal   = Join-Path $base 'journal.log'
$jourFait  = Join-Path $base 'dernier-jour.txt'
$claude    = 'C:\Users\Administrator\.local\bin\claude.exe'
$python    = 'C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe'
$modele    = 'sonnet'
$defautJours = 30
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
if (-not (Test-Path $consigne)) { Note "ECHEC, consigne.md introuvable"; exit 1 }
if (-not (Test-Path $coffre))   { Note "ECHEC, coffre introuvable"; exit 1 }
if (-not $Sec -and -not (Test-Path $claude)) { Note "ECHEC, claude.exe introuvable"; exit 1 }

# 1 bis. Garde, un passage par jour.
# La tache se redeclenche toutes les 30 minutes tant qu Obsidian est ouvert.
# Sans ce garde, chaque reessai relancerait le modele. Le mode sec est
# exempte, il ne coute rien.
if (-not $Manuel -and -not $Sec) {
    if ((Test-Path $jourFait) -and ((Get-Content $jourFait -TotalCount 1).Trim() -eq $aujourdhui)) {
        Note "saute, reunions deja relevees aujourd hui"
        exit 0
    }
}

if (-not (Test-Path $travail)) { New-Item -ItemType Directory -Path $travail | Out-Null }

# 2. Le repertoire du coffre, deterministe, aucun token depense ici.
# Il dit au modele qui existe dans 06 Personnes et dans le pipeline, pour
# qu il n ait pas a fouiller le coffre lui-meme. Meme role que index.py.
# Un repertoire manquant n empeche pas un passage, mais le modele devient
# alors incapable de trancher : on s arrete plutot que de deposer n importe
# quoi.
$repTxt = Join-Path $travail 'repertoire.txt'
if (-not (Test-Path $python)) {
    $repli = (Get-Command python -ErrorAction SilentlyContinue)
    if ($repli) { $python = $repli.Source }
}
if ((Test-Path $repPy) -and (Test-Path $python)) {
    & $python $repPy $coffre $repTxt | Out-Null
    if ($LASTEXITCODE -ne 0) { Note "ECHEC du repertoire, code $LASTEXITCODE"; exit 1 }
    $repLignes = (Get-Content $repTxt -Encoding utf8 | Measure-Object -Line).Lines
    Note "repertoire du coffre, $repLignes lignes"
} else {
    Note "ECHEC, repertoire.py ou python introuvable, on ne depose rien sans savoir qui compte"
    exit 1
}

# 3. Depuis quand chercher. Le marqueur porte la date de la reunion la plus
# recente deja traitee. Au premier passage, une fenetre de 30 jours.
$depuis = ''
if (Test-Path $marqueur) { $depuis = (Get-Content $marqueur -TotalCount 1).Trim() }
if (-not $depuis) {
    if ($Jours -gt 0) { $n = $Jours } else { $n = $defautJours }
    $depuis = $maintenant.AddDays(-$n).ToString('yyyy-MM-dd')
    Note "premier passage, fenetre de $n jours, depuis $depuis"
}

# 3 bis. Ce qui a deja ete depose. Le lanceur seul ecrit ce fichier, et
# seulement apres reussite. Les identifiants Fathom sont stables, c est ce
# qui empeche un doublon meme si deux reunions tombent le meme jour.
$deja = ''
if (Test-Path $deposes) {
    $ids = @(Get-Content $deposes -Encoding utf8 | Where-Object { $_.Trim() })
    if ($ids.Count -gt 0) { $deja = ($ids -join ' ') }
}

if ($Sec) {
    Write-Output "depuis=$depuis"
    Write-Output "plafond=$Plafond"
    Write-Output "deja=$deja"
    Write-Output "repertoire=$repTxt"
    Note "mode sec, le modele n est pas appele, marqueur inchange"
    exit 0
}

# 4. Ce que le modele doit savoir, calcule ici et pas devine par lui
$semaine = Get-SemaineIso $maintenant
$lignes = @(
    "coffre=$coffre",
    "date=$aujourdhui",
    "semaine=$semaine",
    "depuis=$depuis",
    "plafond=$Plafond",
    "travail=$travail",
    "repertoire=$repTxt",
    "deja=$deja"
)
Set-Content -Path $contexte -Value $lignes -Encoding utf8

# 4 bis. Les deux fichiers que le modele doit reecrire. On les vide avant,
# sinon un passage rate laisserait les reponses du precedent et le marqueur
# avancerait sur du vieux.
Set-Content -Path (Join-Path $travail 'traitees.txt') -Value '' -Encoding utf8
Set-Content -Path (Join-Path $travail 'maxi.txt') -Value '' -Encoding utf8

# 5. Le passage
Set-Location $coffre
$avantEtat = @(git status --porcelain)
$avant = (git rev-parse --short HEAD).Trim()
Note "debut, depuis $depuis, plafond $Plafond, commit avant $avant, semaine $semaine"
$chrono = [Diagnostics.Stopwatch]::StartNew()

$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele --output-format json
$code = $LASTEXITCODE
$chrono.Stop()
$duree = [math]::Round($chrono.Elapsed.TotalSeconds, 1)

if ($code -ne 0) {
    Note "ECHEC du passage, code $code, apres $duree s"
    if ($sortie) { Note "sortie : $sortie" }
    Note "marqueur inchange, les memes reunions seront relues au prochain passage"
    exit 1
}

# La sortie est un objet JSON, meme mesure que le bibliothecaire depuis le
# 6 septembre 2026. Le chiffre qui compte est num_turns. total_cost_usd est
# un equivalent, pas un debit : ce qui tourne ici passe sur le quota de l
# abonnement, pas sur la carte.
# Si le format change un jour, on retombe sur le texte brut. Une mesure
# perdue ne doit jamais faire perdre un passage.
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

# 6. Rien d autre que 00 Inbox et son journal ne doit avoir bouge.
# On ne corrige pas, on le dit. Le filet horaire garde tout de toute facon.
$apresEtat = @(git status --porcelain)
# Pas de Compare-Object ici : en PowerShell 5.1 il refuse un tableau vide.
$nouveaux = $apresEtat | Where-Object { $avantEtat -notcontains $_ }
foreach ($n in $nouveaux) {
    if ($n -match '00 Inbox/') { continue }
    if ($n -match 'Biblioth') { continue }
    if ($n -match '\.obsidian/') { continue }
    Note "ATTENTION, hors perimetre : $n"
}

# 7. Enregistrer, par chemin et pas avec git add -A. Le passage tourne
# pendant que Souleman peut avoir des choses en cours dans le coffre, et un
# git add -A les embarquerait dans un commit qui dit Reunions.
# Le dossier du journal porte un accent, et ce fichier reste en ascii pur.
# Il est donc construit par code de caractere, comme les mois de matin.ps1.
$b = '_Biblioth' + [char]0x00E9 + 'caire'
git add -- "00 Inbox" $b 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Reunions, $aujourdhui" -- "00 Inbox" $b
    $apresHash = (git rev-parse --short HEAD).Trim()
    Note "fin en $duree s, commit $apresHash, annuler avec git revert $apresHash"
} else {
    Note "fin en $duree s, rien depose"
}

# 8. Avancer le marqueur, seulement maintenant que le passage a reussi.
# Le modele ecrit la date de la plus recente reunion qu il a reellement
# traitee, pas celle de la liste : s il s est arrete au plafond, les autres
# doivent revenir au passage suivant.
$maxiTx = Join-Path $travail 'maxi.txt'
if (Test-Path $maxiTx) {
    $maxi = (Get-Content $maxiTx -TotalCount 1 -Encoding utf8).Trim()
    if ($maxi -match '^\d{4}-\d{2}-\d{2}$') {
        Set-Content -Path $marqueur -Value $maxi -Encoding ascii
        Note "marqueur avance a $maxi"
    } else {
        Note "maxi.txt illisible, marqueur inchange, tout sera relu au prochain passage"
    }
} else {
    Note "maxi.txt absent, marqueur inchange, tout sera relu au prochain passage"
}

# 8 bis. Ce qui a ete traite, pour ne jamais doubler une capture. Les
# identifiants Fathom sont stables, donc une reunion vue une fois ne revient
# plus, meme si le marqueur recule.
$traitees = Join-Path $travail 'traitees.txt'
if (Test-Path $traitees) {
    $ajout = @(Get-Content $traitees -Encoding utf8 | Where-Object { $_.Trim() })
    if ($ajout.Count -gt 0) {
        Add-Content -Path $deposes -Value $ajout -Encoding ascii
        Note "$($ajout.Count) reunion(s) inscrites dans deposes.txt"
    }
    # Garder la liste bornee. Une reunion vieille de plusieurs mois ne
    # reviendra pas, et le marqueur la protege deja.
    $tout = @(Get-Content $deposes -Encoding utf8)
    if ($tout.Count -gt 400) {
        $tout | Select-Object -Last 200 | Set-Content -Path $deposes -Encoding ascii
    }
}

# 9. Marquer la journee comme faite, pour les reessais du bibliothecaire.
# En ascii, volontairement : -Encoding utf8 ajouterait un BOM que la
# comparaison plus haut lirait comme un caractere de plus.
Set-Content -Path $jourFait -Value $aujourdhui -Encoding ascii

# 10. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}
