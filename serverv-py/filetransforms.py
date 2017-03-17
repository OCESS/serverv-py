"""Functions that copy file io functionality of serverv.bas."""
from os import SEEK_SET
import struct  # Reading floats from bytearrays


def simulator_HABeng_orb5res_parse(src, file_vars):
    """Block 300."""
    if file_vars['RCload'] != 0:
        src.seek(255, SEEK_SET)
        file_vars['Rt'] = int.from_bytes(
            src.read(2), byteorder='little') + file_vars['RCload'] * 4


def simulator_HABeng_orb5res_transform(file_contents, file_vars):
    """Block 320."""
    if file_vars['RCload'] != 0:
        file_contents[255:256] = file_vars['Rt'].to_bytes(
            2, byteorder='little')
    if file_vars['FCenable'] == 0:
        file_contents[293:294] = (3).to_bytes(2, byteorder='little')


def HABeecom_HABeng_gastelemetry_parse(src, file_vars):
    """Block 400."""
    # Note we're doing float/int equality. I dunno man, I just copy
    # serverv.bas1
    src.seek(323, SEEK_SET)
    file_vars['PROBEflag'] = struct.unpack_from("<f", src.read(4))[0]
    src.seek(251, SEEK_SET)
    file_vars['RCload'] = struct.unpack_from("<f", src.read(4))[0]
    src.seek(399, SEEK_SET)
    file_vars['O2a1'] = struct.unpack_from("<f", src.read(4))[0]
    file_vars['O2a2'] = struct.unpack_from("<f", src.read(4))[0]
    src.seek(415, SEEK_SET)
    file_vars['O2b1'] = struct.unpack_from("<f", src.read(4))[0]
    file_vars['O2b2'] = struct.unpack_from("<f", src.read(4))[0]
    if file_vars['O2a1'] > 0 and file_vars['O2a2'] == 1:
        file_vars['FCenable'] = 1
    if file_vars['O2b1'] > 0 and file_vars['O2b2'] == 1:
        file_vars['FCenable'] = 1


def HABeecom_HABeng_gastelemetry_transform(file_contents, file_vars):
    """Block 420."""
    pass
