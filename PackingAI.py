from julesTk import app
from CONTROLLER.MainController import MainController
__author__ = "Chen JinSong <jinsong.chen@siemens.com>"

class PackingAI(app.Application):

    def __init__(self):
        super(PackingAI, self).__init__()

    def _prepare(self):
        self.add_controller("mainCtrl", MainController(self))

    @property
    def mainCtrl(self):
        return self.get_controller("mainCtrl")

    def _start(self):
        self.mainCtrl.start()


if __name__ == "__main__":
    app = PackingAI()
    app.run()
