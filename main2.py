import networkx as nx
import matplotlib.pyplot as plt

class Circuit:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node)

    def add_resistance(self, node1, node2, resistance):
        self.graph.add_edge(node1, node2, weight=resistance)

    def series_resistance(self, resistances):
        return sum(resistances)

    def parallel_resistance(self, resistances):
        reciprocal_sum = sum(1 / r for r in resistances)
        return 1 / reciprocal_sum if reciprocal_sum != 0 else float('inf')

    def simplify_parallel(self):
        while True:
            nodes_to_contract = []
            for node in self.graph.nodes:
                neighbors = list(self.graph.neighbors(node))
                if len(neighbors) == 2:
                    weight1 = self.graph[node][neighbors[0]]['weight']
                    weight2 = self.graph[node][neighbors[1]]['weight']
                    parallel_res = self.parallel_resistance([weight1, weight2])
                    nodes_to_contract.append((neighbors[0], neighbors[1], parallel_res, node))

            if not nodes_to_contract:
                break

            for n1, n2, res, intermediate in nodes_to_contract:
                self.graph.add_edge(n1, n2, weight=res)
                self.graph.remove_node(intermediate)

    def equivalent_resistance(self):
        self.simplify_parallel()

        total_resistance = 0
        for edge in self.graph.edges(data=True):
            total_resistance += edge[2]['weight']

        return total_resistance

    def display_graph(self):
        pos = nx.spring_layout(self.graph)
        weights = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw(self.graph, pos, with_labels=True, node_color='skyblue', node_size=700, edge_color='gray')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=weights)
        plt.show()

# Ejemplo de uso
circuit = Circuit()
circuit.add_node('A')
circuit.add_node('B')
circuit.add_node('C')
circuit.add_node('D')

# Añadir resistencias
circuit.add_resistance('A', 'B', 2)  # R1
circuit.add_resistance('B', 'C', 5)  # R2
circuit.add_resistance('B', 'D', 5)  # R3
circuit.add_resistance('C', 'D', 0)  # Conexión entre R2 y R3

# Calcular resistencia equivalente total
R_total = circuit.equivalent_resistance()
print("Resistencia equivalente total:", R_total)

# Mostrar el grafo
circuit.display_graph()
