# PROJET_PYTHON_G1

Entrainement evolutif de l'IA : https://www.youtube.com/watch?v=gVEWaOtEASM

Entrainement plus poussé en évolutif + renforcement learning : https://www.youtube.com/watch?v=kojH8a7BW04



* Super class unité
* Class cavalier, lancier, archer
* CLass map
* pathfinder
* Class IA + DAFT et BRAINDEAD


#  SAUVEGARDE 

HEADERS : Carte utilisée


ID; TYPE; VIE; DIRECTION; DEPLACEMENT; COOR_DEBUT; COOR_FIN;

ID; TYPE; VIE; DIRECTION; ATTACK; ID_ENEMY;

#  MAP 

1000x1000; [L,R,U,D] <- Left Right Up Down, c'est pour saoir sur quel arrête on doit faire la duplication

      B
      
KKKK  B

kkkk  B

kkkk  B 

      B
      
      B
