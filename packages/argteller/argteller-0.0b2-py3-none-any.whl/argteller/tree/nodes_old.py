from .base_node import BaseNode

class ArgTree(BaseNode):
    
    def __init__(self, name=None, depth=None):
        super(ArgTree, self).__init__(name, depth, node_type='tree')


    def check_params(self):

        missing_params = []

        for param in self.params:

            if param.value is None:

                missing_params.append(param.name)

        return missing_params



    def traverse_tree_tell(self):
        
        ArgTree._traverse_tree_tell(self)
    
    @staticmethod
    def _traverse_tree_tell(self):
        
        if self.has_topics():  # perhaps change it to checking the type of the node for stronger contract
        
            for topic in self.topics:

                print("\u2714 Checking {} requirements...     ".format(
                    topic.name), end="", flush=True)
                
                num_missing_args = ArgTree._traverse_tree_tell(topic)

                

                if num_missing_args > 0:
                    # print('asdifjaosdjf;oajsdf;ajdf;ajds;lfjads;lfjka;dslfja;sldfk')

                    return 

                else:
                    print('HERE')

                # if missing args at this topic is greater than 1, return here at this for loop iteration





                
        if self.has_params():

            # print(self.name, self.node_type, '----')

            # check if all the params at this layer are specified

            num_missing_args = 0

            missing_required_arguments = []
            for param in self.params:
                if param.value is None:
                    missing_required_arguments.append(param.name)


            num_missing_args += len(missing_required_arguments)



            






            if len(missing_required_arguments)>0 and self.node_type=='topic':
                # print("Failed!")
                print('\nRequired argument(s):\n\n\u25BA {}'.format('  '.join(missing_required_arguments)))

                # return len(missing_required_arguments)


            





            if len(missing_required_arguments)>0 and self.has_param():


                print('\nRequired argument(s) for [{}] {}:\n\n\u25BA {}'.format(
                    self.name, self.param, '  '.join(missing_required_arguments)))

                # return len(missing_required_arguments)


            # elif num_missing_args > 0:

                # print('a;sdifja;sdfj;adsoijf')

            else:
                print("Passed!")
                return num_missing_args




            for param in self.params:
                
                num_missing_args_from_below = ArgTree._traverse_tree_tell(param)

                if num_missing_args_from_below is None:

                    num_missing_args_from_below = 0
                    # print(self.name, param.name, 'has none')

                

                num_missing_args += num_missing_args_from_below

                # print(num_missing_args, num_missing_args_from_below, '======|||')



            # for param in self.params:
                
            #     num_missing_args_from_below = ArgTree._traverse_tree_tell(param)

            #     if num_missing_args_from_below is None:

            #         num_missing_args_from_below = 0
            #         print(self.name, param.name, 'has none')

                

            #     num_missing_args += num_missing_args_from_below

            #     print(num_missing_args, num_missing_args_from_below, '======|||')
                

            return num_missing_args





                
        if self.has_avails():

            available_arguments = []

            num_missing_args = 0
            
            for avail in self.avails:

                available_arguments.append(avail.name)
                
                if self.value == avail.name:



                    num_missing_args_from_below = ArgTree._traverse_tree_tell(avail)

                    if num_missing_args_from_below is None:
                        num_missing_args_from_below = 0

                    # num_missing_args += num_missing_args_from_below

                    

            print('\nAvailable [ {} ] options:\n\n'
                  '\u25BA {}'.format(self.name, '  '.join(available_arguments)))

            return num_missing_args
                
        if self.has_examples():

            print('has examples')
            
            for example in self.examples:
                
                # print('{}=={}'.format(' '*example.depth*4, example.name))
                
                ArgTree._traverse_tree_tell(example)
                
        if self.has_options():

            print('has has_options')
            
            
            for option in self.options:
                
                # print('{}+{}'.format(' '*option.depth*4, option.name))
                
                ArgTree._traverse_tree_tell(option)


        
class TopicNode(BaseNode):
    
    def __init__(self, name, depth):
        super(TopicNode, self).__init__(name, depth, node_type='topic')
        
class ParamNode(BaseNode):
    
    def __init__(self, name, depth):
        super(ParamNode, self).__init__(name, depth, node_type='param')


    def set_value(self, value):

        self.value = value
        
class AvailNode(BaseNode):
    
    def __init__(self, name, depth):
        super(AvailNode, self).__init__(name, depth, node_type='avail')

        self.param = None

    def set_param(self, value):

        self.param = value

    def has_param(self):

        return self.param is not None
        
class ExampleNode(BaseNode):
    
    def __init__(self, name, depth):
        super(ExampleNode, self).__init__(name, depth, node_type='example')
        
class OptionNode(BaseNode):
    
    def __init__(self, name, depth):
        super(OptionNode, self).__init__(name, depth, node_type='option')
        