"""

    Termux Error Log

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from termuxmenu import DefaultError, OptionMenu

class ErrorLog(DefaultError):
    def show(self,escape: str,title: str):
        self.menu = OptionMenu(options=self.get(),escape=escape,title=title,format="%s")
        self.menu.show()