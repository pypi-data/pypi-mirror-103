"""

    Termux Error

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from abc import abstractclassmethod

class Error():
    @abstractclassmethod
    def clear(self):
        pass
    @abstractclassmethod
    def size(self) -> int:
        pass
    @abstractclassmethod
    def get(self) -> list:
        pass
    @abstractclassmethod
    def add(self,string: str):
        pass