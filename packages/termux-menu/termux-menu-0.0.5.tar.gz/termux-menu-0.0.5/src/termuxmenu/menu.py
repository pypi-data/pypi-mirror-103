"""

    Termux Menu Interface

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

from abc import abstractclassmethod

class Menu():
    @abstractclassmethod
    def show(self):
        pass