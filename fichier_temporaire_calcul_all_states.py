import json
from state import State

from game import Game
import numpy as np
from players import RandomPlayer
from players import Randomselector


#### FONCTIONS TECHNIQUES ######


def tuple_to_state(grid_tuple):
    """Converts a tuple into a State"""
    np_grid = np.array(grid_tuple, dtype=bool).T
    return State(len(grid_tuple[0]), len(grid_tuple), np_grid)


def state_to_tuple(state: State):
    """Converts a State into a tuple"""
    return tuple(tuple(1 if c else 0 for c in row) for row in state.grid.T)


def state_in_listState(list_state: list[State], state: State):
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


def fils_noeud(state: State, n: int):
    """A partir d'un certain état renvoie tous les états suivants possibles"""
    play = RandomPlayer()
    sele = Randomselector()
    jeu = Game(n, n, play, sele)
    jeu.state = state
    resultat = []
    for piece_a in jeu.pieces:
        for act in jeu.player_actions:
            piece = piece_a.copy()
            newstate, player_r, selector_r = jeu.next_state(jeu.state, act, piece)
            if selector_r != 1:
                resultat.append(newstate)
            else:
                pass
    return resultat


def calcul_all_states(state0: State, n: int):
    """Renvoie l'ensemble de tous les états (sous forme de tuples) accessibles au cours du jeu"""
    rst = []
    count = 0
    liste_attente = [state0]
    while len(liste_attente) != 0:
        new_attente = []
        for state in liste_attente:
            rst.append(state)
            count += 1
            print(count)
            liste_fils = fils_noeud(state, n)
            for fils in liste_fils:
                if (
                    not (fils in liste_attente)
                    and not (fils in rst)
                    and not (fils in new_attente)
                ):
                    new_attente.append(fils)
        liste_attente = new_attente

    return [state_to_tuple(elt) for elt in rst]


######## DATA FILE RELATED ###################


def charger(mat: any):
    """Charge sur le fichier all_states.json la matrice mat"""
    with open("all_states.json", "w") as f:
        json.dump(mat, f)
        print("Chargement DONE")


def afficher(lst):
    for elt in lst:
        print(elt)
        print("\n")


def lire_all_states():
    """renvoie la liste des états du fichier all_states.json"""
    with open("all_states.json", "r") as f:
        data = json.load(f)
    rst = []
    for grid in data:
        rst.append(tuple_to_state(grid))
    return rst


def length_data():
    """gives the length of the saved data (to verify coherence)"""
    with open("all_states.json", "r") as f:
        data = json.load(f)
    print("The length of the data is : ")
    print(len(data))


######################################""


def check(etat):
    """Verifie si etat est dans la liste des états enregistrés"""
    lst = lire_all_states()
    return etat in lst


def main(n: int):
    """Initialise et charge tous les états sur le fichier"""
    s0 = State(n, n)
    all_states = calcul_all_states(s0, n)
    charger(all_states)


########## EXECUTION ###################

# main(n) pour acutaliser le fichier /!\ à ne plus éxécuter, on a déjà tout enregistré.
# les fonctions data files permettent d'afficher la longueur, où tous les états,
# ou charger un fichier (ne plus utiliser aussi ce dernier)

# for elt in lire_all_states():
#     print(elt)
#     print("\n")

# main(4)

print(
    check(
        tuple_to_state(
            (
                (np.float64(1.0), np.float64(1.0), np.float64(1.0), np.float64(1.0)),
                (np.float64(1.0), np.float64(1.0), np.float64(1.0), np.float64(0.0)),
                (np.float64(1.0), np.float64(1.0), np.float64(1.0), np.float64(0.0)),
                (np.float64(1.0), np.float64(1.0), np.float64(1.0), np.float64(0.0)),
            )
        )
    )
)
print(length_data())
lst = lire_all_states()
for k in range(19):
    print(lst[k])
    print("\n")

print(state_to_tuple(lst[2]))
print(lst[2])
