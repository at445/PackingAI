from julesTk import app
from CONTROLLER.MainController import MainController
__author__ = "Chen JinSong <jingsong@foxmail.com>"

class PackingAI(app.Application):

    def __init__(self):
        super(PackingAI, self).__init__()

    def _prepare(self):
        self.add_controller("mainCtrl", MainController(self))

    @property
    def mainCtrl(self):
        return self.get_controller("mainCtrl")

    def _start(self):
        self.root.attributes("-topmost", True)
        self.root.title("Packing AI")
        self.root.geometry("1070x535")
        self.mainCtrl.start()


if __name__ == "__main__":
    app = PackingAI()
    app.run()
