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
#   Enrico Faulhaber <enrico.faulhaber@frm2.tum.de>
#
# *****************************************************************************

# pylint: disable=invalid-name, unused-argument, no-value-for-parameter, line-too-long

from zapf.device import typecode_description
from zapf.simulator.funcs import adr, memcpy, memset, sizeof
from zapf.simulator.runtime import Globals, Struct, Var, array, boolean, \
    byte, dword, lreal, lword, program, real, string, word


class ST_DeviceInfo(Struct):
    TypCode = Var(word, 0)
    Size = Var(word, 0)
    Offset = Var(word, 0)
    Unit = Var(word, 0)
    Flags = Var(dword, 0)
    Params = Var(array(word, 1, 16), [0] * 16)
    Name = Var(string(34))
    Aux = Var(array(string(34), 0, 23))
    AbsMax = Var(real, 3.402823e38)
    AbsMin = Var(real, -3.402823e38)


class ST_Indexer(Struct):
    Request = Var(word, 0)
    Data = Var(array(word, 1, 17))


class DevicesLayout(Struct):
    # note: with this mapping a sensible sim isn't possible
    # as we don't know which of the overlayed devs was started...

    # used for sai64, sao64, ai64, ao64, rv64  (re-using aox_target as aix_value, rv64)
    ax64_value = Var(lreal, 0)             # 0..7
    ax64_target = Var(lreal, 0)            # 8..15
    ax64_estatus = Var(dword, 0x10000000)  # 16..19
    ax64_nerrid = Var(word, 0)             # 20..21
    ax64_reserved = Var(word, 0)           # 22..23
    # used for sai32, sao32, ai32, ao32, sw32 (re-using aox_target as aix_value)
    ax32_value = Var(real, 0)              # 24..27
    ax32_target = Var(real, 0)             # 28..31
    ax32_estatus = Var(dword, 0x10000000)  # 32..35
    # used for legacy_ai32, _ao32, rv32, sw16  (re-using aox_target as aix_value, rv32)
    lax32_value = Var(real, 0)             # 36..39
    lax32_target = Var(real, 0)            # 40..43
    lax32_status = Var(word, 0x1000)       # 44..45
    # used for sdi16, sdo16, di16, do16, kv16, sw16 (re-using dox_target as dix_value)
    dx16_value = Var(word, 0)              # 46..47
    dx16_target = Var(word, 0)             # 48..49
    dx16_status = Var(word, 0x1000)        # 50..51
    # used for sdi32, sdo32, di32, do32, kv32, sw32  (re-using dox_target as dix_value)
    dx32_value = Var(dword, 0)             # 52..55
    dx32_target = Var(dword, 0)            # 56..59
    dx32_estatus = Var(dword, 0x10000000)  # 60..63
    # used for sdi64, sdo64, di64, do64, kv64 (re-using dox_target as dix_value)
    dx64_value = Var(lword, 0)             # 64..71
    dx64_target = Var(lword, 0)            # 72..79
    dx64_estatus = Var(dword, 0x10000000)  # 80..83
    dx64_nerrid = Var(word, 0)             # 84..85
    dx64_reserved = Var(word, 0)           # 86..87
    # used for all flatin/out in 64 bit (re-using fo_target as fi_value)
    fax64_value = Var(lreal, 0)            # 88..95
    fax64_target = Var(lreal, 0)           # 96..103
    fax64_estatus = Var(dword, 0x10000000) # 104..107
    fax64_nerrid = Var(word, 0)            # 108..109
    fax64_reserved = Var(word, 0)          # 110..111
    # 112..239
    fax64_params = Var(array(lreal, 1, 16), [0, 100, 10, 90, 5, 500, 0, 10, 2, 0, 0.01, 0, 10, 1, 0, 0])

    # used for all pi/po/vectorin/out in 64 (re-using vo_target(s) as vi_value(s))
    # 240..495
    vx64_valuetargets = Var(array(lreal, 1, 32), [0] * 32)
    vx64_estatus = Var(dword, 0x10000000)  # 496..499
    vx64_nerrid = Var(word, 0)             # 500..501
    vx64_pctl = Var(word, 0)               # 502..503
    vx64_pvalue = Var(real, 0)             # 504..507
    # used for all pi/po/vectorin/out in 32 (re-using vo_target(s) as vi_value(s))
    # 508..635
    vx32_valuetargets = Var(array(real, 1, 32), [0] * 32)
    vx32_status = Var(word, 0x1000)        # 636..637
    vx32_pctl = Var(word, 0)               # 638..639
    vx32_pvalue = Var(real, 0)             # 640..643
    # used for all flatin/out in 32 bit (re-using fo_target as fi_value)
    fax32_value = Var(real, 0)             # 644..647
    fax32_target = Var(real, 0)            # 648..651
    fax32_status = Var(word, 0x1000)       # 652..653
    fax32_reserved = Var(word, 0)          # 654..655
    # 656..719
    fax32_params = Var(array(real, 1, 16), [0, 100, 10, 90, 5, 500, 0, 10, 2, 0, 0.01, 0, 10, 1, 0, 0])

AUX8 = ['AUX bit %d/8 is set!'%i for i in range(8)]
AUX24 = ['AUX bit %d/24 is set!'%i for i in range(24)]


class Global(Globals):
    fMagic = Var(real, 2015.02, at='%MB0')
    iOffset = Var(word, 64, at='%MB4')

    stIndexer = Var(ST_Indexer, at='%MB64')

    data = Var(DevicesLayout, at='%MB200')

    # note: Name fileds will be overriden later in Init(). here they are only a programming/ers hint.
    Devices = Var(array(ST_DeviceInfo, 1, 57), [
        ST_DeviceInfo(TypCode=0x1201, Name='sdi16', Offset=200+48),
        ST_DeviceInfo(TypCode=0x1202, Name='sdi32', Offset=200+56),
        ST_DeviceInfo(TypCode=0x1204, Name='sdi64', Offset=200+72),
        ST_DeviceInfo(TypCode=0x1302, Name='sai32', Offset=200+28),
        ST_DeviceInfo(TypCode=0x1304, Name='sai64', Offset=200+8),
        ST_DeviceInfo(TypCode=0x1401, Name='kw16', Offset=200+48),
        ST_DeviceInfo(TypCode=0x1402, Name='kw32', Offset=200+56),
        ST_DeviceInfo(TypCode=0x1404, Name='kw64', Offset=200+72),
        ST_DeviceInfo(TypCode=0x1502, Name='rv32', Offset=200+40),
        ST_DeviceInfo(TypCode=0x1504, Name='rv64', Offset=200+8),
        ST_DeviceInfo(TypCode=0x1602, Name='sdo16', Offset=200+46),
        ST_DeviceInfo(TypCode=0x1604, Name='sdo32', Offset=200+52),
        ST_DeviceInfo(TypCode=0x1608, Name='sdo64', Offset=200+64),
        ST_DeviceInfo(TypCode=0x1704, Name='sao32', Offset=200+24),
        ST_DeviceInfo(TypCode=0x1708, Name='sao64', Offset=200+0),
        ST_DeviceInfo(TypCode=0x1801, Name='sw16', Offset=200+44, Aux=AUX8),
        ST_DeviceInfo(TypCode=0x1802, Name='sw32', Offset=200+32, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1a02, Name='di16', Offset=200+48, Aux=AUX8),
        ST_DeviceInfo(TypCode=0x1a04, Name='di32', Offset=200+56, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1a08, Name='di64', Offset=200+72, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1b03, Name='lai32', Offset=200+40, Aux=AUX8),
        ST_DeviceInfo(TypCode=0x1b04, Name='ai32', Offset=200+28, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1b08, Name='ai64', Offset=200+8, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1e03, Name='do16', Offset=200+46, Aux=AUX8),
        ST_DeviceInfo(TypCode=0x1e06, Name='do32', Offset=200+52, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1e0c, Name='do64', Offset=200+64, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1f05, Name='lao32', Offset=200+36, Aux=AUX8),
        ST_DeviceInfo(TypCode=0x1f06, Name='ao32', Offset=200+24, Aux=AUX24),
        ST_DeviceInfo(TypCode=0x1f0c, Name='ao64', Offset=200+0, Aux=AUX24),

        ST_DeviceInfo(TypCode=0x2006, Name='fa32i1', Offset=200+648, Unit=0xfd04, Aux=AUX8, Params=[0x20, 0]),
        ST_DeviceInfo(TypCode=0x2714, Name='fa32i8', Offset=200+648, Unit=0xfd04, Aux=AUX8, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0]),
        ST_DeviceInfo(TypCode=0x2f24, Name='fa32i16', Offset=200+648, Unit=0xfd04, Aux=AUX8, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0x3534, 0x3938, 0x3d3c, 0x4645, 0]),

        ST_DeviceInfo(TypCode=0x200c, Name='fa64i1', Offset=200+96, Unit=0xfd04, Aux=AUX24, Params=[0x20, 0]),
        ST_DeviceInfo(TypCode=0x2728, Name='fa64i8', Offset=200+96, Unit=0xfd04, Aux=AUX24, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0]),
        ST_DeviceInfo(TypCode=0x2f48, Name='fa64i16', Offset=200+96, Unit=0xfd04, Aux=AUX24, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0x3534, 0x3938, 0x3d3c, 0x4645, 0]),

        ST_DeviceInfo(TypCode=0x3008, Name='fa32o1', Offset=200+644, Unit=0xfd04, Aux=AUX8, Params=[0x20, 0]),
        ST_DeviceInfo(TypCode=0x3716, Name='fa32o8', Offset=200+644, Unit=0xfd04, Aux=AUX8, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0]),
        ST_DeviceInfo(TypCode=0x3f26, Name='fa32o16', Offset=200+644, Unit=0xfd04, Aux=AUX8, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0x3534, 0x3938, 0x3d3c, 0x4645, 0]),

        ST_DeviceInfo(TypCode=0x3010, Name='fa64o1', Offset=200+88, Unit=0xfd04, Aux=AUX24, Params=[0x20, 0]),
        ST_DeviceInfo(TypCode=0x372c, Name='fa64o8', Offset=200+88, Unit=0xfd04, Aux=AUX24, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0]),
        ST_DeviceInfo(TypCode=0x3f4c, Name='fa64o16', Offset=200+88, Unit=0xfd04, Aux=AUX24, Params=[0x2120, 0x2322, 0x2524, 0x3328, 0x3534, 0x3938, 0x3d3c, 0x4645, 0]),

        ST_DeviceInfo(TypCode=0x4006, Name='pi32', Offset=200+632, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x5008, Name='po32', Offset=200+628, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),

        ST_DeviceInfo(TypCode=0x400c, Name='pi64', Offset=200+488, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x5010, Name='po64', Offset=200+480, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),

        ST_DeviceInfo(TypCode=0x4108, Name='v2i32', Offset=200+628, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x4714, Name='v8i32', Offset=200+604, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x4f24, Name='v16i32', Offset=200+572, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),

        ST_DeviceInfo(TypCode=0x510c, Name='v2o32', Offset=200+620, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x5724, Name='v8o32', Offset=200+572, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x5f44, Name='v16o32', Offset=200+508, Unit=0xfe00, Aux=AUX8, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),

        ST_DeviceInfo(TypCode=0x4110, Name='v2i64', Offset=200+480, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x4728, Name='v8i64', Offset=200+432, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x4f48, Name='v16i64', Offset=200+368, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),

        ST_DeviceInfo(TypCode=0x5118, Name='v2o64', Offset=200+464, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x5748, Name='v8o64', Offset=200+368, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
        ST_DeviceInfo(TypCode=0x5f88, Name='v16o64', Offset=200+240, Unit=0xfe00, Aux=AUX24, Params=[0xe, 0, 0x197f, 0xffb8, 0x73, 0x0, 0x0, 0x0, 0x4221,]),
    ])

    sPLCName = Var(string(34), 'lazy test plc')
    sPLCVersion = Var(string(34), '0.0.1alpha')
    sPLCAuthor1 = Var(string(34), 'anonymous')
    sPLCAuthor2 = Var(string(34), 'coward')
    iCycle = Var(word, 0)

g = Global()


@program(
    nDevices = Var(word),
    devnum = Var(word),
    infotype = Var(word),
    is_initialized = Var(boolean, False),
    itemp = Var(byte),
    tempofs = Var(word))
def Indexer(v):
    if not v.is_initialized:
        v.tempofs = g.iOffset + sizeof(g.stIndexer)
        v.nDevices = sizeof(g.Devices) // sizeof(g.Devices[1])
        v.itemp = 1
        while v.itemp <= v.nDevices:
            dev = g.Devices[v.itemp]
            # for i in range(8):
            dev.Flags[[0]] = len(dev.Aux[0]) > 0
            dev.Flags[[1]] = len(dev.Aux[1]) > 0
            dev.Flags[[2]] = len(dev.Aux[2]) > 0
            dev.Flags[[3]] = len(dev.Aux[3]) > 0
            dev.Flags[[4]] = len(dev.Aux[4]) > 0
            dev.Flags[[5]] = len(dev.Aux[5]) > 0
            dev.Flags[[6]] = len(dev.Aux[6]) > 0
            dev.Flags[[7]] = len(dev.Aux[7]) > 0
            dev.Flags[[8]] = len(dev.Aux[8]) > 0
            dev.Flags[[9]] = len(dev.Aux[9]) > 0
            dev.Flags[[10]] = len(dev.Aux[10]) > 0
            dev.Flags[[11]] = len(dev.Aux[11]) > 0
            dev.Flags[[12]] = len(dev.Aux[12]) > 0
            dev.Flags[[13]] = len(dev.Aux[13]) > 0
            dev.Flags[[14]] = len(dev.Aux[14]) > 0
            dev.Flags[[15]] = len(dev.Aux[15]) > 0
            dev.Flags[[16]] = len(dev.Aux[16]) > 0
            dev.Flags[[17]] = len(dev.Aux[17]) > 0
            dev.Flags[[18]] = len(dev.Aux[18]) > 0
            dev.Flags[[19]] = len(dev.Aux[19]) > 0
            dev.Flags[[20]] = len(dev.Aux[20]) > 0
            dev.Flags[[21]] = len(dev.Aux[21]) > 0
            dev.Flags[[22]] = len(dev.Aux[22]) > 0
            dev.Flags[[23]] = len(dev.Aux[23]) > 0
            if dev.Size < (dev.TypCode & 0xff) << 1:
                dev.Size = (dev.TypCode & 0xff) << 1
            if dev.Offset == 0:
                dev.Offset = v.tempofs
            else:
                v.tempofs = dev.Offset
            v.tempofs += dev.Size
            v.itemp += 1
        v.is_initialized = True

    if g.fMagic != 2015.02:
        g.fMagic = 2015.02
    if g.iOffset != 64:
        g.iOffset = 64

    v.devnum = g.stIndexer.Request & 0xff
    v.infotype = (g.stIndexer.Request >> 8) & 0x7f

    data = g.stIndexer.Data

    # short cut, if there is no request, do nothing.
    if g.stIndexer.Request[[15]] == 1:
        if v.infotype == 127:
            data[1] = g.iCycle

        g.iCycle += 1
        return

    memset(adr(data), 0, sizeof(data))

    if v.devnum == 0:
        if v.infotype == 0:
            data[1] = 0
            data[2] = sizeof(g.stIndexer)
            data[3] = g.iOffset
            data[4] = 0
            data[5] = v.nDevices
            data[6] = 0x8000
        elif v.infotype == 1:
            data[1] = sizeof(g.stIndexer)
        elif v.infotype == 4:
            memcpy(adr(data), adr(g.sPLCName),
                   min(sizeof(g.sPLCName), sizeof(data)))
        elif v.infotype == 5:
            memcpy(adr(data), adr(g.sPLCVersion),
                   min(sizeof(g.sPLCVersion), sizeof(data)))
        elif v.infotype == 6:
            memcpy(adr(data), adr(g.sPLCAuthor1),
                   min(sizeof(g.sPLCAuthor1), sizeof(data)))
        elif v.infotype == 7:
            memcpy(adr(data), adr(g.sPLCAuthor2),
                   min(sizeof(g.sPLCAuthor2), sizeof(data)))
    elif v.devnum <= v.nDevices:
        dev = g.Devices[v.devnum]
        if v.infotype == 0:
            data[1] = dev.TypCode
            data[2] = dev.Size
            data[3] = dev.Offset
            data[4] = dev.Unit
            data[5] = dev.Flags
            data[6] = dev.Flags >> 16
            memcpy(adr(data[7]), adr(dev.AbsMin), sizeof(dev.AbsMin))
            memcpy(adr(data[9]), adr(dev.AbsMax), sizeof(dev.AbsMax))
            memcpy(adr(data[11]), adr(dev.Name),
                   min(sizeof(dev.Name), sizeof(data) - 20))
        elif v.infotype == 1:
            data[1] = dev.Size
        elif v.infotype == 2:
            data[1] = dev.Offset
        elif v.infotype == 3:
            data[1] = dev.Unit
        elif v.infotype == 4:
            memcpy(adr(data), adr(dev.Name),
                   min(sizeof(dev.Name), sizeof(data)))
        elif v.infotype == 15:
            memcpy(adr(data), adr(dev.Params),
                   min(sizeof(dev.Params), sizeof(data)))
        elif v.infotype >= 0x10 and v.infotype <= 0x27:
            memcpy(adr(data), adr(dev.Aux[v.infotype - 0x10]),
                   min(sizeof(dev.Aux[v.infotype - 0x10]), sizeof(data)))

    if v.infotype == 127:
        data[1] = g.iCycle

    g.stIndexer.Request[[15]] = 1
    g.iCycle += 1

# helper
def advance(value, target, status, usermin=0.0, usermax=100.0, warnmin=10.0, warnmax=90.0, speed=10.0):
    state = status >> 12
    reason = 0
    if state == 0:
        state = 1, 0
    elif state in [1, 3, 7]:
        state = 1 if warnmin <= value <= warnmax else 3
    elif state == 5:
        state,reason = (6, 0) if usermin <= target <= usermax else (8, 1)
    elif state == 6:
        if value == target:
            state, reason = 1, 0
        value += max(min((target - value), speed/20), -speed/20)
    target = max(min(usermax, target), usermin)
    if value < warnmin:
        reason |= 4
    if value > warnmax:
        reason |= 8

    return value, target, (state << 12) | (reason << 8)

# same as above but for 32 bit status fields
def advancE(value, target, status, *args, **kwds):
    v, t, s = advance(value, target, status >> 16, *args, **kwds)
    return v, t, s << 16


@program()
def Implementierung(v):
    d = g.data

    d.ax64_value, d.ax64_target, d.ax64_estatus = advancE(d.ax64_value.value, d.ax64_target.value, d.ax64_estatus.value)
    d.ax64_nerrid = d.ax64.estatus >> 15 if d.ax64_estatus[[31]] else 0

    d.ax32_value, d.ax32_target, d.ax32_estatus = advancE(d.ax32_value.value, d.ax32_target.value, d.ax32_estatus.value)

    d.lax32_value, d.lax32_target, d.lax32_estatus = advance(d.lax32_value.value, d.lax32_target.value, d.lax32_status.value)

    d.dx16_target &= 0xff
    if d.dx16_status >> 12 == 5:
        d.dx16_value = d.dx16_target
    d.dx16_status = 0x1000

    d.dx32_target &= 0xffff
    if d.dx32_estatus >> 28 == 5:
        d.dx32_value = d.dx32_target
    d.dx32_estatus = 0x10000000

    d.dx64_target &= 0xffffffff
    if d.dx64_estatus >> 28 == 5:
        d.dx64_value = d.dx64_target
    d.dx64_estatus = 0x10000000
    d.dx64_nerrid = d.dx64_target >> 30


    for i in range(1, 17):
        d.fax64_params[i] = max(0, d.fax64_params[i])
    d.fax64_value, d.fax64_target, d.fax64_estatus = advancE(d.fax64_value, d.fax64_target, d.fax64_estatus,
                                                             usermin=d.fax64_params[1], usermax=d.fax64_params[2],
                                                             warnmin=d.fax64_params[3], warnmax=d.fax64_params[4],
                                                             speed=d.fax64_params[13])
    d.fax64_nerrid = d.fax64.estatus >> 15 if d.fax64_estatus[[31]] else 0

    for i in range(1, 17):
        d.fax32_params[i] = max(0, d.fax32_params[i])
    d.fax32_value, d.fax32_target, d.fax32_status = advance(d.fax32_value, d.fax32_target, d.fax32_status,
                                                             usermin=d.fax32_params[1], usermax=d.fax32_params[2],
                                                             warnmin=d.fax32_params[3], warnmax=d.fax32_params[4],
                                                             speed=d.fax32_params[13])


    d.vx32_valuetargets[31], d.vx32_valuetargets[32], d.vx32_status = \
        advance(d.vx32_valuetargets[31].value, d.vx32_valuetargets[32].value, d.vx32_status.value)
    if d.vx32_status[[14]]:  # while start/busy/stop
        for i in range(1, 31):
            d.vx32_valuetargets[i] = d.vx32_valuetargets[31]
    # XXX: handle pctl.
    if not d.vx32_pctl[[15]]:  # there is some request -> ERR_NO_IDX
        d.vx32_pctl[[15]] = 1
        d.vx32_pctl[[15]] = 0
        d.vx32_pctl[[15]] = 1

    d.vx64_valuetargets[31], d.vx64_valuetargets[32], d.vx64_estatus = \
        advancE(d.vx64_valuetargets[31].value, d.vx64_valuetargets[32].value, d.vx64_estatus.value)
    if d.vx64_estatus[[30]]:  # while start/busy/stop
        for i in range(1, 31):
            d.vx64_valuetargets[i] = d.vx64_valuetargets[31]
    d.vx64_nerrid = d.vx64.estatus >> 15 if d.vx64_estatus[[31]] else 0
    # XXX: handle pctl.
    if not d.vx64_pctl[[15]]:  # there is some request -> ERR_NO_IDX
        d.vx64_pctl[[15]] = 1
        d.vx64_pctl[[15]] = 0
        d.vx64_pctl[[15]] = 1


@program()
def Init(v):
    i = 1
    while True:
        try:
            g.Devices[i].Name = typecode_description(int(g.Devices[i].TypCode+0))
            i+= 1
        except RuntimeError:
            break


@program(
    is_initialized = Var(boolean, False),
)
def Main(v):
    if not v.is_initialized:
        Init()
        v.is_initialized = True
    Indexer()
    Implementierung()
