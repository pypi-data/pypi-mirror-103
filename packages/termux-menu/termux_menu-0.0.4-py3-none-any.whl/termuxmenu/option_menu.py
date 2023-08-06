"""

    Termux Option Menu

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

from termuxmenu.options_menu import OptionsMenu
from termuxmenu.encapsulate import Encapsulate
from termuxmenu.string_generator import StringGenerator

class OptionMenu(OptionsMenu):

    TITLE_LENGHT = 35
    SPACING = 2

    def __init__(self, escape: str, options: list,title: str,format: str,number: int = 1,enable_numbers: bool = True) -> None:
        super().__init__(escape, options)
        self.title = title
        self.format = format
        self.number = number
        self.enable_numbers = enable_numbers
    def generateTitle(self) -> str:
        return Encapsulate.inlineEncapsulate(self.title,OptionMenu.TITLE_LENGHT,OptionMenu.SPACING)
    def generateBottom(self) -> str:
        return StringGenerator.generateString('-',OptionMenu.TITLE_LENGHT)
    def showOptions(self):
        n = self.number
        for option in self.options:
            if self.enable_numbers:
                print(("\n" + self.escapeCharacters + "%-5d" + self.format) % (n,option),end="")
            else:
                print(("\n" + self.escapeCharacters + self.format) % option,end="")
            n += 1
    @staticmethod
    def setTitleLenght(lenght: int):
        OptionMenu.TITLE_LENGHT = lenght
    @staticmethod
    def setSpacing(spacing: int):
        OptionMenu.SPACING = spacing
    def update(self):
        print("\n" + self.escapeCharacters + "%s" % self.generateTitle(),end="")
        self.showOptions()
        print("\n" + self.escapeCharacters + "%s\n" % self.generateBottom(),end="")