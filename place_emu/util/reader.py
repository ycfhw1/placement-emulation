# read graphml, calculate delays, return NetworkX graph
# for consistent calculation and rounding of delays across placement algorithms and with emulation!
import networkx as nx
from geopy.distance import vincenty
import numpy as np
import yaml


# read graphml, calculate delays, return undirected(!) NetworkX graph
# if specified (as dict), set additional node and/or edge attributes (e.g., resources)
def read_network(file, node_attr=None, edge_attr=None):
    SPEED_OF_LIGHT = 299792458  # meter per second
    PROPAGATION_FACTOR = 0.77  	# https://en.wikipedia.org/wiki/Propagation_delay

    network = nx.Graph(nx.read_graphml(file, node_type=int))    # don't allow multi graphs (2+ edges between nodes)
    # add 'pop' to node index (eg, 1 --> pop1)
    node_mapping = {n: 'pop{}'.format(n) for n in network.node}
    network = nx.relabel_nodes(network, node_mapping)
    # calculate link delay based on geo positions of nodes
    for e in network.edges(data=True):
        n1=None
        n2=None
        for node in network.nodes(data=True):
            if node[0]==e[0]:
                n1 = network.nodes(data=True)[network.nodes(data=True).index(node)]
            if node[0]==e[1]:
                n2 = network.nodes(data=True)[network.nodes(data=True).index(node)]
        n1_lat, n1_long = n1[1].get('Latitude'), n1[1].get('Longitude')
        n2_lat, n2_long = n2[1].get('Latitude'), n2[1].get('Longitude')
        distance = vincenty((n1_lat, n1_long), (n2_lat, n2_long)).meters  # in meters
        delay = (distance / SPEED_OF_LIGHT * 1000) * PROPAGATION_FACTOR  # in milliseconds
        # round to integer delays! use np.around for consistent behavior in python2 vs 3
        network[e[0]][e[1]]['delay'] = int(np.around(delay))
        network[e[0]][e[1]]['distance'] = int(distance)



    # set node and edge attributes if specified
    # all attributes are set equally for all nodes/edges
    if node_attr:
        for key, value in node_attr.items():
            nx.set_node_attributes(network, value, key)     # different order of args in older NetworkX version!
    if edge_attr:
        for key, value in edge_attr.items():
            nx.set_edge_attributes(network, value, key)

    return network
def read_service(service_file):
        with open(service_file) as f:
            service = yaml.load(f, Loader=yaml.FullLoader)
if __name__ == '__main__':
    read_network("/home/xiaofu/placement-emulation/inputs/networks/Aarnet.graphml")