# Typostéroïdes — projet Python L2 (2026-2027)

Un jeu de frappe façon *Glyphica* / *ZType* en **pygame**, construit pas à pas pendant le module.
Le vaisseau est immobile au centre de l'écran. Des mots arrivent de tous les côtés, de plus en plus vite,
et il faut les **taper** pour les détruire avant qu'ils ne touchent le bouclier.

![Menu de la version prof master](PROF_MASTER/captures/menu.png)

Contrainte pédagogique : **tout le jeu tient dans un seul fichier `.py`**, organisé en classes
(`Joueur`, `Mot`, `Laser`, `Jeu`…).

---

## Organisation du module (14 h)

| Séance | Durée | Contenu | Fichiers |
|---|---|---|---|
| **TD1** | 2 h | Fonctionnement de pygame, boucle de jeu, `dt`, joueur, mots en mouvement (vecteurs), apparition, collisions, vies | `TD1/` |
| **TD2** | 2 h | Machine à états (menu / jeu / game over), clavier, ciblage, lasers, score et combo, précision, MPM, difficulté progressive | `TD2/` |
| TP1 | 4 h | *Game feel* : particules, tremblement d'écran, sons, dictionnaire externe, accents | base : `TD2/td2_correction.py` |
| TP2 | 3 h | *Gameplay* : ennemis spéciaux (héritage), bonus, vagues, améliorations, boss | idem |
| TP3 | 3 h | *Finition* : pause, top 10 en JSON, pseudo, statistiques, options, rendu | idem |

La feuille de route des TP, le barème indicatif et le **backlog complet** (toutes les fonctionnalités à
ajouter, avec leur difficulté) sont à la fin des deux PDF de TD.

---

## Arborescence

```
2026-2027/
├── README.md
├── TD1/
│   ├── TD1.tex                         fiche de TD (source LaTeX)
│   ├── TD1_Typosteroides_enonce.pdf    -> à distribuer aux étudiants
│   ├── TD1_Typosteroides_corrige.pdf   -> version enseignant (corrections incluses)
│   ├── TD1_Typosteroides_fiche_prof.pdf -> DÉROULÉ MINUTE PAR MINUTE (enseignant)
│   ├── TD1_fiche_prof.tex              source de la fiche enseignant
│   ├── demo_prof/demo_pygame.py        démo écrite en direct (version finale)
│   ├── prof_live/td1_etape_XX.py       sauvegarde du jeu à la fin de chaque étape
│   ├── td1_eleve.py                    -> squelette à compléter (TODO numérotés)
│   ├── td1_correction.py               -> corrigé
│   └── img/                            captures utilisées dans le PDF
├── TD2/
│   ├── TD2.tex, TD2_Typosteroides_enonce.pdf, TD2_Typosteroides_corrige.pdf
│   ├── TD2_Typosteroides_fiche_prof.pdf -> DÉROULÉ MINUTE PAR MINUTE (enseignant)
│   ├── demo_prof/demo_clavier.py       démo écrite en direct (version finale)
│   ├── prof_live/td2_etape_XX.py       sauvegarde du jeu à la fin de chaque étape
│   ├── td2_eleve.py                    -> squelette (repart du corrigé du TD1)
│   ├── td2_correction.py               -> corrigé = BASE COMMUNE DES TP
│   └── img/
├── PROF_MASTER/
│   ├── typosteroides_master.py         -> version complète de démonstration
│   └── captures/
└── _outils/                            (enseignant uniquement : ne pas distribuer)
    ├── source_td1.py, source_td2.py    sources annotées des fichiers .py
    ├── generer.py                      -> produit *_eleve.py et *_correction.py
    ├── preambule_td.tex, backlog.tex   préambule LaTeX commun et backlog
    ├── macros_fiche_prof.tex           mise en page des fiches enseignant
    └── compiler_pdf.py                 -> compile les 6 PDF (énoncé, corrigé, fiche prof)
```

---

## Les fiches de TD

Chaque PDF contient :

1. **Comment fonctionne pygame** : modules, squelette minimal, boucle de jeu, `Clock` et `dt`,
   surfaces, repère (y vers le bas), `Rect`, dessin, texte, événements, vecteurs `Vector2`,
   erreurs fréquentes. Le TD2 ajoute le clavier en détail (`key` et `unicode`, AZERTY),
   la transparence, `get_rect(**position)`, les rotations et la machine à états.
2. **Construire le jeu étape par étape**, dans l'ordre où un développeur de jeu le ferait :
   chaque étape apporte une seule chose, puis un encadré vert **« Testez »** dit ce qu'on doit
   voir à l'écran avant de passer à la suite. **Le numéro de l'étape est le numéro du `TODO`**
   dans le fichier `.py`.
3. Des exercices de compréhension, un « pour aller plus loin », le **backlog** et le bilan.

La version *corrigée* du PDF contient en plus la correction de chaque étape et de chaque question.

### Fiches enseignant : scripts de live-coding

`TDN_Typosteroides_fiche_prof.pdf` est un **script de live-coding** pensé pour une classe qui ne
peut pas encore coder seule : **l'enseignant tape tout le code au vidéoprojecteur**, les élèves
recopient la même ligne au même moment, et on lance le jeu toutes les 3 à 5 minutes. **Les fiches
ne sont pas à distribuer.** Pour chaque étape, la fiche donne :

- l'horaire et le mode de travail (démo, live-coding, tableau) ;
- **où taper** (classe, méthode, ligne repère) et le **code exact** à taper ;
- **ce qu'il faut dire** en tapant ;
- ce que l'écran doit montrer quand on lance (point de contrôle) ;
- les erreurs de recopie fréquentes, un mini-défi d'une minute et un plan B ;
- la **sauvegarde d'étape** à ouvrir si la démo dérape.

**Sauvegardes d'étapes** : `TD1/prof_live/td1_etape_00.py` à `td1_etape_11.py`, et
`TD2/prof_live/td2_etape_00.py` à `td2_etape_12.py`. Chaque fichier contient le jeu tel qu'il doit
être **à la fin** de l'étape, et il est exécutable. On peut aussi les mettre dans le dossier partagé
pour que les élèves perdus rattrapent la classe (« règle des 60 secondes »).

Les démos écrites en direct (`demo_pygame.py` au TD1, `demo_clavier.py` au TD2) sont fournies dans
`demo_prof/`, en version finale commentée.

## Lancer le jeu

```bash
pip install pygame
python TD2/td2_correction.py                 # le jeu à la fin des TD
python PROF_MASTER/typosteroides_master.py   # la version complète
```

Testé avec Python 3.13 et pygame 2.6.

---

## Version « prof master »

`PROF_MASTER/typosteroides_master.py` réalise une grande partie du backlog, **toujours dans un seul
fichier et sans aucun fichier externe** : les sons sont synthétisés et le décor est dessiné par le code.
Elle sert de démonstration en début de module (« voilà où vous pouvez arriver ») et de réservoir
d'exemples pendant les TP.

| Boss | Pouvoirs en action | Choix d'un pouvoir |
|---|---|---|
| ![](PROF_MASTER/captures/boss.png) | ![](PROF_MASTER/captures/pouvoirs.png) | ![](PROF_MASTER/captures/amelioration.png) |

- **Décor** : dégradé, nébuleuses, planète à anneau, 3 couches d'étoiles en parallaxe qui scintillent,
  étoiles filantes.
- **Game feel** : particules, ondes de choc, lettres qui s'envolent en tournant, tremblement d'écran,
  flash rouge, vignette de danger, canon qui pivote en douceur, flamme du réacteur, textes de score
  flottants, couleur du vaisseau selon le combo.
- **Sons synthétisés** (frappe, faute, explosion, choc, bonus, éclair, missile, boss). `F2` coupe le son.
- **Ennemis** (héritage de `Mot`) : rapide, zigzag, blindé (cache un second mot), diviseur (se brise
  en deux), fantôme (disparaît par moments).
- **Bonus** qui traversent l'écran : soin, bombe, gel (ralentit tout), bouclier.
- **Pouvoirs rogue-like** : entre deux vagues, on choisit **1 pouvoir parmi 3**, tirés selon leur
  **rareté** (commun, rare, épique, légendaire ; les raretés élevées sortent plus souvent quand les
  vagues avancent). Reprendre un pouvoir le fait **monter de niveau** (jusqu'à 5), et on a
  **2 relances** (`R`) par partie.

  | Rareté | Pouvoirs |
  |---|---|
  | Commun | Coque renforcée, Kit de survie, Canon à recul, Champ ralentisseur, Bouclier d'énergie, Aimant à bonus |
  | Rare | **Frappe critique** (une lettre en retire deux), **Laser perforant** (touche un 2e mot), **Lettres incendiaires** (les mots brûlent lettre par lettre), **Missiles autoguidés**, Amplificateur de combo, Condensateur |
  | Épique | **Éclair en chaîne** (rebondit de mot en mot), **Bombes à fragmentation**, **Satellites de défense** en orbite, **Nova de givre** (gèle tout quand on est touché), Onde de choc |
  | Légendaire | **Vampirisme** (+1 vie tous les N mots), **Réflexes surhumains** (points x2), **Tempête** (la foudre frappe tout l'écran à intervalles réguliers) |

- **Surcharge** : chaque bonne lettre remplit une jauge. Quand elle est pleine, `Entrée` lance la
  foudre sur tous les mots à l'écran (−3 lettres chacun).
- **Évolutions** (mythiques) : un pouvoir au niveau 4 (ou au maximum) + son partenaire fusionnent.
  La carte d'évolution est alors toujours proposée.

  | Évolution | Fusion | Effet |
  |---|---|---|
  | Orage perpétuel | Éclair + Condensateur | éclairs à 2 dégâts, la surcharge se remplit seule |
  | Napalm | Bombes + Feu | chaque mot détruit lâche une bombe incendiaire |
  | Essaim | Missiles + Satellites | les satellites tirent des missiles, salves doublées |
  | Zéro absolu | Givre + Ralentisseur | gel total toutes les 15 s, puis tout éclate |
  | Lame quantique | Critique + Perforant | chaque critique transperce 3 autres mots |
  | Phénix | Vampirisme + Coque | une renaissance par partie |

- **5 vaisseaux** jouables, chacun avec sa silhouette et ses pouvoirs de départ : Aiguille, Bastion,
  Foudroyeur, Artilleur, Pyromane.
- **Hangar (rogue-lite)** : chaque partie rapporte des **éclats** (score, vagues, boss, difficulté).
  On les dépense pour des améliorations permanentes (vie, relances, chance de rareté, batterie,
  prime, 4ᵉ carte) et pour débloquer les vaisseaux. Tout est sauvegardé dans
  `typosteroides_profil.json`.
- **Événements de vague** (35 % de chance dès la vague 3) : pluie de météores, vague dorée
  (points ×3), nuée de fantômes, brouillard cosmique (on ne voit qu'autour du vaisseau), tempête
  magnétique.
- **Capacités de boss** : barrage de mots rapides (Compilateur), décalage de tous les mots
  (Indenteur), résurrection des derniers mots détruits (Bug éternel), couvée de diviseurs (Reine),
  gravité qui accélère tout (Trou noir). Sur sa dernière phrase, le boss **enrage** et attaque plus
  souvent.
- **15 succès**, avec une notification à l'écran et des éclats en récompense.
- **Musique synthétisée** (une ambiance et un thème de boss), composée dans un *thread* pour ne pas
  ralentir le démarrage. Il y a aussi un ralenti cinématographique, des bandes noires façon cinéma à
  l'arrivée des boss et une aura de combo.

| Choix du vaisseau | Hangar | Évolution |
|---|---|---|
| ![](PROF_MASTER/captures/vaisseaux.png) | ![](PROF_MASTER/captures/hangar_plein.png) | ![](PROF_MASTER/captures/carte_evolution.png) |
- **Boss toutes les 5 vagues**, avec des phrases à taper (espaces compris), des répliques dans une
  bulle, des sbires et une barre de vie : *Le Compilateur*, *L'Indenteur fou*, *Le Bug éternel*,
  *La Reine des astéroïdes*, *Le Trou noir*.
- **Accents** : taper `e` valide `é è ê ë` (sauf en difficulté *Difficile*).
- **Menu** (difficulté Facile / Normal / Difficile), aide, pause, **top 10 sauvegardé** dans
  `typosteroides_scores.json` avec saisie du pseudo, **statistiques de fin** (histogramme des lettres
  les plus ratées), mode debug `F1`.

**Commandes** : `Jouer` ouvre le choix du vaisseau · lettres pour taper · `Retour arrière` pour changer de cible · `Entrée` pour la
surcharge · `Échap`/`Tab` pour la pause · flèches + `Entrée` dans les menus · `1`/`2`/`3` pour choisir
un pouvoir, `R` pour relancer le tirage.

Les pouvoirs sont aussi un bon support de TP : chacun tient en quelques lignes dans
`mettre_a_jour_pouvoirs` ou `declencher_pouvoirs_de_destruction`, et `Missile`, `Bombe` et `Eclair`
reprennent le même schéma « objet à durée de vie » que le `Laser` du TD2.

---

## Pour l'enseignant : modifier les fichiers

Les fichiers `*_eleve.py` et `*_correction.py` sont **générés** : ne les modifiez pas à la main, sinon
la prochaine génération écrasera vos changements. Modifiez `_outils/source_tdN.py`, où chaque trou est
délimité ainsi :

```python
#<TODO 6a> Consigne affichée dans la version élève
#| suite de la consigne (facultatif)
self.direction = (centre - self.position).normalize()   # code de la correction
#<STUB> self.direction = pygame.Vector2(0, 0)           # ce qui reste côté élève (sinon `pass`)
#</TODO>
```

puis, depuis le dossier `2026-2027` :

```bash
python _outils/generer.py       # régénère td*_eleve.py, td*_correction.py et prof_live/
python _outils/compiler_pdf.py  # recompile énoncés, corrigés et fiches prof (nécessite pdflatex)
```

Les versions élèves sont conçues pour **se lancer sans planter** même avant d'être complétées.
Si vous renumérotez un `TODO`, mettez à jour l'étape correspondante dans `TDN.tex`.
