import json
import os
from shisenException import shisenException

class configShisen:
    
    def __init__(self):
        self.__filename = 'data/config.json'
        self.__fp = None
        self.content = None
    
    def __loadFile(self):
        try:
            self.__fp = open(configShisen.getAbsPath(self.__filename),'r')
        except FileNotFoundError:
            raise shisenException("The json file can't be loaded")
        self.content = self.__fp.read()
    
    def load(item):
        cs = configShisen()
        cs.__loadFile()
        cs.__fp.close()
        try:
            content = json.loads(cs.content)
        except ValueError:
            raise shisenException("The json file can't be loaded")
        #print('config shisen load, content:',content)
        
        return content[item]
     
    def loadFile(item):    
        item = configShisen.load(item)
        return configShisen.getAbsPath(item)
        
    def getAbsPath(filename):
        """
        return absolute path from file
        pay attention if this file is moved from basedir
        """
        return os.path.dirname(os.path.realpath(__file__)) + '/'+filename
        #return os.path.dirname(__file__) + '/'+filename