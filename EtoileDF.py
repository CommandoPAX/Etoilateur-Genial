# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import numpy as np
from math import*
import pandas as pd
import seaborn as sns
import sys
if sys.version_info[0] < 3: 
    from StringIO import StringIO
else:
    from io import StringIO
    
sns.set(color_codes = True)
sns.set(font_scale=1.5,font="Ubuntu") # fixe la taille de la police à 1.5 * 12pt

"""Programme qui parcourt les fichiers générés par Genec et Starevol
Permet entre autres de générer le diagramme HR ou l'évolution d'un paramètre au cours du temps, ainsi que renvoyer l'intégralité des paramètres a un age donné
F Castillo et T Bruant 2023
Conventions pour les données et leurs unités :
Luminosité : L | L/Lo
Rayon : R | R/Ro
Température : T | T/To
Masse : M | M/Mo
temps/age : t | annees
"""

class Structure (object):
    def __init__ (self, modele, source):
        global axes
        
        self.modele = modele
        self.source = source
        self.test = "Erreur" #Fonction test
        self.elts = ["n","X","2H","3He","Y","6Li","7Li","9Be","10B","11B",
            "12C","13C","14C","14N","15N","15O","16O","17O","18O","18F","19F","20Ne",
            "21Ne","22Ne","23Na","24Mg","25Mg","26Mg","27Al", "Alg26","28Si", "32S", 
            "36Ar", "Ca40", "44Ti", "48Cr", "52Fe", "56Ni"] #Homogénéisation de la notation Genec-Starevol
        self.elts_sv = ["n","H1","H2","He3","He4","Li6","Li7","Be9","B10","B11",
            "C12","C13","C14","N14","N15","O15","O16","O17","O18","F18","F19","Ne20",
            "Ne21","Ne22","Na23","Mg24","Mg25","Mg26","Al27", "26Alg","Si28", "S32", 
            "Ar36", "Ca40", "Ti44", "Cr48", "Fe52", "Ni56"]  

        self.dico_elts = {}
        
        for k in range(len(self.elts_sv)) : self.dico_elts[self.elts_sv[k]] = self.elts[k]

        if self.modele == "Genec" :
            fichier = open(self.source,"r")
            
            '''Import des données pour le cas du modèle GENEC'''

            fichier = open(self.source,'r')
            
            Data = ""

            fichier.readline() #enlève les deux premières lignes sans données intéressantes
            fichier.readline()
            while 1 : #J'aime le danger
                line = fichier.readline() #lis les lignes

                if line == "" : break #On a toujours une ligne vide à la fin, sert de check pour la fin de la boucle

                for j in range(10): #Vire les espaces de merde
                    line = line.replace("  "," ")
                    line = line.replace("\n ","\n")
                    line = line.replace(" \n","\n")
                    line = line.replace("#","")
                Data += line

            for k in self.dico_elts : #change le nom des élements pour être en accord avec les conventions
                    Data = Data.replace(k,self.dico_elts[k])

            Data=StringIO(Data)
            
            self.DF = pd.read_csv(Data, delimiter = " ") #crée le dataframe ou sont stocké les données dans le format standard. Attention : pas d'index
            self.test = self.DF
            
            self.args = {}        

            for i in self.DF.columns : #Passe les colonnes en array numpy, plus rapide pour les calculs
                if not i in self.args : self.args[i] = np.array(self.DF[i])

            fichier.close()
        
        if self.modele == "Starevol":
                
            fichiers = [0,0,0,0,0,0,0]
            DFS = [0,0,0,0,0,0,0]
                    
            for root,dirs,files in os.walk(self.source): #ouvre tout les fichiers utiles
                for file in files:
                    if not ".gz" in file :
                        if (".p1" in file and not ".p10" in file
                            and not ".p11" in file and not ".p12" in file
                            and not ".p13" in file and not "._" in file): fichiers[0] = open(os.path.join(root,file),"r")
                        if ".p2" in file : fichiers[1] = open(os.path.join(root,file),"r")
                        if ".p3" in file : fichiers[2] = open(os.path.join(root,file),"r")
                        if ".p4" in file : fichiers[3] = open(os.path.join(root,file),"r")
                        if ".p5" in file : fichiers[4] = open(os.path.join(root,file),"r")
                        if ".p6" in file : fichiers[5] = open(os.path.join(root,file),"r")
                        if ".p7" in file : fichiers[6] = open(os.path.join(root,file),"r")
                            
            for i in range(len(fichiers)) :
                k = fichiers[i]

                if k == "":
                    raise NameError ("Des fichiers n'ont pas été trouvés")

                texte = ""
                while 1 :
                    l = k.readline()
                    if l =="" : break
                    if (not "@" in l) and (not "<" in l) and (not ">" in l) :
                        texte+=l
                    
                for j in range(10):
                    texte = texte.replace("  "," ")
                    texte = texte.replace("\n ","\n")
                    texte = texte.replace(" \n","\n")

                texte = texte.replace("# ","")

                for k in self.dico_elts :
                    texte = texte.replace(k,self.dico_elts[k])
                
                texte=StringIO(texte)
                DFS[i]=pd.read_csv(texte,delimiter =" ")

            self.DF = pd.concat(DFS,axis=1)

            self.args = {}        

            for i in self.DF.columns :
                if not i in self.args : self.args[i] = np.array(self.DF[i])
            for k in fichiers : k.close()

    def Evolution (self,parametre,legende,X = "R", couleur="black",masse = True):
        if masse : legende += " ; M = "+str(self.vraiemasse[0])+" Mo"

        plt.plot(self.args[X],self.args[parametre], label=legende,color=couleur)

        axes.set_xlabel(X)
        axes.set_ylabel(parametre)

    def Convection (self) :
        for i in range(len(self.nablad)):
            nablad = self.nablad[i]
            nablarad= self.nablarad[i]

            if abs(nablad-nablarad) < 0.01 :
                plt.axvline(x = self.R[i],color='gray',linestyle='--',label="nablad=nablarad")
                return self.R[i]
            
    def Test (self) : #Utilisé pour le débugging, inutile sinon
        print(self.test)

class Etoile (object): 
    def __init__(self, modele, source):
        
        # Définition de la classe Etoile
        # source est un fichier pour Genec, et le repertoire qui contient tous les fichiers pour Starevol (il faut les dezipper)
        # Pour accéder à l'abondance au coeur du carbone 12 (par exemple) > Etoile.abondances_coeur["12C"]
        
        self.DF = pd.DataFrame() #Création du dataframe ou seront stocké les données, index par rapport au temps

        if modele not in ("Genec","Starevol") :
            raise ValueError ("Le modele doit etre Genec ou Starevol")
        
        self.modele = modele
        self.source = source

        self.Z_surf = []
        self.Z_coeur = [] 

        elts = ["X","2H","3He","Y","6Li","7Li","7Be","9Be","10B","11B",
            "12C","13C","14C","14N","15N","15O","16O","17O","18O","19F","20Ne",
            "21Ne","22Ne","23Na","24Mg","25Mg","26Mg","26Alm","26Alg","27Al","28Si","29Si",
            "30Si","31P","32S","33S","34S","35S","35Cl","36S","36Cl","37Cl","heavy"] #liste de tous les éléments considérés
        
        self.abondances_surf={}
        self.abondances_coeur={}
        for i in elts :
            self.abondances_surf [i] = []
            self.abondances_coeur[i] = []
        
        if self.modele == "Genec" :

            '''Import des données pour le cas du modèle GENEC'''

            fichier = open(self.source,'r')

            # Rajout de la légende des colonnes
            # Aucune idée d'à quoi servent la moitié des variables
            
            colonnes = ["nm","t","M/Mo","log(L/Lo)","log(Teff)","X_surf","Y_surf","3He_surf","12C_surf","13C_surf","14N_surf","16O_surf","17O_surf","18O_surf","20Ne_surf","22Ne_surf",
                        "Mcc","log(Teff_nc)","log(M)","log(rho_c)","log(Tc)","X_coeur","Y_coeur","3He_coeur","12C_coeur","13C_coeur","14N_coeur","16O_coeur","17O_coeur","18O_coeur","20Ne_coeur","22Ne_coeur","7Be_coeur","8Be_coeur",
                        "nu7Be","nu8Be","snuBe7","snuBe8","Omega/Omega_crit","Omega_surf","Omega_coeur","Rpol/Req","26Al_surf","26Al_coeur","M(Omega)/M(0)","lcnom","xmcno","scno",
                        "j(3Mo)","j(5Mo)","vcrit1","vcrit2","veq","lim_Gamma_Omega","Gamma_Edd","vcrit1b","vcrit2b","veqb","GammaOmegab","GammaEdb","Delta_Mneed","Mneed","Delta_L","I","Ltot","Erot","Epot","Egaz","Erad"]

            for j in range(70,110) : colonnes.append("uudrawc"+str(j))  
            colonnes.append("Ltottot")

            texte = ""
            for k in colonnes :
                texte += k+" "
            texte+="\n"

            texte += fichier.read()

            for i in range(10):  
                    texte = texte.replace("  "," ")
                    texte = texte.replace("\n ","\n")

            texte=StringIO(texte)
            self.DF=pd.read_csv(texte,delimiter=" ")

            for i in elts :
                try :
                    self.abondances_surf[i]=np.array(self.DF[i+"_surf"])
                    self.abondances_coeur[i]=np.array(self.DF[i+"_coeur"])
                except KeyError : #Il n'y a pas tous les éléments dans Genec
                    pass
                
            self.T = 10**np.array(self.DF["log(Teff)"])
            self.L = 10**np.array(self.DF["log(L/Lo)"])
            self.M = np.array(self.DF["M/Mo"])
            self.t = np.array(self.DF["t"])
            self.X = np.array(self.DF["X_coeur"])
            self.Y = np.array(self.DF["Y_coeur"])
            self.R = np.array(np.sqrt(self.L*3.828e26/(4*pi*(5.67e-8)*self.T**4))/696342e+3)

        if modele == "Starevol" : 
                
            fichiers = [0,0,0,0,0,0,0,0,0]
            DFS = [0,0,0,0,0,0,0,0,0]
                    
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
                            
            for i in range(len(fichiers)) :
                k = fichiers[i]

                if k == "":
                    raise NameError ("Des fichiers n'ont pas été trouvés")

                texte = ""
                while 1 :
                    l = k.readline()
                    if l =="" : break
                    if (not "@" in l) and (not "<" in l) and (not ">" in l) :
                        texte+=l
                    
                for j in range(10):
                    texte = texte.replace("  "," ")
                    texte = texte.replace("\n ","\n")
                    texte = texte.replace(" \n","\n")

                texte=StringIO(texte)
                DFS[i]=pd.read_csv(texte,delimiter =" ",skiprows=[0,1,2,4,5])

            self.DF = DFS[0]                     
            self.DF_coeur = pd.concat([DFS[0],DFS[5],DFS[6],DFS[7],DFS[8]],axis=1)
            self.DF_surf = pd.concat([DFS[0],DFS[1],DFS[2],DFS[3],DFS[4]],axis=1)

            self.T = np.array(self.DF["Teff"])
            self.L = np.array(self.DF["L"])
            self.R = np.array(self.DF["Reff"])
            self.t = np.array(self.DF["t"])
            self.M = np.array(self.DF["M"])

            for e in elts :
                if e == "X" :
                    self.abondances_coeur[e] = np.array(self.DF_coeur["H1"]) 
                    self.abondances_surf[e]  = np.array(self.DF_surf["H1"])
                elif e == "Y" :
                    self.abondances_coeur[e] = np.array(self.DF_coeur["He4"]) 
                    self.abondances_surf[e]  = np.array(self.DF_surf["He4"])
                elif e=="heavy" :
                    self.abondances_coeur[e] = np.array(self.DF_coeur["heavy"]) 
                    self.abondances_surf[e]  = np.array(self.DF_surf["heavy"])
                else:
                    try :
                        self.abondances_coeur[e] = np.array(self.DF_coeur[e[-1:]+e[:-1]])   #transforme par exemple 12C en C12
                        self.abondances_surf[e]  = np.array(self.DF_surf[e[-1:]+e[:-1]])
                    except KeyError:
                        try :
                            self.abondances_coeur[e] = np.array(self.DF_coeur[e[-2:]+e[:-2]])   #idem pour les elts de deux lettres, par exemple He
                            self.abondances_surf[e]  = np.array(self.DF_surf[e[-2:]+e[:-2]])
                        except KeyError:
                            pass    #ca bugue encore pour Al26m, flemme de réfléchir

        self.Z_coeur = 1- self.abondances_coeur["X"]-self.abondances_coeur["Y"]
        self.Z_surf = 1- self.abondances_surf["X"]-self.abondances_surf["Y"]

        self.DF["Z_coeur"] = self.Z_coeur
        self.DF["Z_surf"] = self.Z_surf

        self.args = {"T" : self.T,
                     "L" : self.L,
                     "M" : self.M,
                     "t" : self.t,
                     "R" : self.R,
                     "Z_surf" : self.Z_surf,
                     "Z_coeur" : self.Z_coeur
                     }
        
        for e in elts :
            self.args[e+"_surf"] = self.abondances_surf[e]
            self.args[e+"_coeur"] = self.abondances_coeur[e]
        
        for i in self.DF.columns :                       # Rajout des nouvelles variables qu'on sait pas à quoi elles servent
            if not i in self.args : self.args[i] = np.array(self.DF[i])

        self.M_ini = self.M[0]
        self.Z_ini = self.Z_coeur[0]

        self.DF.set_index("t", inplace = True)

    def HR (self,couleur="black",legende="graphique",masse = True,Zini = False,axes ="",show = False): #Définit la fonction qui trace les diagrammes HR

        if axes == "" : 
            axes = plt.gca()
            axes.invert_xaxis()
            
        if masse : legende += " ; M = "+str(self.M_ini)+" Mo"
        if Zini  : legende += " ; Z_ini ="+str(self.Z_ini)

        plt.plot(np.log10(self.T/5777),np.log10(self.L),label=legende)
        plt.legend()

        axes.set_xlabel("log T/To")
        axes.set_ylabel("log L/Lo")

        if show : plt.show()

    def Evolution (self, Varx = "t", Vary = [], xlegend = "xlegend", ylegend = "ylegend", label="", logx = False, masse = False, Zini = False, show = True) : 
        
        if xlegend == "xlegend":
            xlegend = Varx
            if logx : xlegend ="log "+xlegend
            
        if type(Vary) == str : Vary = [Vary] #Verifie le bon type de données

        X = self.args[Varx]
        if logx : X = np.log10(X)

        for i in Vary : 
            lab = label + "; " + i

            if masse : lab += " ; M = "+str(self.M_ini)+" Mo"
            if Zini  : lab += " ; Z_ini ="+str(self.Z_ini)

            plt.plot(X,self.args[i],label=lab)
        
        plt.xlabel(xlegend) 
        plt.ylabel(ylegend)

        plt.legend()

        if show : plt.show()
            
    def Para (self, age, parametres): #Affiche les valeurs de certains parametres à un age donné. Prend une liste de str comme argument

        index_DF = list(self.DF.index.values.tolist())
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

        print("t : ", index_DF[i]) #Affiche l'âge trouvé

        for para in parametres : #Affiche tout les paramètres
            try :
                print(para, ": ", self.DF[para].iloc[i])
            except :
                print("Erreur : ", para),
                pass

    def Age (self, X, err = 0.01):

        i = 0

        for x in self.abondances_coeur["X"] :
            if abs(x-X) < err: break
            i +=1

        return self.t[i]

    def Rien (self):    #fonction qui ne fait rien
        pass
    
    def Spammer_Aaron (self):
        for k in self.DF.columns :
            try:
                self.Evolution(Varx="t",Vary=k,ylegend=k,logx=True,label="Aaron",show=False)
                plt.savefig("./Aaron/Aaron "+k.replace("/","-")+".png")
                plt.cla()
            except : print(k)

if __name__ == "__main__" :

    axes = plt.gca()
    axes.invert_xaxis()

    Sol = Etoile(modele = "Genec", source = "T:\Cours\DATA\GENEC\classique_m1.0.wg")
    Sol.Para(570000, ["X_coeur", "Y_coeur"])
