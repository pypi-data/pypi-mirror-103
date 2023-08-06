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

"""Implements communication via a Tango device."""

import re
from struct import pack, unpack

import PyTango

from zapf import ApiError, CommError
from zapf.proto import Protocol

TANGO_ADDR_RE = tangodev_re = re.compile(
    r'tango://([\w.-]+:[\d]+/)?([\w-]+/){2}[\w-]+(#dbase=(no|yes))?$')


class TangoProtocol(Protocol):
    # Since a Tango device can represent both Modbus and ADS, we have to try
    # all offsets.
    OFFSETS = [0, 0x6000, 0x8000]

    def __init__(self, url, log):
        if not TANGO_ADDR_RE.match(url):
            raise ApiError('invalid Tango address, must be '
                           'ads://host/amsnetid:amsport')
        self._proxy = None

        Protocol.__init__(self, url, log)

    def connect(self):
        try:
            self._proxy = PyTango.DeviceProxy(self.url)
            self._proxy.state
        except PyTango.DevFailed as err:
            self.log.exception('while creating Tango proxy')
            raise CommError('cannot connect to Tango device: %s' % err) from err
        except AttributeError:
            self.log.error('no connection to Tango device')
            raise CommError('Tango device exists, but seems to be not '
                            'running') from None
        try:
            self._proxy.ReadOutputWords
            self._proxy.WriteOutputWords
        except AttributeError:
            self.log.error('Tango device has wrong interface')
            raise CommError('Tango device seems to have the wrong '
                            'interface') from None
        self.connected = True

    def disconnect(self):
        self._proxy = None
        self.connected = False

    def read(self, addr, length):
        if not self.connected:
            self.reconnect()
        assert addr % 2 == 0
        nregs = (length + 1) // 2
        try:
            result = self._proxy.ReadOutputWords(((self.offset + addr) // 2,
                                                  nregs))
        except PyTango.DevFailed as err:
            self.log.exception('during read')
            raise CommError('Tango error during read: %s' % err) from err
        return pack('<%dH' % nregs, *result)[:length]

    def write(self, addr, data):
        if not self.connected:
            self.reconnect()
        assert addr % 2 == 0 and len(data) % 2 == 0
        nregs = len(data) // 2
        payload = ((self.offset + addr) // 2,) + unpack('<%dH' % nregs, data)
        try:
            self._proxy.WriteOutputWords(payload)
        except PyTango.DevFailed as err:
            self.log.exception('during read')
            raise CommError('Tango error during read: %s' % err) from err
