# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import numpy as np
from math import*

#Programme qui parcourt les fichiers générés par Genec et Starevol
#Permet entre autres de générer le diagramme HR ou l'évolution d'un paramètre au cours du temps
#F Castillo et T Bruant 2023

class Etoile (object): #Définition de la classe Etoile
    def __init__(self, modele, source):
        
        if modele not in ("Genec","Starevol") :
            print ValueError ("Le modele doit etre Genec ou Starevol") : #a remplacer par raise pour python 3
        
        self.modele = modele
        self.source = source

        self.L = [] # log L/Lo
        self.R = [] # R/Ro
        self.T = [] # log T/To
        self.M = [] # M/Mo
        self.t = [] # log t [annees]
        self.Z_surf = []
        self.Z_coeur = [] 

        elts = ["n","X","2H","3He","Y","6Li","7Li","7Be","9Be","10B","11B",
            "12C","13C","14C","14N","15N","15O","16O","17O","18O","19F","20Ne",
            "21Ne","22Ne","23Na","24Mg","25Mg","26Mg","26Alm","26Alg","27Al","28Si","29Si",
            "30Si","31P","32S","33S","34S","35S","35Cl","36S","36Cl","37Cl","heavy"] #liste de tout les éléments considérés


        self.abondances_surf={}
        self.abondances_coeur={}
        for i in elts :
            self.abondances_surf[i]=[]
            self.abondances_coeur[i] = []


        if self.modele == "Genec" :
            fichier = open(self.source,'r')

            elts_surf = ["X","Y","3He","12C","13C","14N","16O","17O","18O","20Ne","22Ne"]
            elts_coeur = ["X","Y","3He","12C","13C","14N","16O","17O","18O","20Ne","22Ne","7Be","8Be"]
            indices_surf = {}
            indices_coeur = {}
            
            for i in range(len(elts_surf)):
                indices_surf[6+i]=elts_surf[i]
                indices_coeur[22+i] = elts_coeur[i]
            
            while 1 :   #Parcourt le fichier et enregistre les informations suivantes :
                        #Masse,luminosite, Temperature, Rayon, abondances, metallicite au cours du temps

                ligne = fichier.readline()
                for i in range(3):  
                    ligne = ligne.replace("  "," ")
                ligne = ligne.split(" ")

                if ligne == [""] : break

                if float(ligne[2]) != 0:
                    self.t.append(log(float(ligne[2]),10))
                    self.M.append(float(ligne[3]))
                    self.L.append(float(ligne[4]))
                    self.T.append(float(ligne[5])-log(5700,10))

                    # Calcul du Rayon avec la loi de Stefan

                    L = 10**float(ligne[4])*3.828e+26
                    T = 10**float(ligne[5])
                    self.R.append(sqrt(L/(4*pi*(5.67e-8)*T**4))/696342e+3) 

                    X_surf = float(ligne[6])
                    Y_surf = float(ligne[7])
                    X_coeur = float(ligne[22])
                    Y_coeur = float(ligne[23])

                    for k in range(len(indices_surf.items())):
                        self.abondances_surf[indices_surf[6+k]].append(float(ligne[6+k]))
                    for k in range(len(indices_coeur.items())):
                        self.abondances_coeur[indices_coeur[22+k]].append(float(ligne[22+k]))

                    self.Z_surf.append(1-X_surf-Y_surf)
                    self.Z_coeur.append(1-X_coeur-Y_coeur)

        if modele == "Starevol" :
                
            fichiers = [0,0,0,0,0,0,0,0,0]
                    
                    

            for root,dirs,files in os.walk(source): #ouvre tout les fichiers utiles
                for file in files :
                    if not ".gz" in file :
                        if "c1" in file :
                            fichier_c1 = open(os.path.join(root,file),"r")
                            fichiers[5]=fichier_c1
                        if "c2" in file :
                            fichier_c2 = open(os.path.join(root,file),"r")
                            fichiers[6]=fichier_c2
                        if "c3" in file :
                            fichier_c3 = open(os.path.join(root,file),"r")
                            fichiers[7] = fichier_c3
                        if "c4" in file :
                            fichier_c4 = open(os.path.join(root,file),"r")
                            fichiers[8] = fichier_c4
                        if "s1" in file :
                            fichier_s1 = open(os.path.join(root,file),"r")
                            fichiers[1] = fichier_s1
                        if "s2" in file :
                            fichier_s2 = open(os.path.join(root,file),"r")
                            fichiers[2] = fichier_s2
                        if "s3" in file :
                            fichier_s3 = open(os.path.join(root,file),"r")
                            fichiers [3] = fichier_s3
                        if "s4" in file :
                            fichier_s4 = open(os.path.join(root,file),"r")
                            fichiers[4] = fichier_s4
                        if file == "mevol.hr":
                            fichier_hr = open(os.path.join(root,file),"r")
                            fichiers[0] = fichier_hr
                            

            for k in fichiers :
                if k == 0:
                    raise NameError ("Des fichiers n'ont pas été trouvés")
                for j in range(6):
                    k.readline()

            indices_surf = {}
            indices_coeur = {}
            delta =16

            for i in range(len(elts)):
                if i % 11 == 0 : delta +=2
                indices_surf[i+delta]=elts[i]

            delta =68
            for i in range(len(elts)):

                if i % 11 == 0 : delta +=2
                indices_coeur[i+delta]=elts[i]

            while 1 :

                ligne = ""
                for k in fichiers :
                    l = k.readline()

                    ligne += k.readline()
    
                for i in range(10):
                    ligne = ligne.replace("  "," ")
                ligne = ligne.split(" ")

                if ligne == [""] : break

                if float(ligne[12])>1e4 and (">\n" not in ligne) and ("<\n" not in ligne) and ("@\n" not in ligne):
                    
                    self.M.append(float(ligne[10]))
                    self.R.append(float(ligne[5]))
                    self.t.append(log(float(ligne[12]),10))
                    self.L.append(log(float(ligne[3]),10))
                    self.T.append(log(float(ligne[6])/5778,10))

                    X_surf=float(ligne[19])
                    Y_surf=float(ligne[22])
                    X_coeur = float(ligne[71])
                    Y_coeur = float(ligne[74])

                    if 1-X_surf-Y_surf > 0.2 : print(ligne)

                    for k in range(len(ligne)):
                        if k in indices_surf :
                            self.abondances_surf[indices_surf[k]].append(float(ligne[k]))

                        if k in indices_coeur:
                            self.abondances_coeur[indices_coeur[k]].append(float(ligne[k]))
                        

                    self.Z_surf.append(1-X_surf-Y_surf)
                    self.Z_coeur.append(1-X_coeur-Y_coeur)

            for k in fichiers : k.close()

        try :
            self.M_ini = self.M[0]
            self.Z_ini = self.Z_surf[0]
            self.X_ini = self.abondances_surf["X"][0]
            self.Y_ini = self.abondances_surf["Y"][0]
        except: pass

    def HR (self,couleur="black",legende="graphique",masse = True,Zini = True): #Définit la fonction qui trace les diagrammes HR


        if masse : legende += " ; M = "+str(self.M_ini)+" Mo"
        if Zini  : legende += " ; Z_ini ="+str(self.Z_ini)

        plt.plot(self.T,self.L,linewidth=1,label=legende,color=couleur)


    def Evolution (self, parametre ,couleur="black",legende="graphique"): #Définit la fonction qui trace les évolutions
        plt.plot(self.t, parametre,color=couleur,label=legende)

if __name__ == "__main__" :

    axes = plt.gca()

    A_Starevol = Etoile(modele="Starevol",source="./A/")
    A_Starevol.Evolution(A_Starevol.Z_coeur,"green","Etoile A Starevol")

    A_Genec = Etoile(modele="Genec",source="A.wg")
    A_Genec.Evolution(A_Genec.Z_coeur,"red","Etoile A Genec")

    B_Genec = Etoile(modele="Genec",source="B.wg")
    B_Genec.Evolution(B_Genec.Z_coeur,"blue","Etoile B Genec")

    axes.set_xlabel("log t")
    axes.set_ylabel("Z")

    axes.legend()
    
    plt.show()
