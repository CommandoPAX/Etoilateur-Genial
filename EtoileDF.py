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
sns.set(font_scale=1.5) # fixe la taille de la police à 1.5 * 12pt

""" Programme qui parcourt les fichiers générés par Genec et Starevol
Permet entre autres de générer le diagramme HR ou l'évolution d'un paramètre au cours du temps, ainsi que renvoyer l'intégralité des paramètres a un age donné
F Castillo et T Bruant 2023
Conventions pour les données et leurs unités :
Luminosité : L | L/Lo
Rayon : R | R/Ro
Température : T | K
Masse : M | M/Mo
temps/age : t | annees
ABondances : fractions massiques """

fg, ax1 = plt.subplots()

class Structure (object):
    def __init__ (self, modele, source):
        global axes
        
        self.modele = modele
        self.source = source

        # Homogénéisation de la notation Genec-Starevol

        self.elts = ["n","X","2H","3He","Y","6Li","7Li","9Be","10B","11B",
            "12C","13C","14C","14N","15N","15O","16O","17O","18O","18F","19F","20Ne",
            "21Ne","22Ne","23Na","24Mg","25Mg","26Mg","27Al", "Alg26","28Si", "32S", 
            "36Ar", "Ca40", "44Ti", "48Cr", "52Fe", "56Ni"]     
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
            
            Data = fichier.read()

            for j in range(10): # Vire les espaces de merde
                Data = Data.replace("  "," ")
                Data = Data.replace("\n ","\n")
                Data = Data.replace(" \n","\n")
                Data = Data.replace("#","")

            Data = Data.replace("Nabad","nablad")
            Data = Data.replace("Nabrad","nablarad")

            for k in self.dico_elts : # Change le nom des élements pour être en accord avec les conventions
                Data = Data.replace(k,self.dico_elts[k])

            Data=StringIO(Data)
            
            self.DF = pd.read_csv(Data, delimiter = " ",skiprows = [0,1]) # Crée le dataframe ou sont stocké les données dans le format standard. Attention : pas d'index
            self.test = self.DF
            
            self.args = {}        

            for i in self.DF.columns : # Passe les colonnes en array numpy, plus rapide pour les calculs
                if not i in self.args : self.args[i] = np.array(self.DF[i])

            fichier.close()

            self.args["r"] = 10**self.args["r"]/6.96e10
            self.args["T"] = 10**self.args["t"]
            self.args["P"] = 10**self.args["p"]
        
        if self.modele == "Starevol":
                
            fichiers = [0,0,0,0,0,0,0]
            DFS = [0,0,0,0,0,0,0]
                    
            for root,dirs,files in os.walk(self.source): # Ouvre tout les fichiers utiles
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

                if k == 0:
                    raise NameError ("Des fichiers n'ont pas été trouvés")

                texte = k.read()
                    
                for j in range(10):
                    texte = texte.replace("  "," ")
                    texte = texte.replace("@","")
                    texte = texte.replace(">","")
                    texte = texte.replace("<","")
                    texte = texte.replace("\n ","\n")
                    texte = texte.replace(" \n","\n")

                texte = texte.replace("# ","")
                texte = texte.replace("abadd","nablad")
                texte = texte.replace("abrad","nablarad")

                for k in self.dico_elts :
                    texte = texte.replace(k,self.dico_elts[k])
                
                texte=StringIO(texte)
                DFS[i]=pd.read_csv(texte,delimiter =" ")
                
            self.DF = pd.concat(DFS,axis=1)

            self.args = {}        

            for i in self.DF.columns :
                if not i in self.args : self.args[i] = np.array(self.DF[i])

            for k in fichiers : k.close()

        self.args["Z"] = 1-self.args["X"]-self.args["Y"]

    def __getitem__ (self,x): # Permet d'accéder à un paramètre directement en tapant Etoile["parametre"]
        return self.args[x]

    def Evolution (self,parametres,legende,X = "r", masse = True,xlegende="",ylegende="",show=False, ls = ""):

        if type(parametres) == str : parametres = [parametres]

        if xlegende == "" : xlegende = X

        for y in parametres :
            try :
                if ls == "" : plt.plot(self.args[X],self.args[y], label=legende+" ; "+y)
                else : plt.plot(self.args[X],self.args[y], label=legende+" ; "+y, linestyle = ls)
            except KeyError : print("Parametre inconnu : "+y)

        axes.set_xlabel(xlegende)
        axes.set_ylabel(ylegende)

        plt.legend()

        if show : ax1.show()

    def Convection (self,couleur="gray",legende="nablad = nablarad") :

        diff = self["nablad"]-self["nablarad"]
        signe = np.sign(diff)

        signechange = np.where(diff[:-1] * diff[1:] < 0 )[0] +1

        r = []

        for k in signechange :
            r.append(self["r"][k])
            plt.axvline(x = self["r"][k],color=couleur,linestyle='--',label=legende)

        return r
            
class Etoile (object): 
    def __init__(self, modele, source):
        
        # Définition de la classe Etoile
        # source est un fichier pour Genec, et le repertoire qui contient tous les fichiers pour Starevol (il faut les dezipper)
        # Pour accéder à l'abondance au coeur du carbone 12 (par exemple) > Etoile["12C_coeur"]
        
        if modele not in ("Genec","Starevol") :
            raise ValueError ("Le modele doit etre Genec ou Starevol")
        
        self.modele = modele
        self.source = source

        self.Z_surf = []
        self.Z_coeur = [] 

        self.elts = ["X","2H","3He","Y","6Li","7Li","7Be","9Be","10B","11B",
            "12C","13C","14C","14N","15N","15O","16O","17O","18O","19F","20Ne",
            "21Ne","22Ne","23Na","24Mg","25Mg","26Mg","26Alm","26Alg","27Al","28Si","29Si",
            "30Si","31P","32S","33S","34S","35S","35Cl","36S","36Cl","37Cl","heavy"] # Liste de tous les éléments considérés
        
        self.abondances_surf={}
        self.abondances_coeur={}
        for i in self.elts :
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

            for i in self.elts :
                try :
                    self.abondances_surf[i]=np.array(self.DF[i+"_surf"])
                    self.abondances_coeur[i]=np.array(self.DF[i+"_coeur"])
                except KeyError : # Il n'y a pas tous les éléments dans Genec
                    pass

            # Conversion des variables les plus utiles dans les mêmes unités pour les deux modèles
                
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
                    
            for root,dirs,files in os.walk(source,topdown=False): # Ouvre tout les fichiers utiles
                for file in files :
                    if not ".gz" in file :
                        if ".c1" in file : fichiers[5] = open(os.path.join(root,file),"r")
                        if ".c2" in file : fichiers[6] = open(os.path.join(root,file),"r")
                        if ".c3" in file : fichiers[7] = open(os.path.join(root,file),"r")
                        if ".c4" in file : fichiers[8] = open(os.path.join(root,file),"r")
                        if ".s1" in file : fichiers[1] = open(os.path.join(root,file),"r")
                        if ".s2" in file : fichiers[2] = open(os.path.join(root,file),"r")
                        if ".s3" in file : fichiers [3] = open(os.path.join(root,file),"r")
                        if ".s4" in file : fichiers[4] = open(os.path.join(root,file),"r")
                        if file == "mevol.hr": fichiers[0] = open(os.path.join(root,file),"r")

            for i in range(len(fichiers)) :
                k = fichiers[i]

                if k == 0:
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

            # A optimiser avec le dico
      
            for e in self.elts :
                try :
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
                            self.abondances_coeur[e] = np.array(self.DF_coeur[e[-1:]+e[:-1]])   # Transforme par exemple 12C en C12
                            self.abondances_surf[e]  = np.array(self.DF_surf[e[-1:]+e[:-1]])
                        except KeyError:
                            try :
                                self.abondances_coeur[e] = np.array(self.DF_coeur[e[-2:]+e[:-2]])   # Idem pour les elts de deux lettres, par exemple He
                                self.abondances_surf[e]  = np.array(self.DF_surf[e[-2:]+e[:-2]])
                            except KeyError:
                                pass    # Ca bugue encore pour Al26m, flemme de réfléchir
                except : print(self.DF_coeur.columns)

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
        
        for e in self.elts :
            self.args[e+"_surf"] = self.abondances_surf[e]
            self.args[e+"_coeur"] = self.abondances_coeur[e]
        
        for i in self.DF.columns :                          # Rajout des nouvelles variables qu'on sait pas à quoi elles servent
            if not i in self.args : self.args[i] = np.array(self.DF[i])

        self.M_ini = self.M[0]
        self.Z_ini = self.Z_coeur[0]

        self.DF.set_index("t", inplace = True)

    def __getitem__ (self,x):           # Permet d'accéder à un paramètre directement en tapant Etoile["parametre"]
        return self.args[x]
    
    def HR (self,couleur="",legende="graphique",masse = True,Zini = False,axes ="",show = False): # Définit la fonction qui trace les diagrammes HR

        if axes == "" : 
            axes = plt.gca()
            axes.invert_xaxis()
            
        if masse : legende += " ; M = "+str(self.M_ini)+" Mo"
        if Zini  : legende += " ; Z_ini ="+str(self.Z_ini)

        if couleur == "" : ax1.plot(np.log10(self.T/5777),np.log10(self.L),label=legende)
        else : ax1.plot(np.log10(self.T/5777),np.log10(self.L),label=legende, color=couleur)
        
        plt.legend()

        axes.set_xlabel("log T/To")
        axes.set_ylabel("log L/Lo")

        if show : plt.show()

    def Evolution (self, x = "t", parametres = [], xlegende = "xlegende", ylegende = "ylegende", ls="", legende="", logx = False, masse = False, Zini = False, show = False) : 
        
        if xlegende == "xlegende":
            xlegende = x
            if logx : xlegende ="log "+xlegende
            
        if type(parametres) == str : Vary = [parametres] 

        X = self.args[x]
        if logx : X = np.log10(X)

        for i in parametres : 
            lab = legende + "; " + i

            if masse : lab += " ; M = "+str(self.M_ini)+" Mo"
            if Zini  : lab += " ; Z_ini ="+str(self.Z_ini)

            try:
                if ls == "" : ax1.plot(X,self.args[i],label=lab)
                else : ax1.plot(X,self.args[i],label=lab, linestyle=ls)
            except KeyError : print("Parametre inconnu : "+i)

        
        plt.xlabel(xlegende) 
        plt.ylabel(ylegende)

        plt.legend()

        if show : plt.show()
            
    def Para (self, age, parametres): # Affiche les valeurs de certains parametres à un age donné

        age_opti = np.argmin(np.abs(self.t - age))

        if type (parametres) == str : parametres = [parametres]

        resultats = []
        for k in parametres : resultats.append(self.args[k][age_opti])

        return resultats

    def Age (self, X):      # Donne l'âge auquel l'étoile atteint une certaine abondance en hydrogène au coeur

        x_opti = np.argmin(np.abs(self["X_coeur"]-X))

        return self.t[x_opti]

    def Derivee(self,x,y,legende = "", plot = True):
        x = self[x]
        y = self[y]

        xn = (x[:-1] + x[1:]) / 2
        yn = (y[1:] - y[:-1]) / (x[1:] - x[:-1])

        if plot : ax1.scatter(xn, yn, label = legende,s=0.01)

        return [xn,yn]

    def Rien (self):    # Fonction qui ne fait rien
        pass
    
    def Spammer_Aaron (self):       # Permet d'enregistrer plein de graphes qu'on peut envoyer aux collègues pour les spammer
        for k in self.DF.columns :
            try:
                self.Evolution(Varx="t",Vary=k,ylegende=k,logx=True,label="Aaron",show=False)
                plt.savefig("./Aaron/Aaron "+k.replace("/","-")+".png")
                plt.cla()
            except : print(k)

def Difference (etoile1,etoile2,parametre,show=False,legende="", Evol = False, couleur = "pink") : #Calcule la différence entre deux modèles
    t1 = etoile1["t"].shape
    t2 = etoile2["t"].shape

    if t1 < t2 :
        etoile3 = etoile2
        etoile2 = etoile1
        etoile1 = etoile3

    if legende == "" : legende = parametre

    zeros = np.zeros(shape = etoile1["t"].shape)

    if Evol == True : #True si pour ajouter a un autre graphe, False sinon
        fg, axdiff = plt.subplots()
        axdiff = ax1.twinx()

    for i in range(len(etoile1["t"])):
        zeros[i] = etoile1[parametre][i]-etoile2.Para(age = float(etoile1["t"][i]),parametres=parametre)[0]

    axdiff.plot(etoile1["t"],zeros,label=legende, color = couleur)
    if show : plt.show()

    return zeros

if __name__ == "__main__" :

    axes = plt.gca()

    Rot = Structure(modele = "Starevol", source = r"C:\Users\bruan\Pictures\ProjetTutore\DATA\Rotation14\Structure_M1")
    NoRot = Structure(modele = "Starevol", source = r"C:\Users\bruan\Pictures\ProjetTutore\DATA\Structure\STAREVOL")

    Rot.Evolution(parametres = ["T"], legende= "Avec rotation")
    NoRot.Evolution(parametres = ["T"], legende = "Sans Rotation", ls = "--")

    Difference(Rot, NoRot, "T", legende = "Différence", show = False, Evol = True)

    plt.legend()
    
    plt.show()
