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

"""Basic test suite for the scanner."""

from zapf.device import typecode_description

from zapf.scan import Scanner


def test_scan(plc_io):
    scanner = Scanner(plc_io, plc_io.log)

    plc_data = scanner.get_plc_data()
    assert plc_data.indexer_addr == 64
    assert plc_data.indexer_size == 36
    assert plc_data.plc_name == 'lazy test plc'
    assert plc_data.plc_author == 'anonymous\ncoward'
    assert plc_data.plc_version == '0.0.1alpha'

    for devinfo in scanner.scan_devices():
        # the test devices have the same name as the typecode description
        assert typecode_description(devinfo.typecode) == devinfo.name
