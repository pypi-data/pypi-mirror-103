from .nodes import ArgTree
from .nodes import TopicNode
from .nodes import ParamNode
from .nodes import AvailNode
from .nodes import ExampleNode
# from .nodes import OptionNode

import re

class TreeParser():


    def __init__(self):

        self.topic_nodes_dict = dict()
        self.param_nodes_dict = dict()
        self.option_nodes_dict = dict()

        self.tree = None

    def parse_tree(self, string):
        
        current_topic = None
        current_param = None

        self.tree = ArgTree(name='tree', depth=-2)

        node_count = 0
        current_pos_dict = {}

        for line in string.splitlines():

            num_white_spaces = len(line) - len(line.lstrip(' '))
            depth = int(num_white_spaces/4)

            line = line.strip()

            if line=='':
                continue
            if line[0] == '-':
                node_type = 'param'
            elif line[0] == '+':
                node_type = 'option'
            elif line[0:2] == '==':
                node_type = 'example'
            elif line[0] == '=':
                node_type = 'avail'
            elif line[0:2] == 'if':
                pass
            else:
                node_type = 'topic'


            name = re.sub('^[\s=+-]+', '', line)

            if node_type=='topic':

                if name != current_topic:
                    current_topic = name
                    topic_node = TopicNode(name, depth=-1)
                    self.tree.add_topic(topic_node)

                    current_pos_dict[-1] = topic_node

                    self.topic_nodes_dict[name] = topic_node

            elif node_type=='param':

                current_param = name

                prev_node = current_pos_dict[depth-1]

                current_node = ParamNode(name, depth)
                prev_node.add_param(current_node)

                current_pos_dict[depth] = current_node


                self.param_nodes_dict[name] = current_node


            elif node_type=='avail':

                prev_node = current_pos_dict[depth-1]

                current_node = AvailNode(name, depth)
                current_node.set_param(current_param)

                prev_node.add_avail(current_node)

                current_pos_dict[depth] = current_node

            elif node_type=='example':

                prev_node = current_pos_dict[depth-1]

                current_node = ExampleNode(name, depth)
                prev_node.add_example(current_node)

                current_pos_dict[depth] = current_node

            elif node_type=='option':

                prev_node = current_pos_dict[depth-1]

                current_node = ParamNode(name, depth)
                prev_node.add_option(current_node)

                current_pos_dict[depth] = current_node

                self.option_nodes_dict[name] = current_node
                
        return self.tree


