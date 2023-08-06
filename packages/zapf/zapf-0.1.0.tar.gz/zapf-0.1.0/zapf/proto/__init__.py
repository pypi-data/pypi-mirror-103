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

"""Support for an abstract communication protocol."""


class Protocol:
    OFFSETS = []

    def __init__(self, url, log):
        self.url = url
        self.log = log
        self.offset = 0
        self.connected = False

    @staticmethod
    def create(url, log):
        if url.startswith('ads://'):
            return ADSProtocol(url, log)
        elif url.startswith('modbus://'):
            return ModbusProtocol(url, log)
        elif url.startswith('tango://'):
            return TangoProtocol(url, log)
        raise Exception('unsupported connection URL: %s' % url)

    def connect(self):
        raise NotImplementedError

    def disconnect(self):
        raise NotImplementedError

    def reconnect(self):
        self.connect()

    def read(self, addr, length):
        raise NotImplementedError

    def write(self, addr, data):
        raise NotImplementedError


# pylint: disable=wrong-import-position
from zapf.proto.ads import ADSProtocol
from zapf.proto.modbus import ModbusProtocol
from zapf.proto.tango import TangoProtocol
