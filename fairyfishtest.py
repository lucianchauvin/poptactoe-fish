#!/usr/bin/env python3
#
# fairyfishtest is a script for automated chess variant engine matches.
# Copyright (C) 2020 Fabian Fichter
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import argparse
from collections import Counter
import logging
import math, time
import random
import subprocess
import threading
import time

import pyffish as sf


class Engine:
    def __init__(self, args, options):
        self.process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        self.lock = threading.Lock()
        self.partner = None
        self.rank_conversion = False  # convert ranks from zero-based to one-based
        self.options = options

    def initialize(self, variant):
        with self.lock:
            self.process.stdin.write('xboard\n')
            # self.process.stdin.write('protover 2\n')
            self.process.stdin.write('new\n')
            self.process.stdin.write('variant {}\n'.format(variant))
            self.process.stdin.flush()

    def get_best_move(self, FEN):
        self.process.stdin.write('setboard {}\n'.format(FEN))

        self.process.stdin.write('go\n')
        self.process.stdin.flush()
        time.sleep(3.5)
        self.process.stdin.write('stop\n')
        self.process.stdin.flush()
        while True:
            line = self.process.stdout.readline()
            if line.startswith('move'):
                return line

