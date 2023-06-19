import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

G = nx.Graph()
location_coords = {
        "A": [11.00181192050863, 76.96284240627635],
        "B": [11.001805924614195, 76.96775084781647],
        "C": [11.004862098960513, 76.9643195271492],
        "D": [11.008062321360944, 76.96188813447952],
        "E": [11.012236420342886, 76.96526223421097],
        "F": [11.017950403276413, 76.96662217378616],
        "G": [10.890000000000000, 76.90880000000000],
        "H": [11.010200000000000, 76.95040000000000]
        }
G.add_edge("A", "B", weight=geodesic((11.00181192050863, 76.96284240627635), (11.001805924614195, 76.96775084781647)).km)
G.add_edge("A", "C", weight=geodesic((11.00181192050863, 76.96284240627635), (11.004862098960513, 76.9643195271492)).km)
G.add_edge("B", "C", weight=geodesic((11.001805924614195, 76.96775084781647), (11.004862098960513, 76.9643195271492)).km)
G.add_edge("B", "D", weight=geodesic((11.001805924614195, 76.96775084781647), (11.008062321360944, 76.96188813447952)).km)
G.add_edge("C", "D", weight=geodesic((11.004862098960513, 76.9643195271492), (11.008062321360944, 76.96188813447952)).km)
G.add_edge("C", "E", weight=geodesic((11.004862098960513, 76.9643195271492), (11.012236420342886, 76.96526223421097)).km)
G.add_edge("D", "E", weight=geodesic((11.008062321360944, 76.96188813447952), (11.012236420342886, 76.96526223421097)).km)
G.add_edge("D", "F", weight=geodesic((11.008062321360944, 76.96188813447952), (11.017950403276413, 76.96662217378616)).km)
G.add_edge("E", "F", weight=geodesic((11.012236420342886, 76.96526223421097), (11.017950403276413, 76.96662217378616)).km)
G.add_edge("G", "A", weight=geodesic(location_coords["G"], location_coords["A"]).km)
G.add_edge("H", "A", weight=geodesic(location_coords["H"], location_coords["A"]).km)

pos = nx.spring_layout(G)

node_colors = ['red' if node in ['B', 'D', 'E'] else 'blue' for node in G.nodes()]

nx.draw(G, pos, with_labels=True, node_color=node_colors)

edge_labels = nx.get_edge_attributes(G, 'weight')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.show()
