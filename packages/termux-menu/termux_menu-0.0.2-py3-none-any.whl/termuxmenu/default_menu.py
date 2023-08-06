"""

    Termux Default Menu

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

from abc import abstractclassmethod
from termuxmenu import Menu

class DefaultMenu(Menu):
    def __init__(self,escape: str) -> None:
        super().__init__()
        self.escapeCharacters = escape
    @abstractclassmethod
    def update(self):
        pass
    def show(self):
        self.update()