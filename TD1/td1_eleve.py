"""
===============================================================================
  TYPOSTEROIDES  -  TD1 : la boucle de jeu et les mots-asteroides
===============================================================================
  Version ELEVE : completez les TODO dans l'ordre de l'enonce.

  Objectif de la seance (2h) :
      Une fenetre pygame, un vaisseau immobile au centre de l'ecran, et des
      mots qui apparaissent sur les bords puis foncent vers lui. Si un mot
      touche le vaisseau, le joueur perd une vie. A 0 vie : GAME OVER.
      (La frappe au clavier pour detruire les mots arrive au TD2.)

  Lancement :
      pip install pygame
      python td1_eleve.py

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
        # TODO 10a : Renvoyer True s'il reste au moins une vie, False sinon.
        return True

    def perdre_vie(self):
        """Retire une vie au joueur."""
        # TODO 9b : Retirer une vie au joueur.
        pass

    def dessiner(self, ecran):
        """Dessine le bouclier (cercle) et le vaisseau (triangle)."""
        # TODO 4 : Dessiner un cercle CYAN (bouclier, epaisseur 2) de rayon
        #   self.rayon, puis un triangle BLANC pointe vers le haut au centre.
        #   Aide : pygame.draw.circle(ecran, couleur, centre, rayon, epaisseur)
        #   pygame.draw.polygon(ecran, couleur, [p1, p2, p3])
        pass


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
        # TODO 7 : Tirer un angle t au hasard entre 0 et 2*pi, puis calculer
        #   self.position (un pygame.Vector2) sur l'ellipse de demi-axes
        #   a = LARGEUR/2 + MARGE_APPARITION et b = HAUTEUR/2 + MARGE_APPARITION.
        self.position = pygame.Vector2(0, 0)

        # --- Vecteur vitesse ----------------------------------------------
        # direction = vecteur UNITAIRE (norme 1) qui pointe vers le centre
        # vitesse   = direction * norme de la vitesse (en pixels/seconde)
        # TODO 6a : Calculer self.direction (vecteur unitaire vers le centre)
        #   puis self.vitesse. Aide : (B - A) va de A vers B, .normalize()
        #   renvoie le meme vecteur ramene a une longueur de 1.
        self.direction = pygame.Vector2(0, 0)
        self.vitesse = pygame.Vector2(0, 0)

    def mettre_a_jour(self, dt):
        """Fait avancer le mot pendant dt secondes."""
        # TODO 6b : Integrer le mouvement : position = position + vitesse * dt
        pass

    def touche(self, joueur):
        """Renvoie True si le mot est entre dans le bouclier du joueur."""
        # TODO 9a : Collision cercle/point : le mot touche le joueur si la
        #   distance entre leurs positions est inferieure au rayon du joueur.
        #   Aide : v1.distance_to(v2)
        return False

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
        # TODO 8a : Choisir un texte au hasard dans MOTS, creer un Mot qui vise
        #   la position du joueur, et l'ajouter a la liste self.mots.
        pass

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
        # TODO 8b : Ajouter dt au minuteur. Quand il depasse DELAI_APPARITION,
        #   lui retirer DELAI_APPARITION et faire apparaitre un mot.
        pass

        # --- Deplacement de tous les mots ---------------------------------
        # TODO 6c : Mettre a jour chaque mot de la liste.
        pass

        # --- Collisions avec le joueur ------------------------------------
        # ATTENTION : on ne supprime JAMAIS un element d'une liste pendant
        # qu'on la parcourt. On reconstruit une nouvelle liste a la place.
        # TODO 9c : Construire la liste des mots "survivants". Un mot qui
        #   touche le joueur lui fait perdre une vie et n'est pas garde.
        pass

        # --- Fin de partie ------------------------------------------------
        # TODO 10b : Si le joueur n'est plus vivant : self.game_over = True
        pass

    # ------------------------------------------------------------------ #
    #  3) Dessin                                                         #
    # ------------------------------------------------------------------ #
    def dessiner_fond(self):
        self.ecran.fill(FOND)
        for x, y, taille in self.etoiles:
            pygame.draw.circle(self.ecran, GRIS, (x, y), taille)

    def dessiner_hud(self):
        """HUD = Head-Up Display : les infos affichees par-dessus le jeu."""
        # TODO 11 : Afficher "Vies : N" en haut a gauche (position (20, 15)).
        #   Aide : image = police.render(texte, True, couleur)
        #   self.ecran.blit(image, (x, y))
        pass

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
        # TODO 2 : Ecrire la boucle de jeu : tant que self.en_cours est vrai,
        #   1) attendre la prochaine image et recuperer dt (en SECONDES)
        #   avec self.horloge.tick(FPS) qui renvoie des MILLISECONDES,
        #   2) gerer les evenements, 3) mettre a jour, 4) dessiner.
        pass
        pygame.quit()


# =============================================================================
# 5. POINT D'ENTREE
# =============================================================================
if __name__ == "__main__":
    Jeu().executer()
