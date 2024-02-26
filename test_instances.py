
from instances_reader import *
from solver import *



file_path = r"C:\\Users\\margo\\OneDrive\\Documents\\TRAVAIL\\Master\\MPRO\\S3\\PPC\\Margot_graphes\\myciel4.col.txt"

#file_path = r"C:\\Users\\margo\\OneDrive\\Documents\\TRAVAIL\\Master\\MPRO\\S3\\PPC\\Margot_graphes\\mulsol.i.5.col"


#Création k colorations
def k_coloration(n):
    print(f"Création de l'instance {n}-colorations ...")
    graph = parse_graph_file(file_path)
    domains = {vertice : list(range(n)) for vertice in range(1, graph.num_vertices+1)}
    variables = range(1,graph.num_vertices+1)
    constraints = {}
    for edge in graph.edges :
        constraints[edge]= [(i,j) for i in range(n) for j in range(n) if i!=j]
    return variables, constraints, domains


# Creation reines instance
def n_reines(n):
    print(f"Création de l'instance {n} reines ...")
    variables = range(n)
    domains = {key : list(range(n)) for key in range(n)}
    constraints = {}

    for i in range(n):
        for j in range(i+1,n):
            constraints[(i,j)] = [(a,b) for a in range(n) for b in range(n)
                                        if (a - b != j - i) and (b - a != j - i) and (a != b)]
    return variables, constraints, domains



if __name__ == "__main__":

    n = 5

    is_n_reine = False
    if is_n_reine: 
        variables, constraints, domains = n_reines(n)
        start = time.time()        
        Solver = Solver(variables,constraints,domains)  
        solution, compteur = Solver.backtrack(algo = "forward-checking", method = "PC")
        execution_time = time.time() - start
        plot_n_queens(solution,n)

    else : 
        variables, constraints, domains = k_coloration(n)
        start = time.time()        
        Solver = Solver(variables,constraints,domains)  
        solution, compteur = Solver.backtrack(algo = "AC3", method = "PPD")
        execution_time = time.time() - start

    print("Solution : ", solution)
    print("Temps d'exécution : ", execution_time)


