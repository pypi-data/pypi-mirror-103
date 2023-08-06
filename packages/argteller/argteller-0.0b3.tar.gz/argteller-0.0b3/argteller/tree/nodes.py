from .base_node import BaseNode

class ArgTree(BaseNode):
    
    def __init__(self, name=None, depth=None):
        super(ArgTree, self).__init__(name, depth, node_type='tree')

        self.total_num_missing_args = 0


    def check_params(self):

        missing_params = []

        for param in self.params:

            if param.value is None:

                missing_params.append(param.name)

        return missing_params



    def traverse_tree_tell(self):
        
        ArgTree._traverse_tree_tell(self, False)
        ArgTree._traverse_tree_tell_options(self)

    @staticmethod
    def _traverse_tree_tell_options(self):

        

        if self.has_topics():

            for topic in self.topics:

                ArgTree._traverse_tree_tell_options(topic)

        if self.has_params() and (self.node_type=='topic' or self.node_type=='avail'):

            for param in self.params:

                ArgTree._traverse_tree_tell_options(param)

        if self.has_avails() and self.node_type=='param':

            for avail in self.avails:
                
                ArgTree._traverse_tree_tell_options(avail)

        if self.has_examples() and self.node_type=='param':
            
            for example in self.examples:

                ArgTree._traverse_tree_tell_options(example)

        if self.has_options():

            missing_optional_arguments = []

            for option in self.options:

                if option.value is None:
                    missing_optional_arguments.append(option.name)

            if len(missing_optional_arguments) > 0:

                print('\nOptional argument(s) for {}:\n\n\u25BA {}'.format(self.name, '  '.join(missing_optional_arguments)))


            for option in self.options:

                ArgTree._traverse_tree_tell_options(option)


        #     missing_args = self.missing_required_arguments(OPTIONALS_Expi)
        # if len(missing_args)>0:
        #     print('\nOptional argument(s) for Expi:\n\n\u25BA {}'.format('  '.join(missing_args)))


    @staticmethod
    def _traverse_tree_tell(self, missing=False, fail_not_messaged=True):

        # print()
        # print('-----')
        # print(self.name, self.node_type, fail_not_messaged)
        # print()

        num_missing_args = 0
        
        
        if self.has_topics():  # perhaps change it to checking the type of the node for stronger contract
        
            for topic in self.topics:

                

                print("\u2714 Checking {} requirements...     ".format(
                    topic.name), end="", flush=True)
                
                num_missing_args = ArgTree._traverse_tree_tell(topic, fail_not_messaged = True)

                self.total_num_missing_args += num_missing_args

                if num_missing_args > 0:
                    # print('asdifjaosdjf;oajsdf;ajdf;ajds;lfjads;lfjka;dslfja;sldfk')

                    return 

                else:
                    print('Passed!')

                # if missing args at this topic is greater than 1, return here at this for loop iteration






                
        if self.has_params() and (self.node_type=='topic' or self.node_type=='avail'):

            # print(self.name, self.node_type, '----')

            # check if all the params at this layer are specified

            num_missing_args = 0

            missing_required_arguments = []
            for param in self.params:
                if param.value is None:
                    missing_required_arguments.append(param.name)


            num_missing_args += len(missing_required_arguments)




            if len(missing_required_arguments)>0 and self.node_type=='topic':

                if fail_not_messaged:
                    print("Failed!")
                    fail_not_messaged = False
                    # print('set to False')

                print('\nRequired argument(s):\n\n\u25BA {}'.format('  '.join(missing_required_arguments)))

                # return len(missing_required_arguments)



            elif len(missing_required_arguments)>0 and self.has_param():

                if fail_not_messaged:
                    print("Failed!")
                    fail_not_messaged = False
                    # print('set to False')


                print('\nRequired argument(s) for [{}] {}:\n\n\u25BA {}'.format(
                    self.name, self.param, '  '.join(missing_required_arguments)))

                # return len(missing_required_arguments)


            # elif num_missing_args > 0:

                # print('a;sdifja;sdfj;adsoijf')

            # else:
            #     print("Passed!")
            #     return num_missing_args




            for param in self.params:

                num_missing_args_from_below = 0

                if param.name in missing_required_arguments:
                
                    num_missing_args_from_below = ArgTree._traverse_tree_tell(param, True, fail_not_messaged)

                else:
                    num_missing_args_from_below = ArgTree._traverse_tree_tell(param, False, fail_not_messaged)


                if num_missing_args_from_below is None:

                    num_missing_args_from_below = 0

                num_missing_args += num_missing_args_from_below


            # if self.has_options():

            #     print('HAS OPTION')


            # return num_missing_args


                
        if self.has_avails() and self.node_type=='param':

            available_arguments = []

            num_missing_args = 0
            
            for avail in self.avails:

                available_arguments.append(avail.name)
                
                if self.value == avail.name:

                    # print('AHAHAHA', avail.name, fail_not_messaged)


                    num_missing_args_from_below = ArgTree._traverse_tree_tell(avail, fail_not_messaged=fail_not_messaged)


                    # print('AHAHAH')

                    if num_missing_args_from_below is None:
                        num_missing_args_from_below = 0

                    num_missing_args += num_missing_args_from_below

                    
            if missing:
                print('\nAvailable [ {} ] options:\n\n'
                      '\u25BA {}'.format(self.name, '  '.join(available_arguments)))

            return num_missing_args
                

        if self.has_examples() and self.node_type=='param':
            
            for example in self.examples:

                if missing:
                    print('\nExamples for [ {} ]: {}'.format(self.name, example.name))
                

                ArgTree._traverse_tree_tell(example)

        # print(self.name, self.options)
                
        if self.has_options():
            
            for option in self.options:
                
                # print('{}+{}'.format(' '*option.depth*4, option.name))
                
                ArgTree._traverse_tree_tell(option)



        if num_missing_args is not None:
            return num_missing_args
        else:
            return 0
        
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
        
# class OptionNode(BaseNode):
    
#     def __init__(self, name, depth):
#         super(OptionNode, self).__init__(name, depth, node_type='option')
#         