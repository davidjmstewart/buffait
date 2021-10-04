# buffait.py
from enum import Enum
from typing import Union, List
import re
from functools import reduce

'''
    BUFFAIT
    
    Limitations:
        Single closure
        Does not support buffer resizing (e.g. through realloc)
        Does not understand commented out buffer declarations
        
'''
class NodeType(Enum):
    BUFFER = 1
    INT    = 2

buffer_regex = re.compile(r'[a-z]* (?P<name>[\w\d]*)\[(?P<size>[\w_]*)\].*')
integer_define_regex = re.compile(r'#define (?P<name>\w+) (?P<value>\d+)') # for #define declarations
integer_declaration_regex = re.compile(
    r'int (?P<name>\w+)[ =]*(?P<value>\d+);.*')  # for int declarations

# Node in the graph of buffer objects and types used in the creation/mutation/access
# of buffers
class Node:

    node_type: NodeType = NodeType.BUFFER
    name: str = ""

    def __init__(self, type: NodeType, name: str):
        self.node_type = type    
        self.name = name

class BufferNode(Node):
    # TODO: support a list of size_dependencies that could be values or integer nodes e.g. for declarations like char *buf[BUFF_SIZE - 10]
            # we would require 2 size dependencies: BUFF_SIZE (an integer Node) and -10
    size: Union[str, int, 'IntegerNode'] = -1

    def __init__(self, size: Union[str, int, 'IntegerNode'], name: str):
        super().__init__(NodeType.BUFFER, name)
        self.size = int(size) if size.isdigit() else size  

    # if the size member is an IntegerNode, follow the nodes until the actual
    # value is reached
    def get_actual_size() -> int:
        size = 0

        pass

class IntegerNode(Node):
    value: int = 0

    def __init__(self, value: Union[int, 'IntegerNode'], name: str):
        super().__init__(NodeType.INT, name)
        self.value = value   

# given a line of source code, create Node objects for any declared integers or buffers on the line of code
def make_nodes_from_line(line: str) -> List[Node]:
    # use all of our regex types on this source code line to determine all possible node types included on this line

    integer_define_nodes = list(map(lambda m: IntegerNode(
        m.group('value'), m.group('name')), integer_define_regex.finditer(line)))

    integer_declaration_nodes = list(map(lambda m: IntegerNode(
        m.group('value'), m.group('name')), integer_declaration_regex.finditer(line)))

    buffer_nodes = list(map(lambda m: BufferNode(m.group('size'), m.group('name')), buffer_regex.finditer(line)))

    nodes = [integer_define_nodes, integer_declaration_nodes, buffer_nodes]

    # flat map the return value
    res = [inner_nodes for outer_list in nodes for inner_nodes in outer_list]
    # strip out empty lists 
    return list(filter(None, res))
    



# currently this is identical in functionality to the next_integer_nodes function
# as we are simply creating a set of nodes at this stage
def next_buffer_nodes(current_nodes: List[BufferNode], new_nodes: List[BufferNode]) -> List[BufferNode]:
    if not new_nodes:
        return current_nodes
    l = list(
        filter(
            lambda e: e not in current_nodes, new_nodes
        )
    )
    current_nodes = current_nodes + l if len(l) > 0 else current_nodes
    return current_nodes

# currently this is identical in functionality to the next_buffer_nodes function
# as we are simply creating a set of nodes at this stage
def next_integer_nodes(current_nodes: List[IntegerNode], new_nodes: List[IntegerNode]) -> List[IntegerNode]:
    if not new_nodes:
        return current_nodes
    l = list(
        filter(
            lambda e: e not in current_nodes, new_nodes
        )
    )
    current_nodes = current_nodes + l if len(l) > 0 else current_nodes
    return current_nodes


# def update_graph_list(current_graphs: List[BufferNode], non_buffer_nodes: List[Node], new_nodes: List[Node]) -> List[BufferNode]:

#     pass

def update_graph_list(buffer_nodes: List[BufferNode], non_buffer_nodes: List[Node]) -> List[BufferNode]:

    pass

def node_by_var_name(name: str, all_nodes: List[Node]) -> Node:
    N = list(filter(lambda x: x.name == name, all_nodes))
    res = N[0] if N else []
    return res

def connect_chain(A: Node, all_nodes: List[Node]):
    if type(A) == BufferNode:
        if type(A.size) != int:
            new_size = node_by_var_name(A.size, all_nodes)
            A.size = new_size

            pass

def connect_nodes(buffer_nodes: List[BufferNode], non_buffer_nodes: List[Node]) -> List[BufferNode]:
    for buffer in buffer_nodes:
        connect_chain(buffer, buffer_nodes + non_buffer_nodes)
        
    
def make_graph(source_file: str) -> Node:
    # for the sake of demonstration, we assume source_file will always be a valid path to C source code
    # read every line of source code from the file pointed to by source_file
    f = open(source_file, "r")          
    source_lines = f.readlines() # N.B. Parsing a C file line-by-line will be error prone as there are no semantic newlines in C (instructions are separated with ; not a newline)
    
    buffer_nodes = []
    non_buffer_nodes = [] # nodes that are relevant to buffer analysis (e.g. integers) but are not buffers themselves
    buffer_graphs = []    # A list of graphs of buffer allocations found in the program. These are the graphs that will be used to determine if
                          # operations could lead to a buffer overflow. 

    for line in source_lines:
        #
        nodes_in_line = make_nodes_from_line(line) # get nodes relating to buffer and variable declarations
        integer_nodes_in_line = list(
            filter(lambda x: type(x) is IntegerNode, nodes_in_line))
        buffer_nodes_in_line = list(
            filter(lambda x: type(x) is BufferNode, nodes_in_line))



        buffer_nodes = next_buffer_nodes(
            buffer_nodes, buffer_nodes_in_line)

        non_buffer_nodes = next_integer_nodes(
            non_buffer_nodes, integer_nodes_in_line)

    # buffer_graphs = update_graph_list( buffer_graphs, non_buffer_nodes, nodes_in_line)  # buffer_graphs represents the snapshot of buffer allocations up to the current iteration point
                                                             # Now we want to obtain the next state by giving our update function the current state, and the nodes we just found
                                                             # so it can determine if a new graph needs to be added to the list, or if an existing list element needs to be changed
        
    connect_nodes(buffer_nodes, non_buffer_nodes)
                                                          


if __name__ == '__main__':
    single_buffer_graph = make_graph('./tests/single_buffer.c')
