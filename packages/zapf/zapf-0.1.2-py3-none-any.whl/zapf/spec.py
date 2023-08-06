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

"""Contains all necessary constants and mappings from the spec."""

from zapf.util import BitFields, ParamMap, UncasedMap

SUPPORTED_MAGICS = ['2015_02']

OFFSET_ADDR = 4

INDEXER_DEV = 0

INFO_STRUCT  = 0
INFO_SIZE    = 1
INFO_ADDR    = 2
INFO_UNIT    = 3
INFO_NAME    = 4
INFO_VERSION = 5
INFO_AUTHOR1 = 6
INFO_AUTHOR2 = 7
INFO_PARAMS  = 15
INFO_AUX1    = 16
INFO_CYCLE   = 127


UNIT_CODES    = ('', 'V', 'A', 'W', 'm', 'g', 'Hz', 'T', 'K', 'degC', 'degF',
                 'bar', 'deg', 'Ohm', 'm/s', 'm^2/s', 'm^3/s', 's', 'cts',
                 'bar/s', 'bar/s^2', 'F', 'H', 'l/min')
UNIT_EXPONENT = {0: '', 2: 'h', 3: 'k', 6: 'M', 9: 'G', 12: 'T', 15: 'P',
                 18: 'E', -1: 'd', -2: 'c', -3: 'm', -6: 'u', -9: 'n',
                 -12: 'f', -15: 'a'}
UNIT_SPECIAL  = {(-2, 0): '%', (-3, 16): 'l/s'}

FLOAT32_MAX = 3.402823e+38
FLOAT64_MAX = 1.7976931348623158e+308

StatusStruct = BitFields(STATE=(15, 12), REASON=(11, 8), AUX=(7, 0))
ParamControl = BitFields(CMD=(15, 13), SUBINDEX=(12, 8), IDX=(7, 0))

ReasonMap = [
    '',
    'inhibit',
    'timeout',
    '(inhibit, timeout)',
    'lower limit reached',
    '(inhibit, lower limit)',
    '(timeout, lower limit)',
    '(inhibit, timeout, lower limit)',
    'upper limit reached',
    '(inhibit, upper limit)',
    '(timeout, upper limit)',
    '(inhibit, timeout, upper limit)',
    'both limits reached',
    '(inhibit, both limits)',
    '(timeout, both limits)',
    '(inhibit, timeout, both limits)',
]

ParamCMDs = UncasedMap(
    INIT=0,
    DO_READ=1,
    DO_WRITE=2,
    BUSY=3,
    DONE=4,
    ERR_NO_IDX=5,
    ERR_RO=6,
    ERR_RETRY=7,
)

PLCStatus = UncasedMap(
    RESET=0,
    IDLE=1,
    DISABLED=2,
    WARN=3,
    START=5,
    BUSY=6,
    STOP=7,
    ERROR=8,
    DIAGNOSTIC_ERROR=13,
)

# The first (numbered) parameter whose value is float instead of integer.
FIRST_FLOAT_PARAM = 30

# Parameter 0 should not be used.
Parameters = ParamMap(
    UNUSED=0,
    Mode=1,
    Microsteps=2,
    CoderBits=3,
    ExtStatus=4,
    # HwOffset=5,
    AbsMin=30,  # deprecated
    AbsMax=31,  # deprecated
    UserMin=32,
    UserMax=33,
    WarnMin=34,
    WarnMax=35,
    TimeoutTime=36,
    MaxTravelDist=37,
    AccelTime=38,
    Offset=40,
    BlockSize=43,
    Opening=44,
    PidP=51,
    PidI=52,
    PidD=53,
    DragError=55,
    Hysteresis=56,
    Holdback=57,
    RefSpeed=58,
    Jerk=59,
    Speed=60,
    Accel=61,
    IdleCurrent=62,
    RampCurrent=63,
    MoveCurrent=64,
    StopCurrent=65,
    # AbortDecel=66,
    LegacyMicrosteps=67,  # deprecated
    Slope=68,
    RefPos=69,
    Setpoint=70,

    # special functions

    FactoryReset=128,
    RefMinus=131,  # deprecated
    RefPlus=132,  # deprecated
    Ref=133,
    SetPosition=137,
    ContMove=142,
)


def is_function(idx):
    return 128 <= idx < 192 or 224 <= idx < 240
