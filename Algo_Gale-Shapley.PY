## BLACK-LAB SAS
#  19 rue du val es Dunes Caen
#  
#  Black-lab.eu
#
#  This file is owned by BLACK-LAB No portion of this document may be reproduced, 
#  copied or revised without written permission of the authors.


## @author <Hector MIKOLAJCZAK>
#  @version <1.0>

import function
from math import *

"""
Objectif : on part des 5 listes suivantes :
    - liste_cv : contient les clé des cv
    - liste_cluster : contient les clé_cluster
    - liste_cv_url : liste_cv_url[i] contient l'url de liste_cv[i] 
    - liste_cluster_token :liste_cluster_token[i] contient le token (nom) de 
    liste_cluster[i]
    - liste_cluster_nbplace :liste_cluster_nbplace[i] contient le nb de places 
    dans liste_cluster[i]
    - cle_globale : correspond à la clé représentant tous les cv a placer dans les clusters
"""

def scoring_matrice(liste_cv,liste_cluster,cle_globale):
    Matrice_score=[]
    for i in range (len(liste_cluster)):
        Matrice_score.append([])

        
        for j in range (len(liste_cv)):
            Matrice_score[i].append(function.score(liste_cv[j][0], 
                                                    liste_cv[j][1], 
                                                    liste_cluster[i][0],
                                                    liste_cluster[i][1], 
                                                    cle_globale))
    return Matrice_score

def tri_double(L,V):
    M=[]
    for i in range (len(V)):
        M.append([L[i],V[i]])
    M=sorted(M)
    for i in range (len(M)):
        L[i]=M[i][0]
        V[i]=M[i][1]
    return V

def pref(Matrice_score,liste_cluster_token, liste_cv_url):
    liste_cluster_pref=[]
    liste_cv_pref=[]
    for i in range (len(Matrice_score)):
        url_temp=liste_cv_url
        token_temp=liste_cluster_token
        liste_cluster_pref.append(tri_double(Matrice_score[i],url_temp))
    Matrice_score=switch(Matrice_score)

    for i in range (len(Matrice_score)):
        url_temp=liste_cv_url
        token_temp=liste_cluster_token
        liste_cv_pref.append(tri_double(Matrice_score[i],token_temp))
    return liste_cluster_pref, liste_cv_pref

def switch (M):
    N=[]
    for i in range (len(M[0])):
        N.append([])
        for j in range(len(M)):
            N[i].append(M[j][i])
    return N
"""
def  (liste_cluster_nbplace, 
                            liste_cluster_pref, 
                            liste_cluster_token, 
                            liste_cv_pref, 
                            liste_cv_url):
    return liste_cv_cluster
 """   
def main (liste_cv,
          liste_cluster,
          liste_cv_url,
          liste_cluster_token, 
          liste_cluster_nbplace, 
          cle_globale):
    #Recherche de la matrice de score
    Matrice_score = scoring_matrice(liste_cv,liste_cluster,cle_globale)
    print(Matrice_score)
    #Recherche des préféences de chaque CV
    X=pref (Matrice_score,liste_cluster_token, liste_cv_url)
    liste_cluster_pref, liste_cv_pref=X[0],X[1]
    #répartition des CV en fonction de leurs préférences 
    Liste_Finale=Gale_Shapley (liste_cluster_nbplace, 
                                         liste_cluster_pref, 
                                         liste_cluster_token, 
                                         liste_cv_pref, 
                                         liste_cv_url)
    return Liste_Finale
    
def Gale_Shapley(liste_cluster_nbplace, 
                           liste_cluster_pref, 
                           liste_cluster_token, 
                           liste_cv_pref, 
                           liste_cv_url):
    Position_cluster=[]
    Placement_definitif=[]
    Annex=[]
    relegable=[]
    #on créer la liste des mots à classer
    for i in range (len(liste_cv_url)):
        Annex.append(liste_cv_url[i])
    #on donne la forme 
    for i in range(len(liste_cluster_token)):
        Position_cluster.append([])
    Annex_temp=[]
    while Annex!=[]:
        #Annex=Annex_temp
        Annex_temp=[]
        for i in range (len(Annex)):
            #on repartie les url d' Annex dans Position_cluster
            indice_url = liste_cv_url.index(Annex[i])#indice de l'url d'annex[i]
            indice_cl = liste_cluster_token.index(liste_cv_pref[indice_url][-1])#indice[cluster]
            Position_cluster[indice_cl].append(Annex[i])#on ajoute l'url au cluster correspondant
        for i in range (len(Position_cluster)):
            #virer les url aux moins bons scores, les ajouter a Annex_temp
            if  len(Position_cluster[i])>liste_cluster_nbplace[i]:
                #on supprime les moins envié
                for k in range (len(Position_cluster[i])-liste_cluster_nbplace[i]):
                    #On pop l'url au score le moins haut
                    for j in range (len(liste_cluster_pref[i])):
                        if liste_cluster_pref[i][j] in Position_cluster[i]:
                            #on supprime l'url de Position_cluster[i] et on l'ajoute à une liste annex
                            Annex_temp.append(Position_cluster[i].pop(Position_cluster[i].index(liste_cluster_pref[i][j])))
                            break
        n=0
        while n < len(Annex_temp):
            #on fait oublier les préférences des url (.pop())
            indice=liste_cv_url.index(Annex_temp[n])
            liste_cv_pref[indice].pop()
            if liste_cv_pref[indice]==[]:
                relegable.append(Annex_temp.pop(n))
            else :
                n+=1
        Annex=Annex_temp
    
    return Position_cluster,relegable
