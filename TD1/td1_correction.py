"""
===============================================================================
  TYPOSTEROIDES  -  TD1 : la boucle de jeu et les mots-asteroides
===============================================================================
  Version CORRECTION.

  Objectif de la seance (2h) :
      Une fenetre pygame, un vaisseau immobile au centre de l'ecran, et des
      mots qui apparaissent sur les bords puis foncent vers lui. Si un mot
      touche le vaisseau, le joueur perd une vie. A 0 vie : GAME OVER.
      (La frappe au clavier pour detruire les mots arrive au TD2.)

  Lancement :
      pip install pygame
      python td1_correction.py

  Commandes :
      Echap : quitter        R : rejouer (apres un game over)
===============================================================================
"""

import math
import random

import pygame

# =============================================================================
# 1. CONSTANTES
#    Tous les "reglages" du jeu sont regroupes ici, en MAJUSCULES.
#    Pour equilibrer le jeu, on ne touche qu'a cette partie.
# =============================================================================
LARGEUR, HAUTEUR = 1000, 700
FPS = 60
TITRE = "Typosteroides - TD1"

# Couleurs (Rouge, Vert, Bleu) entre 0 et 255
FOND = (8, 10, 24)
BLANC = (235, 235, 245)
GRIS = (110, 110, 130)
CYAN = (80, 220, 255)
ROUGE = (255, 80, 90)

# Joueur
RAYON_JOUEUR = 30            # rayon du bouclier (pixels)
VIES_INITIALES = 3

# Mots
VITESSE_MOT = 55             # pixels par seconde
DELAI_APPARITION = 2.0       # secondes entre deux apparitions
MARGE_APPARITION = 40        # les mots naissent un peu en dehors de l'ecran
NB_ETOILES = 120

MOTS = [
    "air", "arc", "axe", "bit", "bloc", "bus", "ciel", "code", "cube",
    "dune", "eau", "feu", "fil", "gaz", "gel", "halo", "ion", "jeu", "kilo",
    "lac", "lune", "mer", "mur", "nuit", "onde", "orbe", "pic", "port",
    "quai", "rail", "roue", "sol", "vent", "volt", "watt", "yoga", "zone",
    "canon", "comete", "fusee", "laser", "nuage", "orbite", "photon",
    "radar", "signal", "sonde", "titan", "vortex", "python", "objet",
]


# =============================================================================
# 2. LE JOUEUR
# =============================================================================
class Joueur:
    """Le vaisseau, immobile au centre de l'ecran."""

    def __init__(self):
        # pygame.Vector2 : un vecteur (x, y) avec lequel on peut calculer
        self.position = pygame.Vector2(LARGEUR / 2, HAUTEUR / 2)
        self.rayon = RAYON_JOUEUR
        self.vies = VIES_INITIALES

    def est_vivant(self):
        """Renvoie True s'il reste au moins une vie."""
        return self.vies > 0

    def perdre_vie(self):
        """Retire une vie au joueur."""
        self.vies -= 1

    def dessiner(self, ecran):
        """Dessine le bouclier (cercle) et le vaisseau (triangle)."""
        x, y = self.position
        pygame.draw.circle(ecran, CYAN, self.position, self.rayon, 2)
        pointe = (x, y - 18)
        gauche = (x - 13, y + 12)
        droite = (x + 13, y + 12)
        pygame.draw.polygon(ecran, BLANC, [pointe, gauche, droite])


# =============================================================================
# 3. UN MOT-ASTEROIDE
# =============================================================================
class Mot:
    """Un mot qui avance en ligne droite, a vitesse constante, vers un centre."""

    def __init__(self, texte, centre, vitesse):
        self.texte = texte

        # --- Position de depart -------------------------------------------
        # Un point au hasard sur une ellipse qui entoure l'ecran :
        #     x = cx + a * cos(t)      y = cy + b * sin(t)
        angle = random.uniform(0, 2 * math.pi)
        a = LARGEUR / 2 + MARGE_APPARITION
        b = HAUTEUR / 2 + MARGE_APPARITION
        self.position = pygame.Vector2(centre.x + a * math.cos(angle),
                                       centre.y + b * math.sin(angle))

        # --- Vecteur vitesse ----------------------------------------------
        # direction = vecteur UNITAIRE (norme 1) qui pointe vers le centre
        # vitesse   = direction * norme de la vitesse (en pixels/seconde)
        self.direction = (centre - self.position).normalize()
        self.vitesse = self.direction * vitesse

    def mettre_a_jour(self, dt):
        """Fait avancer le mot pendant dt secondes."""
        self.position += self.vitesse * dt

    def touche(self, joueur):
        """Renvoie True si le mot est entre dans le bouclier du joueur."""
        return self.position.distance_to(joueur.position) < joueur.rayon

    def dessiner(self, ecran, police):
        """Affiche le texte du mot, centre sur sa position."""
        image = police.render(self.texte, True, BLANC)
        rectangle = image.get_rect(center=self.position)
        ecran.blit(image, rectangle)


# =============================================================================
# 4. LE JEU
# =============================================================================
class Jeu:
    """Contient tout l'etat du jeu et la boucle principale."""

    def __init__(self):
        pygame.init()
        self.ecran = pygame.display.set_mode((LARGEUR, HAUTEUR))
        pygame.display.set_caption(TITRE)
        self.horloge = pygame.time.Clock()

        self.police_mot = pygame.font.SysFont("consolas", 26, bold=True)
        self.police_hud = pygame.font.SysFont("consolas", 22)
        self.police_titre = pygame.font.SysFont("consolas", 64, bold=True)

        # Fond etoile : une liste de tuples (x, y, taille)
        self.etoiles = [(random.randint(0, LARGEUR),
                         random.randint(0, HAUTEUR),
                         random.randint(1, 2)) for _ in range(NB_ETOILES)]

        self.en_cours = True
        self.nouvelle_partie()

    def nouvelle_partie(self):
        """(Re)initialise tout ce qui change pendant une partie."""
        self.joueur = Joueur()
        self.mots = []
        # On demarre le minuteur "plein" pour qu'un mot apparaisse tout de suite
        self.minuteur_apparition = DELAI_APPARITION
        self.game_over = False

    # ------------------------------------------------------------------ #
    #  Apparition des mots                                               #
    # ------------------------------------------------------------------ #
    def faire_apparaitre_mot(self):
        """Cree un nouveau mot au hasard et l'ajoute a la liste."""
        texte = random.choice(MOTS)
        self.mots.append(Mot(texte, self.joueur.position, VITESSE_MOT))

    # ------------------------------------------------------------------ #
    #  1) Evenements                                                     #
    # ------------------------------------------------------------------ #
    def gerer_evenements(self):
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                self.en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_ESCAPE:
                    self.en_cours = False
                elif evenement.key == pygame.K_r and self.game_over:
                    self.nouvelle_partie()

    # ------------------------------------------------------------------ #
    #  2) Mise a jour                                                    #
    # ------------------------------------------------------------------ #
    def mettre_a_jour(self, dt):
        if self.game_over:
            return

        # --- Minuteur d'apparition ----------------------------------------
        self.minuteur_apparition += dt
        if self.minuteur_apparition >= DELAI_APPARITION:
            self.minuteur_apparition -= DELAI_APPARITION
            self.faire_apparaitre_mot()

        # --- Deplacement de tous les mots ---------------------------------
        for mot in self.mots:
            mot.mettre_a_jour(dt)

        # --- Collisions avec le joueur ------------------------------------
        # ATTENTION : on ne supprime JAMAIS un element d'une liste pendant
        # qu'on la parcourt. On reconstruit une nouvelle liste a la place.
        survivants = []
        for mot in self.mots:
            if mot.touche(self.joueur):
                self.joueur.perdre_vie()
            else:
                survivants.append(mot)
        self.mots = survivants

        # --- Fin de partie ------------------------------------------------
        if not self.joueur.est_vivant():
            self.game_over = True

    # ------------------------------------------------------------------ #
    #  3) Dessin                                                         #
    # ------------------------------------------------------------------ #
    def dessiner_fond(self):
        self.ecran.fill(FOND)
        for x, y, taille in self.etoiles:
            pygame.draw.circle(self.ecran, GRIS, (x, y), taille)

    def dessiner_hud(self):
        """HUD = Head-Up Display : les infos affichees par-dessus le jeu."""
        texte = f"Vies : {self.joueur.vies}"
        image = self.police_hud.render(texte, True, BLANC)
        self.ecran.blit(image, (20, 15))

    def dessiner_game_over(self):
        titre = self.police_titre.render("GAME OVER", True, ROUGE)
        aide = self.police_hud.render("R : rejouer    Echap : quitter",
                                      True, BLANC)
        cx, cy = LARGEUR / 2, HAUTEUR / 2
        self.ecran.blit(titre, titre.get_rect(center=(cx, cy - 30)))
        self.ecran.blit(aide, aide.get_rect(center=(cx, cy + 30)))

    def dessiner(self):
        self.dessiner_fond()
        for mot in self.mots:
            mot.dessiner(self.ecran, self.police_mot)
        self.joueur.dessiner(self.ecran)
        self.dessiner_hud()
        if self.game_over:
            self.dessiner_game_over()
        # On affiche enfin a l'ecran l'image qu'on vient de composer
        pygame.display.flip()

    # ------------------------------------------------------------------ #
    #  La boucle de jeu                                                  #
    # ------------------------------------------------------------------ #
    def executer(self):
        while self.en_cours:
            dt = self.horloge.tick(FPS) / 1000
            self.gerer_evenements()
            self.mettre_a_jour(dt)
            self.dessiner()
        pygame.quit()


# =============================================================================
# 5. POINT D'ENTREE
# =============================================================================
if __name__ == "__main__":
    Jeu().executer()
