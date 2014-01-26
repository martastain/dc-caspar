from controller_skin import *

import sys


class BaseButton(QPushButton):
    def __init__(self, parent):
        super(BaseButton, self).__init__(parent)
        size_policy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        size_policy.setHeightForWidth(True)
        self.setSizePolicy(size_policy)

    def heightForWidth(self, width):
        print (width)
        return width


class BigButton(BaseButton):
    pass

class SmallButton(BaseButton):
    def heightForWidth(self, width):
        return width/2




class Controller(QMainWindow):
    def __init__(self, parent):
        super(Controller, self).__init__()


        big_buttons_layout = QGridLayout()
        self.big_buttons = []

        for i in range (8):
            btn = SmallButton(self)
            btn.setText("%03d"%i)
            self.big_buttons.append(btn)
            big_buttons_layout.addWidget(btn, int(i/4), i%4)

        for i in range (16):
            btn = BigButton(self)
            btn.setText("%03d"%i)
            self.big_buttons.append(btn)
            big_buttons_layout.addWidget(btn, 2+int(i/4), i%4)


        bbar = QWidget()
        bbar.setLayout(big_buttons_layout)            

        self.setCentralWidget(bbar)
        self.setStyleSheet(base_css)
        self.show()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Controller(app)
    app.exec_()