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

"""Interaction with the indexer."""

import time

from zapf import SpecError, spec


class Indexer:
    def __init__(self, io, log):
        self.io = io
        self.log = log
        self.magicstr = None
        self.addr = None
        self.size = None
        self.num_devices = 0
        self.plc_name = None
        self.plc_version = None
        self.plc_author = None

    def detect_plc(self, extended=True):
        """Checks if the HW follows the spec and which MAGIC number it has.

        Afterwards, checks the indexer and reads extended meta information
        about the PLC if wanted.
        """
        if self.addr:
            return

        # check MAGIC
        magic = self.io.detect_magic()
        magicstr = ('%.2f' % round(magic, 4)).replace('.', '_')
        if magicstr not in spec.SUPPORTED_MAGICS:
            raise SpecError(f'magic {magicstr} is not supported by this client')
        self.magicstr = magicstr

        # read indexer offset from memory address 4
        addr = self.io.read_u16(spec.OFFSET_ADDR)
        if addr < 6 or addr & 1:
            raise SpecError('indexer offset %s is invalid' % addr)
        self.addr = addr

        # query indexer size
        size = self.query_word(spec.INDEXER_DEV, spec.INFO_SIZE)
        if size < 22 or size > 66 or size & 1:
            raise SpecError('indexer size %s is invalid' % size)
        self.size = size

        # query indexer size and offset again, through the info struct,
        # and ensure consistency
        info = self.query_infostruct(spec.INDEXER_DEV)
        if info[0] + info[1] + info[2] != 0:
            if info[0] != 0 or info[1] != size or info[2] != addr:
                raise SpecError('indexer information from infostruct does not '
                                'match with OFFSET or size')

            # total number of devices can be given in flags
            self.num_devices = info[4] & 0xFF

        # query firmware information
        if extended:
            self.plc_name = self.query_string(spec.INDEXER_DEV, spec.INFO_NAME)
            self.plc_version = self.query_string(spec.INDEXER_DEV,
                                                 spec.INFO_VERSION)
            author1 = self.query_string(spec.INDEXER_DEV, spec.INFO_AUTHOR1)
            author2 = self.query_string(spec.INDEXER_DEV, spec.INFO_AUTHOR2)
            self.plc_author = (author1 or 'Anonymous') + '\n' + author2

    # lowlevel methods to query the indexer

    def query_infostruct(self, devnum):
        # fields in the infostruct: typecode, size, addr, unitcode, unitexp,
        # flags, absmin, absmax, the rest is the name
        result = self.query_data(devnum, spec.INFO_STRUCT,
                                 'HHHBbIII%ds' % (self.size - 22))
        # convert min/max; these are floats, but we need to potentially word-
        # swap them
        absmin = self.io.float_from_dword(result[6])
        absmax = self.io.float_from_dword(result[7])
        # convert unit to a string
        unit = self.convert_unit(*result[3:5])
        # only use the name if it has a trailing null byte, so we can be
        # sure it was fully transferred in the reduced space at the end
        name_parts = result[-1].partition(b'\0')
        name = name_parts[0].decode('latin1') if name_parts[1] else ''
        return result[:3] + (unit, result[5], absmin, absmax, name)

    def query_word(self, devnum, infotype):
        return self.query_data(devnum, infotype, 'H')[0]

    def query_unit(self, devnum, infotype):
        return self.convert_unit(*self.query_data(devnum, infotype, 'Bb'))

    def query_string(self, devnum, infotype):
        result = self.query_bytes(devnum, infotype)
        return result.partition(b'\0')[0].decode('latin1')

    def query_bitmap(self, devnum, infotype):
        return [grp*8 + bit
                for grp, byte in enumerate(self.query_bytes(devnum, infotype))
                for bit in range(8)
                if byte & (1 << bit)]

    def query_bytes(self, devnum, infotype):
        return self.query_data(devnum, infotype, '%ds' % (self.size - 2))[0]

    # even lower level methods to do an indexer transaction

    def query_data(self, devnum, infotype, fmt):
        request = infotype << 8 | devnum
        self.io.write_u16s(self.addr, [request])
        for i in range(32):
            reply = self.io.read_fmt(self.addr, 'H' + fmt)
            if reply[0] == request | 0x8000:
                return reply[1:]
            # refresh the query if it got overwritten by a different host
            if reply[0] & 0x7fff != request:
                self.io.write_u16s(self.addr, [request])
            time.sleep(0.001*i*i)
        raise SpecError('indexer not responding in time!')

    def convert_unit(self, code, exponent):
        if (code, exponent) in spec.UNIT_SPECIAL:
            return spec.UNIT_SPECIAL[code, exponent]
        try:
            unit = spec.UNIT_CODES[code]
        except IndexError:
            unit = 'unit'
        if '^' in unit:
            return '10^%d %s' % (exponent, unit)
        return spec.UNIT_EXPONENT.get(exponent, '10^%d ' % exponent) + unit
