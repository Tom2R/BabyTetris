import json
from state import State
from state import Piece
from game import Game
import numpy as np
from players import RandomPlayer
from players import Randomselector

#### FONCTIONS TECHNIQUES ######

def tuple_to_state(grille_tuple : tuple[tuple[int]]): #prend en argument une matrice tuple \in {0,1}
    """From a matrice tuple of 1 and 0 it gives the associated state"""
    d1,d2 = len(grille_tuple),len(grille_tuple[0])
    transgrid = np.ones((d1,d2))
    for i in range(d1):
        for j in range(d2):
            if grille_tuple[i][j]:
                transgrid[i][j] = 1
            else:
                transgrid[i][j] = 0
    return State(d1,d2,transgrid)
    

def state_to_tuple(state : State):
    """From a state it gives his associated tuple grid with 0 and 1"""
    newgrid = np.ones((np.shape(state.grid)))
    print(state)
    for i in range(np.shape(state.grid)[0]):
        for j in range(np.shape(state.grid)[1]):
            if state.grid[i][j]:
                newgrid[i][j] = 1
            else:
                newgrid[i][j] = 0
    return tuple(tuple(row) for row in newgrid)

def state_in_listState(list_state : list[State],state: State):
    """Nous dit si l'état donné en argument est dans la liste donnée (comparaison de grilles)"""
    for etats in list_state:
        var_bool2 = True
        for i in range(np.shape(state.grid)[0]):
            for j in range(np.shape(state.grid)[1]):
                if state.grid[i][j] != etats.grid[i][j]:
                    var_bool2 = False
        if var_bool2:
            return True
        else:
            pass
    return False
    
################################

####### FONCTIONS GLOBALES  #########

def fils_noeud(state : State , n : int):
    """A partir d'un certain état renvoie tous les états suivants possibles"""
    play = RandomPlayer()
    sele = Randomselector()
    jeu = Game(n,n,play,sele)
    jeu.state = state
    resultat = []
    for piece in jeu.pieces:
        for act in jeu.player_actions:
            newstate,player_r,selector_r = jeu.next_state(jeu.state,act,piece)
            if selector_r != 1 :
                resultat.append(newstate)
            else:
                pass
    return resultat

def calcul_all_states(state0 : State, n : int):
    """Renvoie l'ensemble de tous les états (sous forme de tuples) accessibles au cours du jeu"""
    rst = []
    liste_attente = [state0]
    count = 0
    while len(liste_attente) != 0:
        for state in liste_attente:
            rst.append(state)
            count+=1
            print(count)
            liste_attente.remove(state)
            liste_fils = fils_noeud(state,n)
            for fils in liste_fils:
                if not(state_in_listState(liste_attente,fils)) and not(state_in_listState(rst,fils)):
                    liste_attente.append(fils)
    
    return [state_to_tuple(elt) for elt in rst]


######## DATA FILE REALTED ###################

def charger(mat : any):
    """Charge sur le fichier all_states.json la matrice mat"""
    with open('all_states.json','w') as f:
        json.dump(mat,f)
        print("Chargement DONE")

def lire_all_states():
    """renvoie la liste des états du fichier all_states.json"""
    with open('all_states.json','r') as f:
        data = json.load(f)
    rst = []
    for grid in data:
        rst.append(tuple_to_state(grid))
    return rst

def length_data():
    """gives the length of the saved data (to verify coherence)"""
    with open('all_states.json','r') as f:
        data = json.load(f)
    print("The length of the data is : ")
    print(len(data))
######################################""


def main(n : int):
    """Initialise et charge tous les états sur le fichier"""
    s0 = State(n,n)
    all_states = calcul_all_states(s0,n)
    charger(all_states)


########## EXECUTION ###################

# main(n) pour acutaliser le fichier /!\ à ne plus éxécuter, on a déjà tout enregistré.
# les fonctions data files permettent d'afficher la longueur, où tous les états, 
# ou charger un fichier (ne plus utiliser aussi ce denier) 




