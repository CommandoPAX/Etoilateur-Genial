# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import numpy as np
from math import*
import pandas as pd
import seaborn as sns
sns.set(color_codes = True)
sns.set(font_scale=1.5) # fixe la taille de la police à 1.5 * 12pt

"""Programme qui parcourt les fichiers générés par Genec et Starevol
Permet entre autres de générer le diagramme HR ou l'évolution d'un paramètre au cours du temps, ainsi que renvoyer l'intégralité des paramètres a un age donné
F Castillo et T Bruant 2023

Version utilisant les dataframe
"""


'''
Conventions pour les données et leurs unités :

Luminosité : L | log L/Lo
Rayon : R | R/Ro
Température : T | logT/To
Masse : M | M/Mo
temps/age : t | annees

'''

class Etoile (object): 
    def __init__(self, modele, source):
        
        # Définition de la classe Etoile
        # source est un fichier pour Genec, et le repertoire qui contient tous les fichiers pour Starevol (il faut les dezipper)
        # Pour accéder à l'abondance au coeur du carbone 12 (par exemple) > Etoile.abondances_coeur["12C"]

        if modele not in ("Genec","Starevol") :
            raise ValueError ("Le modele doit etre Genec ou Starevol")

        self.modele = modele
        self.source = source
        
        if self.modele == "Genec" :

            '''Import des données pour le cas du modèle GENEC'''

            fichier = open(self.source,'r')
            
            self.DF = pd.DataFrame(columns=["t", "M", "L", "T", "X_surf","Y_surf", "3He_surf", "12C_surf", "13C_surf", "14N_surf", "16O_surf", "17O_surf", "18O_surf", "20Ne_surf", "22Ne_surf",
                                            "Mcc", "Tnc", "log(M)", "log(rhoc)", "log(Tc)", "X_coeur","Y_coeur", "3He_coeur", "12C_coeur", "13C_coeur", "14N_coeur", "16O_coeur", "17O_coeur", "18O_coeur", "20Ne_coeur",
                                            "22Ne_coeur", "7Be_coeur", "8Be_coeur"])

            while 1 :   #Parcourt le fichier et enregistre les informations suivantes :
                        #Masse,luminosite, Temperature, Rayon, abondances, metallicite au cours du temps

                ligne = fichier.readline()
                for i in range(3):  
                    ligne = ligne.replace("  "," ")
                ligne = ligne.split(" ")

                if ligne == [""] : break

                Data = []

                if float(ligne[2]) != 0: #Récupère les valeurs utiles
                    for i in range(2,35) :
                        Data.append(float(ligne[i]))
                        
                if Data != []: #Nécessaire car il existe des listes vides
                    try :
                        self.DF.loc[len(self.DF)] = Data #Ajoute les valeurs au dataframe
                    except : 
                        print(len(Data))
                        pass

            Zcoeur = []
            Zsurf = []

            for i in range(len(self.DF["X_coeur"])) :
                Zc = 1 - self.DF["X_coeur"].iloc[i] - self.DF["Y_coeur"].iloc[i]
                Zcoeur.append(Zc)

            for i in range(len(self.DF["X_surf"])) :
                Zs = 1 - self.DF["X_surf"].iloc[i] - self.DF["Y_surf"].iloc[i]
                Zsurf.append(Zs)

            self.DF["Z_coeur"] = Zcoeur
            self.DF["Z_surf"] = Zsurf

            self.DF.set_index("t", inplace=True)

        #if modele == "Starevol" : #PROBLEME D'INDICE, PREND UNE COLONNE A GAUCHE, ARRIVE PAS A FIX
                
            #TBA

        self.M_ini = self.DF["M"].iloc[0]
        self.Z_ini = self.DF["Z_surf"].iloc[0]
        self.X_ini = self.DF["X_surf"].iloc[0]
        self.Y_ini = self.DF["Y_surf"].iloc[0]

    def HR (self,couleur="black",legende="graphique",masse = True,Zini = True): #Définit la fonction qui trace les diagrammes HR

        ax = plt.subplot() #Force tout les graphes a apparaitre sur le même
        if masse : legende += " ; M = "+str(self.M_ini)+" Mo"
        if Zini  : legende += " ; Z_ini ="+str(self.Z_ini)

        sns.lineplot(data = self.DF, x="T", y = "L", ax = ax, label = legende, color = couleur)
        plt.show()

        #Le graphique est bizarre

    def Evolution (self, Varx = "t", Vary = [], xlegend = "xlegend", ylegend = "ylegend", logx = False, masse = False, Zini = False) : 
        #Définit la fonction qui trace les évolutions, par défaut au cours du temps
        
        ax = plt.subplot() #Force tout les graphes a apparaitre sur le même

        if type(Vary) != list : print("Mauvais type de données") #Verifie le bon type de données

        if logx == True : #Crée une nouvelle colonne avec les valeurs log et change la variable utilisée
            loogx = []
            if Varx != "t" :
                for i in range(len(self.DF[Varx])) :
                    loogx.append(log(self.DF[Varx].iloc[i], 10))
            if Varx == "t" :
                index_DF = list(self.DF.index.values.tolist())
                for i in range(len(index_DF)) :
                    loogx.append(log(index_DF[i], 10))
            self.DF["log(" + Varx + ")"] = loogx
            Varx = "log(" + Varx + ")"

        for i in Vary : #Trace tout les graphes
            lab = i

            if masse : lab += " ; M = "+str(self.M_ini)+" Mo"
            if Zini  : lab += " ; Z_ini ="+str(self.Z_ini)

            sns.lineplot(data = self.DF, x = Varx, y = i, ax = ax, label = lab) #La partie qui trace vraiment les graphes
        
        plt.xlabel(xlegend) #gère les légendes
        plt.ylabel(ylegend)

        plt.show()


    def Para (self, age, parametres): #Affiche les valeurs de certains parametres à un age donné. Prend une liste de str comme argument
        
        index_DF = list(self.DF.index.values.tolist())
        print(index_DF)
        if type(parametres) != list : print("Mauvais type de données")

        varage = age - index_DF[0]
        varage_pre = varage #evite un crash si le programme stop à l'itération 0
        i = 1
        while varage > 0 : #cherche les plus proches valeurs
            varage_pre = varage
            varage = age - index_DF[i]
            i += 1
        
        if abs(varage) < abs(varage_pre) : i = i-1
        if abs(varage) > abs(varage_pre) : i = i-2
        if abs(varage) == abs(varage_pre) : i = i-1

        for para in parametres : #Affiche tout les paramètres
            try :
                print(para, ": ", self.DF[para].iloc[i])
            except :
                print("Erreur : ", para),
                pass


    def Age (self, X, err = 0.01): #Renvoie l'âge de l'étoile pour un X donné
        index_DF = list(self.DF.index.values)
        i = 0

        for x in len(self.DF["X_coeur"]) :
            if abs(self.DF["X_coeur"].iloc[x]-X) < err: break
            i +=1

        return index_DF[i]


    def Test (self): #Fonction test pour les erreurs
        print(self.DF)


#TBA : class Structure (object):

if __name__ == "__main__" :

    Star = Etoile(modele = "Genec", source = "T:\Cours\DATA\GENEC\classique_m1.0.dat")
    Star.HR()
