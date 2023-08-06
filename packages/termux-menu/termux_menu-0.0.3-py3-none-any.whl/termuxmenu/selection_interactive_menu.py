"""

    Termux Selection Menu

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from termuxmenu.default_interactive_menu import DefaultInteractiveMenu
from termuxmenu.default_menu import DefaultMenu
from termuxmenu.logger import ErrorLog
from termuxmenu.parser import CommandParser
from termuxmenu.selection_menu import SelectionMenu

class SelectionInteractiveMenu(DefaultInteractiveMenu):
    def __init__(self, error_log: ErrorLog, option_menu: DefaultMenu, command_parser: CommandParser, shell: str,selection_menu: SelectionMenu) -> None:
        super().__init__(error_log, option_menu, command_parser, shell)
        self.selection_menu = selection_menu
    def loopBlock(self):
        self.selection_menu.show()
        self.option_menu.show()