# This file is placed in the Public Domain.

from err import ENOTXT
from obj import Default, Object
from tms import parse_time
from zzz import time

class Token(Object):

    def __init__(self, txt):
        super().__init__()
        self.txt = txt

class Option(Default):

    def __init__(self, txt):
        super().__init__()
        if txt.startswith("--"):
            self.opt = txt[2:]
        if txt.startswith("-"):
            self.opt = txt[1:]

class Getter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("==")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post

class Setter(Object):

    def __init__(self, txt):
        super().__init__()
        try:
            pre, post = txt.split("=")
        except ValueError:
            pre = post = ""
        if pre:
            self[pre] = post

class Skip(Object):

    def __init__(self, txt):
        super().__init__()
        pre = ""
        if txt.endswith("-"):
            try:
                pre, _post = txt.split("=")
            except ValueError:
                try:
                    pre, _post = txt.split("==")
                except ValueError:
                    pre = txt
        if pre:
            self[pre] = True

class Timed(Object):

    def __init__(self, txt):
        super().__init__()
        v = 0
        vv = 0
        try:
            pre, post = txt.split("-")
            v = parse_time(pre)
            vv = parse_time(post)
        except ValueError:
            pass
        if not v or not vv:
            try:
                vv = parse_time(txt)
            except ValueError:
                vv = 0
            v = 0
        if v:
            self["from"] = time.time() - v
        if vv:
            self["to"] = time.time() - vv

def parseargs(o, ptxt=None):
    if ptxt is None:
        raise ENOTXT(o)
    o.txt = ptxt
    o.otxt = ptxt
    o.gets = Default()
    o.opts = Default()
    o.timed = []
    o.index = None
    o.sets = Default()
    o.skip = Default()
    args = []
    for token in [Token(txt) for txt in ptxt.split()]:
        s = Skip(token.txt)
        if s:
            o.skip.update(s)
            token.txt = token.txt[:-1]
        t = Timed(token.txt)
        if t:
            o.timed.append(t)
            continue
        g = Getter(token.txt)
        if g:
            o.gets.update(g)
            continue
        s = Setter(token.txt)
        if s:
            o.sets.update(s)
            continue
        opt = Option(token.txt)
        if opt:
            try:
                o.index = int(opt.opt)
                continue
            except ValueError:
                pass
            if len(opt.opt) > 1:
                for op in opt.opt:
                    o.opts[op] = True
            else:
                o.opts[opt.opt] = True
            continue
        args.append(token.txt)
    if not args:
        o.args = []
        o.cmd = ""
        o.rest = ""
        o.txt = ""
        return o
    o.cmd = args[0]
    o.args = args[1:]
    o.txt = " ".join(args)
    o.rest = " ".join(args[1:])
    return o
