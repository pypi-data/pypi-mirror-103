#  -*- coding: utf-8 -*-
# *****************************************************************************
# PILS PLC client library
# Copyright (c) 2019-2021 by the authors, see LICENSE
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc.,
# 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
#
# Module authors:
#   Georg Brandl <g.brandl@fz-juelich.de>
#
# *****************************************************************************

import logging
import struct
import threading
import time

import pytest

from zapf import CommError
from zapf.io import PlcIO
from zapf.proto import Protocol

from test.simulator import runtime, testplc


def prettify(data):
    if len(data) == 2:
        val = struct.unpack('H', data)[0]
        return f'{val} {val:#x}'
    elif len(data) == 4:
        val_i = struct.unpack('I', data)[0]
        val_f = struct.unpack('f', data)[0]
        return f'{val_i} {val_i:#x} {val_f}'
    elif len(data) == 8:
        val_i = struct.unpack('Q', data)[0]
        val_f = struct.unpack('d', data)[0]
        return f'{val_i} {val_i:#x} {val_f}'
    return ''


class TestProtocol(Protocol):
    OFFSETS = [0, 0x6000, 0x8000, 0x10000]

    def __init__(self, url, log, read, write):
        Protocol.__init__(self, url, log)
        self._handle_read = read
        self._handle_write = write

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False

    def read(self, addr, length):
        try:
            data = self._handle_read(self.offset + addr, length)
        except Exception as err:
            self.log.warning(f'R {addr:#x} {length} !! {err}')
            raise CommError(f'read failed: {err}') from err
        else:
            self.log.info(f'R {addr:#x} {length} -> {data} {prettify(data)}')
            return data

    def write(self, addr, data):
        try:
            self._handle_write(self.offset + addr, data)
        except Exception as err:
            self.log.warning(f'W {addr:#x} {data} {prettify(data)} !! {err}')
            raise CommError(f'write failed: {err}') from err
        else:
            self.log.info(f'W {addr:#x} {data} {prettify(data)} ok')


@pytest.fixture(scope='function', autouse=True)
def plc_io(caplog):
    caplog.set_level(logging.INFO)

    cond = threading.Condition()
    stopflag = False

    def thread():
        while not stopflag:
            with cond:
                testplc.Main()  # pylint: disable=no-value-for-parameter
                cond.notify()
            time.sleep(.005)

    def handle_read(addr, length):
        with cond:
            cond.wait()
            return runtime.mem.read(addr, length)

    def handle_write(addr, data):
        with cond:
            cond.wait()
            runtime.mem.write(addr, data)

    plc = threading.Thread(target=thread, daemon=True)
    plc.start()

    plogger = logging.getLogger('simplc')
    proto = TestProtocol('test://', plogger, handle_read, handle_write)
    yield PlcIO(proto, logging.root)

    stopflag = True
    plc.join()
