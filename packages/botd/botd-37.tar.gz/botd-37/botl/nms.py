# This file is placed in the Public Domain.

from .obj import Default, Object
from .itr import findmods, findnames
from .utl import direct
from .zzz import js

class Names(Object):

    names = Default({
        "bus": [
            "botl.bus.Bus"
        ],
        "cfg": [
            "botl.irc.Cfg",
            "botl.obj.Cfg",
            "botd.rss.Cfg",
            "botd.udp.Cfg"
        ],
        "client": [
            "botl.hdl.Client"
        ],
        "command": [
            "botl.evt.Command"
        ],
        "dcc": [
            "botl.irc.DCC"
        ],
        "default": [
            "botl.obj.Default"
        ],
        "email": [
            "botl.mbx.Email"
        ],
        "enoclass": [
            "botl.err.ENOCLASS"
        ],
        "enofilename": [
            "botl.err.ENOFILENAME"
        ],
        "enomore": [
            "botl.err.ENOMORE"
        ],
        "enotimplemented": [
            "botl.err.ENOTIMPLEMENTED"
        ],
        "enotxt": [
            "botl.err.ENOTXT"
        ],
        "enouser": [
            "botl.err.ENOUSER"
        ],
        "event": [
            "botl.evt.Event",
            "botl.irc.Event"
        ],
        "feed": [
            "botd.rss.Feed"
        ],
        "fetcher": [
            "botd.rss.Fetcher"
        ],
        "getter": [
            "botl.prs.Getter"
        ],
        "handler": [
            "botl.hdl.Handler"
        ],
        "httperror": [
            "urllib.error.HTTPError"
        ],
        "irc": [
            "botl.irc.IRC"
        ],
        "loader": [
            "botl.ldr.Loader"
        ],
        "log": [
            "botd.log.Log"
        ],
        "names": [
            "botl.nms.Names"
        ],
        "o": [
            "botl.obj.O"
        ],
        "obj": [
            "botl.obj.Obj"
        ],
        "object": [
            "botl.obj.Object"
        ],
        "objectlist": [
            "botl.obj.ObjectList"
        ],
        "option": [
            "botl.prs.Option"
        ],
        "output": [
            "botl.opt.Output"
        ],
        "repeater": [
            "botl.clk.Repeater"
        ],
        "request": [
            "urllib.request.Request"
        ],
        "rss": [
            "botd.rss.Rss"
        ],
        "seen": [
            "botd.rss.Seen"
        ],
        "setter": [
            "botl.prs.Setter"
        ],
        "skip": [
            "botl.prs.Skip"
        ],
        "textwrap": [
            "botl.irc.TextWrap"
        ],
        "thr": [
            "botl.thr.Thr"
        ],
        "timed": [
            "botl.prs.Timed"
        ],
        "timer": [
            "botl.clk.Timer"
        ],
        "todo": [
            "botd.tdo.Todo"
        ],
        "token": [
            "botl.prs.Token"
        ],
        "udp": [
            "botd.udp.UDP"
        ],
        "urlerror": [
            "urllib.error.URLError"
        ],
        "user": [
            "botl.usr.User"
        ],
        "users": [
            "botl.usr.Users"
        ]
    })

    modules = Object({
        "cfg": "botl.irc",
        "cmd": "botl.cmd",
        "dlt": "botl.usr",
        "dne": "botl.tdo",
        "dpl": "botl.rss",
        "flt": "botl.adm",
        "fnd": "botl.fnd",
        "ftc": "botl.rss",
        "krn": "botl.adm",
        "log": "botl.log",
        "mbx": "botl.mbx",
        "met": "botl.usr",
        "rem": "botl.rss",
        "rss": "botl.rss",
        "slg": "botd.slg",
        "sve": "botl.adm",
        "tdo": "botl.tdo",
        "thr": "botl.adm",
        "upt": "botl.adm"
    })

    inits =  Object({
        "adm": "botl.adm",
        "bus": "botl.bus",
        "clk": "botl.clk",
        "dbs": "botl.dbs",
        "edt": "botl.edt",
        "err": "botl.err",
        "evt": "botl.evt",
        "fnd": "botl.fnd",
        "hdl": "botl.hdl",
        "irc": "botl.irc",
        "itr": "botl.itr",
        "ldr": "botl.ldr",
        "log": "botl.log",
        "mbx": "botl.mbx",
        "nms": "botl.nms",
        "obj": "botl.obj",
        "opt": "botl.opt",
        "prs": "botl.prs",
        "rss": "botl.rss",
        "tdo": "botl.tdo",
        "thr": "botl.thr",
        "tms": "botl.tms",
        "trc": "botl.trc",
        "trm": "botl.trm",
        "udp": "botl.udp",
        "url": "botl.url",
        "usr": "botl.usr",
        "utl": "botl.utl",
        "zzz": "botl.zzz"
    })

    @staticmethod
    def getnames(nm, dft=None):
        return Names.names.get(nm, dft)

    @staticmethod
    def getmodule(mn):
        return Names.modules.get(mn, None)

    @staticmethod
    def getinit(mn):
        return Names.inits.get(mn, None)

    @staticmethod
    def tbl(tbl):
        Names.names.update(tbl["names"])
        Names.modules.update(tbl["modules"])
        Names.inits.update(tbl["inits"])
