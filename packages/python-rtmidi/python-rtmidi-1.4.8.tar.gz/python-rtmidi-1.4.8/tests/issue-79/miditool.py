#!/bin/env python3

import argparse
import mido
import os
import re
import sys
import time


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", "-p", action="store", help="port (regexp) to use when playing the MIDI file. use 'list' to list available ports", default=None)
    parser.add_argument("--input_file", '-i', action="store", help="play a MIDI file", default=None)
    parser.add_argument("--dump", action="store", help="dump received MIDI", default=None)
    parser.add_argument("--hex", action="store", help="hex data to parse or send", default=None)
    parser.add_argument("--flood", help="send hex data over and over", default=False)
    parser.add_argument("--maxtime", type=float, action="store", help="max playback time", default=None)
    parser.add_argument("--speed", action="store", type=float, help="speed to play the MIDI file", default=1)
    parser.add_argument("--parse_midi", action="store_true", help="parse MIDI bytes with the register_parsers_static")
    parser.add_argument("--quiet", "-q", action="store_true", help="do not print the messages")
    return parser.parse_args(args)


def get_port(port_expr):
    gon = mido.get_output_names()

    outport = None
    for pn in gon:
        p = re.findall(port_expr, pn)
        if p:
            outport = pn
            break

    if outport is None:
        print(f"Error: no port matches {port_expr}")
        return None
    else:
        try:
            outport = mido.open_output(outport)
            return outport
        except IOError:
            print(f"cannot open output port {outport}")
            return None


def main(args=None):
    args = parse_args(args)

    if args.port:
        if args.port == "list":
            def print_ports(heading, port_names):
                print(heading)
                for name in port_names:
                    print("    '{}'".format(name))
                print()

            print_ports('Input Ports:', mido.get_input_names())
            print_ports('Output Ports:', mido.get_output_names())
            sys.exit(0)

    if args.dump:
        print("Not implemented")
        sys.exit(1)

    elif args.hex:
        outport = None
        if args.port:
            outport = get_port(args.port)
            if outport:
                print(f"Using output port {outport}")
            else:
                sys.exit(1)

        messages = re.split("\s|,", args.hex)
        mm = list()
        for m in messages:
            if m == "":
                continue
            elif m.startswith("0x"):
                mm.append(int(m[2:], 16))
            else:
                mm.append(int(m))

        i = 0
        j = 1
        exit = False

        midi_msgs = []
        while True:
            while True:
                if i + j > len(mm):
                    exit = True
                    break
                sub = mm[i:i+j]
                msg = None
                # print(i, j, sub)
                msg = mido.parse(sub)
                if msg is None:
                    j += 1
                    continue
                else:
                    mb = msg.bytes()
                    if mb != sub:
                        print(f"WARNING: ignored bytes! {sub[0:len(sub) - len(mb)]}")
                    midi_msgs.append(msg)

                    i += j
                    j = 1
                    break
            if exit:
                break
        sub = mm[i:i+j]
        if not args.quiet:
            print(f"Sending: {[msg for msg in midi_msgs]}")
            if sub:
                print(f"messages left: {sub}")

        if outport:
            if args.flood is not None:
                count = 0
                start = time.time()
                sleeptime = float(args.flood)
                try:
                    while True:
                        for msg in midi_msgs:
                            outport.send(msg)
                            count += 1

                        if sleeptime > 0.0:
                            time.sleep(sleeptime)
                except KeyboardInterrupt:
                    pass

                dur = time.time() - start
                print("{} messages sent in {} seconds, {} msg/sec".format(count, dur, count/dur))
            else:
                for msg in midi_msgs:
                    outport.send(msg)
        sys.exit(0)

    elif args.input_file:
        outport = None
        srp = None
        if args.port is None:
            if not args.quiet:
                print("No MIDI port specified, just printing midi messages")
        else:
            outport = get_port(args.port)
            if outport is None:
                sys.exit(1)
            print(f"Using output port {outport}")

        midifile = mido.MidiFile(args.input_file)
        mf = list(midifile)
        t0 = time.time()
        acc_t = 0.0
        print(f"Midifile length: {midifile.length}s")
        try:
            for msg in mf:
                acc_t += msg.time
                when = acc_t / args.speed
                now = time.time() - t0
                sleep_time = when - now
                do_print = not args.quiet
                do_send = False

                if sleep_time > 0:
                    time.sleep(sleep_time)

                if msg.type == "sysex" or isinstance(msg, mido.midifiles.meta.MetaMessage) or args.quiet is False:
                    do_print = True
                    do_send = False

                if do_send and outport:
                    outport.send(msg)

                if do_print:
                    pt = '{:.2f}s'.format(acc_t)
                    print(f"{pt}: {msg}")

                if args.maxtime is not None and acc_t >= args.maxtime:
                    break
        except KeyboardInterrupt:
            print()
            if outport:
                outport.reset()

    else:
        print("No action specified")
        sys.exit(1)


if __name__ == '__main__':
    sys.exit(main() or 0)
