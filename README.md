### Etude des modèles d'évolution stellaire (Projet tutoré à l'IPHC sous la direction de Mme Courtin et M. Heine)
#### Par Théo BRUANT et Fabien CASTILLO

Modèles supportés : STAREVOL, GENEC


MAJ 16/02/2023
J'ai rajouté la variable Etoile.args qui permer de passer les arguments aux fonctions Evolution et Para en donnant un str. Exemple : Etoile.args["T"] > Etoile.T

J'ai changé la fonction Para pour qu'elle fasse environ 40 lignes de moins : elle prend en argument la liste des parametres (dans Etoile.args)  qu'il faut afficher et renvoie la liste des valeurs correspondantes. Exemple : Etoile.Para (age, ["T","L","12C_surf"])

J'ai aussi converti les listes en np.array, ce qui est plus pratique pour les graphes

Correction d'un bug mineur dans starevol
Suppression de variables inutiles
Rajout d'un parametre "log" dans la fonction Evolution qui permet de tracer l'évolution du log d'un parametre

TBA : 
- nouveau modèle d'évolution stellaire
- interface graphique ?
