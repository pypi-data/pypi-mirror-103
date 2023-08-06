from .tree.tree_parser import TreeParser

import inspect
import os

def initializer_error_handler(func):
    def wrapped_init(*args, **kwargs):
        
        try:
            func(*args, **kwargs)
            
        except Exception as e:
            
            sub_str = 'takes 1 positional argument but'
            
            if sub_str in str(e):
                raise Exception('Argteller disallows positional arguments. Please only use keyword arguments.')
                
            else:
                raise type(e)(str(e))
            

    return wrapped_init


class ArgtellerClassDecorator():
    
    def __init__(self, map_str, override=False):
        
        if os.path.exists(map_str):
            with open(map_str) as f:
                map_str = f.read()
                
        self.override = override
        self.tree_parser = TreeParser()
        self.arg_tree = self.tree_parser.parse_tree(map_str)
        
    def __call__(self, cls):
        
        class Wrapped(cls):
            
            @initializer_error_handler
            def __init__(cls_self, **kwargs):
                
                tmp_cls_obj = cls.__new__(cls)
                names, _, _, defaults, _, _, _ = inspect.getfullargspec(tmp_cls_obj.__init__)
                
                if defaults is not None:
                    for name, default in zip(reversed(names), reversed(defaults)):

                        if not hasattr(cls_self, name):
                            setattr(cls_self, name, default)
                
                for k, v in kwargs.items():
                    
                    if k in self.tree_parser.param_nodes_dict:
                        self.tree_parser.param_nodes_dict[k].set_value(v)

                for k, v in self.tree_parser.param_nodes_dict.items():
                    
                    if self.override:
                        setattr(cls_self, k, v.value)
                        
                    else:
                        
                        if not hasattr(cls_self, k):
                            setattr(cls_self, k, v.value)

                # for optional arguments
                for k, v in kwargs.items():
                    
                    if k in self.tree_parser.option_nodes_dict:
                        self.tree_parser.option_nodes_dict[k].set_value(v)

                for k, v in self.tree_parser.option_nodes_dict.items():
                    
                    if self.override:
                        setattr(cls_self, k, v.value)
                        
                    else:
                        
                        if not hasattr(cls_self, k):
                            setattr(cls_self, k, v.value)

                            
                
                
                self.arg_tree.traverse_tree_tell()

                if self.arg_tree.total_num_missing_args > 0:
                    
                    return
                

                tmp_kwargs = {k: v for k, v in kwargs.items() if k in names[1:]}
                super(Wrapped, cls_self).__init__(**tmp_kwargs)
                
            cls.injected_method = self.injected_method
            
        return Wrapped
            
    def injected_method(self, a):
        return(a)
        
# @ArgtellerClassDecorator(map_str=string)
# class A():
    
#     def __init__(self, a=None):
#         self.a = a
#         pass
    
