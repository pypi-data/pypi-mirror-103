#!/usr/bin/env python3

import time
import rtmidi
import queue


class Context:
    def handle_midi_in(self, event, data):
        message, deltatime = event
        q.put(event)
        # print("p1", event)

    def __init__(self, pn, q):
        self.pn = pn
        self.q = q
        self.mi = rtmidi.MidiIn(name=pn)
        #self.mi.ignore_types(sysex=False, timing=True, active_sense=True)
        self.mi.open_virtual_port(name=pn)
        self.mo = rtmidi.MidiOut(name=pn)
        self.mo.open_virtual_port()
        self.mi.set_client_name(pn)
        self.mo.set_client_name(pn)
        self.mi.set_callback(self.handle_midi_in)


q = queue.Queue()

c1 = Context("p1", q)
c2 = Context("p2", q)
c3 = Context("p3", q)
c4 = Context("p4", q)


while True:
    m = q.get(True)
    #print(m)
