#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
#
# Université de Lorraine - Licence informatique
# Dessin de segments du module ig
#
################################################################################

################################################################################
# Chargement des modules standards
################################################################################
from math import *
################################################################################

################################################################################
# Chargement des définitions persos
################################################################################
from donnees import *
from base import *
from transfos import *
################################################################################

################################################################################
# Dessin d'un segment image en version entière (avec pas de traçage et épaisseur)
# le paramètre optionnel fi permet de limiter le tracé à une fenêtre image
################################################################################
def DessineSegmentImage(p1, p2, coul, pas=1, epaisseur=1, fi=None):
    pi1 = PointImage(p1.col, p1.lig)
    pi2 = PointImage(p2.col, p2.lig)

    dc = pi2.col - pi1.col # Variation en colonnes
    dl = pi2.lig - pi1.lig # Variation en lignes
    absdc = abs(dc)        # Valeur absolue de dc
    absdl = abs(dl)        # Valeur absolue de dl
    cumul = 0              # Cumul des déplacements selon l'axe non parcouru
    col = pi1.col          # Initialisation de la colonne de départ
    lig = pi1.lig          # Initialisation de la ligne de départ
    sdl = sdc = pas          # Sens des variations selon l'axe non parcouru

    # Détermination des sens de variation lors des changements de ligne ou colonne
    if dc < 0:
        sdc = -pas
    if dl < 0:
        sdl = -pas

    # Cas d'un déplacement plus grand en colonnes
    if absdc >= absdl:
        cumul = absdc
        for col in range(pi1.col, pi2.col+sdc, sdc):
            ColoriePixel(col, lig, coul)
            cumul += 2 * absdl
            if cumul >= 2 * absdc:
                lig += sdl
                cumul -= 2 * absdc
    else:
    # Cas d'un déplacement plus grand en lignes
        cumul = absdl
        for lig in range(pi1.lig, pi2.lig+sdl, sdl):
            ColoriePixel(col, lig, coul)
            cumul += 2 * absdc
            if cumul >= 2 * absdl:
                col += sdc
                cumul -= 2 * absdl                
            


    # Prise en compte de la fenêtre fi si elle est spécifiée
    if (fi != None):
        pass
        
    # On ne dessine que si le pas d'affichage est non nul
    if (pas > 0):
        pass
################################################################################

################################################################################
# Dessin d'un segment réel
# Le paramètre 'pasHF' peut être omis et représente le pas des pointillés
# pour les parties du segment qui sont hors de la fenêtre
# Le paramètre epaisseur spécifie le nombre de pixels pour l'épaisseur du trait
################################################################################

def DessineSegmentReel(p1, p2, coul, transfo, pasHF=0, epaisseur=1):
    i1, i2 = PointImage(), PointImage()
    r1, r2 = PointReel(), PointReel()
    coulExt = Couleur(255 - coul.R, 255 - coul.V, 255 - coul.B) # Couleur inversée

    # Transformation de nos deux points réels en points images

    r1 = p1
    r2 = p2

    # Découpage

    r1, r2 = DecoupeSegmentReel(r1, r2, transfo.fr)

    i1 = TransformationRvI(r1, transfo)
    i2 = TransformationRvI(r2, transfo)


    if (r1.x < transfo.fr.bg.x):
    	pass

    else:
    	DessineSegmentImage(i1, i2, coul, pas=1, epaisseur=1, fi=None)
    


################################################################################

################################################################################
# Transfert du point p1 à la position "bord" sur l'axe spécifié et info de
# position par rapport à l'autre axe dans l'intervalle [mini:maxi]
################################################################################
def TransfertSurBord(p1, p2, bord, axe, mini, maxi):

    #
    if axe == 'y': # Bord vertical
        # Calcul des nouvelles coordonnées du point p1
        p1.x += (bord - p1.y) * (p2.x - p1.x) / (p2.y - p1.y)
        p1.y = bord
        # Mise à jour des informations de position du point p1 par rapport à l'intervalle [mini:maxi] sur l'autre axe
        sousmin = p1.x < mini
        surmax  = p1.x > maxi
    else:          # Bord horizontal
        # Calcul des nouvelles coordonnées du point p1
        p1.y += (bord - p1.x) * (p2.y - p1.y) / (p2.x - p1.x)
        p1.x = bord
        # Mise à jour des informations de position du point p1 par rapport à l'intervalle [mini:maxi] sur l'autre axe
        sousmin = p1.y < mini
        surmax  = p1.y > maxi    

    # La position relative de p1 n'est plus à l'extérieur par rapport au bord
    exterieur  = False

    return (exterieur, sousmin, surmax)
################################################################################

################################################################################
# Découpage d'un segment réel
################################################################################
def DecoupeSegmentReel(pr1, pr2, fr):

    npr1 = PointReel(pr1.x, pr1.y) # Copie de pr1
    npr2 = PointReel(pr2.x, pr2.y) # Copie de pr2
	
	
    # --------------------------------------------------------------------- #
    # --------------------------------------------------------------------- #

	
    # Conditions de sortie/d'entrée dans la future boucle
	
    toutDehors = False
    toutDedans = False
	
    
    # --------------------------------------------------------------------- #
    # --------------------------------------------------------------------- #
	
	
    # Boucle des projections sur les bords
	
    while (not toutDedans):
	
        # Initialisation et actualisation de la position des points
		
        gauche1  = npr1.x < fr.bg.x
        dessus1  = npr1.y > fr.hd.y
        droite1  = npr1.x > fr.hd.x
        dessous1 = npr1.y < fr.bg.y
        gauche2  = npr2.x < fr.bg.x
        dessus2  = npr2.y > fr.hd.y
        droite2  = npr2.x > fr.hd.x
        dessous2 = npr2.y < fr.bg.y
		
		
        # --------------------------------------------------------------------- #
        # --------------------------------------------------------------------- #
		
		
        # Vérification de la condition de sortie de la boucle
		
        if ( (not gauche1) and (not gauche2) and (not dessus1) and (not dessus2) and (not droite1) and (not droite2) and (not dessous1) and (not dessous2) ):
			
            toutDedans = True
            break
		
			
        # --------------------------------------------------------------------- #
        # --------------------------------------------------------------------- #

		
        # Vérificiation de la condition de rupture de la boucle
		
        if ( ((gauche1) and (gauche2)) or ((dessus1) and (dessus2)) or ((droite1) and (droite2)) or ((dessous1) and (dessous2)) ):
		
            toutDehors = True
            break # On sort de la boucle : nous ne pouvons projeter les points dans la fenêtre image
		
		
        # --------------------------------------------------------------------- #
        # --------------------------------------------------------------------- #
		
		
        # Corps de la boucle
		

        if (gauche1):
		
            dx = fr.bg.x - npr1.x
            dy =  dx * (npr2.y - npr1.y) / (npr2.x - npr1.x)
			
            npr1.x = npr1.x + dx
            npr1.y = npr1.y + dy
			
            continue # On utilise continue pour entrer de nouveau dans la boucle et mettre à jour les conditions gauche1, dessus1...

        elif (dessus1):
		
            dy = npr1.y - fr.hd.y
            dx = dy * (npr2.x - npr1.x) / (npr1.y - npr2.y)
		
            npr1.x = npr1.x + dx
            npr1.y = npr1.y - dy
			
            pass
    
        elif (droite1):
		
            dx = npr1.x - fr.hd.x
            dy = dx * (npr2.y - npr1.y) / (npr1.x - npr2.x)
			
            npr1.x = npr1.x - dx
            npr1.y = npr1.y + dy
			
            continue
			
        elif (dessous1):
		
            dy = fr.bg.y - npr1.y
            dx = dy * (npr2.x - npr1.x) / (npr2.y - npr1.y)
            
            npr1.x = npr1.x + dx
            npr1.y = npr1.y + dy
			
            continue
		
		
        # --------------------------------------------------------------------- #
        # --------------------------------------------------------------------- #
		
		
        if (gauche2):
		
            dx = fr.bg.x - npr2.x
            dy =  dx * (npr1.y - npr2.y) / (npr1.x - npr2.x)
			
            npr2.x = npr2.x + dx
            npr2.y = npr2.y + dy
			
            continue
			
        elif (dessus2):
		
            dy = npr2.y - fr.hd.y
            dx = dy * (npr1.x - npr2.x) / (npr2.y - npr1.y)
		
            npr2.x = npr2.x + dx
            npr2.y = npr2.y - dy
			
            continue
			
        elif (droite2):
		
            dx = npr2.x - fr.hd.x
            dy = dx * (npr1.y - npr2.y) / (npr2.x - npr1.x)
			
            npr2.x = npr2.x - dx
            npr2.y = npr2.y + dy
			
            continue
			
        elif (dessous2):
		
            dy = fr.bg.y - npr2.y
            dx = dy * (npr1.x - npr2.x) / (npr1.y - npr2.y)
		
            npr2.x = npr2.x + dx
            npr2.y = npr2.y + dy
			
            continue
    
	
    # --------------------------------------------------------------------- #
    # --------------------------------------------------------------------- #

	
    # Affectation hors fenêtre si le segment est tout dehors

    if (toutDehors):
        npr1.x = fr.bg.x-1.0
        npr1.y = fr.bg.y-1.0
        npr2.x = fr.bg.x-1.0
        npr2.y = fr.bg.y-1.0

    return (npr1, npr2)

################################################################################

################################################################################
# Dessin d'un ensemble de segments réels issus d'un même point
################################################################################
def DessineFuseau(pr1, pr2, source, coulS, coulP):

	# A FINIR : COLORIER LES POINTS DE DEPART AVEC COULP

	p1, p2, p3, p4 = PointReel(), PointReel(), PointReel(), PointReel()

	p1 = pr1
	p2 = pr2
	
	transfo = TransfosFenetres() # Sera utilisé pour la fonction DessineSegmentReel
	transfo.fr = FenetreReel()
	fi = FenetreImage()

	transfo.fr.bg = p1
	transfo.fr.hd = p2

	transfo = CalculTransfosFenetres(transfo.fr, fi)

	# Boucle parcourant l'axe des x

	if ( (source == "bg") ):
		p3 = p1
		p4.x = p1.x
		p4.y = p2.y
		while (p4.x <= p2.x):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.x += 1

	elif ( (source == "hg") ):
		p3.x = p1.x
		p3.y = p2.y
		p4.x = p1.x
		p4.y = p1.y
		while (p4.x <= p2.x):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.x += 1

	elif ( (source == "bd") ):
		p3.x = p2.x
		p3.y = p1.y
		p4.x = p3.x
		p4.y = p2.y
		while (p4.x >= p1.x):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.x -= 1

	elif ( (source == "hd") ):
		p3 = p2
		p4.x = p3.x
		p4.y = p1.y
		while (p4.x >= p1.x):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.x -= 1

	# Boucle parcourant l'axe des y

	
	if ( (source == "bg") ):
		while (p4.y >= p1.y):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.y -= 1

	elif ( (source == "hg") ):
		while (p4.y <= p2.y):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.y += 1

	elif ( (source == "bd") ):
		while (p4.y >= p1.y):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.y -= 1

	elif ( (source == "hd") ):
		while (p4.y <= p2.y):
			DessineSegmentReel(p3, p4, coulS, transfo)
			p4.y += 1

################################################################################
