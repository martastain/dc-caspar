from controller_skin import *
from actions import Session
from midi import Midi

import sys
import time

BTN_ON   = [1, 0][INVERT_COLORS]
BTN_OFF  = [0, 1][INVERT_COLORS]

midi = Midi()


BTN_MAP = {
    0   : (16, "1"),
    1   : (17, "2"),
    2   : (18, "3"),
    3   : (19, "4"),
    4   : (20, "5"),
    5   : (21, "6"),
    6   : (22, "7"),
    7   : (23, "8"),

    8   : (48, "13"),
    9   : (49, "14"),
    10  : (50, "15"),
    11  : (51, "16"),
    12  : (44, "09"),
    13  : (45, "10"),
    14  : (46, "11"),
    15  : (47, "12"),
    16  : (40, "05"),
    17  : (41, "06"),
    18  : (42, "07"),
    19  : (43, "08"),
    20  : (36, "01"),
    21  : (37, "02"),
    22  : (38, "03"),
    23  : (39, "04"),
}


SHIFTS = {
    0 : "a",
    4 : "b",
    3 : "c",
    7 : "d"
}


MIDI_MAP = {BTN_MAP[key][0]:key for key in BTN_MAP}



class MidiSignal(QObject):
    sig = Signal(list)

class MidiCtrl(QThread):
    def __init__(self, parent):
        super(MidiCtrl, self).__init__(parent)
        self.parent = parent
        self.signal = MidiSignal()
        self._halt   = False
        self._halted = False

    def run(self):
        print "enable start"
        while not self._halt:
            msg = midi.recv()
            if msg:
                msg, deltatime = msg
                self.signal.sig.emit(msg)
            time.sleep(0.01)

        self._halted = True

    def halt(self):
        self._halt = True

    def halted(self):
        return self._halted

    def listen(self,handler):
        self.signal.sig.connect(handler)


class BaseButton(QPushButton):
    def __init__(self, parent, id_button):
        super(BaseButton, self).__init__(parent)
        self.parent = parent
        self.id_button = id_button
        self.mkey = BTN_MAP[id_button][0]
        self.setText(BTN_MAP[id_button][1])
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.setSizePolicy(size_policy)
        
        self.setProperty("ccheck",False);

        self.pressed.connect(self.on_press)
        self.released.connect(self.on_release)

    def on_press(self):
        if self.id_button in self.parent.session.actions:
            print self.id_button
            self.parent.session.actions[self.id_button].on_press()

    def on_release(self):
        if self.id_button in self.parent.session.actions:
            self.parent.session.actions[self.id_button].on_release()

    def is_enabled(self):
        return self.property("ccheck")

    def enable(self):
        self.setProperty("ccheck",True)
        self.setProperty("cblink",False)
        self.setStyleSheet(base_css)
        midi.send(149, self.mkey, BTN_ON)

    def disable(self):
        self.setProperty("ccheck",False)
        self.setProperty("cblink",False)
        self.setStyleSheet(base_css)
        midi.send(149, self.mkey, BTN_OFF)

    def blink(self):
        self.setProperty("ccheck",False)
        self.setProperty("cblink",True)
        self.setStyleSheet(base_css)
        midi.send(149, self.mkey, 2)



class BigButton(BaseButton):
    pass

class SmallButton(BaseButton):
    pass




class Controller(QMainWindow):
    def __init__(self, parent):
        super(Controller, self).__init__()

        buttons_layout = QGridLayout()
        self.buttons = []
        self.shift_state = ""

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
        
        self.midictrl = MidiCtrl(self)
        if midi.midiin:
            self.midictrl.listen(self.midi_handler)
            self.midictrl.start()

        self.session = Session(self)
        self.session.load("test.json")


        self.stat_timer = QTimer()
        self.connect(self.stat_timer,SIGNAL("timeout()"),self.update_stat)
        self.stat_timer.start(120)

        self.show()


    def update_stat(self):
        self.session.main()


    def midi_handler(self, msg):
        ch, k, v = msg

        if k in SHIFTS:
            if ch == 149:
                midi.send(149, k, BTN_ON)
                self.shift_state += SHIFTS[k]
            else:
                midi.send(149, k, BTN_OFF)
                self.shift_state = self.shift_state.replace(SHIFTS[k],"")
            print "Shift state:" , self.shift_state
        
        elif k in MIDI_MAP:
            if ch == 149:
                self.buttons[MIDI_MAP[k]].on_press()
            elif ch == 133:
                self.buttons[MIDI_MAP[k]].on_release()





if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = Controller(app)
    app.exec_()

    wnd.midictrl.halt()
    while not wnd.midictrl.halted():
        time.sleep(.2)
