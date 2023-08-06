"""

    Termux Default Console

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from abc import abstractclassmethod
from termuxmenu.console import Console
from termuxmenu.error.logger import ErrorLog

class DefaultConsole(Console):
    def __init__(self,error_log: ErrorLog) -> None:
        super().__init__()
        self.error_log = error_log
    @abstractclassmethod
    def main(self):
        pass
    def start(self):
        self.main()