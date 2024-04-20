import json
import utils
import sys
data = {
    'project_name': 'network',
    'solver': {
        'Ccfl': 0.9,
        'convergence_tolerance': 1.0,
        'cycles': 300,
        'jump': 10
    },
    'write_results': ['P', 'Q', 'A', 'u', 'c'],
    'blood': {
        'mu': 0.004,
        'rho': 1060.0
    },
    'network': [
        
        # Add more network elements as needed
    ]
}
def vvg_to_edgelist():
    # Load the JSON data from the file
    # Get the file path from the command line argument
    file_path = sys.argv[1]
    with open(file_path, 'r') as file:
        data = json.load(file)
    # Extract the graph data
    graph_data = data['graph']

    # Extract nodes and edges
    nodes = graph_data['nodes']
    edges = graph_data['edges']

    # Prepare the node list
    node_list = [node['id'] for node in nodes]

    # Prepare the edge list with the total volume for each edge
    edge_list = [
        (edge['node1'], edge['node2'], sum(v['volume'] for v in edge['skeletonVoxels']))
        for edge in edges
    ]

    # Example of how to display the first 5 edges
    return edge_list
        
def vvg_to_yml():
    global data
    edgelist = vvg_to_edgelist()
    network_head_node = {'E': 125000.0, 'L': 0.01, 'M': 10, 'Rd': 0.0075824225, 'Rp': 0.0082, 'gamma profile': 9, 'label': 'v0', 'sn': edgelist[0][0], 'tn': edgelist[0][1]}
    data['network'].append(network_head_node)
    network_node = {'E': 125000.0, 'L': 0.01, 'R0': 0.005492, 'label': 'v1', 'sn': 2, 'tn': 3}
    for edges in edgelist[1:]:
        network_node['sn'] = edges[0]
        network_node['tn'] = edges[1]
        network_node['R0'] = edges[2]
        data['network'].append(network_node)
    utils.save_yml(data)
    
vvg_to_yml()
