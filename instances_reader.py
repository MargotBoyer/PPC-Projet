import numpy as np
import matplotlib.pyplot as plt

class Graph:
    def __init__(self, edges, num_vertices, num_edges):
        self.edges = edges
        self.num_vertices = num_vertices
        self.num_edges = num_edges

def parse_graph_file(file_path):
    edges = []
    num_vertices = 0
    num_edges = 0

    with open(file_path, 'r') as file:
        for line in file:
            tokens = line.strip().split()

            if tokens and tokens[0] == 'p':
                num_vertices = int(tokens[2])
                num_edges = int(tokens[3])
            elif tokens and tokens[0] == 'e':
                edge = (int(tokens[1]), int(tokens[2]))
                edges.append(edge)

    print("Graphe généré : ")
    print("Nombre de noeuds : ", num_vertices)
    print("Nombre d'arêtes : ", num_edges)

    return Graph(edges, num_vertices, num_edges)


def plot_n_queens(board, n):

    chessboard = np.zeros((n, n, 3))
    for i in range(n):
        for j in range(n): 
            chessboard[i,j] = [1,1,1]

    # Color the cells based on the presence of a queen
    for row, col in board.items():
        chessboard[n - 1 - row, col] = [0.8, 0.8, 0]

    plt.xticks(np.arange(-0.5, n, 1), [])
    plt.yticks(np.arange(-0.5, n, 1), [])
    plt.grid(color='black', linestyle='-', linewidth=1)

    # Create the chessboard plot
    plt.imshow(chessboard, cmap='grey', origin='lower')
    plt.title("N-Queens Problem")
    plt.show()

