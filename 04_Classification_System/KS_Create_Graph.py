# -*- coding: utf-8 -*-
"""
Created on Mon Jul 19 15:55:10 2021

@author: Jonathan Rockstroh
"""

import yaml
import os
import networkx as nx
import nxv

def main():
    # Names of the yml files, which contain the Graphs of the KS
    KS_file_names = ["KS_Tree_Main.yml", "KS_Tree_Math_Representation.yml",
                          "KS_Tree_Model_Attributes.yml", 
                          "KS_Tree_Usage_Area.yml"]
    # File Names for drawn graphs
    drawn_file_names = [file_name[:-4] for file_name in KS_file_names]

    # create Multi-Directed-Graphs
    KS_graph_list = [nx.MultiDiGraph() for i in KS_file_names]
    # keyword of the yml file for the Edge name
    edge_name_kw = "Edge_Name"
    # create list of graphs, files, drawn file names
    KS_lists = []
    for i in range(len(KS_file_names)):
        sublist = [KS_graph_list[i], KS_file_names[i], 
                   drawn_file_names[i]]
        KS_lists.append(sublist)
    # fill Graphs
    for sublist in KS_lists:
        add_nodes_from_yml(sublist[0], sublist[1], edge_name_kw)

    # draw graph and write it to file
    # define style entries for the graph   
    graph_style = nxv.Style(
        graph={"rankdir": "BT"},
        node=lambda u, d: {"shape": "circle", "fixedsize": "shape", 
                              "width": 1, "fontsize": 10, 
                              "label": get_node_label(u, d) },
         
        edge=lambda u, v, k, d:{"style": "solid", "arrowType": "normal", 
                     "label": get_edge_label(u, v, d, 
                                             relation_kw=edge_name_kw),}       
    )
    # write files   
    for sublist in KS_lists:
        write_graph_to_file(sublist[0], graph_style, sublist[2])
    
    # create and print complete graph of the KS
    full_KS_graph = nx.MultiDiGraph()
    for graph in KS_graph_list:
        full_KS_graph.add_nodes_from(graph.nodes(data=True))
        full_KS_graph.add_edges_from(graph.edges(data=True))
    
    print("Number of Nodes: ", len(full_KS_graph.nodes()))
    full_KS_file_name = "Full_KS"
    write_graph_to_file(full_KS_graph, graph_style, full_KS_file_name)
    
    # write small, grey, unlabeled graph to file
    style = nxv.Style(
    graph={"rankdir": "BT", "nodesep": 0.05},
    node=lambda u, d: {
        "shape": "point",
        "fixedsize": True,
        "width": 0.1,
        "fontsize": 10,
    },
    edge=lambda u, v, k, d: {"style": "solid", "arrowhead": "none", "color": "#959595ff"},
    )
    file_name = "KS_grey"
    write_graph_to_file(full_KS_graph, style, file_name)
    
    return
    
    
    # ----------- PARSE_YAML ---------- #

def parse_yaml(path, file_name):
    """ Parses yaml file of the Klassification_System to a list of lists, where
    each sublist has the information for one single Node
    
    :param path: path to the folder of the yaml file
    :param file_name: full file name: file_name.extension
    
    :return: nested list, each sublist has the attributes of one Node of the KS
    """
    # change current directory 
    os.chdir(path)
    # load yaml file and read it
    with open(file_name, "r") as yml_file:
        yml_raw = yml_file.read()
        # parse read yml file into dict
    yml_parsed = yaml.safe_load(yml_raw)
    # get list of the keys of the created dict
    key_list = yml_parsed.keys()
    # initialize Variable 
    node_list = []
    # fill list - every entry is list with information for one single Node
    for key in key_list:
        new_entry = [key] + yml_parsed[key] 
        node_list.append(new_entry)
        
    return node_list


    # ----------- INTERPRET_KS_ENTRY ---------- #
    
def interpret_ks_entry(entry, pre_node_kw="Pre_Node", 
                       edge_note_kw="Edge_Note"):
    """Interpreter for an Entry of the KS. Currently only recognizes Edges.
    
    :param entry: parsed entry of one Node of the KS
    :param pre_node_kw: keyword for Attribute: Edge in the KS file
    :param edge_note_kw: keyword for Attrute: Edge_Note (weight) in KS file
    
    :return: list of tuples, which accord to the given entry
    """
    # initialize edge_list
    edge_list = []
    # get Name of the current KS Node
    current_node_name = entry[0]
    # iterate over the attributes of the KS Node 
    for key in entry:
        if isinstance(key, dict):
            key_list = key.keys()
            # Case: Attribute is Edge
            if len(key_list) == 1 and pre_node_kw in key_list:
                # Case: pre_node value is None or named "None"
                if key[pre_node_kw] == "None" or key[pre_node_kw] is None:
                    # skip this Node
                    continue
                # define edge (starting node, ending node)
                edge_tuple = (current_node_name, key[pre_node_kw])
                edge_list.append(edge_tuple)
            # Case: Attribute is Edge_Note
            if len(key_list) == 1 and edge_note_kw in key_list:
                last_edge = ()
                try: # to get last edge entry
                    last_edge = edge_list[len(edge_list)-1]
                    # define new tuple, add attribute "edge_note" to edge    
                    edge_tuple = (*last_edge, {edge_note_kw: key[edge_note_kw]})
                    # replace last edge
                    edge_list[len(edge_list)-1] = edge_tuple
                except IndexError:
                    # skip
                    continue
    return edge_list            


    # ----------- GET_NODE_ATTRIBUTES ---------- #
    
def get_node_label(u=None, d=None):
    """Splits the Node Names at underscores in several line 
    to make it better fitting into the circles in the drawn graph
    :param u: node of the Graph
    :param d: attribute dict of the Graph
    
    :return: string, node_label
    """
    node_label = d["label"]

    return node_label


    # ----------- GET_EDGE_ATTRIBUTES ---------- #
    
def get_edge_label(u=None, v=None, d=None, relation_kw="Relation"):
    """Creates label for the edges
    :param (u, v): edge of the Graph
    :param d: attribute dict of the edge
    
    :return: attribute dict for the graph drawing
    """
    relation_label = None
    # get label for the relation from edge attributes
    if d is not None:
        try:
            relation_label = d[relation_kw]
        except KeyError:
            relation_label = ""
    else:
        relation_label = ""
    return relation_label


    # ----------- write_graph_to_file ---------- #
    
def write_graph_to_file(graph, graph_style, file_name):    
    """creates a svg picture of a networkx graph with help of the nxv package
    :param graph: Networkx Graph, which shall be drawn
    :param graph_style: nxv.Style object, which defines the Style of the 
                        elements of the drawn graph
    :param file_name: string, name which the file shall get
    
    :return: None
    """
    # create svg data
    svg_data = nxv.render(graph, graph_style, format="svg")
    # Name of the file, in which the svg data shall be written
    svg_name = file_name + ".svg"
    # write svg file
    with open(svg_name, "wb") as svgfile:
        svgfile.write(svg_data)
    return
    

    # ----------- yml_to_graph ---------- #
    
def add_nodes_from_yml(graph, graph_file_name, relation_kw):
    """Takes a yml file, which contains the Information of a graph, reads it 
    and adds them to a given networkx graph
    :param graph: Networkx Graph
    :param graph_file_name: Name of the yaml file, which contains the graph
    
    :return: None
    """
    # get current working directory
    cwd = os.path.dirname(os.path.abspath(__file__))
    # parse yaml to list of lists
    nodes_lst = parse_yaml(cwd, graph_file_name)
    # create edges (and their according nodes)
    for entry in nodes_lst:
        edges_list = interpret_ks_entry(entry, edge_note_kw=relation_kw)
        graph.add_edges_from(edges_list)
    # add label attribute to every node
    for node in graph.nodes:
        # get node name and convert to string
        node_label = str(node)
        # remove leading and trailing whitespaces
        node_label.strip()
        # replace underscore with underscore+\n
        node_label = node_label.replace("_", "_\n")
        print("Label: ", node_label)
        # add label as node attribute
        graph.nodes[node]["label"] = node_label
    return


if __name__ == "__main__":
    main()
