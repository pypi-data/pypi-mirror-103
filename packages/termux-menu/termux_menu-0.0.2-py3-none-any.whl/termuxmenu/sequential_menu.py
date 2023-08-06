"""

    Termux Sequential Menu

    AUTHOR: Carlos Pomares (https://www.github.com/pomaretta) 
    LAST REV: 2021/04/22

"""

from termuxmenu import ValidationException, Menu, ErrorLog, Question

class SequentialMenu(Menu):
    def __init__(self,questions: list,escape: str,error_log: ErrorLog,validation: list = None) -> None:
        self.questions = questions
        self.escape = escape
        self.error_log = error_log
        self.validation = validation
        self.output = list()
        self.step = 0
    def incrementStep(self):
        self.step += 1
    def decrementStep(self):
        self.step -= 1
    def resetStep(self):
        self.step = 0
    def loop(self):
        while self.output.count() < self.questions.count():
            try:
                if self.validation != None:
                    self.output.append(Question.ask(self.questions[self.step],self.escape,self.validation[self.step]))
                else:
                    self.output.append(Question.ask(self.questions[self.step],self.escape))
            except ValidationException as validationException:
                self.error_log.add(validationException)
                self.decrementStep()
            except Exception as ioException:
                self.error_log.add(ioException)
            finally:
                self.incrementStep()
    def getOutput(self) -> list:
        return self.output
    def update(self):
        self.loop()
    def show(self):
        self.update()