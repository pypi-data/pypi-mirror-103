from .BaseTest import BaseTest


class TestClass(BaseTest):
    def __init__(self, Class, *args):
        objects = dict(Class.__dict__)
        if '__init__' in objects:
            init = objects.pop('__init__')
        else:
            init=False
        objects = {x:y for x,y in objects.items() if '__' not in x}

        for key in objects:
            setattr(TestClass, key, objects[key])
        if init:
            Class.__init__(self, *args)
                    
    def main(self):
        for key in TestClass.__dict__:
            if 'test' in key:
                if 'output' in TestClass.__dict__[key].__code__.co_varnames:
                    self.print_results(key, TestClass.__dict__[key], 
                                      main=True, output=True)
                else:
                    self.print_results(key, TestClass.__dict__[key], 
                                       main=True, output=False)