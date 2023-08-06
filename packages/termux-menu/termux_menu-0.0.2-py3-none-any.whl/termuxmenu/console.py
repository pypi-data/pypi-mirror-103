"""

    Termux Console

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from abc import abstractclassmethod

class Console():
    @abstractclassmethod
    def start(self):
        pass