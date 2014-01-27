import os
import json
import time

from caspar import CasparServer

SESSION_DIR = "sessions"

KEYS = {
    "LG01" : 20,
    "LG02" : 21,
    "LG03" : 22,
    "LG04" : 23,

    "LG05" : 16,
    "LG06" : 17,
    "LG07" : 18,
    "LG08" : 19,

    "LG09" : 12,
    "LG10" : 13,
    "LG11" : 14,
    "LG12" : 15,

    "LG13" : 8,
    "LG14" : 9,
    "LG15" : 10,
    "LG16" : 11,

    "SM01" : 00,
    "SM02" : 01,
    "SM03" : 02,
    "SM04" : 03,

    "SM05" : 0,
    "SM06" : 1,
    "SM07" : 2,
    "SM08" : 3,
}




class BaseAction():
    def __init__(self, parent, id_button):
        self.parent = parent
        self.id_button = id_button
        self.state = 0
        self.on_init()

    def on_init(self):
        pass

    def on_press(self):
        pass

    def on_release(self):
        pass

    def on_main(self):
        pass


    def _main(self):
        ch = self.caspar[self.id_channel]
        if not ch:
            return

        l = ch[self.id_layer]

        if l.current_file:

            if l.current_file == self.filename.lower():
                if self.state != 1:
                    self.state = 1
                    self.enable()
            
            elif l.cued_file == self.filename.lower():
                if self.state != 2:
                    self.state = 2
                    self.blink()
            
            elif self.state != 0:
                self.state = 0
                self.disable()

        elif self.state != 0:
                self.state = 0
                self.disable()

        self.on_main()

    def enable(self):
        self.parent.button_enable(self.id_button)

    def disable(self):
        self.parent.button_disable(self.id_button)

    def blink(self):
        self.parent.button_blink(self.id_button)



class ClipAction(BaseAction):
    def on_init(self):
        self.id_channel = 1
        self.id_layer = 1
        self.filename = False
        self.loop = False
        self.caspar = self.parent.caspar

    def on_press(self):
        if self.parent.shift_state("b"):
            cmds = ["CLEAR %s-%s" % (self.id_channel, self.id_layer)]

        elif self.parent.shift_state("a"):
            cmds = ["LOADBG %s-%s %s%s AUTO" % (self.id_channel, self.id_layer, self.filename, [""," LOOP"][self.loop])]

        else:
            cmds = ["PLAY %s-%s %s%s AUTO" % (self.id_channel, self.id_layer, self.filename, [""," LOOP"][self.loop])]
            
            if self.end_action == "CLEAR":
                cmds.append("LOADBG %s-%s BLANK AUTO" % (self.id_channel, self.id_layer))

            elif str(self.end_action).startswith("LOOP"):
                cmds.append( "LOADBG %s-%s %s LOOP AUTO" % (self.id_channel, self.id_layer, self.end_action.split(" ")[1]))

            elif str(self.end_action).startswith("PLAY"):
                cmds.append("LOADBG %s-%s %s AUTO" % (self.id_channel, self.id_layer, self.end_action.split(" ")[1]))

        for cmd in cmds:
            self.caspar.query(cmd)






class ImageAction(BaseAction):
    def on_init(self):
        self.caspar = self.parent.caspar

        self.id_channel = 1
        self.id_layer = 1
        self.filename = False
        
        self.auto_hide  = False
        self.show_time  = 0
        self.show       = ""
        self.hide       = ""


    def on_press(self):
        if self.parent.shift_state("b"):
            self.caspar.query("CLEAR %s-%s" % (self.id_channel, self.id_layer))
            return

        if self.state == 0:
            self.do_show()
        else:
            self.do_hide()

    def do_show(self):
        cmd = "PLAY %s-%s %s %s" % (self.id_channel, self.id_layer, self.filename, self.show)
        self.show_time = time.time()
        self.caspar.query(cmd)

    def do_hide(self):
        cmd = "PLAY %s-%s BLANK %s" % (self.id_channel, self.id_layer, self.show)
        self.caspar.query(cmd)


    def on_main(self):
        if self.state == 1 and self.auto_hide and time.time() - self.show_time > self.auto_hide:
            self.do_hide()











class Session():
    def __init__(self, parent):
        self.parent = parent
        self.actions = {}
        self.caspar = CasparServer()

    def load(self, fname):
        data = json.loads(open(os.path.join(SESSION_DIR, fname)).read())
        for id_button in data["actions"]:
            action = data["actions"][id_button]
            id_button = KEYS[id_button]

            if action["class"] == "clip":
                a = ClipAction(self, id_button)
                a.filename = action["filename"]
                a.title    = action.get("title", a.filename)
                a.id_channel  = action.get("channel", 1)
                a.id_layer    = action.get("layer", 1)
                
                a.loop    = action.get("loop", False)
                a.end_action = action.get("end_action", False)
                
                self.parent.buttons[id_button].setText(a.title)
                #self.parent.buttons[id_button].setText("<font color='red'>%s</font> %s" % (a.id_layer, a.title))
                self.actions[id_button] = a


            elif action["class"] == "image":
                a = ImageAction(self, id_button)
                a.filename = action["filename"]
                a.title    = action.get("title", a.filename)
                a.id_channel  = action.get("channel", 1)
                a.id_layer    = action.get("layer", 1)

                a.auto_hide  = action.get("auto_hide", False)
                a.show       = action.get("show", "")
                a.hide       = action.get("hide", "")
                
                self.parent.buttons[id_button].setText(a.title)
                self.actions[id_button] = a

    def shift_state(self, key):
        return key in self.parent.shift_state


    def button_enable(self, id_button):
        self.parent.buttons[id_button].enable()

    def button_disable(self, id_button):
        self.parent.buttons[id_button].disable()

    def button_blink(self, id_button):
        self.parent.buttons[id_button].blink()


    def main(self):
        self.caspar.main()
        for action in self.actions:
            self.actions[action]._main()