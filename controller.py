from controller_skin import *

import sys



class BaseButton(QPushButton):
    def __init__(self, parent, id_button):
        super(BaseButton, self).__init__(parent)
        self.id_button = id_button
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        self.setText("%03d" % self.id_button)

        self.setProperty("ccheck",False);

        self.pressed.connect(self.on_press)
        self.released.connect(self.on_release)

    def on_press(self):
        print (self.is_enabled())
        if self.is_enabled():
            self.disable()
        else:
            self.enable()

    def on_release(self):
        print (self.is_enabled())

    def is_enabled(self):
        return self.property("ccheck")

    def enable(self):
        self.setProperty("ccheck",True)
        self.setStyleSheet(base_css)

    def disable(self):
        self.setProperty("ccheck",False)
        self.setStyleSheet(base_css)



class BigButton(BaseButton):
    pass

class SmallButton(BaseButton):
    pass


class Controller(QMainWindow):
    def __init__(self, parent):
        super(Controller, self).__init__()

        buttons_layout = QGridLayout()
        self.buttons = []

        for i in range (8):
            btn = SmallButton(self, len(self.buttons))
            self.buttons.append(btn)
            buttons_layout.addWidget(btn, int(i/4), i%4)

        for i in range (16):
            btn = BigButton(self, len(self.buttons))
            self.buttons.append(btn)
            buttons_layout.addWidget(btn, 2+int(i/4), i%4)

        bbar = QWidget()
        bbar.setLayout(buttons_layout)            

        self.setCentralWidget(bbar)
        self.setStyleSheet(base_css)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Controller(app)
    app.exec_()