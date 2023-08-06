"""

    Termux Error Log

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from termuxmenu.menu import Menu
from termuxmenu.default_menu import DefaultMenu
from termuxmenu.logger import ErrorLog
from termuxmenu.parser import CommandParser
from abc import abstractclassmethod

class DefaultInteractiveMenu(Menu):
    def __init__(self,error_log: ErrorLog,option_menu: DefaultMenu,command_parser: CommandParser,shell: str) -> None:
        super().__init__()
        self.error_log = error_log
        self.option_menu = option_menu
        self.command_parser = command_parser
        self.shell = shell
        self.exit = False
    @abstractclassmethod
    def outsideLoop(self):
        pass
    @abstractclassmethod
    def loopBlock(self):
        pass
    def loop(self):
        self.outsideLoop()
        while not self.exit:
            self.loopBlock()
            try:
                print(self.shell,end="")
                if CommandParser.parseCommand(input(),self.command_parser) == -1:
                    self.exit = True
            except Exception as error:
                self.error_log.add(error)
    def update(self):
        self.loop()
    def show(self):
        self.update()