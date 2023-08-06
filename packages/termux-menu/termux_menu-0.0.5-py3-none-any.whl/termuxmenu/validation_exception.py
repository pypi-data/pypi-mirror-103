"""

    Termux Validation Exception

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/20 

"""

class ValidationException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)