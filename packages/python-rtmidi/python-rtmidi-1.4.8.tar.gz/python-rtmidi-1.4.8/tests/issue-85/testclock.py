import time

import rtmidi
from rtmidi.midiutil import open_midioutput,open_midiport
from rtmidi.midiconstants import NOTE_OFF, NOTE_ON

class SomeClass:

    def init(self):
        midiInAlsa = rtmidi.MidiIn(rtapi=rtmidi.API_LINUX_ALSA)
        midiInAlsa.ignore_types(timing=False)
        midiInAlsa.set_callback(self.rtMidiInputCallback)
        midiInAlsa.set_error_callback(self.rtMidiErrorCallback)
        self.inMidiAlsaPort, port_name = open_midiport(None,
            type_="input", api=rtmidi.API_LINUX_ALSA, interactive=True)

    def run(self):
        while True:
            print ("wait")
            time.sleep(0.1)

    def rtMidiInputCallback(self, message, data):
        print("rtMidiInputCallback")

    def rtMidiErrorCallback(self, type, message:str, data):
        print("rtMidiErrorCallback")


c=SomeClass()
c.init()
c.run()
