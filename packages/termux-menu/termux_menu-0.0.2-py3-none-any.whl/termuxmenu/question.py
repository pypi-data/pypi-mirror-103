"""

    Termux Question

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

import re
from termuxmenu import ValidationException

class Question():
    shell = "> "
    @staticmethod
    def ask(message: str,escape: str) -> str:
        print(("\n" + escape + "{}").format(message),end="")
        return input(("\n" + escape + "{}").format(Question.shell))
    @staticmethod
    def ask(message: str,escape: str,pattern: str) -> str:
        print(("\n" + escape + "{}").format(message),end="")
        answer = input(("\n" + escape + "{}").format(Question.shell))
        if not re.match(pattern=pattern,string=answer):
            raise ValidationException("Validation failed, doesn't match with: {}".format(pattern))
        return answer
