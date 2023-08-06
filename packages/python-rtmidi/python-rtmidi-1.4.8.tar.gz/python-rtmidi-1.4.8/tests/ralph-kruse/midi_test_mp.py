#!/usr/bin/env python

import rtmidi
import sys
import multiprocessing as mp
import time


class CMidi:
    def __init__(self, port):
        self.midiout = rtmidi.MidiOut()
        self.midiout.open_port(port)
        self.txQueue = mp.Queue()
        self.proc = mp.Process(target=self.start)
        self.proc.start()

    def __del__(self):
        self.proc.join()
        self.midiout.close_port()
        del self.midiout

    def start(self):
        while True:
            data = self.txQueue.get()
            if not data:
                break
            self.sendMidiDirect(data)

    def sendMidi(self, data):
        self.txQueue.put_nowait(data)

    def sendMidiDirect(self, data):
#        print("sendMidi", data)
        startTime = time.monotonic()
        self.midiout.send_message(data)
        endTime = time.monotonic()
        print("send", endTime - startTime)


midi = CMidi(int(sys.argv[1]))
print(midi.midiout.get_ports())

sysex = bytearray(2048)
sysex[0] = 0xF0
sysex[-1] = 0xF7

for i in range(10):
    print("main", time.monotonic())
    midi.sendMidi(sysex)

midi.sendMidi([])

