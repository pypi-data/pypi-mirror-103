import os
import pickle
import types
from IPython.display import display, Markdown

from .BaseTest import BaseTest
from .TestClass import TestClass


class Tests(BaseTest):
    def __init__(self):
        if not os.path.isdir('.solution_files'):
            os.mkdir('.solution_files')
        self.test_dir = os.path.join('.solution_files', '.test_obj')
        if not os.path.isdir(self.test_dir):
            os.mkdir(self.test_dir)
            
    def save(self, executable, name, assertion=True):
        objects = [assertion, executable]
        path = os.path.join(self.test_dir, name.strip().lower() + '.pkl')
        file = open(path, 'wb')
        pickle.dump(objects, file)
        file.close()

    def run(self, name, *args):
        path = os.path.join(self.test_dir, name.strip().lower() + '.pkl')
        file = open(path, 'rb')
        assertion, executable = pickle.load(file)
        
        if isinstance(executable, types.FunctionType) and assertion:
            self.print_results(name, executable, *args)
            
        elif isinstance(executable, types.FunctionType):
            output = executable(*args)
            markdown = Markdown(f"""**{name}:** {output}""")
            display(markdown)
        
        elif isinstance(executable, type):
            tests = TestClass(executable, *args)
            tests.main()