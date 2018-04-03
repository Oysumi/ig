#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Université de Lorraine - Licence informatique
# Fonction générale d'affichage du module ig
#
################################################################################

################################################################################
# Chargement des modules standards
################################################################################
import sys
import pygame
import time
import math
################################################################################

################################################################################
# Chargement des définitions du module ig
################################################################################
import ecran as ecr
import donnees as don
from base import *
from evenements import *
from cube import *
from transfos import *
from segments import *
from fenim import *
from fonction import *
from param import *
from tangentes import *
from bezier import *
from remplissage import *
from iso import *
from triangles import *
################################################################################

################################################################################
# Affichage  principal : dessins successifs des différents TPs
################################################################################
def Affichage(action):
    # Variables locales
    Bleu = don.Couleur(0, 0, 255)        # Définition de la couleur bleue
    Jaune = don.Couleur(255, 255, 0)     # Définition de la couleur jaune
    Rouge = don.Couleur(255, 0, 0)       # Définition de la couleur rouge
    Cyan = don.Couleur(0, 255, 255)      # Définition de la couleur verte
    Blanc = don.Couleur(255, 255, 255)   # Définition du blanc (ce n'est pas une couleur !)
    couleur = don.Couleur(200, 150, 250) # Couleur de dessin des segments
    fi = don.FenetreImage()              # Fenêtre image

    # Détermination de la dimension minimale de la fenêtre
    minDim = ecr.Hauteur
    if minDim > ecr.Largeur:
        minDim = ecr.Largeur

    # Réglage automatique de la fenêtre image
    fi.bg.col = don.MARGE + (ecr.Largeur - minDim) // 2
    fi.bg.lig = minDim - don.MARGE - (ecr.Hauteur - minDim) // 2
    fi.hd.col = ecr.Largeur - don.MARGE - (ecr.Largeur - minDim) // 2
    fi.hd.lig = don.MARGE + (ecr.Hauteur - minDim) // 2

    # Réglage automatique de la fenêtre réelle
    fr = don.FenetreReel(don.PointReel(-11.0,-11.0), don.PointReel(11.0,11.0))
    
    # Affichage seulement s'il n'a pas déjà été fait (pour éviter une charge CPU inutile)
    if (not don.dejaFait):
        don.aMettreAJour = True # Indique qu'il faudra mettre à jour l'écran
        don.dejaFait = True     # Indique que les dessins sont faits

        #
        # Sélection de l'action à effectuer
        #
        if action == don.Actions.CUBE: 
            #
            # Cube des couleurs
            #

            Effacer()   # Initialisation de la fenêtre en noir
            AfficheTexte("Cube des couleurs", (600, don.MARGE), Jaune)
            DessineRectangleUni(PointImage(10,10), PointImage(200,200), don.Couleur(245, 123, 20))
            DessineRectangleUni(PointImage(600,525), PointImage(700,700), don.Couleur(45, 223, 20))
            DessineRectangleUni(PointImage(10,550), PointImage(200,650), don.Couleur(45, 123, 120))
            DessineRectangleUni(PointImage(550,125), PointImage(850,225), don.Couleur(145, 223, 250))
            DessineFacesCubeCouleurs() # Affichage des faces du cube

        elif action == don.Actions.TRIANGLES:
            #
            # Segments et triangles vides
            #

            Effacer()   # Initialisation de la fenêtre en noir
            AfficheTexte("Triangles", (don.MARGE, don.MARGE), Jaune)

            # Dessin du contour de la fenêtre image
            DessineContours(fi, Rouge)

            # Dessin d'un triangle image en traits pleins
            i1 = PointImage(fi.bg.col + 10, fi.bg.lig - 10)
            i2 = PointImage(fi.hd.col - 10, (2*fi.bg.lig + fi.hd.lig)//3)
            i3 = PointImage((fi.bg.col + fi.hd.col)//2, fi.hd.lig + 10)
            DessineTriangleImage(i1, i2, i3, Cyan)

            # Dessin d'un triangle image en pointillés
            i1 = PointImage(i1.col + 20, i1.lig - 15)
            i2 = PointImage(i2.col - 20, i2.lig - 5)
            i3 = PointImage(i3.col, i3.lig + 20)
            DessineTriangleImage(i1, i2, i3, Cyan, 4)

            # Calcul de la transfo Réel -> Image
            don.tr1 = CalculTransfosFenetres(fr, fi)
            
            # Dessin de triangles réels sortant de la fenêtre image
            r1 = don.PointReel(0.0,  0.0)
            r2 = don.PointReel(15.0,  2.5)
            r3 = don.PointReel(-7.5, 12.5)
            DessineTriangleReel(r1, r2, r3, Jaune, don.tr1, 3)
            DessineTriangleReel(r1, r2, r3, Bleu, don.tr1)
            DessinePointReel(r1, Jaune, don.tr1)
            DessinePointReel(r2, Jaune, don.tr1)
            DessinePointReel(r3, Jaune, don.tr1)

            r1 = don.PointReel(-15.0, -3.0)
            r2 = don.PointReel(2.0,  -12.0)
            r3 = don.PointReel(17.5,  -1.5)
            DessineTriangleReel(r1, r2, r3, Jaune, don.tr1, 3)
            DessineTriangleReel(r1, r2, r3, Bleu, don.tr1)
            DessinePointReel(r1, Jaune, don.tr1)
            DessinePointReel(r2, Jaune, don.tr1)
            DessinePointReel(r3, Jaune, don.tr1)
    
        elif action == don.Actions.TRISPLEINS: 
            #
            # Étape optionnelle : triangles pleins
            #

            if (ecr.fenCop == None): # 1ère exécution

               don.fond = don.Couleur(255,255,255)
               Effacer()   # Initialisation de la fenêtre en noir

               AfficheTexte("Triangles pleins et transparence", (600, don.MARGE), don.Couleur(0, 0, 0))
               AfficheTexte("Premier pas vers la visu 3D 'solide'", (600, 3*don.MARGE//2), don.Couleur(0, 0, 0))
               AfficheTexte("Si on a le temps...", (600, 2*don.MARGE), don.Couleur(0, 0, 0))

               DessineTrianglePlein(don.PointImage(10,10), don.PointImage(30,40), don.PointImage(40,30), Bleu)
               DessineTrianglePlein(don.PointImage(250,250), don.PointImage(100,100), don.PointImage(0,250), don.Couleur(128,128,128))
               DessineTrianglePlein(don.PointImage(100,10), don.PointImage(300,50), don.PointImage(150,200), don.Couleur(255,0,0,200))
               DessineTrianglePlein(don.PointImage(80,200), don.PointImage(200,400), don.PointImage(50,350), Jaune)

               don.fond = don.Couleur(0,0,0)

               ecr.fenCop = ecr.fen.copy()
            else:                    # exécutions suivantes
               ecr.fen.blit(ecr.fenCop, (0,0))

        elif action == don.Actions.FUSEAU1: 
            #
            # Fuseau issu du point haut-gauche
            #

            Effacer()   # Initialisation de la fenêtre en noir
            AfficheTexte("Fuseau n°1", (don.MARGE, don.MARGE), Jaune)

            # Dessin du contour de la fenêtre image
            DessineContours(fi, Rouge)

            # Calcul de la transfo Réel -> Image
            don.tr1 = CalculTransfosFenetres(fr, fi) # Calcul de la transfo Réel -> Image

            # Définition des points extrêmes
            pr1 = don.PointReel(-12.0, -12.0)
            pr2 = don.PointReel( 12.0,  12.0)

            # Dessin du fuseau
            DessineFuseau(pr1, pr2, "hg", Bleu, Jaune)

        elif action == don.Actions.FUSEAU2: 
            #
            # Fuseau issu du point haut-droit
            #

            Effacer()   # Initialisation de la fenêtre en noir
            AfficheTexte("Fuseau n°2", (don.MARGE, don.MARGE), Jaune)

            # Dessin du contour de la fenêtre image
            DessineContours(fi, Rouge)

            # Calcul de la transfo Réel -> Image
            don.tr1 = CalculTransfosFenetres(fr, fi) # Calcul de la transfo Réel -> Image

            # Définition des points extrêmes
            pr1 = don.PointReel(-12.0, -12.0)
            pr2 = don.PointReel( 12.0,  12.0)

            # Dessin du fuseau
            DessineFuseau(pr1, pr2, "hd", Bleu, Jaune)

        elif action == don.Actions.FUSEAU3:
            #
            # Fuseau issu du point bas-droit
            #

            Effacer()   # Initialisation de la fenêtre en noir
            AfficheTexte("Fuseau n°3", (don.MARGE, don.MARGE), Jaune)

            # Dessin du contour de la fenêtre image
            DessineContours(fi, Rouge)

            # Calcul de la transfo Réel -> Image
            don.tr1 = CalculTransfosFenetres(fr, fi) # Calcul de la transfo Réel -> Image

            # Définition des points extrêmes
            pr1 = don.PointReel(-12.0, -12.0)
            pr2 = don.PointReel( 12.0,  12.0)

            # Dessin du fuseau
            DessineFuseau(pr1, pr2, "bd", Bleu, Jaune)

        elif action == don.Actions.FUSEAU4:
            #
            # Fuseau issu du point bas-gauche
            #

            Effacer()   # Initialisation de la fenêtre en noir
            AfficheTexte("Fuseau n°4", (don.MARGE, don.MARGE), Jaune)

            # Dessin du contour de la fenêtre image
            DessineContours(fi, Rouge)

            # Calcul de la transfo Réel -> Image
            don.tr1 = CalculTransfosFenetres(fr, fi) # Calcul de la transfo Réel -> Image

            # Définition des points extrêmes
            pr1 = don.PointReel(-12.0, -12.0)
            pr2 = don.PointReel( 12.0,  12.0)

            # Dessin du fuseau
            DessineFuseau(pr1, pr2, "bg", Bleu, Jaune)
            
        elif action == don.Actions.FONCTION:
            #
            # Dessin d'une fonction analytique
            #

            if (ecr.fenCop == None): # 1ère exécution
                Effacer()
                AfficheTexte("Fonction et tangentes", (don.MARGE, don.MARGE), Jaune)

                # Définition de la fenêtre réelle pour la fonction sinus
                fr = FenetreReel(don.PointReel(-3.0,-3.0), don.PointReel(3.0,3.0))
                # Calcul de la transformation
                don.tr1 = CalculTransfosFenetres(fr, fi)

                # Dessin des contours et des axes avec graduations
                DessineContours(fi, Rouge)
                DessineAxes(1.0, don.tr1, Rouge, 1, 5)

                # Dessin de la fonction
                DessineFonction(couleur, don.tr1)
            
                # Dessin de la tangente en plusieurs points
                DessineTangente(-2.0, "f", Jaune, don.tr1)
                DessineTangente(0.0, "f", Jaune, don.tr1)
                DessineTangente(2.0, "f", Jaune, don.tr1)

                # Initialisation position de départ pour animation
                don.position = -3.0

                # Récupération de la 1ère image générée
                ecr.fenCop = ecr.fen.copy()
            else:                    # exécutions suivantes
                # Affichage de la 1ère image générée
                ecr.fen.blit(ecr.fenCop, (0,0))

            # Animation
            DessineTangente(don.position, "f", Cyan, don.tr1)
            if (don.position <= 3.0 and don.tr1.riA != None):
                don.position += 2.0 / don.tr1.riA
                don.dejaFait = False

            # Lecture d'un point
            if (don.posS != None):
                pr = TransformationIvR(don.posS, don.tr1)
                pr.y = FonctionF(pr.x)
                pi = TransformationRvI(pr, don.tr1)
                DessineTangente(pr.x, "f", Cyan, don.tr1)
                ColoriePoint(pi, Jaune, 2)
                texte = "sin(%.3f) = %.3f" % (pr.x,pr.y)
                AfficheTexte(texte, (don.MARGE, 3*don.MARGE/2), Jaune, False, 18)
                                    
        elif action == don.Actions.PARAM:
            #
            # Dessin d'une courbe paramétrique
            #

            if (ecr.fenCop == None): # 1ère exécution
                Effacer()
                AfficheTexte("Courbe paramétrique", (don.MARGE, don.MARGE), Jaune)

                # Définition des deux fenêtres image et deux fenêtres réelles
                fi1 = FenetreImage(don.PointImage(20,400), don.PointImage(620,100))
                fi2 = FenetreImage(don.PointImage(640,400), don.PointImage(940,100))
                fr1 = FenetreReel(don.PointReel(0.0,-30.0),don.PointReel(120.0,30.0))
                fr2 = FenetreReel(don.PointReel(0.0,-16.0),don.PointReel(32.0,16.0))

                # Calculs des transformations entre les fenêtres réel et image
                don.tr1 = CalculTransfosFenetres(fr1, fi1)
                don.tr2 = CalculTransfosFenetres(fr2, fi2)

                # Dessin des contours et des axes
                DessineContours(fi1, Rouge)
                DessineContours(fi2, Rouge)
                DessineAxes(5.0, don.tr1, Rouge)
                DessineAxes(5.0, don.tr2, Rouge, 1, 5)

                # Tracé dans première fenêtre
                DessineCourbeParametrique(-2*3.15, 2*3.15, 0.5, couleur, don.tr1, True)

                # Tracé dans seconde fenêtre
                DessineCourbeParametrique(-2*3.15, 2*3.15, 0.1, couleur, don.tr2, True)

                # Dessin de la tangente en plusieurs points
                DessineTangente(-3.14/2, "p", Jaune, don.tr1)
                DessineTangente(0.0, "p", Jaune, don.tr1)
                DessineTangente(3.14/2, "p", Jaune, don.tr1)
                DessineTangente(3.14, "p", Jaune, don.tr2)
                DessineTangente(-3.14, "p", Jaune, don.tr2)

                # Initialisation position de départ pour animation
                don.position = 0.0

                # Récupération de la 1ère image générée
                ecr.fenCop = ecr.fen.copy()
            else:                    # exécutions suivantes
                # Affichage de la 1ère image générée
                ecr.fen.blit(ecr.fenCop, (0,0))

            # Animation
            DessineTangente(don.position, "p", Cyan, don.tr1)
            DessineTangente(don.position, "p", Cyan, don.tr2)
            if (don.position <= 4*3.15 and don.tr2.riA != None):
                don.position += 0.1 / don.tr2.riA
                don.dejaFait = False

        elif action == don.Actions.BEZIER:
            #
            # Dessin de courbes de Bezier de degrés 1, 2 et 3
            #

            if (ecr.fenCop == None): # 1ère exécution
                Effacer()   # Initialisation de la fenêtre en noir
                AfficheTexte("Courbes de Bezier", (don.MARGE, don.MARGE), Jaune)

                # Dessin du contour de la fenêtre image
                DessineContours(fi, Rouge)

                # Calcul de la transfo Réel -> Image
                don.tr1 = CalculTransfosFenetres(fr, fi) # Calcul de la transfo Réel -> Image

                # Pas du paramètre pour le tracé
                pas = 0.01

                # Courbes de degré 1
                r1 = don.PointReel(-2, -7)
                r2 = don.PointReel( 2, -7)
                r3 = don.PointReel( 1, -10)
                r4 = don.PointReel(-1, -10)
                DessineBezier((r1, r2), pas, Cyan, don.tr1, Cyan) #, 3)
                DessineBezier((r2, r3), pas, Cyan, don.tr1, Cyan) #, 3)
                DessineBezier((r3, r4), pas, Cyan, don.tr1, Cyan) #, 3)
                DessineBezier((r4, r1), pas, Cyan, don.tr1, Cyan) #, 3)

                # Courbes de degré 2
                r1 = don.PointReel( 0,  1)
                r2 = don.PointReel( 2,  1)
                r3 = don.PointReel( 2,  3)
                DessineBezier((r1, r2, r3), pas, Jaune, don.tr1)
                r1 = don.PointReel( 0,  5)
                r2 = don.PointReel( 2,  5)
                DessineBezier((r1, r2, r3), pas, Jaune, don.tr1)
                r1 = don.PointReel( 0,  1)
                r2 = don.PointReel(-2,  1)
                r3 = don.PointReel(-2,  3)
                DessineBezier((r1, r2, r3), pas, Jaune, don.tr1)
                r1 = don.PointReel( 0,  5)
                r2 = don.PointReel(-2,  5)
                DessineBezier((r1, r2, r3), pas, Jaune, don.tr1)

                # Courbes de degré 3
                r1 = don.PointReel( 0, -7)
                r2 = don.PointReel( 1, -4)
                r3 = don.PointReel(-1, -2)
                r4 = don.PointReel( 0,  0)
                DessineBezier((r1, r2, r3, r4), pas, Jaune, don.tr1)
                r1 = don.PointReel( 0.5, -4)
                r2 = don.PointReel( 3, -3)
                r3 = don.PointReel( 2, -1)
                DessineBezier((r1, r2, r3, r1), pas, Jaune, don.tr1)
                r1 = don.PointReel(0.0, -5)
                r2 = don.PointReel(-2.5, -4)
                r3 = don.PointReel(-1.5, -2)
                DessineBezier((r1, r2, r3, r1), pas, Jaune, don.tr1)
                r1 = don.PointReel( 0,  1)
                r2 = don.PointReel( 0, -3)
                r3 = don.PointReel( 6,  3)
                r4 = don.PointReel( 2,  3)
                DessineBezier((r1, r2, r3, r4), pas, Rouge, don.tr1)
                r1 = don.PointReel( 0,  5)
                r2 = don.PointReel( 0,  9)
                r3 = don.PointReel( 6,  3)
                r4 = don.PointReel( 2,  3)
                DessineBezier((r1, r2, r3, r4), pas, Rouge, don.tr1)
                r1 = don.PointReel( 0,  1)
                r2 = don.PointReel( 0, -3)
                r3 = don.PointReel(-6,  3)
                r4 = don.PointReel(-2,  3)
                DessineBezier((r1, r2, r3, r4), pas, Rouge, don.tr1)
                r1 = don.PointReel( 0,  5)
                r2 = don.PointReel( 0,  9)
                r3 = don.PointReel(-6,  3)
                r4 = don.PointReel(-2,  3)
                DessineBezier((r1, r2, r3, r4), pas, Rouge, don.tr1)

                ecr.fenCop = ecr.fen.copy()

            # Remplissage uniforme (parties de la fleur)
            if (don.remplissage): 
                AfficheTexte("et remplissage", (MARGE, 3*MARGE//2), Jaune)
                AfficheTexte("de zones uniformes", (MARGE, 2*MARGE), Jaune)

                pr = don.PointReel(0, -9)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Couleur(0,200,200), don.tr1.fi)

                pr = don.PointReel(0, 3)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Jaune, don.tr1.fi)

                pr = don.PointReel(2, 5)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Rouge, don.tr1.fi)

                pr = don.PointReel(-2, 5)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Rouge, don.tr1.fi)

                pr = don.PointReel(2, 1)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Rouge, don.tr1.fi)

                pr = don.PointReel(-2, 1)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Rouge, don.tr1.fi)

                pr = don.PointReel(1.5, -3)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Rouge, don.tr1.fi)

                pr = don.PointReel(-1, -4)
                pi = TransformationRvI(pr, don.tr1)
                RemplissageUni(pi, Rouge, don.tr1.fi)

        elif action == don.Actions.HORLOGE:
            #
            # dessin d'une horloge analogique circulaire
            #

            temps = time.localtime()
            if (temps.tm_sec != don.tempsPrec.tm_sec):
                # Mise à jour seulement si le temps a changé !
                don.tempsPrec = deepcopy(temps)
                centre = don.PointReel(0.0, 0.0)
                rayonInt = 7.0
                rayonExt = 8.0
                rayonH = 3.0
                rayonM = 4.5
                rayonS = 6.5
                Noir = don.Couleur(0, 0, 0)

                # Dessin du contour de la fenêtre image
                DessineContours(fi, Rouge)

                # Calcul de la transfo Réel -> Image
                don.tr1 = CalculTransfosFenetres(fr, fi) # Calcul de la transfo Réel -> Image

                if (ecr.fenCop == None): # 1ère exécution
                    AfficheTexte("Horloge", (don.MARGE, don.MARGE), Jaune)
                    DessineContours(fi, Rouge)
                
                    if (don.tr1.riA != None):
                        ci = TransformationRvI(centre, don.tr1)
                        ColoriePoint(ci, Bleu, int(round(rayonExt * don.tr1.riA)))
                        ColoriePoint(ci, Noir, int(round(rayonInt * don.tr1.riA)))

                        # Affichage des heures sur le tour de l'horloge
                        centreCouronne = rayonInt + (rayonExt - rayonInt) / 2
                        p1 = PointReel()
                        
                        i = 3
                        p = 0
                        sens = -1
                        while (p <= 2*math.pi):
                            if (i == 0):
                                i = 12
                            txtH = str(i)
                            p1.x = fr.bg.x + 382
                            p1.y = fr.hd.y + 680

                            AfficheTexte(txtH, (p1.x + 304 + 210*cos(p), p1.y - 320 - 214*sin(p)), Blanc)
                            i += sens
                            p += math.pi/6

                    ecr.fenCop = ecr.fen.copy()
                else:                    # exécutions suivantes
                    ecr.fen.blit(ecr.fenCop, (0,0))

                # Calcul des positions des trois aiguilles (extrémités à la pointe des aiguilles)
                heure = temps.tm_hour % 12
                angleH = -2 * (heure - 3.0 + temps.tm_min / 60.0) * math.pi / 12.0
                angleM = -2 * (temps.tm_min - 15.0) * math.pi / 60.0
                angleS = -2 * (temps.tm_sec - 15.0) * math.pi / 60.0
                ptH = don.PointReel(rayonH * cos(angleH), rayonH * sin(angleH))
                ptM = don.PointReel(rayonM * cos(angleM), rayonM * sin(angleM))
                ptS = don.PointReel(rayonS * cos(angleS), rayonS * sin(angleS))
                DessineSegmentReel(centre, ptS, Rouge, don.tr1, 1, 3)
                DessineSegmentReel(centre, ptM, Cyan, don.tr1, 1, 7)
                DessineSegmentReel(centre, ptH, Bleu, don.tr1, 1, 11)

                # Affichage de la date
                txtDate = "{0:02d} / {1:02d} / {2}".format(temps.tm_mday, temps.tm_mon, temps.tm_year)
                AfficheTexte(txtDate, (fi.bg.col+don.MARGE, fi.bg.lig-don.MARGE), Jaune)
            
            # On indique qu'il faut refaire le dessin (pour assurer l'animation)
            don.dejaFait = False

        elif action == don.Actions.ISO:
            #
            # 3D isométrique
            #

            if (ecr.fenCop == None): # 1ère exécution
                Effacer()   # Initialisation de la fenêtre en noir
                AfficheTexte("3D isométrique", (don.MARGE, don.MARGE), Jaune)

                # Dessin du contour de la fenêtre image
                DessineContours(fi, Rouge)

                # Chargement de l'objet
                nomFic = "objs/cube.obj"
                don.obj = Obj(nomFic, True)

                # Définition du reprère 3D isométrique
                if (don.obj.estValide()):
                    don.repIso = CalculeRepereIso(don.obj, fi)
                else:
                    AfficheTexte("Pas de fichier objet !", ((fi.bg.col + fi.hd.col)/2, (fi.bg.lig + fi.hd.lig)/2), Rouge, True)

                ecr.fenCop = ecr.fen.copy()
            else:                    # exécutions suivantes
                ecr.fen.blit(ecr.fenCop, (0,0))

            # Affichage de l'objet
            if (don.obj.estValide()):
                DessineObjet(don.obj, don.repIso, Jaune, fi, True)
################################################################################
