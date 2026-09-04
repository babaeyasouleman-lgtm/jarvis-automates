# La note du matin. Phase 3 du Plan Jarvis.
# Elle ecrit la note du jour dans 01 Journal a partir de ce que le coffre
# contient deja : agenda, veille, decisions a revoir, relances dues,
# prochaine action de chaque projet actif, deux questions en attente.
#
# Elle ne touche qu un seul fichier, la note du jour. Elle ne supprime rien.
# Aucune commande de suppression dans ce script.
#
# Elle est appelee par passage.ps1 en premier, avant l extraction et avant
# les deux gardes du bibliothecaire. Raison : une note du matin qui attend
# trois heures qu Obsidian se ferme n est plus une note du matin, et elle ne
# cree qu un fichier neuf.
#
# Aucun accent dans ce fichier, volontairement. PowerShell 5.1 lit les .ps1
# en ANSI et abimerait les accents. Les deux mois accentues sont construits
# par code de caractere plus bas, et tout le reste du texte accentue vit dans
# consigne.md, que Claude lit lui-meme en UTF8.
#
# Lancement manuel, en ignorant le marqueur du jour :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\matin\matin.ps1 -Manuel

param([switch]$Manuel)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre   = 'C:\Obsidian\Second Brain'
$base     = 'C:\Obsidian\matin'
$consigne = Join-Path $base 'consigne.md'
$contexte = Join-Path $base 'contexte.txt'
$jourFait = Join-Path $base 'dernier-jour.txt'
$journal  = Join-Path $base 'journal.log'
$claude   = 'C:\Users\Administrator\.local\bin\claude.exe'
$modele   = 'sonnet'
$python   = 'C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe'
$agendaPy = Join-Path $base 'agenda.py'
$agendaTx = Join-Path $base 'agenda.txt'
# -------------------------------------------------------------------------

function Note($texte) {
    $ligne = "{0}  {1}" -f (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'), $texte
    Add-Content -Path $journal -Value $ligne -Encoding utf8
}

$maintenant = Get-Date
$aujourdhui = $maintenant.ToString('yyyy-MM-dd')

# 1. Garde, une note par jour.
# La tache du bibliothecaire se redeclenche toutes les 30 minutes tant qu
# Obsidian est ouvert. Sans ce garde, chaque reessai relancerait le modele.
# En ascii, volontairement : -Encoding utf8 ajouterait un BOM que la
# comparaison ci-dessous lirait comme un caractere de plus.
if (-not $Manuel) {
    if ((Test-Path $jourFait) -and ((Get-Content $jourFait -TotalCount 1).Trim() -eq $aujourdhui)) {
        Note "saute, note deja ecrite aujourd hui"
        exit 0
    }
}

# 2. Verifications
if (-not (Test-Path $claude))   { Note "ECHEC, claude.exe introuvable"; exit 1 }
if (-not (Test-Path $consigne)) { Note "ECHEC, consigne.md introuvable"; exit 1 }
if (-not (Test-Path $coffre))   { Note "ECHEC, coffre introuvable"; exit 1 }

Set-Location $coffre

# 3. Ce que la note du matin doit savoir, calcule ici et pas devine par elle.
# Les accents des deux mois concernes sont poses par code de caractere pour
# garder ce fichier en ascii pur. contexte.txt part bien en UTF8.
$e = [char]0x00E9   # e accent aigu
$u = [char]0x00FB   # u accent circonflexe
$jours = @('Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi')
$mois  = @('janvier', "f${e}vrier", 'mars', 'avril', 'mai', 'juin', 'juillet',
           "ao${u}t", 'septembre', 'octobre', 'novembre', "d${e}cembre")

$titre  = "{0} {1} {2} {3}" -f $jours[[int]$maintenant.DayOfWeek], $maintenant.Day,
                               $mois[$maintenant.Month - 1], $maintenant.Year
$noteRel   = "01 Journal/$aujourdhui.md"
$veilleRel = "01 Journal/{0}.md" -f $maintenant.AddDays(-1).ToString('yyyy-MM-dd')
$veilleEst = if (Test-Path (Join-Path $coffre $veilleRel)) { 'oui' } else { 'non' }
$noteEst   = if (Test-Path (Join-Path $coffre $noteRel))   { 'oui' } else { 'non' }

# 3 bis. Le pont vers Google Agenda, deterministe, avant l appel au modele.
# Les connecteurs Google de l app Claude ne sont pas visibles en mode
# claude -p, verifie le 3 septembre 2026. Ce pont interroge l API avec le
# jeton que l agent WhatsApp utilise deja, et depose agenda.txt. Il ne
# plante jamais : sans identifiants il ecrit statut=indisponible, et la
# note du matin continue sans agenda.
$agendaStatut = 'indisponible'
if (Test-Path $agendaPy) {
    if (-not (Test-Path $python)) {
        $repli = Get-Command python -ErrorAction SilentlyContinue
        if ($repli) { $python = $repli.Source }
    }
    if (Test-Path $python) {
        & $python $agendaPy $base | Out-Null
        if (Test-Path $agendaTx) {
            $premiere = Get-Content $agendaTx -TotalCount 1 -Encoding utf8
            if ($premiere -match '^statut=(.+)$') { $agendaStatut = $matches[1].Trim() }
        }
        Note "agenda, statut $agendaStatut"
    } else {
        Note "agenda saute, python introuvable"
    }
} else {
    Note "agenda.py introuvable, la note se fera sans agenda"
}

$lignes = @(
    "coffre=$coffre",
    "date=$aujourdhui",
    "titre=$titre",
    "note=$noteRel",
    "note_existe=$noteEst",
    "veille=$veilleRel",
    "veille_existe=$veilleEst",
    "agenda=$agendaTx",
    "agenda_statut=$agendaStatut"
)
Set-Content -Path $contexte -Value $lignes -Encoding utf8

# 4. Etat du coffre avant, pour verifier qu elle n a touche que sa note
$avantEtat = @(git status --porcelain)
$avant = (git rev-parse --short HEAD).Trim()

Note "debut, $titre, note existante $noteEst, veille $veilleEst, agenda $agendaStatut, commit avant $avant"
$chrono = [Diagnostics.Stopwatch]::StartNew()

$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele
$code = $LASTEXITCODE
$chrono.Stop()
$duree = [math]::Round($chrono.Elapsed.TotalSeconds, 1)

if ($code -ne 0) {
    Note "ECHEC, code $code, apres $duree s"
    if ($sortie) { Note "sortie : $sortie" }
    Note "marqueur inchange, un nouvel essai aura lieu au prochain passage"
    exit 1
}

foreach ($l in @($sortie)) { if ($l) { Note "dit : $l" } }

# 5. Rien d autre que la note du jour ne doit avoir bouge.
# On ne corrige pas, on le dit. Le filet horaire garde tout de toute facon.
$apresEtat = @(git status --porcelain)
# Pas de Compare-Object ici : en PowerShell 5.1 il refuse un tableau vide.
$nouveaux = $apresEtat | Where-Object { $avantEtat -notcontains $_ }
# .obsidian est la configuration de l application, elle bouge toute seule
# des qu Obsidian tourne, graph.json en tete. Ce n est pas le modele.
foreach ($n in $nouveaux) {
    if ($n -match [regex]::Escape($aujourdhui)) { continue }
    if ($n -match '\.obsidian/') { continue }
    Note "ATTENTION, hors perimetre : $n"
}

# 6. Enregistrer, la note du jour seulement, sans pousser.
# Le pathspec evite d embarquer ce que Souleman ou un autre automate a
# laisse en cours dans le coffre.
git add -- $noteRel 2>&1 | Out-Null
git diff --cached --quiet -- $noteRel
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Note du matin, $aujourdhui" -- $noteRel
    $apresHash = (git rev-parse --short HEAD).Trim()
    Note "fin en $duree s, commit $apresHash, annuler avec git revert $apresHash"
} else {
    Note "fin en $duree s, la note n a pas change"
}

# 7. Marquer la journee comme faite
Set-Content -Path $jourFait -Value $aujourdhui -Encoding ascii

# 8. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}
