"""

    Termux String Generator

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

class StringGenerator():
    @staticmethod
    def generateString(character: str,lenght: int) -> str:
        output = ""
        for i in range(lenght):
            output += character
        return output
