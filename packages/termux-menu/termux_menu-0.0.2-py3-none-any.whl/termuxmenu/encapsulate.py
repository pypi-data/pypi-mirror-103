"""

    Termux Encapsulate

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

import math
from termuxmenu import StringGenerator

class Encapsulate():
    @staticmethod
    def encapsulateString(message: str,escape: str,space: str = None):
        if space == None:
            Encapsulate.encapsulate(message=message,character='-',escape=escape,lenght=len(message))
        else:
            Encapsulate.encapsulate(message=message,character=space,escape=escape,lenght=len(message))
    @staticmethod
    def inlineEncapsulate(message: str,lenght: int,spacing: int) -> str:
        firstStage = math.ceil(((lenght - len(message)) / 2) - math.ceil(spacing / 2))
        secondStage = math.floor(((lenght - len(message)) / 2) - math.floor(spacing / 2))
        firstSpacing = math.ceil(spacing / 2)
        secondSpacing = math.floor(spacing / 2)
        return (
            StringGenerator.generateString(character="-",lenght=firstStage) 
            + StringGenerator.generateString(character=" ",lenght=firstSpacing)
            + message
            + StringGenerator.generateString(character=" ",lenght=secondSpacing)
            + StringGenerator.generateString(character="-",lenght=secondStage)
        )
    @staticmethod
    def inlineCenter(message: str,character: str,lenght: int) -> str:
        return '{:{}^{}}'.format(message,character,lenght)
    @staticmethod
    def encapsulate(message: str,character: str,escape: str,lenght: int):
        firstPhaseCheck = False
        secondPhaseCHeck = False
        stringCheck = False
        for x in range((lenght + 1) * 3):
            if not firstPhaseCheck:
                if x == 0:
                    print("\n" + escape,end="")
                print(character, end="")
                if x == (lenght + 1):
                    firstPhaseCheck = True
            elif not secondPhaseCHeck:
                if x == (lenght + 2):
                    print("\n" + escape + "|", end="")
                elif x == ((lenght * 2) + 1):
                    print("|", end="")
                    secondPhaseCHeck = True
                elif not stringCheck:
                    print(message,end="")
                    stringCheck = True
            else:
                if x == ((lenght * 2) + 2):
                    print("\n" + escape + character,end="")
                print(character,end="")