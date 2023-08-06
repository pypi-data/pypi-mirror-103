"""

    Termux Inline Menu

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

from termuxmenu import OptionsMenu

class InlineMenu(OptionsMenu):
    MAX_ITEMS_PER_ROW = 5
    def __init__(self, escape: str, options: list,number: int) -> None:
        super().__init__(escape, options)
        self.number = number
    def showOptions(self) -> str:
        n = self.number
        c = 1
        output = ""
        for option in self.options:
            if c > InlineMenu.MAX_ITEMS_PER_ROW:
                output += "\n"
                c = 1
            if c == 1:
                output += self.escapeCharacters
            output += n + " " + option + " "
            c += 1
            n += 1
        return output
    def update(self):
        print("\n%s\n" % self.showOptions(),end="")