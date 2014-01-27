import rtmidi


class Midi():
    def __init__(self):
        self.midiin  = rtmidi.MidiIn()
        self.midiout = rtmidi.MidiOut()

        for i, port in enumerate(self.midiin.get_ports()):
            if port.find("DC-1") > -1:
                self.midiin.open_port(i)
                break
        else:
            print ("CMD DC-1 input is not available")
            self.midiin = False

        for i, port in enumerate(self.midiout.get_ports()):
            if port.find("DC-1") > -1:
                self.midiout.open_port(i)
                break
        else:
            print ("CMD DC-1 output is not available")
            self.midiout = False


    def send(self, ch, key, val):
        if self.midiout:
            self.midiout.send_message([ch,key,val])

    def recv(self):
        if self.midiin:
            return self.midiin.get_message()
        return False