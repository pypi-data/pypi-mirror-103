# This file is placed in the Public Domain.

import unittest

from botl.edt import edit
from botl.obj import Cfg, cfg
from botl.prs import parseargs

cfg = Cfg()

class Test_Cfg(unittest.TestCase):

    def test_parse(self):
        parseargs(cfg, "mods=irc")
        self.assertEqual(cfg.sets.mods, "irc")

    def test_parse2(self):
        parseargs(cfg, "mods=irc,udp")
        self.assertEqual(cfg.sets.mods, "irc,udp")

    def test_edit(self):
        d = {"mods": "rss"}
        edit(cfg, d)
        self.assertEqual(cfg.mods, "rss")
