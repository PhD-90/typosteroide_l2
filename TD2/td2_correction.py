"""
===============================================================================
  TYPOSTEROIDES  -  TD2 : taper pour survivre
===============================================================================
  Version CORRECTION.

  Objectif de la seance (2h) :
      Partir du jeu du TD1 et le rendre jouable :
        - un menu, une partie, un ecran de fin (machine a etats) ;
        - taper la 1re lettre d'un mot le verrouille, chaque bonne lettre
          tire un laser, le mot explose quand il est entierement tape ;
        - score, combo, precision, mots par minute ;
        - difficulte progressive (vitesse, cadence, longueur des mots).

  Ce fichier (version correction) sert de BASE DE DEPART pour les TP.

  Lancement :
      pip install pygame
      python td2_correction.py

  Commandes :
      Entree : jouer / rejouer       lettres : taper les mots
      Retour arriere : changer de cible        Echap : menu / quitter
===============================================================================
"""

import math
import random

import pygame

# =============================================================================
# 1. CONSTANTES
# =============================================================================
LARGEUR, HAUTEUR = 1000, 700
FPS = 60
TITRE = "Typosteroides"

# Couleurs (Rouge, Vert, Bleu)
FOND = (8, 10, 24)
BLANC = (235, 235, 245)
GRIS = (110, 110, 130)
CYAN = (80, 220, 255)
ROUGE = (255, 80, 90)
ORANGE = (255, 170, 60)
JAUNE = (255, 230, 90)
CADRE = (20, 24, 48)

# Joueur
RAYON_JOUEUR = 30
VIES_INITIALES = 3
LONGUEUR_CANON = 24

# Mots
MARGE_APPARITION = 40
RECUL = 6                    # pixels de recul a chaque lettre touchee
DISTANCE_DANGER = 160        # en dessous, le mot s'affiche en rouge
NB_ETOILES = 120

# Tir
DUREE_LASER = 0.12           # secondes

# Score
POINTS_PAR_LETTRE = 10
COMBO_PAR_PALIER = 10        # +1 au multiplicateur tous les 10 mots
MULTIPLICATEUR_MAX = 4

# Difficulte
MOTS_PAR_NIVEAU = 10
VITESSE_BASE = 45            # pixels / seconde au niveau 1
GAIN_VITESSE = 0.12          # +12 % de vitesse par niveau
DELAI_BASE = 2.4             # secondes entre deux mots au niveau 1
FACTEUR_DELAI = 0.88         # le delai est multiplie par 0.88 a chaque niveau
DELAI_MIN = 0.55
DUREE_MESSAGE_NIVEAU = 1.5

# Les mots sont ranges par longueur : la difficulte choisit dans quels
# paquets on pioche. (Pas d'accents : plus simple a taper sur tout clavier.)
MOTS = {
    "courts": [
        "air", "arc", "axe", "bit", "bloc", "bus", "ciel", "code", "cube",
        "dune", "eau", "feu", "fil", "gaz", "gel", "halo", "ion", "jeu",
        "kilo", "lac", "lune", "mer", "mur", "nuit", "onde", "orbe", "pic",
        "port", "quai", "rail", "roue", "sol", "tank", "vent", "volt",
        "watt", "yoga", "zone",
    ],
    "moyens": [
        "alerte", "boucle", "canon", "comete", "donnee", "eclair", "etoile",
        "fusee", "fusion", "hublot", "impact", "laser", "liste", "module",
        "nuage", "objet", "octet", "orbite", "photon", "python", "quartz",
        "radar", "signal", "sonde", "titan", "tuple", "unique", "vortex",
        "wagon", "xenon", "yaourt", "zenith", "kayak", "jungle", "classe",
    ],
    "longs": [
        "asteroide", "bouclier", "capsule", "cosmique", "energie",
        "fonction", "galaxie", "gravite", "horizon", "integrale", "joystick",
        "kilowatt", "lumiere", "methode", "navette", "orbital", "planete",
        "quantique", "reacteur", "satellite", "telescope", "univers",
        "vaisseau", "variable", "xylophone", "zodiaque",
    ],
    "tres_longs": [
        "algorithme", "atmosphere", "bibliotheque", "compilateur",
        "constellation", "dictionnaire", "encapsulation", "exoplanete",
        "gravitation", "instruction", "interstellaire", "magnetisme",
        "observatoire", "polymorphisme", "propulsion", "recursivite",
        "singularite", "teleportation", "trajectoire",
    ],
}


def mots_du_niveau(niveau):
    """Renvoie la liste des mots dans laquelle on pioche a ce niveau."""
    if niveau <= 2:
        return MOTS["courts"]
    if niveau <= 4:
        return MOTS["courts"] + MOTS["moyens"]
    if niveau <= 6:
        return MOTS["moyens"] + MOTS["longs"]
    return MOTS["longs"] + MOTS["tres_longs"]


# =============================================================================
# 2. LE JOUEUR
# =============================================================================
class Joueur:
    """Le vaisseau au centre ; son canon s'oriente vers le mot vise."""

    def __init__(self):
        self.position = pygame.Vector2(LARGEUR / 2, HAUTEUR / 2)
        self.rayon = RAYON_JOUEUR
        self.vies = VIES_INITIALES
        self.direction = pygame.Vector2(0, -1)   # le canon pointe en haut

    def est_vivant(self):
        return self.vies > 0

    def perdre_vie(self):
        self.vies -= 1

    def viser(self, point):
        """Oriente le canon vers un point de l'ecran."""
        vecteur = point - self.position
        if vecteur.length() > 0:
            self.direction = vecteur.normalize()

    def bout_du_canon(self):
        """Point d'ou partent les lasers."""
        return self.position + self.direction * LONGUEUR_CANON

    def dessiner(self, ecran):
        pygame.draw.circle(ecran, CYAN, self.position, self.rayon, 2)
        d = self.direction
        pointe = self.position + d * 22
        gauche = self.position + d.rotate(140) * 15
        droite = self.position + d.rotate(-140) * 15
        pygame.draw.polygon(ecran, BLANC, [pointe, gauche, droite])


# =============================================================================
# 3. UN MOT-ASTEROIDE
# =============================================================================
class Mot:
    """Un mot qui fonce vers le centre ; on le detruit en le tapant."""

    def __init__(self, texte, centre, vitesse):
        self.texte = texte
        self.tape = 0              # nombre de lettres deja tapees
        self.centre = centre

        angle = random.uniform(0, 2 * math.pi)
        a = LARGEUR / 2 + MARGE_APPARITION
        b = HAUTEUR / 2 + MARGE_APPARITION
        self.position = pygame.Vector2(centre.x + a * math.cos(angle),
                                       centre.y + b * math.sin(angle))
        self.direction = (centre - self.position).normalize()
        self.vitesse = self.direction * vitesse

    # --- Logique de frappe ---------------------------------------------
    def lettre_attendue(self):
        """La prochaine lettre a taper."""
        return self.texte[self.tape]

    def est_termine(self):
        """True quand toutes les lettres ont ete tapees."""
        return self.tape == len(self.texte)

    def taper(self, lettre):
        """Essaie de taper une lettre. Renvoie True si c'etait la bonne."""
        if lettre == self.lettre_attendue():
            self.tape += 1
            self.position -= self.direction * RECUL
            return True
        return False

    def abandonner(self):
        """Le joueur change de cible : le mot repart de zero."""
        self.tape = 0

    # --- Mouvement -----------------------------------------------------
    def mettre_a_jour(self, dt):
        self.position += self.vitesse * dt

    def touche(self, joueur):
        return self.position.distance_to(joueur.position) < joueur.rayon

    # --- Affichage -----------------------------------------------------
    def dessiner(self, ecran, police, est_cible):
        """Partie deja tapee en orange, reste en blanc (ou rouge si danger)."""
        en_danger = self.position.distance_to(self.centre) < DISTANCE_DANGER
        couleur_reste = ROUGE if en_danger else BLANC

        image_tapee = police.render(self.texte[:self.tape], True, ORANGE)
        image_reste = police.render(self.texte[self.tape:], True,
                                    couleur_reste)
        largeur = image_tapee.get_width() + image_reste.get_width()
        hauteur = police.get_height()
        x = self.position.x - largeur / 2
        y = self.position.y - hauteur / 2

        fond = pygame.Rect(x - 6, y - 2, largeur + 12, hauteur + 4)
        pygame.draw.rect(ecran, CADRE, fond, border_radius=6)
        if est_cible:
            pygame.draw.rect(ecran, ORANGE, fond, 2, border_radius=6)

        ecran.blit(image_tapee, (x, y))
        ecran.blit(image_reste, (x + image_tapee.get_width(), y))


# =============================================================================
# 4. UN TIR LASER (purement visuel)
# =============================================================================
class Laser:
    """Un trait lumineux qui s'efface en DUREE_LASER secondes."""

    def __init__(self, depart, arrivee):
        self.depart = pygame.Vector2(depart)      # copies : le mot continue
        self.arrivee = pygame.Vector2(arrivee)    # de bouger, pas le laser
        self.temps_restant = DUREE_LASER

    def mettre_a_jour(self, dt):
        self.temps_restant -= dt

    def est_fini(self):
        return self.temps_restant <= 0

    def dessiner(self, ecran):
        ratio = max(0.0, self.temps_restant / DUREE_LASER)
        couleur = tuple(int(f + (c - f) * ratio) for c, f in zip(CYAN, FOND))
        epaisseur = 1 + int(3 * ratio)
        pygame.draw.line(ecran, couleur, self.depart, self.arrivee, epaisseur)


# =============================================================================
# 5. LE JEU
# =============================================================================
class Jeu:
    """Etat global + boucle principale. self.etat vaut "menu", "jeu" ou
    "game_over" : c'est une MACHINE A ETATS."""

    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption(TITRE)
        self.horloge = pygame.time.Clock()

        self.police_mot = pygame.font.SysFont("consolas", 26, bold=True)
        self.police_hud = pygame.font.SysFont("consolas", 22)
        self.police_titre = pygame.font.SysFont("consolas", 64, bold=True)

        self.etoiles = [(random.randint(0, LARGEUR),
                         random.randint(0, HAUTEUR),
                         random.randint(1, 2)) for _ in range(NB_ETOILES)]

        self.meilleur_score = 0    # garde pendant la session (fichier : TP)
        self.en_cours = True
        self.etat = "menu"
        self.nouvelle_partie()

    def nouvelle_partie(self):
        self.joueur = Joueur()
        self.mots = []
        self.lasers = []
        self.cible = None          # le Mot verrouille, ou None

        self.niveau = 1
        self.minuteur_apparition = self.delai_actuel()
        self.message_niveau = 0.0  # temps d'affichage restant de "NIVEAU n"

        self.score = 0
        self.combo = 0
        self.meilleur_combo = 0
        self.mots_detruits = 0
        self.frappes_correctes = 0
        self.frappes_totales = 0
        self.temps_jeu = 0.0

    # ------------------------------------------------------------------ #
    #  Difficulte                                                        #
    # ------------------------------------------------------------------ #
    def vitesse_actuelle(self):
        return VITESSE_BASE * (1 + GAIN_VITESSE * (self.niveau - 1))

    def delai_actuel(self):
        return max(DELAI_MIN, DELAI_BASE * FACTEUR_DELAI ** (self.niveau - 1))

    def faire_apparaitre_mot(self):
        reserve = mots_du_niveau(self.niveau)
        initiales = {mot.texte[0] for mot in self.mots}
        libres = [m for m in reserve if m[0] not in initiales]
        texte = random.choice(libres if libres else reserve)
        vitesse = self.vitesse_actuelle() * random.uniform(0.85, 1.15)
        self.mots.append(Mot(texte, self.joueur.position, vitesse))

    # ------------------------------------------------------------------ #
    #  Frappe et ciblage                                                 #
    # ------------------------------------------------------------------ #
    def chercher_cible(self, lettre):
        """Renvoie le mot le plus proche du joueur qui commence par
        `lettre`, ou None s'il n'y en a pas."""
        meilleur = None
        meilleure_distance = math.inf
        for mot in self.mots:
            if mot.texte[0] == lettre:
                distance = mot.position.distance_to(self.joueur.position)
                if distance < meilleure_distance:
                    meilleur = mot
                    meilleure_distance = distance
        return meilleur

    def gerer_frappe(self, lettre):
        """Appelee a chaque lettre tapee pendant la partie."""
        self.frappes_totales += 1
        if self.cible is None:
            self.cible = self.chercher_cible(lettre)
            if self.cible is None:
                self.rater()
                return

        if self.cible.taper(lettre):
            self.frappes_correctes += 1
            self.joueur.viser(self.cible.position)
            self.lasers.append(Laser(self.joueur.bout_du_canon(),
                                     self.cible.position))
            if self.cible.est_termine():
                self.detruire(self.cible)
        else:
            self.rater()

    def changer_de_cible(self):
        if self.cible is not None:
            self.cible.abandonner()
            self.cible = None

    def rater(self):
        """Une faute de frappe casse le combo."""
        self.combo = 0

    def multiplicateur(self):
        return min(1 + self.combo // COMBO_PAR_PALIER, MULTIPLICATEUR_MAX)

    def detruire(self, mot):
        """Le mot est entierement tape : on le retire et on marque des points."""
        self.mots.remove(mot)
        self.cible = None
        self.mots_detruits += 1
        self.combo += 1
        self.meilleur_combo = max(self.meilleur_combo, self.combo)
        self.score += POINTS_PAR_LETTRE * len(mot.texte) * self.multiplicateur()

        nouveau_niveau = 1 + self.mots_detruits // MOTS_PAR_NIVEAU
        if nouveau_niveau > self.niveau:
            self.niveau = nouveau_niveau
            self.message_niveau = DUREE_MESSAGE_NIVEAU

    # --- Statistiques -------------------------------------------------
    def precision(self):
        """Pourcentage de frappes correctes."""
        if self.frappes_totales == 0:
            return 100.0
        return 100 * self.frappes_correctes / self.frappes_totales

    def mpm(self):
        """Mots par minute, convention standard : 1 mot = 5 frappes."""
        if self.temps_jeu < 1:
            return 0.0
        return (self.frappes_correctes / 5) / (self.temps_jeu / 60)

    # ------------------------------------------------------------------ #
    #  1) Evenements                                                     #
    # ------------------------------------------------------------------ #
    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                self.gerer_touche(evenement)

    def gerer_touche(self, evenement):
        entree = evenement.key in (pygame.K_RETURN, pygame.K_KP_ENTER)
        if self.etat == "menu":
            if entree:
                self.nouvelle_partie()
                self.etat = "jeu"
            elif evenement.key == pygame.K_ESCAPE:
                self.en_cours = False

        elif self.etat == "jeu":
            if evenement.key == pygame.K_ESCAPE:
                self.etat = "menu"
            elif evenement.key == pygame.K_BACKSPACE:
                self.changer_de_cible()
            elif evenement.unicode.isalpha():
                self.gerer_frappe(evenement.unicode.lower())

        elif self.etat == "game_over":
            if entree:
                self.nouvelle_partie()
                self.etat = "jeu"
            elif evenement.key == pygame.K_ESCAPE:
                self.etat = "menu"

    # ------------------------------------------------------------------ #
    #  2) Mise a jour                                                    #
    # ------------------------------------------------------------------ #
    def mettre_a_jour(self, dt):
        # Les etats "menu" et "game_over" sont figes
        if self.etat != "jeu":
            return

        self.temps_jeu += dt
        self.message_niveau = max(0.0, self.message_niveau - dt)

        # Apparitions : le delai depend du niveau
        self.minuteur_apparition += dt
        delai = self.delai_actuel()
        if self.minuteur_apparition >= delai:
            self.minuteur_apparition -= delai
            self.faire_apparaitre_mot()

        for mot in self.mots:
            mot.mettre_a_jour(dt)

        for laser in self.lasers:
            laser.mettre_a_jour(dt)
        self.lasers = [laser for laser in self.lasers if not laser.est_fini()]

        # Collisions
        survivants = []
        for mot in self.mots:
            if mot.touche(self.joueur):
                self.joueur.perdre_vie()
                self.combo = 0
                if mot is self.cible:
                    self.cible = None
            else:
                survivants.append(mot)
        self.mots = survivants

        if not self.joueur.est_vivant():
            self.meilleur_score = max(self.meilleur_score, self.score)
            self.etat = "game_over"

    # ------------------------------------------------------------------ #
    #  3) Dessin                                                         #
    # ------------------------------------------------------------------ #
    def ecrire(self, texte, police, couleur, **position):
        """Petit utilitaire : affiche un texte. Exemple :
        self.ecrire("Score", police, BLANC, topleft=(20, 15))"""
        image = police.render(texte, True, couleur)
        self.ecran.blit(image, image.get_rect(**position))

    def dessiner_fond(self):
        self.ecran.fill(FOND)
        for x, y, taille in self.etoiles:
            pygame.draw.circle(self.ecran, GRIS, (x, y), taille)

    def dessiner_partie(self):
        # La cible est dessinee en dernier pour passer au-dessus des autres
        for mot in self.mots:
            if mot is not self.cible:
                mot.dessiner(self.ecran, self.police_mot, False)
        if self.cible is not None:
            self.cible.dessiner(self.ecran, self.police_mot, True)
        for laser in self.lasers:
            laser.dessiner(self.ecran)
        self.joueur.dessiner(self.ecran)

    def dessiner_hud(self):
        h = self.police_hud
        self.ecrire(f"Score  {self.score}", h, BLANC, topleft=(20, 15))
        self.ecrire(f"Niveau {self.niveau}", h, BLANC, topleft=(20, 42))
        self.ecrire(f"Combo  {self.combo}  x{self.multiplicateur()}", h,
                    JAUNE if self.multiplicateur() > 1 else GRIS,
                    topleft=(20, 69))
        self.ecrire(f"Precision {self.precision():5.1f} %", h, GRIS,
                    bottomleft=(20, HAUTEUR - 15))
        self.ecrire(f"{self.mpm():5.1f} mots/min", h, GRIS,
                    bottomright=(LARGEUR - 20, HAUTEUR - 15))
        # Vies : un petit cercle plein par vie
        for i in range(self.joueur.vies):
            pygame.draw.circle(self.ecran, ROUGE,
                               (LARGEUR - 30 - i * 28, 28), 9)

        if self.message_niveau > 0:
            self.ecrire(f"NIVEAU {self.niveau}", self.police_titre, JAUNE,
                        center=(LARGEUR / 2, HAUTEUR / 4))

    def dessiner_menu(self):
        cx = LARGEUR / 2
        self.ecrire("TYPOSTEROIDES", self.police_titre, CYAN,
                    center=(cx, HAUTEUR / 3))
        lignes = [
            "Des mots foncent sur votre vaisseau : tapez-les pour les detruire.",
            "La 1re lettre verrouille la cible, Retour arriere la libere.",
            "",
            "ENTREE : jouer        ECHAP : quitter",
        ]
        for i, ligne in enumerate(lignes):
            self.ecrire(ligne, self.police_hud, BLANC,
                        center=(cx, HAUTEUR / 2 + i * 32))
        if self.meilleur_score > 0:
            self.ecrire(f"Meilleur score : {self.meilleur_score}",
                        self.police_hud, JAUNE,
                        center=(cx, HAUTEUR - 80))

    def dessiner_game_over(self):
        # Voile sombre semi-transparent par-dessus la partie figee
        voile = pygame.Surface((LARGEUR, HAUTEUR), pygame.SRCALPHA)
        voile.fill((0, 0, 0, 170))
        self.ecran.blit(voile, (0, 0))

        cx = LARGEUR / 2
        self.ecrire("GAME OVER", self.police_titre, ROUGE,
                    center=(cx, HAUTEUR / 3))
        lignes = [
            f"Score            {self.score}",
            f"Meilleur score   {self.meilleur_score}",
            f"Niveau           {self.niveau}",
            f"Mots detruits    {self.mots_detruits}",
            f"Meilleur combo   {self.meilleur_combo}",
            f"Precision        {self.precision():.1f} %",
            f"Vitesse          {self.mpm():.1f} mots/min",
        ]
        for i, ligne in enumerate(lignes):
            self.ecrire(ligne, self.police_hud, BLANC,
                        midleft=(cx - 170, HAUTEUR / 3 + 70 + i * 30))
        self.ecrire("ENTREE : rejouer     ECHAP : menu", self.police_hud,
                    JAUNE, center=(cx, HAUTEUR - 60))

    def dessiner(self):
        self.dessiner_fond()
        if self.etat == "menu":
            self.dessiner_menu()
        elif self.etat == "jeu":
            self.dessiner_partie()
            self.dessiner_hud()
        elif self.etat == "game_over":
            self.dessiner_partie()
            self.dessiner_game_over()
        pygame.display.flip()

    # ------------------------------------------------------------------ #
    #  Boucle de jeu (identique au TD1)                                  #
    # ------------------------------------------------------------------ #
    def executer(self):
        while self.en_cours:
            dt = self.horloge.tick(FPS) / 1000
            self.gerer_evenements()
            self.mettre_a_jour(dt)
            self.dessiner()
        pygame.quit()


# =============================================================================
# 6. POINT D'ENTREE
# =============================================================================
if __name__ == "__main__":
    Jeu().executer()
