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

"""Implements communication via ADS, the Beckhoff universal protocol."""

import re
import socket
import time
from struct import Struct, pack

from zapf import ApiError, CommError
from zapf.proto import Protocol

# Allow omitting the first 4 NetID bytes if it's the same as the IP address,
# but always require the port.
ADS_ADDR_RE = re.compile(r'ads://(.*?)/(\d+.\d+.\d+.\d+(.\d+.\d+)?)?:(\d+)$')

# TCP port to use for ADS.
ADS_PORT = 0xBF02

# AMS header including AMS/TCP header.
REQ_HEADER = Struct('<xxIQQHHIII')
# AMS reply header including error field.
REP_HEADER = Struct('<xxIQQHHIII')
# Reply to device info command.
DEVINFO = Struct('<BBH16s')

REQ_HEADER_SIZE = REQ_HEADER.size
REP_HEADER_SIZE = REP_HEADER.size
AMS_HEADER_SIZE = REQ_HEADER_SIZE - 6

# ADS commands.
ADS_DEVINFO = 1
ADS_READ    = 2
ADS_WRITE   = 3

# Formats for payload.
ADS_ADR_LEN = Struct('<III')
ADS_ERRID = Struct('<I')

# Index group for %M memory area.
INDEXGROUP_M = 0x4020

# UDP port
BECKHOFF_UDP_PORT = 0xBF03
# UDP message to set a route.
UDP_MESSAGE = Struct(
    '<I'     # magic
    '4x'     # pad
    'I'      # operation
    'Q'      # source netaddr
    'I'      # nitems=5
    'HH25s'  # desig=12 (routename), strlen=25, content
    'HH6s'   # desig=7 (netid), len=6, content
    'HH14s'  # desig=13 (username), len=14, content
    'HH2s'   # desig=2 (password), len=2, content
    'HH16s'  # desig=5 (host), len=16, content
)
# UDP magic header number.
UDP_MAGIC = 0x71146603
# UDP packet operations and data designators.
UDP_ADD_ROUTE = 6
UDP_PASSWORD = 2
UDP_HOST = 5
UDP_NETID = 7
UDP_ROUTENAME = 12
UDP_USERNAME = 13


def pack_net_id(netidstr, amsport):
    # convert a.b.c.d.e.f to a single integer
    amsnetid = i = 0
    for (i, x) in enumerate(netidstr.split('.')):
        amsnetid |= (int(x) << (8 * i))
    if i != 5:
        raise ApiError('incomplete NetID; use format a.b.c.d.e.f '
                       'with 6 integers in the range 0-255')

    # pack the whole address into a 64-bit integer
    return amsnetid | (amsport << 48)


class ADSProtocol(Protocol):
    OFFSETS = [0]

    def __init__(self, url, log):
        adr = ADS_ADDR_RE.match(url)
        if not adr:
            raise ApiError('invalid ADS address, must be '
                           'ads://host[:port]/amsnetid:amsport')
        host = adr.group(1)
        if ':' in host:
            host, port = host.split(':')
            port = int(port)
        else:
            port = ADS_PORT
        host_ip = socket.gethostbyname(host)

        if adr.group(3):    # full AMS netid specified
            netidstr = adr.group(2)
        elif adr.group(2):  # only first 4 specified
            netidstr = adr.group(2) + '.1.1'
        else:               # nothing specified, use IP
            netidstr = host_ip + '.1.1'
        amsport = int(adr.group(4))

        self._amsnetaddr = pack_net_id(netidstr, amsport)
        self._iphostport = (host, port)
        self._invoke_id = 1  # should be incremented for every request
        self._socket = None
        self._tried_route = False

        Protocol.__init__(self, url, log)

    def connect(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self._socket.connect(self._iphostport)
            self._myamsnetaddr = pack_net_id(
                self._socket.getsockname()[0] + '.1.1', 800)
            reply = self._comm(ADS_DEVINFO, b'', DEVINFO.size)
            v1, v2, v3, name = DEVINFO.unpack(reply)
            name = name.partition(b'\0')[0].decode('latin1')
            hw_name = '%s %d.%d.%d' % (name, v1, v2, v3)
            self.log.info('connected to %s', hw_name)
        except (OSError, ValueError) as err:
            raise CommError(f'could not connect to {self.url}: {err}') from err
        except CommError as err:
            # if we get a closed connection immediately, the route is not set
            # up correctly.  Try to fix that by setting a route via UDP.  If
            # the target TCP port is not default, we are not talking directly
            # to TwinCAT, so don't even try in that case.
            if str(err) == 'no data in read' and not self._tried_route and \
               self._iphostport[1] == ADS_PORT:
                self.log.warning('connection aborted, trying to set a route...')
                self._tried_route = True
                self._set_route(self._socket.getsockname())
                self.connect()
            raise
        self._connect_callback(True)
        self.connected = True

    def disconnect(self):
        try:
            self._socket.shutdown(socket.SHUT_RDWR)
            self._socket.close()
        except OSError:
            pass
        self._socket = None
        self._connect_callback(False)
        self.connected = False

    def read(self, addr, length):
        if not self.connected:
            self.reconnect()
        payload = ADS_ADR_LEN.pack(INDEXGROUP_M, addr, length)
        try:
            return self._comm(ADS_READ, payload, 4 + length)[4:]
        except OSError as err:
            self.log.exception('during read')
            self.disconnect()
            raise CommError('IO error during read: %s' % err) from err

    def write(self, addr, data):
        if not self.connected:
            self.reconnect()
        payload = ADS_ADR_LEN.pack(INDEXGROUP_M, addr, len(data)) + data
        try:
            self._comm(ADS_WRITE, payload, 0)
        except OSError as err:
            self.log.exception('during write')
            self.disconnect()
            raise CommError('IO error during write: %s' % err) from err

    def _comm(self, cmd, payload, exp_len):
        """One ADS request-reply cycle."""
        invoke_id, self._invoke_id = self._invoke_id, self._invoke_id + 1
        msg = REQ_HEADER.pack(AMS_HEADER_SIZE + len(payload),
                              self._amsnetaddr, self._myamsnetaddr, cmd, 0x4,
                              len(payload), 0, invoke_id) + payload
        expected = REP_HEADER_SIZE + 4 + exp_len
        self._socket.sendall(msg)
        reply = b''
        rephdr = None
        while len(reply) < expected:
            data = self._socket.recv(expected - len(reply))
            if not data:
                raise CommError('no data in read')
            reply += data
            if len(reply) >= REP_HEADER_SIZE and not rephdr:
                rephdr = REP_HEADER.unpack_from(reply)
                if rephdr[4] != 0x5:
                    raise CommError('wrong flags in reply header')
                if rephdr[5] != len(data) - REP_HEADER_SIZE:
                    raise CommError('wrong length in reply header')
                if rephdr[6]:
                    raise CommError('error set in reply packet: %s' %
                                    self._translate_error(rephdr[6]))
                if rephdr[7] != invoke_id:
                    raise CommError('wrong InvokeID on reply packet')
        # check the error field that's only present if there is no general
        # error with the request (e.g. port not found)
        if reply[REP_HEADER_SIZE:REP_HEADER_SIZE+4] != b'\0\0\0\0':
            error = ADS_ERRID.unpack_from(reply, REP_HEADER_SIZE)[0]
            raise CommError('error set in reply packet: %s' %
                            self._translate_error(error))
        return reply[REP_HEADER_SIZE+4:]

    def _translate_error(self, errorcode):
        return ADS_ERRORS.get(errorcode,
                              'Unknown code %#04x' % errorcode)

    def _set_route(self, sockname):
        """Try to set up an ADS route on the target."""
        routename = 'zapf-' + sockname[0]
        udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        mynetid = pack('<Q', self._myamsnetaddr)[:6]
        # The default password is different for different TwinCAT versions.
        # Just try both.
        for password in (b'', b'1'):
            message = UDP_MESSAGE.pack(
                UDP_MAGIC,
                UDP_ADD_ROUTE,
                self._myamsnetaddr,
                5,
                UDP_ROUTENAME, 25, routename.encode(),
                UDP_NETID, 6, mynetid,
                UDP_USERNAME, 14, b'Administrator',
                UDP_PASSWORD, 2, password,
                UDP_HOST, 16, sockname[0].encode(),
            )
            udpsock.sendto(message, (self._iphostport[0], BECKHOFF_UDP_PORT))
        time.sleep(0.5)


ADS_ERRORS = {
    0x001: 'Internal error',
    0x002: 'No Rtime',
    0x003: 'Allocation locked memory error',
    0x004: 'Insert mailbox error',
    0x005: 'Wrong receive HMSG',
    0x006: 'Target port not found',
    0x007: 'Target machine not found',
    0x008: 'Unknown command ID',
    0x009: 'Bad task ID',
    0x00A: 'No IO',
    0x00B: 'Unknown AMS command',
    0x00C: 'Win32 error',
    0x00D: 'Port not connected',
    0x00E: 'Invalid AMS length',
    0x00F: 'Invalid AMS NetID',
    0x010: 'Low installation level',
    0x011: 'No debug available',
    0x012: 'Port disabled',
    0x013: 'Port already connected',
    0x014: 'AMS Sync Win32 error',
    0x015: 'AMS Sync Timeout',
    0x016: 'AMS Sync AMS error',
    0x017: 'AMS Sync no index map',
    0x018: 'Invalid AMS port',
    0x019: 'No memory',
    0x01A: 'TCP send error',
    0x01B: 'Host unreachable',

    0x500: 'Router: no locked memory',
    0x502: 'Router: mailbox full',

    0x700: 'Error class: device error',
    0x701: 'Service is not supported by server',
    0x702: 'Invalid index group',
    0x703: 'Invalid index offset',
    0x704: 'Reading/writing not permitted',
    0x705: 'Parameter size not correct',
    0x706: 'Invalid parameter value(s)',
    0x707: 'Device is not in a ready state',
    0x708: 'Device is busy',
    0x709: 'Invalid context (must be in Windows)',
    0x70A: 'Out of memory',
    0x70B: 'Invalid parameter value(s)',
    0x70C: 'Not found (files, ...)',
    0x70D: 'Syntax error in command or file',
    0x70E: 'Objects do not match',
    0x70F: 'Object already exists',
    0x710: 'Symbol not found',
    0x711: 'Symbol version invalid',
    0x712: 'Server is in invalid state',
    0x713: 'AdsTransMode not supported',
    0x714: 'Notification handle is invalid',
    0x715: 'Notification client not registered',
    0x716: 'No more notification handles',
    0x717: 'Size for watch too big',
    0x718: 'Device not initialized',
    0x719: 'Device has a timeout',
    0x71A: 'Query interface failed',
    0x71B: 'Wrong interface required',
    0x71C: 'Class ID is invalid',
    0x71D: 'Object ID is invalid',
    0x71E: 'Request is pending',
    0x71F: 'Request is aborted',
    0x720: 'Signal warning',
    0x721: 'Invalid array index',

    0x740: 'Error class: client error',
    0x741: 'Invalid parameter at service',
    0x742: 'Polling list is empty',
    0x743: 'Var connection already in use',
    0x744: 'Invoke ID in use',
    0x745: 'Timeout elapsed',
    0x746: 'Error in Win32 subsystem',
    0x748: 'ADS port not opened',
    0x750: 'Internal error in ADS sync',
    0x751: 'Hash table overflow',
    0x752: 'Key not found in hash',
    0x753: 'No more symbols in cache',
}
