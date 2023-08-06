"""

    Termux Default Error

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from termuxmenu.error import Error

class DefaultError(Error):
    def __init__(self) -> None:
        super().__init__()
        self.errors = list()
    def get(self) -> list:
        return self.errors
    def clear(self):
        self.errors.clear()
    def size(self) -> int:
        return len(self.errors)
    def add(self, string: str):
        return self.errors.append(string)