# Le bibliothecaire du coffre Obsidian. Phase 2 du Plan Jarvis.
# Range 00 Inbox une fois par jour, enregistre avant et apres.
# Ce script ne supprime jamais rien. Aucune commande de suppression.
#
# Aucun accent dans ce fichier, volontairement. PowerShell 5.1 lit les .ps1
# en ANSI et abimerait les accents. Tout le texte accentue vit dans consigne.md,
# que Claude lit lui-meme en UTF8.
#
# Lancement manuel, en ignorant les deux gardes :
#   powershell -ExecutionPolicy Bypass -File C:\Obsidian\bibliothecaire\passage.ps1 -Manuel

param([switch]$Manuel)

[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8

# ---------------------------------------------------------------- reglages
$coffre   = 'C:\Obsidian\Second Brain'
$base     = 'C:\Obsidian\bibliothecaire'
$consigne = Join-Path $base 'consigne.md'
$contexte = Join-Path $base 'contexte.txt'
$marqueur = Join-Path $base 'dernier-passage.txt'
$journal  = Join-Path $base 'journal.log'
$compteur = Join-Path $base 'essais.txt'
$verrou   = Join-Path $base 'verrou.txt'
$claude   = 'C:\Users\Administrator\.local\bin\claude.exe'
$python   = 'C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe'
$indexPy  = Join-Path $base 'index.py'
$indexTx  = Join-Path $base 'index.txt'
$lecons   = Join-Path $base 'lecons.md'
$modele   = 'opus'
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

# Toute sortie passe par ici, sinon le verrou resterait pose jusqu a sa peremption.
function Fin($code) {
    Verrou-Lever
    exit $code
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

# 0. Le verrou.
# Deux passages simultanes lancent deux fois Opus, donc deux fois le cout, et
# peuvent s ecrire l un par dessus l autre. Constate le 6 septembre 2026 : la
# tache Windows et un lancement a la main se sont croises. Aucun degat ce
# jour-la, le second bibliothecaire s est arrete de lui-meme au titre du
# quatrieme interdit, celui du doute, mais rien ne l y obligeait.
# Le verrou vaut aussi en mode Manuel, c est justement le cas qui a produit la
# collision. Le garde du jour ne protege pas de ca : il ne se pose qu a la fin.
# Peremption de 2 heures, sinon un passage tue net bloquerait tous les suivants.
# Le plus long passage mesure tient en moins de 6 minutes.
# Pour lever le verrou a la main, ouvrir verrou.txt et remplir la ligne fin=
$peremptionH = 2
if (Test-Path $verrou) {
    $v = @{}
    foreach ($l in (Get-Content $verrou)) {
        if ($l -match '^([a-z]+)=(.*)$') { $v[$matches[1]] = $matches[2].Trim() }
    }
    if ($v['debut'] -and -not $v['fin']) {
        $depuis = $null
        try {
            $depuis = [datetime]::Parse($v['debut'], [Globalization.CultureInfo]::InvariantCulture)
        } catch { $depuis = $null }
        if ($depuis -and ($maintenant - $depuis).TotalHours -lt $peremptionH) {
            $min = [math]::Round(($maintenant - $depuis).TotalMinutes, 1)
            Note "saute, un autre passage tourne depuis $min minutes, verrou pose a $($v['debut'])"
            exit 0
        }
        Note "verrou perime, le passage precedent n a jamais fini. On repart"
    }
}
Set-Content -Path $verrou -Value @("debut=$($maintenant.ToString('o'))", "fin=") -Encoding ascii

# 0 pre. Sous quel compte Claude tourne ce passage.
#
# Ajoute le 8 septembre 2026. Le CLI ne garde qu UNE identite : pas de bascule
# comme gh auth switch, se connecter a un autre compte ecrase le premier.
# Souleman a deux comptes, S-WEB et son perso. Si un soir il se reconnecte sous
# l autre, les cinq automates de cette nuit basculent avec, en silence, sur un
# autre quota. Et le connecteur Fathom, attache au compte, cesse de repondre :
# la phase 4 bis s arrete sans dire pourquoi.
#
# C est le meme piege que les deux comptes GitHub, vecu le meme jour : le
# symptome apparait ailleurs, longtemps apres, et il ne ressemble pas a sa
# cause. Ici il tient dans une ligne de journal.
#
# Ce garde ne bloque JAMAIS le passage. Il constate et il le dit. Un compte
# different n est pas forcement une erreur, c est peut-etre voulu ; ce qui
# serait une erreur, c est de ne pas le voir.
$compteFichier = Join-Path $base 'compte.txt'
$compteJson    = Join-Path $env:USERPROFILE '.claude.json'
$compte = ''
if (Test-Path $compteJson) {
    try {
        $j = Get-Content $compteJson -Raw -Encoding UTF8 | ConvertFrom-Json
        if ($j.oauthAccount -and $j.oauthAccount.emailAddress) {
            $compte = $j.oauthAccount.emailAddress
        }
    } catch { $compte = '' }
}
if ($compte) {
    $attendu = ''
    if (Test-Path $compteFichier) { $attendu = (Get-Content $compteFichier -TotalCount 1).Trim() }
    if (-not $attendu) {
        Set-Content -Path $compteFichier -Value $compte -Encoding ascii
        Note "compte Claude, $compte, premier releve"
    } elseif ($attendu -ne $compte) {
        Note "ATTENTION, le compte Claude a change : $attendu devient $compte"
        Note "  le quota, et le connecteur Fathom, ne sont plus les memes qu hier"
        Note "  si c est voulu, remplacer la ligne de $compteFichier"
    } else {
        Note "compte Claude, $compte"
    }
} else {
    Note "compte Claude illisible, le passage continue sans ce garde"
}

# 0 bis. La phase 3, la note du matin.
# Elle passe en premier, avant l extraction et avant les deux gardes plus bas.
# Raison : une note du matin qui attend trois heures qu Obsidian se ferme n est
# plus une note du matin, et elle ne cree qu un fichier neuf. Son propre
# marqueur du jour la rend idempotente, les reessais de 30 minutes ne la
# relancent pas. Elle enregistre elle-meme sa note, sans pousser.
$matin = 'C:\Obsidian\matin\matin.ps1'
if (Test-Path $matin) {
    & powershell -ExecutionPolicy Bypass -File $matin
    Note "note du matin, code $LASTEXITCODE"
} else {
    Note "matin.ps1 introuvable, on passe a l extraction"
}

# 0 bis. La phase 2 bis, les transcriptions Claude Code.
# Elle depose dans 00 Inbox ce que le bibliothecaire rangera juste apres.
# Elle passe avant les deux gardes ci-dessous, volontairement : elle n ecrit
# que des fichiers neufs, donc Obsidian ouvert ne la gene pas. Son propre
# marqueur la rend idempotente, deux lancements le meme jour ne doublent rien.
$extraction = 'C:\Obsidian\transcriptions\extraction.ps1'
if (Test-Path $extraction) {
    & powershell -ExecutionPolicy Bypass -File $extraction
    Note "extraction des transcriptions, code $LASTEXITCODE"
} else {
    Note "extraction.ps1 introuvable, on passe directement au rangement"
}

# 0 ter. La phase 4, les courriels entrants.
# Elle passe apres l extraction et avant les deux gardes ci-dessous.
# Raison : elle ne cree que des fichiers neufs dans 00 Inbox, donc Obsidian
# ouvert ne la gene pas, et le bibliothecaire doit ranger dans la foulee ce
# qu elle vient de deposer. Le verrou pose plus haut la couvre deja.
# Son propre marqueur d horodatage et son garde du jour la rendent
# idempotente, deux lancements le meme jour ne doublent rien.
$courriels = 'C:\Obsidian\courriels\courriels.ps1'
if (Test-Path $courriels) {
    & powershell -ExecutionPolicy Bypass -File $courriels
    Note "courriels entrants, code $LASTEXITCODE"
} else {
    Note "courriels.ps1 introuvable, on passe directement au rangement"
}

# 0 quater. La phase 4 bis, les reunions Fathom.
# Elle passe apres les courriels et avant les deux gardes ci-dessous, pour la
# meme raison qu eux : elle ne cree que des fichiers neufs dans 00 Inbox, donc
# Obsidian ouvert ne la gene pas, et le bibliothecaire doit ranger dans la
# foulee ce qu elle vient de deposer. Le verrou pose plus haut la couvre deja.
# Son propre marqueur, son garde du jour et sa liste de reunions deja vues la
# rendent idempotente, deux lancements le meme jour ne doublent rien.
$reunions = 'C:\Obsidian\reunions\reunions.ps1'
if (Test-Path $reunions) {
    & powershell -ExecutionPolicy Bypass -File $reunions
    Note "reunions Fathom, code $LASTEXITCODE"
} else {
    Note "reunions.ps1 introuvable, on passe directement au rangement"
}

# 0 quinquies. La phase 7, les captures de l agent WhatsApp.
# Elle passe apres les reunions et avant les deux gardes ci-dessous, meme
# raison qu eux : elle ne cree que des fichiers neufs dans 00 Inbox, donc
# Obsidian ouvert ne la gene pas, et le bibliothecaire doit ranger dans la
# foulee ce qu elle vient de deverser. Le verrou pose plus haut la couvre deja.
# Elle n appelle aucun modele et ne coute rien : elle tire un depot, elle copie.
# Pas de garde du jour, volontairement, contrairement aux quatre au-dessus :
# une capture dictee ce matin n a aucune raison d attendre demain, et un
# deversement qui ne trouve rien de neuf s arrete en une seconde. Ses deux
# filets, marqueur.txt et deposes.txt, empechent le doublon.
$captures = 'C:\Obsidian\captures\captures.ps1'
if (Test-Path $captures) {
    & powershell -ExecutionPolicy Bypass -File $captures
    Note "captures de l agent, code $LASTEXITCODE"
} else {
    Note "captures.ps1 introuvable, les captures de l agent restent dans leur depot"
}

# 1. Garde, deja passe aujourd hui
if (-not $Manuel) {
    if ((Test-Path $marqueur) -and ((Get-Content $marqueur -TotalCount 1).Trim() -eq $aujourdhui)) {
        Note "saute, deja passe aujourd hui"
        Fin 0
    }
}

# 2. Garde, Obsidian ouvert. On attend et on reessaie au lieu d abandonner
# la journee, la tache se redeclenche toutes les 30 minutes.
# Soupape : apres 6 refus, soit trois heures d attente, on range quand meme.
# Sans elle, une journee ou Obsidian reste ouvert ne se rangerait jamais,
# et la boite se remplirait sans fin.
$refusMax = 6
if (-not $Manuel) {
    if (Get-Process Obsidian -ErrorAction SilentlyContinue) {
        $refus = 0
        if (Test-Path $compteur) {
            $c = ((Get-Content $compteur -TotalCount 1).Trim()) -split ' '
            if ($c[0] -eq $aujourdhui) { $refus = [int]$c[1] }
        }
        $refus = $refus + 1
        if ($refus -lt $refusMax) {
            Set-Content -Path $compteur -Value "$aujourdhui $refus" -Encoding ascii
            Note "Obsidian est ouvert, refus $refus sur $refusMax. Nouvel essai dans 30 minutes"
            Fin 0
        }
        Note "Obsidian ouvert depuis $refus essais, on range quand meme"
    }
}

# 3. Verifications
if (-not (Test-Path $claude))   { Note "ECHEC, claude.exe introuvable"; Fin 1 }
if (-not (Test-Path $consigne)) { Note "ECHEC, consigne.md introuvable"; Fin 1 }
if (-not (Test-Path $coffre))   { Note "ECHEC, coffre introuvable"; Fin 1 }

Set-Location $coffre

# 4. Enregistrer l etat avant le passage, pour que l annulation soit propre
git add -A 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Avant le bibliothecaire, $aujourdhui"
    Note "commit avant le passage"
}
$avant = (git rev-parse --short HEAD).Trim()

# 5. L index du coffre, calcule avant chaque passage.
# Il passe apres l extraction, donc il contient deja les captures de la nuit.
# Il repond en une lecture a la question qui coutait le plus de tours d outils :
# est-ce que cette note existe deja ? Un index manquant ne doit jamais empecher
# un rangement, donc un echec ici se note et le passage continue sans lui.
$indexLignes = 0
if (Test-Path $indexPy) {
    if (-not (Test-Path $python)) {
        $repli = Get-Command python -ErrorAction SilentlyContinue
        if ($repli) { $python = $repli.Source }
    }
    if (Test-Path $python) {
        & $python $indexPy $coffre $indexTx | Out-Null
        if ($LASTEXITCODE -eq 0 -and (Test-Path $indexTx)) {
            $indexLignes = (Get-Content $indexTx -Encoding utf8 | Measure-Object -Line).Lines
            Note "index du coffre, $indexLignes notes"
        } else {
            Note "ECHEC de l index, code $LASTEXITCODE, le passage continue sans lui"
        }
    } else {
        Note "index saute, python introuvable, le passage continue sans lui"
    }
} else {
    Note "index.py introuvable, le passage continue sans lui"
}

# 5 bis. Ce que le bibliothecaire doit savoir, calcule ici et pas devine par lui
$semaine = Get-SemaineIso $maintenant
$jourSem = [int]$maintenant.DayOfWeek        # 0 dimanche, 1 lundi
$revue   = if ($jourSem -eq 0 -or $jourSem -eq 1) { 'oui' } else { 'non' }

# La semaine d avant, parce qu une correction ecrite le dimanche se lit le
# lundi, et que le lundi a change de semaine.
$semaineAvant = Get-SemaineIso $maintenant.AddDays(-7)

$lignes = @(
    "date=$aujourdhui",
    "semaine=$semaine",
    "semaine_avant=$semaineAvant",
    "revue_hebdo=$revue",
    "commit_avant=$avant",
    "index=$indexTx",
    "index_lignes=$indexLignes",
    "lecons=$lecons"
)
Set-Content -Path $contexte -Value $lignes -Encoding utf8

# 6. Le passage
Note "debut du passage, commit avant $avant, semaine $semaine, avant $semaineAvant, revue $revue, index $indexLignes notes"
$chrono = [Diagnostics.Stopwatch]::StartNew()

$sortie = & $claude -p "Lis le fichier $consigne et execute exactement ce qu il demande." --model $modele --output-format json
$code = $LASTEXITCODE
$chrono.Stop()

$duree = [math]::Round($chrono.Elapsed.TotalSeconds, 1)

if ($code -ne 0) {
    Note "ECHEC du passage, code $code, apres $duree s"
    if ($sortie) { Note "sortie : $sortie" }
    Fin 1
}

# La sortie est un objet JSON depuis l entretien du 6 septembre 2026. Il
# porte le texte du bibliothecaire dans result, et la mesure du passage.
# Le chiffre qui compte est num_turns : 40 tours pour une nuit ordinaire
# avant l index, 71 sur le gros lot du 2 septembre. Sans lui, personne ne
# peut dire si l index a servi.
# total_cost_usd est un equivalent, pas un debit. Ce qui tourne ici passe
# sur le quota de l abonnement, pas sur la carte.
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

# 7. Filet de securite, au cas ou il aurait oublie d enregistrer
git add -A 2>&1 | Out-Null
git diff --cached --quiet
if ($LASTEXITCODE -ne 0) {
    git commit -q -m "Bibliothecaire, $aujourdhui, enregistrement de secours"
    Note "commit de secours, il avait laisse des choses non enregistrees"
}

$apres = (git rev-parse --short HEAD).Trim()

# 7 bis. Le garde de 08 Billets. Phase 8, 8 septembre 2026.
#
# La consigne lui interdit ce dossier, et la consigne suffit dans les faits :
# c est deja comme ca que la liste noire de 00 Inbox tient depuis le 2
# septembre. Mais un interdit qui ne laisse aucune trace quand il est franchi
# est un interdit qu on decouvre six mois plus tard, et la lecon du 8 septembre
# est exactement celle-la : un maillon manquant ne leve pas d erreur, il
# produit un silence, et un silence se confond avec un comportement normal.
#
# On ne peut pas l empecher d ecrire, il a le coffre entier sous la main. On
# peut refuser que ca passe inapercu. Ce garde ne fait donc rien d autre que
# de le dire, fort, dans le journal que Souleman relit.
if ($apres -ne $avant) {
    $touches = @(git diff --name-only "$avant..$apres" -- "08 Billets")
    if ($touches.Count -gt 0) {
        Note "ALERTE, le bibliothecaire a touche 08 Billets, ce qui lui est interdit"
        foreach ($t in ($touches | Select-Object -First 10)) { Note "  touche : $t" }
        Note "annuler ce passage avec git revert $apres, puis relire sa consigne"
    }
}

if ($apres -eq $avant) {
    Note "fin du passage en $duree s, rien a ranger"
} else {
    Note "fin du passage en $duree s, commit apres $apres, annuler avec git revert $apres"
}

# 8. Pousser
$retard = git rev-list --count '@{u}..HEAD' 2>$null
if ($retard -and [int]$retard -gt 0) {
    git push -q origin main
    if ($?) { Note "pousse, $retard commit(s)" } else { Note "ECHEC push, $retard commit(s) en attente" }
}

# 8 bis. La phase 6, l export du cerveau.
# Il passe ICI et pas plus haut, volontairement : il doit refleter le coffre
# APRES rangement, sinon les captures de la nuit resteraient invisibles a
# l agent pendant vingt-quatre heures.
# Consequence assumee : il suit le sort du rangement. Une nuit ou Obsidian
# reste ouvert repousse les deux de trente minutes a la fois, jusqu a trois
# heures. Le cerveau est alors plus vieux, et l agent l affiche dans chacune
# de ses reponses. Un retard visible vaut mieux qu un export a moitie range.
# Le verrou pose plus haut le couvre deja.
# Il ne juge rien et n appelle aucun modele : il copie une liste blanche et
# il pousse. Un echec ici ne doit pas faire echouer le passage.
$export = 'C:\Obsidian\cerveau\export.ps1'
if (Test-Path $export) {
    & powershell -ExecutionPolicy Bypass -File $export
    Note "export du cerveau, code $LASTEXITCODE"
} else {
    Note "export.ps1 introuvable, le cerveau de l agent ne sera pas rafraichi"
}

# 9. Marquer la journee comme faite
Set-Content -Path $marqueur -Value $aujourdhui -Encoding utf8

# 10. Garder le journal court
if (Test-Path $journal) {
    $l = Get-Content $journal
    if ($l.Count -gt 800) { $l | Select-Object -Last 500 | Set-Content -Path $journal -Encoding utf8 }
}

# 11. Lever le verrou. Fin naturelle du script, la seule qui ne passe pas par Fin().
Verrou-Lever
