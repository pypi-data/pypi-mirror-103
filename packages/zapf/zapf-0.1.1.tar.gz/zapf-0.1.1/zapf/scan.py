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

"""Support for scanning the indexer and creating devices."""

from collections import namedtuple

from zapf import spec
from zapf.device import Device
from zapf.io import PlcIO

DeviceInfo = namedtuple('DeviceInfo', 'number name addr typecode info')


class Scanner:
    def __init__(self, io_or_proto, log):
        self.log = log
        if isinstance(io_or_proto, PlcIO):
            self.io = io_or_proto
        else:
            self.io = PlcIO(io_or_proto, log)

    def get_plc_data(self):
        """Establish communication with the indexer and return it."""
        self.io.indexer.detect_plc()
        return self.io.indexer

    def get_devices(self, _device_filter=None):
        """Scan the PLC and yield device objects."""
        for data in self.scan_devices():
            devcls = Device.class_for(data.typecode)
            if devcls is None:
                self.log.warning('type code %#x is not supported, skipping',
                                 data.typecode)
            else:
                yield devcls(data.number, data.name, data.addr, data.typecode,
                             data.info, self.io, self.log)

    def scan_devices(self):
        """Scan the PLC and yield information about devices."""

        # ensure we can talk to the indexer
        self.io.indexer.detect_plc()

        # check which method we need to scan
        method = getattr(self, 'scan_' + self.io.indexer.magicstr, None)
        if not method:
            raise RuntimeError('Magic %s is supported, but no scanner method '
                               'available' % self.io.indexer.magicstr)

        yield from method()

    def scan_2015_02(self):
        indexer = self.io.indexer
        next_addr = indexer.addr + indexer.size

        for devnum in range(1, 256):
            info = indexer.query_infostruct(devnum)
            typecode, size, addr, unit, flags, absmin, absmax, name = info

            # gone past last device?
            if typecode == 0:
                break

            # if there is not valid data in the infostruct, query individually
            if size + addr + flags == 0 and not name:
                size = indexer.query_word(devnum, spec.INFO_SIZE)
                if not size:
                    size = 2 * (typecode & 0xff)
                addr = indexer.query_word(devnum, spec.INFO_ADDR)
                if not addr:
                    addr = next_addr
                unit = indexer.query_unit(devnum, spec.INFO_UNIT)
                flags = None
                lowlevel = False
                absmin = -spec.FLOAT32_MAX
                absmax = spec.FLOAT32_MAX
            else:
                lowlevel = (flags & 0x80000000) != 0

            # this might be empty even if a valid infostruct was present,
            # e.g. if the full name didn't fit behind the 20 previous bytes
            if not name:
                name = indexer.query_string(devnum, spec.INFO_NAME)

            # extract info about parameters and special functions
            devclass = typecode >> 13
            parameters = []
            functions = []
            if devclass in (1, 2):
                if devclass == 1:  # FlatDevices: a list of indices
                    plist = indexer.query_bytes(devnum, spec.INFO_PARAMS)
                    param_ids = [p for p in plist if p]
                else:  # ParamDevices: a bitmap of indices
                    param_ids = indexer.query_bitmap(devnum, spec.INFO_PARAMS)
                param_ids.sort()  # ... which *should* be unnecessary
                for p in param_ids:
                    if spec.is_function(p):
                        functions.append(spec.Parameters[p])
                    else:
                        parameters.append(spec.Parameters[p])

            # extract AUX string labels
            aux_strings = [''] * 24
            if flags is None:  # old way, stop reading the first empty one
                for idx in range(24):
                    aux_string = indexer.query_string(devnum,
                                                      spec.INFO_AUX1 + idx)
                    aux_strings[idx] = aux_string.strip()
                    if not aux_string:
                        break
            else:  # new way, only read the relevant (flagged ones)
                for idx in range(24):
                    if flags & (1 << idx):
                        aux_string = indexer.query_string(devnum,
                                                          spec.INFO_AUX1 + idx)
                        aux_strings[idx] = aux_string.strip()

            info = dict(lowlevel=lowlevel, unit=unit,
                        absmin=absmin, absmax=absmax,
                        params=parameters, funcs=functions,
                        aux_strings=aux_strings)
            self.log.info('found device %s at addr %s with type %#x',
                          name, addr, typecode)
            yield DeviceInfo(devnum, name, addr, typecode, info)

            next_addr = addr + size
