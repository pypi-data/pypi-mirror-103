"""

    Termux Command Parser

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from abc import abstractclassmethod

class CommandParser():

    @abstractclassmethod
    def parseBlock(self,command: str) -> int:
        pass

    @staticmethod
    def parseCommand(command: str,parser) -> int:
        return CommandParser.parseBlock(parser,command)