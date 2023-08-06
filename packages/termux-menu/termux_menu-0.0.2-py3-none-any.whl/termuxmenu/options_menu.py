"""

    Termux Options Menu

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

from termuxmenu import DefaultMenu

class OptionsMenu(DefaultMenu):
    def __init__(self, escape: str,options: list) -> None:
        super().__init__(escape)
        self.options = options