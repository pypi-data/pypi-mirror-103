"""

    Termux Selection Menu

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from abc import abstractclassmethod
from termuxmenu.default_menu import DefaultMenu
from termuxmenu.encapsulate import Encapsulate
from termuxmenu.string_generator import StringGenerator
import math

class SelectionMenu(DefaultMenu):
    MAX_ITEM_IN_PAGE = 5
    BOX_LENGHT = 35
    HEADER_SPACING = 2
    def __init__(self, escape: str,items: list,header: str) -> None:
        super().__init__(escape)
        self.items = items
        self.header = header
        self.max_page = math.ceil(len(self.items) / SelectionMenu.MAX_ITEM_IN_PAGE)
        self.selectionIndex = 0
        self.pageIndex = 1
        self.currentMinSelection = 0
    def generateTitle(self,title: str) -> str:
        return Encapsulate.inlineEncapsulate(title,SelectionMenu.BOX_LENGHT,SelectionMenu.HEADER_SPACING)
    def generateBottom(self) -> str:
        return StringGenerator.generateString('-',SelectionMenu.BOX_LENGHT)
    def previousPage(self):
        if self.currentMinSelection - SelectionMenu.MAX_ITEM_IN_PAGE < 0:
            raise Exception("MIN PAGE")
        self.currentMinSelection -= SelectionMenu.MAX_ITEM_IN_PAGE
        self.selectionIndex = self.currentMinSelection
        self.pageIndex -= 1
    def nextPage(self):
        if self.currentMinSelection + SelectionMenu.MAX_ITEM_IN_PAGE > (len(self.items) - 1):
            raise Exception("MAX PAGE")
        self.currentMinSelection += SelectionMenu.MAX_ITEM_IN_PAGE
        self.selectionIndex = self.currentMinSelection
        self.pageIndex += 1
    def previousItem(self):
        if self.selectionIndex - 1 < self.currentMinSelection:
            raise Exception("MIN ITEM")
        self.selectionIndex -= 1
    def nextItem(self):
        o = None
        try:
            o = self.items[self.selectionIndex + 1]
        except IndexError:
            pass
        if self.selectionIndex + 1 > (self.currentMinSelection + SelectionMenu.MAX_ITEM_IN_PAGE - 1):
            raise Exception("MAX ITEM")
        if o != None:
            self.selectionIndex += 1
    def select(self) -> object:
        return self.items[self.selectionIndex]
    @abstractclassmethod
    def showItem(self,o: object,selected: bool):
        pass
    def showPage(self):
        print("\n" + self.escapeCharacters + self.generateTitle("%s %d" % ("Page", self.pageIndex)),end="")
        print(self.header,end="")
        i = self.currentMinSelection
        while i < (self.currentMinSelection + SelectionMenu.MAX_ITEM_IN_PAGE):
            o = None
            try:
                o = self.items[i]
            except IndexError:
                pass
            if o != None:
                self.showItem(o,i == self.selectionIndex)
            i += 1
        print("\n%s\n" % (self.escapeCharacters + self.generateBottom(
            "%s %d/%d" % ("Page",self.pageIndex,self.max_page)
        )),end="")
    def update(self):
        self.showPage()
    def show(self):
        self.update()
    @staticmethod
    def setMaxItemInPage(max: int):
        SelectionMenu.MAX_ITEM_IN_PAGE = max