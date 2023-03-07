# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import numpy as np
from math import*

"""Programme qui parcourt les fichiers générés par Genec et Starevol
Permet entre autres de générer le diagramme HR ou l'évolution d'un paramètre au cours du temps, ainsi que renvoyer l'intégralité des paramètres a un age donné
F Castillo et T Bruant 2023"""

class Structure (object):
    def __init__ (self, modele, source):
        global axes
        
        self.modele = modele
        self.source = source
        self.couche = []
        self.M = []
        self.P = []
        self.T = []
        self.R = []
        self.X = []
        self.Y = []
        self.C12 = []
        self.O16 = []
        self.rho = []
        self.nablad = []
        self.nablarad=[]
        self.vraiemasse = []


        if self.modele == "Genec" :
            fichier = open(self.source,"r")
            for i in range(3) :
                ligne = fichier.readline()

            while 1 :
                ligne = fichier.readline()

                if ligne == "" : break

                for i in range(3):  
                    ligne = ligne.replace("  "," ")
                ligne = ligne.split(" ")

                self.couche.append(float(ligne[1]))
                self.M.append(float(ligne[2]))
                self.P.append(float(ligne[3]))
                self.T.append(float(ligne[4]))
                self.R.append(float(ligne[5]))
                self.X.append(float(ligne[7]))
                self.C12.append(float(ligne[9]))
                self.O16.append(float(ligne[10]))
                self.nablad.append(float(ligne[29]))
                self.vraiemasse.append(ligne[50])
                self.nablarad.append(float(ligne[14]))

            self.couche=np.array(self.couche)        
            self.P=10**np.array(self.P)        
            self.T=10**np.array(self.T)        
            self.R=10**np.array(self.R)/6.857e10
            self.M=np.array(self.M)
            self.C12 = np.array(self.C12)
            self.O16 = np.array(self.O16)
            self.nablad = np.array(self.nablad)
            self.X = np.array(self.X)
            self.Y = np.array(self.Y)

            self.args = {"M" : self.M,
                         "P" : self.P,
                         "T" : self.T,
                         "R" : self.R,
                         "12C": self.C12,
                         "16O" : self.O16,
                         "nablad" : self.nablad,
                         "vraiemasse" : self.vraiemasse,
                         "nablarad" : self.nablarad,
                         "X" : self.X,
                         "Y": self.Y
                         }
                         

    def Evolution (self,parametre,legende,X = "R", couleur="black",masse = True):
        if masse : legende += " ; M = "+str(self.vraiemasse[0])+" Mo"

        plt.plot(self.args[X],self.args[parametre], label=legende,color=couleur)

        axes.set_xlabel(X)
        axes.set_ylabel(parametre)

class Etoile (object): 
    def __init__(self, modele, source):

        # Définition de la classe Etoile
        # source est un fichier pour Genec, et le repertoire qui contient tous les fichiers pour Starevol (il faut les dezipper)
        # Pour accéder à l'abondance au coeur du carbone 12 (par exemple) > Etoile.abondances_coeur["12C"]
        
        if modele not in ("Genec","Starevol") :
            raise ValueError ("Le modele doit etre Genec ou Starevol")
        
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
            "30Si","31P","32S","33S","34S","35S","35Cl","36S","36Cl","37Cl","heavy"] #liste de tous les éléments considérés
        
        self.abondances_surf={}
        self.abondances_coeur={}
        for i in elts :
            self.abondances_surf[i]=[]
            self.abondances_coeur[i] = []
            
        indices_surf = {}
        indices_coeur = {}
        
        if self.modele == "Genec" :
            fichier = open(self.source,'r')

            elts_surf = ["X","Y","3He","12C","13C","14N","16O","17O","18O","20Ne","22Ne"]
            elts_coeur = ["X","Y","3He","12C","13C","14N","16O","17O","18O","20Ne","22Ne","7Be","8Be"]
            
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
                        if "c1" in file : fichiers[5] = open(os.path.join(root,file),"r")
                        if "c2" in file : fichiers[6] = open(os.path.join(root,file),"r")
                        if "c3" in file : fichiers[7] = open(os.path.join(root,file),"r")
                        if "c4" in file : fichiers[8] = open(os.path.join(root,file),"r")
                        if "s1" in file : fichiers[1] = open(os.path.join(root,file),"r")
                        if "s2" in file : fichiers[2] = open(os.path.join(root,file),"r")
                        if "s3" in file : fichiers [3] = open(os.path.join(root,file),"r")
                        if "s4" in file : fichiers[4] = open(os.path.join(root,file),"r")
                        if file == "mevol.hr": fichiers[0] = open(os.path.join(root,file),"r")
                            
            for k in fichiers :
                if k == 0:
                    raise NameError ("Des fichiers n'ont pas été trouvés")
                for j in range(6):
                    k.readline()

            delta =16

            for i in range(len(elts)):
                if i % 11 == 0 : delta +=2
                indices_surf[i+delta]=elts[i]
                indices_coeur[i+delta+52]=elts[i]

            while 1 :

                ligne = ""
                for k in fichiers :
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

                    for k in range(len(ligne)):
                        if k in indices_surf :
                            self.abondances_surf[indices_surf[k]].append(float(ligne[k]))

                        if k in indices_coeur:
                            self.abondances_coeur[indices_coeur[k]].append(float(ligne[k]))
                        
                    self.Z_surf.append(1-X_surf-Y_surf)
                    self.Z_coeur.append(1-X_coeur-Y_coeur)

            for k in fichiers : k.close()

        # Convertit les listes en np.array

        self.M = np.array(self.M)
        self.R = np.array(self.R)
        self.L = np.array(self.L)
        self.Z_surf = np.array(self.Z_surf)
        self.Z_coeur = np.array(self.Z_coeur)

        for i in self.abondances_surf :
            self.abondances_surf[i]=np.array(self.abondances_surf[i])
            self.abondances_coeur[i]=np.array(self.abondances_coeur[i])

        self.M_ini = self.M[0]
        self.Z_ini = self.Z_surf[0]
        self.X_ini = self.abondances_surf["X"][0]
        self.Y_ini = self.abondances_surf["Y"][0]

        self.args = {"T" : self.T,
                     "L" : self.L,
                     "M" : self.M,
                     "t" : self.t,
                     "R" : self.R,
                     "Z_surf" : self.Z_surf,
                     "Z_coeur" : self.Z_coeur}
        for e in elts :
            self.args[e+"_surf"] = self.abondances_surf[e]
            self.args[e+"_coeur"] = self.abondances_coeur[e]

    def HR (self,couleur="black",legende="graphique",masse = True,Zini = True): #Définit la fonction qui trace les diagrammes HR

        if masse : legende += " ; M = "+str(self.M_ini)+" Mo"
        if Zini  : legende += " ; Z_ini ="+str(self.Z_ini)

        plt.plot(self.T,self.L,linewidth=1,label=legende,color=couleur)

    def Evolution (self, parametre,couleur="black",legende="graphique",  X="t" ,log = False,logx = False,masse = True,Zini = False): #Définit la fonction qui trace les évolutions, par défaut au cours du temps

        parametre = self.args[parametre]
        X = self.args[X]
        if log : parametre = np.log(parametre)
        if logx : X = np.log(X)

        if masse : legende += " ; M = "+str(self.M_ini)+" Mo"
        if Zini  : legende += " ; Z_ini ="+str(self.Z_ini)
        
        plt.plot(X, parametre,color=couleur,label=legende)
        
    def Para (self, age, parametres, err = 1e7): #Affiche les valeurs de certains parametres à un age donné. Prend une liste de str comme argument

        i = 0

        for t in self.t :
            if abs(10**t-age) < err: break
            i +=1

        valeurs = []

        for p in parametres :
            p = self.args[p]
            if i == len(p) :
                raise ValueError ("Aucune valeur de l'âge ne correspond") #Peut etre causé par une marge d'erreur trop petite, ou l'étoile est deja morte à cet age

            valeurs.append(p[i])

        return valeurs

    def Age (self, X, err = 0.01):

        i = 0

        for x in self.abondances_coeur["X"] :
            if abs(x-X) < err: break
            i +=1

        return self.t[i]


if __name__ == "__main__" :

    axes = plt.gca()

    e1 = Structure(modele = "Genec", source = "Fichiers_structure/classique_m0.8.v1")
    e2 = Structure(modele = "Genec", source = "Fichiers_structure/classique_m0.8.v2")
    e3 = Structure(modele = "Genec", source = "Fichiers_structure/classique_m1.0.v1")
    e4 = Structure(modele = "Genec", source = "Fichiers_structure/classique_m1.0.v2")
    e5 = Structure(modele = "Genec", source = "Fichiers_structure/classique_m1.5.v1")
    e6 = Structure(modele = "Genec", source = "Fichiers_structure/classique_m1.5.v2")

    A_Genec = Etoile(modele="Genec",source = "A.wg")
    B_Genec = Etoile(modele="Genec",source = "B.wg")
    sol = Etoile(modele="Genec",source = "classique_m1.0.wg")

    age_e1 = 10**A_Genec.Age(X=0.62)
    age_e2 = 10**sol.Age(X=0.55)
    age_e3 = 10**B_Genec.Age(X=0.58)

    e1.Evolution("X", legende = "Etoile 1", couleur = "blue")
    e3.Evolution("X", legende = "Etoile 2", couleur = "red")
    e5.Evolution("X", legende = "Etoile 3", couleur = "green")

    axes.set_xlabel("R [Ro]")
    axes.set_ylabel("X")

    axes.legend()
    
    plt.show()
