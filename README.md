### Etude des modèles d'évolution stellaire (Projet tutoré à l'IPHC sous la direction de M. Heine et T. Dumont)
#### Par Fabien CASTILLO et Théo BRUANT

Modèles supportés : STAREVOL, GENEC, MESA

Chargement des données : etoile = Etoile (modele, source)

source est le chemin vers les fichiers de données (le dossier qui contient les fichiers dézippés pour Starevol, le fichier .dat pour Genec).

Pour tracer un diagramme HR : etoile.HR(options)

Pour connaitre l'évolution d'un ou plusieurs parametres : etoile.Evolution (parametres, options).

Pour tracer sur un même graphe la différence entre deux courbes : Difference (etoile1, etoile2, parametre).

etoile.Age(X) : renvoie l'âge qui correspond à une abondance au coeur donnée

etoile.Para(age, parametres) : renvoie les valeurs des parametres à un âge donné

etoile[parametre] > renvoie un tableau numpy avec les valeurs d'un parametre

Pour charger un fichier de structure : structure = Structure (modele, source).

struct.Convection () : trace une ligne verticale qui correspond au changement de régime radiatif/convectif
