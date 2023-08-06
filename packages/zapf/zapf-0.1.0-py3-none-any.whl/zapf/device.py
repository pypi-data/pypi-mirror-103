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

"""Basic device abstraction for PILS devices."""

import time

from zapf import ApiError, SpecError
from zapf.spec import FIRST_FLOAT_PARAM, ParamCMDs, ParamControl, Parameters, \
    PLCStatus, SpecialFunctions, StatusStruct, FLOAT64_MAX, FLOAT32_MAX
from zapf.util import UncasedMap


START16 = PLCStatus.START << 12
START32 = PLCStatus.START << 28


class Device:
    @classmethod
    def class_for(cls, typecode):
        return PLC_CLASSES.get(typecode)

    valuetype = None

    def __init__(self, name, addr, typecode, params, funcs, io, log):
        self.name = name
        self.addr = addr
        self.target_addr = None
        self.status_addr = None
        self.param_addr = None
        self.device_kind = typecode >> 8
        self.total_size = 2 * (typecode & 0xff)
        self.value_size = None
        self.status_size = None
        self.params = params
        self.funcs = funcs
        self.log = log
        self.io = io
        self.init()
        self.io.register_cache_range(self.addr, self.total_size)

    def read_status(self):
        if self.status_addr is None:
            return StatusStruct(PLCStatus.IDLE << 12)
        if self.status_size == 2:
            return StatusStruct(self.io.read_u16(self.status_addr))
        return StatusStruct(self.io.read_u32(self.status_addr) >> 16)

    def read_extended_status(self):
        if self.status_addr is None:
            return (StatusStruct(PLCStatus.IDLE << 12), 0, 0)
        if self.status_size == 2:
            return (StatusStruct(self.io.read_u16(self.status_addr)), 0, 0)
        elif self.status_size == 4:
            value = self.io.read_u32(self.status_addr)
            return (StatusStruct(value >> 16), value & 0xFFFF, 0)
        elif self.status_size == 8:  # actually 6, but this is easier
            value = self.io.read_u64(self.status_addr)
            return (StatusStruct(value >> 48), (value >> 32) & 0xFFFF,
                    (value >> 16) & 0xFFFF)
        raise SpecError('invalid status_size')

    def change_status(self, initial_states=(), final_state=0):
        if self.status_addr is None:
            return False
        status = self.read_status()
        if status.STATE in initial_states:
            status.STATE = final_state
            if self.status_size == 2:
                self.io.write_u16(self.status_addr, int(status))
            else:
                self.io.write_u32(self.status_addr, int(status) << 16)
            return True
        return False

    # to implement:

    def init(self):
        raise NotImplementedError

    def get_limits(self):
        raise NotImplementedError

    def read_value(self):
        raise NotImplementedError

    def read_target(self):
        raise ApiError('reading target of a read-only device')

    def change_target(self, value):
        raise ApiError('writing target of a read-only device')

    def list_params(self):
        return []

    def get_param(self, name):
        raise ApiError('reading parameter of a device without params')

    def set_param(self, name, value):
        raise ApiError('writing parameter of a device without params')

    def list_funcs(self):
        return []

    def exec_func(self, name, value=None):
        raise ApiError('executing function of a device without functions')


class DiscreteDevice(Device):
    def init(self):
        pass

    def get_limits(self):
        if self.value_size == 2:
            return (-2**15, 2**15 - 1)
        elif self.value_size == 4:
            return (-2**31, 2**31 - 1)
        elif self.value_size == 8:
            return (-2**63, 2**63 - 1)
        raise SpecError('invalid value_size')

    def read_value(self):
        return self.io.read_fmt(self.addr, self.value_fmt)[0]

    def read_target(self):
        if self.target_addr is None:
            raise ApiError('reading target of a read-only device')
        return self.io.read_fmt(self.target_addr, self.value_fmt)[0]

    def change_target(self, value):
        if self.target_addr is None:
            raise ApiError('writing target of a read-only device')
        if self.value_size == 2:
            self.io.write_fmt(self.target_addr, self.value_fmt + 'H',
                              value, START16)
        else:
            self.io.write_fmt(self.target_addr, self.value_fmt + 'I',
                              value, START32)


INT_FMT = {2: 'h', 4: 'i', 8: 'q'}


class SimpleDiscreteIn(DiscreteDevice):
    def init(self):
        self.value_size = self.total_size
        self.value_fmt = INT_FMT[self.value_size]


class SimpleDiscreteOut(DiscreteDevice):
    def init(self):
        self.value_size = self.total_size // 2
        self.value_fmt = INT_FMT[self.value_size]
        self.target_addr = self.addr + self.value_size


class DiscreteIn(DiscreteDevice):
    def init(self):
        self.value_size = self.status_size = self.total_size // 2
        self.value_fmt = INT_FMT[self.value_size]
        self.status_addr = self.addr + self.value_size


class DiscreteOut(DiscreteDevice):
    def init(self):
        self.value_size = self.status_size = self.total_size // 3
        self.value_fmt = INT_FMT[self.value_size]
        self.target_addr = self.addr + self.value_size
        self.status_addr = self.target_addr + self.value_size


class Keyword(DiscreteDevice):
    def init(self):
        self.value_size = self.total_size
        self.value_fmt = INT_FMT[self.value_size].upper()
        self.target_addr = self.addr

    def get_limits(self):
        if self.value_size == 2:
            return (0, 2**16 - 1)
        elif self.value_size == 4:
            return (0, 2**32 - 1)
        elif self.value_size == 8:
            return (0, 2**64 - 1)
        raise SpecError('invalid value_size')


class StatusWord(Keyword):
    def init(self):
        Keyword.init(self)
        self.status_addr = self.addr
        self.status_size = self.value_size


class AnalogDevice(Device):
    def init(self):
        pass

    def get_limits(self):
        if self.value_size == 4:
            return (-FLOAT32_MAX, FLOAT32_MAX)
        elif self.value_size == 8:
            return (-FLOAT64_MAX, FLOAT64_MAX)
        raise SpecError('invalid value_size')

    def read_value(self):
        if self.value_size == 4:
            return self.io.read_f32(self.addr)
        elif self.value_size == 8:
            return self.io.read_f64(self.addr)
        raise SpecError('invalid value_size')

    def read_target(self):
        if self.target_addr is None:
            raise ApiError('reading target of a read-only device')
        if self.value_size == 4:
            return self.io.read_f32(self.target_addr)
        elif self.value_size == 8:
            return self.io.read_f64(self.target_addr)
        raise SpecError('invalid value_size')

    def change_target(self, value):
        if self.target_addr is None:
            raise ApiError('writing target of a read-only device')
        if self.value_size == 4:
            if self.status_size == 2:
                self.io.write_f32_u16(self.target_addr, value, START16)
            else:
                self.io.write_f32_u32(self.target_addr, value, START32)
        elif self.value_size == 8:
            self.io.write_fmt(self.target_addr, 'dI', value, START32)


class SimpleAnalogIn(AnalogDevice):
    def init(self):
        self.value_size = self.total_size


class SimpleAnalogOut(AnalogDevice):
    def init(self):
        self.value_size = self.total_size // 2
        self.target_addr = self.addr + self.value_size


class AnalogIn(AnalogDevice):
    def init(self):
        if self.total_size == 6:
            # 32-bit with 16 bit status
            self.value_size = 4
            self.status_size = 2
        else:
            self.value_size = self.status_size = self.total_size // 2
        self.status_addr = self.addr + self.value_size


class AnalogOut(AnalogDevice):
    def init(self):
        if self.total_size == 10:
            # 32-bit with 16 bit status
            self.value_size = 4
            self.status_size = 2
        else:
            self.value_size = self.status_size = self.total_size // 3
        self.target_addr = self.addr + self.value_size
        self.status_addr = self.target_addr + self.value_size


class RealValue(AnalogDevice):
    def init(self):
        self.value_size = self.total_size
        self.target_addr = self.addr


class FlatParams:
    def init(self):
        if self.number != len(self.params):
            raise SpecError('mismatch between parameter count between '
                            'typecode and parameter indices from indexer '
                            f'({self.number}/{len(self.params)})')
        # sort params from indexer by index
        pars_indices = sorted((Parameters[par], par) for par in self.params)
        self.param_map = UncasedMap(*(
            (par[1], (self.param_addr + i * self.value_size, par[0]))
            for (i, par) in enumerate(pars_indices)
        ))

    def list_params(self):
        return self.param_map.init_keys()

    def get_param(self, name):
        (addr, idx) = self.param_map.get(name, (None, None))
        if addr:
            if idx < FIRST_FLOAT_PARAM:
                if self.value_size == 4:
                    return ParamCMDs.DONE, self.io.read_u32(addr)
                else:
                    return ParamCMDs.DONE, self.io.read_u64(addr)
            else:
                if self.value_size == 4:
                    return ParamCMDs.DONE, self.io.read_f32(addr)
                else:
                    return ParamCMDs.DONE, self.io.read_f64(addr)
        return ParamCMDs.ERR_NO_IDX, None

    def set_param(self, name, value):
        (addr, idx) = self.param_map.get(name, (None, None))
        if addr:
            if idx < FIRST_FLOAT_PARAM:
                if self.value_size == 4:
                    self.io.write_u32(addr, int(value))
                    return ParamCMDs.DONE, self.io.read_u32(addr)
                else:
                    self.io.write_u64(addr, int(value))
                    return ParamCMDs.DONE, self.io.read_u64(addr)
            else:
                if self.value_size == 4:
                    self.io.write_f32(addr, value)
                    return ParamCMDs.DONE, self.io.read_f32(addr)
                else:
                    self.io.write_f64(addr, value)
                    return ParamCMDs.DONE, self.io.read_f64(addr)
        return ParamCMDs.ERR_NO_IDX, None


class FlatIn(FlatParams, AnalogDevice):
    def init(self):
        self.number = (self.device_kind & 0xf) + 1
        self.value_size = self.total_size // (self.number + 2)
        self.status_size = 2 if self.value_size == 4 else 8
        self.status_addr = self.addr + self.value_size
        self.param_addr = self.status_addr + self.status_size
        FlatParams.init(self)


class FlatOut(FlatParams, AnalogDevice):
    def init(self):
        self.number = (self.device_kind & 0xf) + 1
        self.value_size = self.total_size // (self.number + 3)
        self.status_size = 2 if self.value_size == 4 else 8
        self.target_addr = self.addr + self.value_size
        self.status_addr = self.target_addr + self.value_size
        self.param_addr = self.status_addr + self.status_size
        FlatParams.init(self)


class ParamInterface:
    param_timeout = 1

    def init(self):
        self.pctrl_addr = self.status_addr + (2 if self.value_size == 4 else 6)
        self.param_addr = self.pctrl_addr + 2
        self.param_map = UncasedMap(*((p, Parameters[p])
                                      for p in self.params))
        self.func_map = UncasedMap(*((p, SpecialFunctions[p])
                                     for p in self.funcs))
        self.sm = ParamControl()

    def _update_sm(self):
        self.sm(self.io.read_u16(self.pctrl_addr))

    def _wait_sm_available(self):
        self._update_sm()
        timesout = time.time() + self.param_timeout
        while not self.sm.available:
            self._update_sm()
            if time.time() > timesout:
                return False
        return True

    def _set_param_value(self, idx, value):
        if idx < FIRST_FLOAT_PARAM:
            if self.value_size == 4:
                self.io.write_u32(self.param_addr, int(value))
            else:
                self.io.write_u64(self.param_addr, int(value))
        else:
            if self.value_size == 4:
                self.io.write_f32(self.param_addr, value)
            else:
                self.io.write_f64(self.param_addr, value)

    def _set_param_value_and_cmd(self, cmd, sub, idx, value):
        self.sm.CMD = cmd
        self.sm.SUB = sub
        self.sm.IDX = idx
        if idx < FIRST_FLOAT_PARAM:
            if self.value_size == 4:
                self.io.write_fmt(self.pctrl_addr, 'HI', int(self.sm), int(value))
            else:
                self.io.write_fmt(self.pctrl_addr, 'HQ', int(self.sm), int(value))
        else:
            if self.value_size == 4:
                self.io.write_u16_f32(self.pctrl_addr, int(self.sm), value)
            else:
                self.io.write_fmt(self.pctrl_addr, 'Hd', int(self.sm), value)

    def _set_param_cmd(self, cmd, sub, idx):
        self.sm.CMD = cmd
        self.sm.SUB = sub
        self.sm.IDX = idx
        self.io.write_u16([self.pctrl_addr, int(self.sm)])

    def _get_param_value(self, idx):
        if idx < FIRST_FLOAT_PARAM:
            if self.value_size == 4:
                return self.io.read_u32(self.param_addr)
            else:
                return self.io.read_u64(self.param_addr)
        else:
            if self.value_size == 4:
                return self.io.read_f32(self.param_addr)
            else:
                return self.io.read_f64(self.param_addr)

    def list_params(self):
        return self.param_map.init_keys()

    def get_param(self, name):
        idx = self.param_map.get(name)
        if idx:
            if self._wait_sm_available():
                self._set_param_cmd(ParamCMDs.DO_READ, self.subdev, idx)
                # now wait until setting parameter is finished and
                # return read-back-value
                if self._wait_sm_available():
                    return self.sm.CMD, self._get_param_value(idx)
            return ParamCMDs.ERR_RETRY, None
        return ParamCMDs.ERR_NO_IDX, None

    def set_param(self, name, value):
        idx = self.param_map.get(name)
        if idx:
            if self._wait_sm_available():
                self._set_param_value_and_cmd(ParamCMDs.DO_WRITE,
                                              self.subdev, idx, value)
                # now wait until setting parameter is finished and
                # return read-back-value
                if self._wait_sm_available():
                    return self.sm.CMD, self._get_param_value(idx)
            return ParamCMDs.ERR_RETRY, None
        return ParamCMDs.ERR_NO_IDX, None

    def list_funcs(self):
        return self.func_map.init_keys()

    def exec_func(self, name, value=None):
        idx = self.func_map.get(name)
        if idx:
            self._update_sm()
            if self.sm.CMD == ParamCMDs.BUSY and \
               self.sm.SUB == self.subdev and \
               self.sm.IDX == idx:
                self._set_param_value(idx, value)
                if self._wait_sm_available():
                    return self.sm.CMD, self._get_param_value(idx)
                return self.sm.CMD, self._get_param_value(idx)  # still BUSY
            if self._wait_sm_available():
                self._set_param_value_and_cmd(ParamCMDs.DO_WRITE,
                                              self.subdev, idx, value)
                # now wait until setting parameter is finished and return
                # read-back-value
                if self._wait_sm_available():
                    return self.sm.CMD, self._get_param_value(idx)
                return self.sm.CMD, self._get_param_value(idx)  # still BUSY
            return ParamCMDs.ERR_RETRY, None
        return ParamCMDs.ERR_NO_IDX, None


class ParamIn(ParamInterface, AnalogDevice):
    def init(self):
        self.value_size = self.total_size // 3
        self.status_size = 2 if self.value_size == 4 else 8
        self.status_addr = self.addr + self.value_size
        ParamInterface.init(self)


class ParamOut(ParamInterface, AnalogDevice):
    def init(self):
        self.value_size = self.total_size // 4
        self.status_size = 2 if self.value_size == 4 else 8
        self.target_addr = self.addr + self.value_size
        self.status_addr = self.target_addr + self.value_size
        ParamInterface.init(self)


class VectorDevice(Device):
    def init(self):
        pass

    def get_limits(self):
        if self.value_size == 4:
            return (-FLOAT32_MAX, FLOAT32_MAX)
        elif self.value_size == 8:
            return (-FLOAT64_MAX, FLOAT64_MAX)
        raise SpecError('invalid value_size')

    def read_value(self):
        if self.value_size == 4:
            return self.io.read_f32s(self.addr, self.number)
        elif self.value_size == 8:
            return self.io.read_f64s(self.addr, self.number)
        raise SpecError('invalid value_size')


class VectorIn(ParamInterface, VectorDevice):
    def init(self):
        self.number = (self.device_kind & 0xf) + 1
        self.value_size = self.total_size // (self.number + 2)
        self.status_size = 2 if self.value_size == 4 else 8
        self.status_addr = self.addr + self.value_size*self.number
        ParamInterface.init(self)


class VectorOut(ParamInterface, VectorDevice):
    def init(self):
        self.number = (self.device_kind & 0xf) + 1
        self.value_size = self.total_size // (2*self.number + 2)
        self.status_size = 2 if self.value_size == 4 else 8
        self.target_addr = self.addr + self.value_size*self.number
        self.status_addr = self.target_addr + self.value_size*self.number
        ParamInterface.init(self)

    def read_target(self):
        if self.value_size == 4:
            return self.io.read_f32s(self.target_addr, self.number)
        elif self.value_size == 8:
            return self.io.read_f64s(self.target_addr, self.number)
        raise SpecError('invalid value_size')

    def change_target(self, value):
        if self.value_size == 4:
            self.io.write_f32s_u16(self.target_addr, value, START16)
        elif self.value_size == 8:
            self.io.write_f64s_u32(self.target_addr, value, START32)


PLC_CLASSES = {
    0x1201: SimpleDiscreteIn,   # 16 bit
    0x1202: SimpleDiscreteIn,   # 32 bit
    0x1204: SimpleDiscreteIn,   # 64 bit
    0x1302: SimpleAnalogIn,     # 32 bit
    0x1304: SimpleAnalogIn,     # 64 bit
    0x1401: Keyword,            # 16 bit
    0x1402: Keyword,            # 32 bit
    0x1404: Keyword,            # 64 bit
    0x1502: RealValue,          # 32 bit
    0x1504: RealValue,          # 64 bit
    0x1602: SimpleDiscreteOut,  # 16 bit
    0x1604: SimpleDiscreteOut,  # 32 bit
    0x1608: SimpleDiscreteOut,  # 64 bit
    0x1704: SimpleAnalogOut,    # 32 bit
    0x1708: SimpleAnalogOut,    # 64 bit
    0x1801: StatusWord,         # simple
    0x1802: StatusWord,         # extended
    0x1a02: DiscreteIn,         # 16 bit
    0x1a04: DiscreteIn,         # 32 bit
    0x1a08: DiscreteIn,         # 64 bit
    0x1b03: AnalogIn,           # 32 bit with 16 bit status
    0x1b04: AnalogIn,           # 32 bit
    0x1b08: AnalogIn,           # 64 bit
    0x1e03: DiscreteOut,        # 16 bit
    0x1e06: DiscreteOut,        # 32 bit
    0x1e0c: DiscreteOut,        # 64 bit
    0x1f05: AnalogOut,          # 32 bit with 16 bit status
    0x1f06: AnalogOut,          # 32 bit
    0x1f0c: AnalogOut,          # 64 bit

    0x2006: FlatIn,             # 32 bit
    0x200c: FlatIn,             # 64 bit
    0x2108: FlatIn,             # 32 bit
    0x2110: FlatIn,             # 64 bit
    0x220a: FlatIn,             # 32 bit
    0x2214: FlatIn,             # 64 bit
    0x230c: FlatIn,             # 32 bit
    0x2318: FlatIn,             # 64 bit
    0x240e: FlatIn,             # 32 bit
    0x241c: FlatIn,             # 64 bit
    0x2510: FlatIn,             # 32 bit
    0x2520: FlatIn,             # 64 bit
    0x2612: FlatIn,             # 32 bit
    0x2624: FlatIn,             # 64 bit
    0x2714: FlatIn,             # 32 bit
    0x2728: FlatIn,             # 64 bit
    0x2816: FlatIn,             # 32 bit
    0x282c: FlatIn,             # 64 bit
    0x2918: FlatIn,             # 32 bit
    0x2930: FlatIn,             # 64 bit
    0x2a1a: FlatIn,             # 32 bit
    0x2a34: FlatIn,             # 64 bit
    0x2b1c: FlatIn,             # 32 bit
    0x2b38: FlatIn,             # 64 bit
    0x2c1e: FlatIn,             # 32 bit
    0x2c3c: FlatIn,             # 64 bit
    0x2d20: FlatIn,             # 32 bit
    0x2d40: FlatIn,             # 64 bit
    0x2e22: FlatIn,             # 32 bit
    0x2e44: FlatIn,             # 64 bit
    0x2f24: FlatIn,             # 32 bit
    0x2f48: FlatIn,             # 64 bit

    0x3008: FlatOut,            # 32 bit
    0x3010: FlatOut,            # 64 bit
    0x310a: FlatOut,            # 32 bit
    0x3114: FlatOut,            # 64 bit
    0x320c: FlatOut,            # 32 bit
    0x3218: FlatOut,            # 64 bit
    0x330e: FlatOut,            # 32 bit
    0x331c: FlatOut,            # 64 bit
    0x3410: FlatOut,            # 32 bit
    0x3420: FlatOut,            # 64 bit
    0x3512: FlatOut,            # 32 bit
    0x3524: FlatOut,            # 64 bit
    0x3614: FlatOut,            # 32 bit
    0x3628: FlatOut,            # 64 bit
    0x3716: FlatOut,            # 32 bit
    0x372c: FlatOut,            # 64 bit
    0x3818: FlatOut,            # 32 bit
    0x3830: FlatOut,            # 64 bit
    0x391a: FlatOut,            # 32 bit
    0x3934: FlatOut,            # 64 bit
    0x3a1c: FlatOut,            # 32 bit
    0x3a38: FlatOut,            # 64 bit
    0x3b1e: FlatOut,            # 32 bit
    0x3b3c: FlatOut,            # 64 bit
    0x3c20: FlatOut,            # 32 bit
    0x3c40: FlatOut,            # 64 bit
    0x3d22: FlatOut,            # 32 bit
    0x3d44: FlatOut,            # 64 bit
    0x3e24: FlatOut,            # 32 bit
    0x3e48: FlatOut,            # 64 bit
    0x3f26: FlatOut,            # 32 bit
    0x3f4c: FlatOut,            # 64 bit

    0x4006: ParamIn,            # 32 bit
    0x400c: ParamIn,            # 64 bit
    0x5008: ParamOut,           # 32 bit
    0x5010: ParamOut,           # 64 bit

    0x4108: VectorIn,           # 32 bit
    0x4110: VectorIn,           # 64 bit
    0x420a: VectorIn,           # 32 bit
    0x4214: VectorIn,           # 64 bit
    0x430c: VectorIn,           # 32 bit
    0x4318: VectorIn,           # 64 bit
    0x440e: VectorIn,           # 32 bit
    0x441c: VectorIn,           # 64 bit
    0x4510: VectorIn,           # 32 bit
    0x4520: VectorIn,           # 64 bit
    0x4612: VectorIn,           # 32 bit
    0x4624: VectorIn,           # 64 bit
    0x4714: VectorIn,           # 32 bit
    0x4728: VectorIn,           # 64 bit
    0x4816: VectorIn,           # 32 bit
    0x482c: VectorIn,           # 64 bit
    0x4918: VectorIn,           # 32 bit
    0x4930: VectorIn,           # 64 bit
    0x4a1a: VectorIn,           # 32 bit
    0x4a34: VectorIn,           # 64 bit
    0x4b1c: VectorIn,           # 32 bit
    0x4b38: VectorIn,           # 64 bit
    0x4c1e: VectorIn,           # 32 bit
    0x4c3c: VectorIn,           # 64 bit
    0x4d20: VectorIn,           # 32 bit
    0x4d40: VectorIn,           # 64 bit
    0x4e22: VectorIn,           # 32 bit
    0x4e44: VectorIn,           # 64 bit
    0x4f24: VectorIn,           # 32 bit
    0x4f48: VectorIn,           # 64 bit

    0x510c: VectorOut,          # 32 bit
    0x5118: VectorOut,          # 64 bit
    0x5210: VectorOut,          # 32 bit
    0x5220: VectorOut,          # 64 bit
    0x5314: VectorOut,          # 32 bit
    0x5328: VectorOut,          # 64 bit
    0x5418: VectorOut,          # 32 bit
    0x5430: VectorOut,          # 64 bit
    0x551c: VectorOut,          # 32 bit
    0x5538: VectorOut,          # 64 bit
    0x5620: VectorOut,          # 32 bit
    0x5640: VectorOut,          # 64 bit
    0x5724: VectorOut,          # 32 bit
    0x5748: VectorOut,          # 64 bit
    0x5828: VectorOut,          # 32 bit
    0x5850: VectorOut,          # 64 bit
    0x592c: VectorOut,          # 32 bit
    0x5958: VectorOut,          # 64 bit
    0x5a30: VectorOut,          # 32 bit
    0x5a60: VectorOut,          # 64 bit
    0x5b34: VectorOut,          # 32 bit
    0x5b68: VectorOut,          # 64 bit
    0x5c38: VectorOut,          # 32 bit
    0x5c70: VectorOut,          # 64 bit
    0x5d3c: VectorOut,          # 32 bit
    0x5d78: VectorOut,          # 64 bit
    0x5e40: VectorOut,          # 32 bit
    0x5e80: VectorOut,          # 64 bit
    0x5f44: VectorOut,          # 32 bit
    0x5f88: VectorOut,          # 64 bit
}
