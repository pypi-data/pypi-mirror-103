# This file is placed in the Public Domain.

from obj import Object, dorepr

class Bus(Object):

    objs = []

    def __iter__(self):
        return iter(Bus.objs)

    @staticmethod
    def add(obj):
        if obj not in Bus.objs:
            Bus.objs.append(obj)

    @staticmethod
    def announce(txt):
        for h in Bus.objs:
            if "announce" in dir(h):
                h.announce(txt)

    @staticmethod
    def byorig(orig):
        for o in Bus.objs:
            if dorepr(o) == orig:
                return o

    @staticmethod
    def byfd(fd):
        for o in Bus.objs:
            if o.fd and o.fd == fd:
                return o

    @staticmethod
    def bytype(typ):
        for o in Bus.objs:
            if isinstance(o, type):
                return o

    @staticmethod
    def resume():
        for o in Bus.objs:
            o.resume()

    @staticmethod
    def say(orig, channel, txt):
        for o in Bus.objs:
            if dorepr(o) == orig:
                o.say(channel, txt)

def first():
    if Bus.objs:
        return Bus.objs[0]
