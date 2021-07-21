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
    # get current working directory
    cwd = os.path.dirname(os.path.abspath(__file__))
    # parse yaml to list of lists
    nodes_lst = parse_yaml(cwd, "KS_Tree_V1.yml")
    # create Multi-Directed-Graph
    KS = nx.MultiDiGraph()
    # create edges (and their according nodes)
    for entry in nodes_lst:
        edges_list = interpret_ks_entry(entry)
        KS.add_edges_from(edges_list)
    print(nodes_lst)
    # create graph and write it to file
    # set style entries for the graph
    graph_style = nxv.Style(
        graph={"rankdir": "BT"},
        node=lambda u, d: {"shape": "circle", "fixedsize": "shape", 
                              "width": 1, "fontsize": 10 },
# TODO : Add node function for line split </br> on underscore to achieve 
#        multiple lines in a node          
        edge=lambda u, v, k, d: {"style": "solid", "arrowType": "normal",},
# TODO : Add edge function for the different edge labels        
    )
    # create svg data
    svg_data = nxv.render(KS, graph_style, format="svg")
    # Name of the file, in which the svg data shall be written
    svg_name = "Test.svg"
    # write svg file
    with open(svg_name, "wb") as svgfile:
        svgfile.write(svg_data)
    
    
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
                    edge_tuple = (last_edge, {edge_note_kw: key[edge_note_kw]})
                    # replace last edge
                    edge_list[len(edge_list)-1]
                except IndexError:
                    # skip
                    continue
    return edge_list            


    # ----------- GET_NODE_ATTRIBUTES ---------- #
def get_node_attributes(u=None, v=None):
    """
    """
    node_att_dict = {"shape": "circle", "fixedsize": "shape", 
                              "width": 1, "fontsize": 10 }
    return node_att_dict


    # ----------- GET_EDGE_ATTRIBUTES ---------- #
    
def get_edge_attributes(u=None, v=None, k=None, d=None):
    """Creates dict for attributes for the 
    """
    edge_att_dict = {"style": "solid", "arrowType": "normal",}
    return edge_att_dict

    
if __name__ == "__main__":
    main()
