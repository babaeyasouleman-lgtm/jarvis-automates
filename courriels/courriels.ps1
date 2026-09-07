# Les courriels entrants. Phase 4 du Plan Jarvis.
# Il lit ce qu on a repondu a Souleman depuis le dernier passage, depose une
# capture par fil dans 00 Inbox, et prepare un brouillon dans Gmail quand un
# fil appelle une reponse.
#
# Il n envoie jamais, il ne marque rien comme lu, il ne supprime rien, il ne
# classe rien. Le seul script qui ecrit dans Gmail est brouillon.py, et il ne
# sait faire qu un brouillon.
#
# Ce script ne supprime rien dans le coffre. Aucune commande de suppression
# ailleurs que sur ses propres fichiers de travail, qui sont des copies.
#
# Aucun accent dans ce fichier, volontairement. PowerShell 5.1 lit les .ps1
# en ANSI et abimerait les accents. Tout le texte accentue vit dans
# consigne.md, que Claude lit lui-meme en UTF8.
#
# Lancement manuel :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\courriels\courriels.ps1
# Voir ce que le collecteur retiendrait, sans appeler le modele :
#   ... \courriels.ps1 -Sec
# Ignorer le garde du jour :
#   ... \courriels.ps1 -Manuel
# Premier passage sur une fenetre plus large que 7 jours :
#   ... \courriels.ps1 -Sec -Jours 30
#
# Ce script ne pousse pas vers GitHub. Le filet horaire et le bibliothecaire
# s en chargent, et rien ne se perd entre deux.

param(
    [switch]$Sec,
    [switch]$Manuel,
    [int]$Jours = 0
)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre    = 'C:\Obsidian\Second Brain'
$base      = 'C:\Obsidian\courriels'
$consigne  = Join-Path $base 'consigne.md'
$collecteur= Join-Path $base 'courriels.py'
$travail   = Join-Path $base 'travail'
$contexte  = Join-Path $base 'contexte.txt'
$marqueur  = Join-Path $base 'marqueur.txt'
$deposes   = Join-Path $base 'deposes.txt'
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
if (-not (Test-Path $collecteur)) { Note "ECHEC, courriels.py introuvable"; exit 1 }
if (-not (Test-Path $consigne))   { Note "ECHEC, consigne.md introuvable"; exit 1 }
if (-not (Test-Path $coffre))     { Note "ECHEC, coffre introuvable"; exit 1 }
if (-not $Sec -and -not (Test-Path $claude)) { Note "ECHEC, claude.exe introuvable"; exit 1 }

# 1 bis. Garde, un passage par jour.
# La tache se redeclenche toutes les 30 minutes tant qu Obsidian est ouvert.
# Sans ce garde, chaque reessai relancerait le modele des qu un courriel
# arrive. Le mode sec est exempte, il ne coute rien.
if (-not $Manuel -and -not $Sec) {
    if ((Test-Path $jourFait) -and ((Get-Content $jourFait -TotalCount 1).Trim() -eq $aujourdhui)) {
        Note "saute, courriels deja releves aujourd hui"
        exit 0
    }
}

# 2. Le collecteur. Deterministe, aucun token depense ici. Il interroge
# l API Gmail depuis le marqueur, jette le bruit, et ecrit un fichier de
# travail par fil retenu. Le modele ne recoit que ce qui demande un jugement.
$argsPy = @($collecteur, $base, $coffre)
if ($Sec)        { $argsPy += '--sec' }
if ($Jours -gt 0) { $argsPy += @('--jours', "$Jours") }
& $python @argsPy
if ($LASTEXITCODE -ne 0) { Note "ECHEC du collecteur, code $LASTEXITCODE"; exit 1 }

$resultat = Join-Path $travail 'resultat.txt'
if (-not (Test-Path $resultat)) { Note "ECHEC, le collecteur n a rien ecrit"; exit 1 }

$vals = @{}
foreach ($l in (Get-Content $resultat -Encoding utf8)) {
    if ($l -match '^([a-z_]+)=(.*)$') { $vals[$matches[1]] = $matches[2] }
}

if ($vals['statut'] -ne 'ok') {
    Note "collecteur indisponible, $($vals['raison'])"
    exit 1
}

$fils = [int]$vals['fils']
$maxi = $vals['maxi']
$echecs = [int]$vals['echecs']

# Un message que le collecteur n a pas pu lire est peut-etre celui qui
# comptait. Le marqueur ne le franchit pas, la meme fenetre sera relue au
# passage suivant, et deposes.txt empeche le doublon. Constate le
# 7 septembre 2026 : Gmail refuse des lectures en rafale, code 403.
if ($echecs -gt 0) {
    Note "ATTENTION, $echecs message(s) illisibles, le marqueur ne bougera pas"
}

Note ("collecteur, {0} fil(s) retenu(s), {1} message(s) lus, {2} jetes, depuis {3}" -f `
      $fils, $vals['messages_lus'], $vals['jetes'], $vals['depuis'])
if ($vals['coupe'] -eq 'oui') {
    Note "plafond de fils atteint, le reste sera relu au prochain passage"
}

if ($Sec) {
    Note "mode sec, le modele n est pas appele, marqueur inchange"
    exit 0
}

if ($fils -eq 0) {
    # Rien a juger, mais le marqueur avance quand meme : le bruit lu ce
    # passage-ci n a pas besoin d etre relu au suivant.
    if ($echecs -eq 0) {
        Set-Content -Path $marqueur -Value $maxi -Encoding ascii
        Note "aucune reponse a traiter, marqueur avance a $maxi"
    } else {
        Note "aucune reponse a traiter, marqueur inchange, $echecs message(s) illisibles"
    }
    Set-Content -Path $jourFait -Value $aujourdhui -Encoding ascii
    exit 0
}

# 3. Ce que le modele doit savoir, calcule ici et pas devine par lui
$semaine = Get-SemaineIso $maintenant
$lignes = @(
    "coffre=$coffre",
    "date=$aujourdhui",
    "semaine=$semaine",
    "fils=$fils",
    "travail=$travail",
    "brouillon=$(Join-Path $base 'brouillon.py')",
    "python=$python"
)
Set-Content -Path $contexte -Value $lignes -Encoding utf8

# 4. Le passage
Set-Location $coffre
$avantEtat = @(git status --porcelain)
$avant = (git rev-parse --short HEAD).Trim()
Note "debut, $fils fil(s), commit avant $avant, semaine $semaine"
$chrono = [Diagnostics.Stopwatch]::StartNew()

$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele --output-format json
$code = $LASTEXITCODE
$chrono.Stop()
$duree = [math]::Round($chrono.Elapsed.TotalSeconds, 1)

if ($code -ne 0) {
    Note "ECHEC du passage, code $code, apres $duree s"
    if ($sortie) { Note "sortie : $sortie" }
    Note "marqueur inchange, les memes fils seront relus au prochain passage"
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

# 5. Rien d autre que 00 Inbox et son journal ne doit avoir bouge.
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

# 6. Enregistrer, par chemin et pas avec git add -A. Le passage tourne
# pendant que Souleman peut avoir des choses en cours dans le coffre, et un
# git add -A les embarquerait dans un commit qui dit Courriels.
# Le dossier du journal porte un accent, et ce fichier reste en ascii pur.
# Il est donc construit par code de caractere, comme les mois de matin.ps1.
$b = '_Biblioth' + [char]0x00E9 + 'caire'
git add -- "00 Inbox" $b 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Courriels, $aujourdhui" -- "00 Inbox" $b
    $apresHash = (git rev-parse --short HEAD).Trim()
    Note "fin en $duree s, commit $apresHash, annuler avec git revert $apresHash"
} else {
    Note "fin en $duree s, rien depose"
}

# 7. Avancer le marqueur, seulement maintenant que le passage a reussi.
# Une session refusee pour limite de quota sort plus haut en code 1 : les
# memes courriels sont relus au passage suivant, sans rien perdre.
if ($echecs -eq 0) {
    Set-Content -Path $marqueur -Value $maxi -Encoding ascii
    Note "marqueur avance a $maxi"
} else {
    Note "marqueur inchange, $echecs message(s) n ont pas pu etre lus"
}

# 7 bis. Ce qui a ete depose, pour ne jamais doubler une capture. Le
# collecteur saute au passage suivant tout fil dont le dernier message est
# deja dans cette liste. Elle n est ecrite qu ici, apres reussite.
$candidats = Join-Path $travail 'candidats.txt'
if (Test-Path $candidats) {
    $ajout = @(Get-Content $candidats -Encoding utf8 | Where-Object { $_.Trim() })
    if ($ajout.Count -gt 0) {
        Add-Content -Path $deposes -Value $ajout -Encoding ascii
        Note "$($ajout.Count) fil(s) inscrits dans deposes.txt"
    }
    # Garder la liste bornee. Un fil vieux de plusieurs mois ne reviendra
    # pas, et le marqueur le protege deja.
    $tout = @(Get-Content $deposes -Encoding utf8)
    if ($tout.Count -gt 500) {
        $tout | Select-Object -Last 300 | Set-Content -Path $deposes -Encoding ascii
    }
}

# 8. Marquer la journee comme faite, pour les reessais du bibliothecaire.
# En ascii, volontairement : -Encoding utf8 ajouterait un BOM que la
# comparaison plus haut lirait comme un caractere de plus.
Set-Content -Path $jourFait -Value $aujourdhui -Encoding ascii

# 9. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}
