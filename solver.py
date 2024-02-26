
import random
from queue import Queue
import time
import copy
from itertools import combinations, product

class Alldiff:
    def __init__(self,variables, domains):
        self.variables = variables
        self.domains = domains

    def create_constraints(self, constraints = None):
        
        tuples = list(combinations(self.variables, 2))
        if constraints is None:
            constraints = {}
            for (x,y) in tuples:
                constraints[(x,y)] = []
                for a in self.domains[x]:
                    for b in self.domains[y]:
                        if not (a==b):
                            constraints[(x,y)].append((a,b))
            return constraints
        else : 
            for (x,y) in tuples:
                for (a,b) in constraints[(x,y)]:
                    if (a==b):
                        constraints[(x,y)].remove((a,b))
            return constraints
        
class SommePonderee:
    def __init__(self,variables, domains, a, b):
        self.variables = variables
        self.domains = domains
        self.a = b

    def create_constraints(self, nom_x = 1000):
        valeurs = {}
        for var in self.variables:
            valeurs[var] = self.domains[var]
        listes_de_valeurs = list(valeurs.values())
    
        # Utiliser la fonction product pour générer les n-uplets possibles
        n_uplets_possibles = list(product(*listes_de_valeurs))

        x = nom_x
        constraints = {}
        domaine_x = n_uplets_possibles
        for i in range(n_uplets_possibles):
            n_uplet = n_uplets_possibles[i]
            for y in self.variables:
                constraints[(x,y)] = []
                for b in self.domains[y]:
                    if b in n_uplet:
                        constraints[(x,y)].append(n_uplet,b)
     
        return x,domaine_x, constraints


class Solver:
    def __init__(self, variables : list,constraints : dict,domains : dict, alldiff : Alldiff = None,SommePonderee : SommePonderee = None):
        self.variables = variables
        self.constraints = constraints
        self.domains = domains
        if alldiff is not None : 
            self.constraints = alldiff.create_constraints()
        if SommePonderee is not None:
            x,domaine_x, constraints_somme = SommePonderee.create_constraints()
            self.variables.append(x)
            self.domains[x] = domaine_x
            self.constraints.update(constraints_somme)

    def print_dom_var(self) -> None:
        print("Variables : \n")
        for key, item in self.domains.items():
            print(key, " ", item, "\n")
        

    def print_cstr_model(self) -> None:
        print("Contraintes : \n")
        for key, cstr in self.constraints.items() : 
            print(key, " :  ", cstr, "\n")

    def backtrack(self, algo = "forward-checking", method = "PPD"):
        solution, compteur = backtrack({}, self.variables, self.domains, self.constraints, method, algo, 0)
        return solution, compteur

    

def backtrack(assignment, variables, domains, constraints, method, algo, compteur):

    if len(assignment) == len(variables):
        print("Compteur final : ", compteur)
        return assignment, compteur

    var = select_unassigned_variable(assignment, variables, domains, constraints, method)
    for value in order_domain_values(var, assignment, domains):
        if is_consistent(var, value, assignment, constraints):
            new_domains = copy.deepcopy(domains)

            if algo=="forward-checking":
                new_domains = forward_checking(var,variables,constraints, value,assignment,new_domains)
            elif algo == "AC3":
                new_domains = AC3(variables,constraints,new_domains)
            elif algo=="AC4":
                new_domains = AC4(variables,constraints,new_domains)
            elif algo == "":
                pass
            else :
                print("ERREUR : Nom d'algorithme faux : ", algo)
                print("Veuillez choisir un nom d'algorithme entre forward-checking, AC3 et AC4, ou un espace vide pour ne pas utiliser d'algorithme.")
            assignment[var] = value

            result, compteur = backtrack(assignment, variables, new_domains, constraints, method, algo, compteur + 1)

            if result is not None:
                return result, compteur
            del assignment[var]
    return None, compteur



def select_unassigned_variable(assignment, variables, domains, constraints, method):
    not_assigned_variables = []
    for var in variables:
        if var not in assignment:
            not_assigned_variables.append(var)
    if len(not_assigned_variables)==0:
        print("toutes les variables ont été assignées ! ")
    if method == "random":
        random_idx_var = random.randrange(len(not_assigned_variables))
        var = not_assigned_variables[random_idx_var]
    elif method == "deterministe":
        var = not_assigned_variables[0]
    elif method == "PPD":
        sorted_var = sorted(not_assigned_variables, key = lambda k: len(domains[k]) )
        var = sorted_var[0]
    elif method=="PC":
        def nombre_de_contraintes(var,contraintes):
            occurrences = sum(1 for cle in contraintes.keys() if var in cle)
            return occurrences
        sorted_var = sorted(not_assigned_variables, key = lambda k: nombre_de_contraintes(k, constraints) )
        var = sorted_var[0]
    else :
        print("ERREUR : Nom de méthode fausse : ", method)
        print("Veuillez choisir un nom de méthode entre random, deterministe, PPD et PC.")
    return var

def order_domain_values(var, assignment, domains):
    return domains[var]

def is_consistent(var, value, assignment, constraints):
    for (var1, var2), allowed_values in constraints.items():
        if var1 == var and var2 in assignment:
            if (value, assignment[var2]) not in allowed_values:
                return False
        elif var2 == var and var1 in assignment:
            if (assignment[var1], value) not in allowed_values:
                return False
    return True

def check_compatibility(var1,val1,var2,val2,constraints):
    return any((val1, val2) in allowed_values for (v_i, v_j), allowed_values in constraints.items() if v_i == var1 and v_j == var2)

def forward_checking(var,variables,constraints,value,assignment,domains):
    for v in variables:
        if v not in assignment and var!=v:
            for val in domains[v]:
                if not check_compatibility(var,value,v,val,constraints):
                    domains[v].remove(val)
    return copy.deepcopy(domains)

def initialize_ac4(variables,constraints, domains):
    Q = Queue()
    S = dict()
    Count = dict()
    for (x,y),allowed_values in constraints.items():
        for a in domains[x]:
            total = 0
            for b in domains[y]:
                if (a,b) in allowed_values:
                    total += 1
                    S[(y, b, x)] = a
            Count[x,y,a] = total
            if total == 0:
                Q.put((x,a))
                domains[x].remove(a)
    return Q, S, Count, domains

def AC4(variables,constraints,domains):
    #print("ac4 : ")
    Q, S, Count, domains = initialize_ac4(variables,constraints,domains)
    while not Q.empty():
        (y,b) = Q.get()
        x_a = [(x,a) for (var_1, val_1, x),a in S.items() if var_1==y and val_1==b]
        for (x,a) in x_a:
            Count[x,y,a] = Count[x,y,a] - 1
            if Count[x,y,a] == 0 and a in domains[x]:
                domains[x].remove(a)
                Q.put((x,a))
    return copy.deepcopy(domains)


def AC3(variables, constraints, domains):
    """Arc consistance : modifie directement les domaines des variables du modèle"""

    toTest = list(constraints.keys())
    toTest.extend([(y,x) for x,y in list(constraints.keys())])

    while toTest:
        x, y = toTest.pop()
        original_domain = list(domains[x])
        
        for val_x in original_domain:
            if not any(
                (val_x, val_y) in constraints.get((x, y), []) or
                (val_y, val_x) in constraints.get((y, x), [])
                for val_y in domains[y]
                ):
                domains[x].remove(val_x)

                if x < y :
                    toTest.extend([(a,b) for (a,b) in constraints.keys() if a == x and b!=y]) 
                else :
                    toTest.extend([(a,b) for (a,b) in constraints.keys() if b == x and a!=y ]) 
    return copy.deepcopy(domains)

