### Etude des modèles d'évolution stellaire (Projet tutoré à l'IPHC sous la direction de Mme Courtin et M. Heine)
#### Par Théo BRUANT et Fabien CASTILLO

Modèles supportés : STAREVOL, GENEC


MAJ de ce matin :

Rajout d'une fonction Etoile.\__getitem__ qui permet d'accéder à une variable sans passer par Etoile.args

Optimisation du code des fichiers de Structure pour Genec qui lisait ligne/ligne (il faudrait voir si on peut trouver un moyen de le faire pour Starevol)

Conversion dans les bonnes unités des trucs qui étaient en log dans les fichiers de structure

Optimisation des fonctions Etoile.Parametre et Etoile.age

Structure.Convection marche de nouveau

TBA : 

Deux ou trois trucs à optimiser

Je n'ai pas trouvé la variable qui donne la masse totale pour le fichiers de Structure Starevol
