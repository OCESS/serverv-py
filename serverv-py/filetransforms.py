"""Functions that copy file io functionality of serverv.bas."""
from os import SEEK_SET
import struct  # Reading floats from bytearrays


def _mki(integer): return integer.to_bytes(2, byteorder='little')


def _cvi(twobytes): return int.from_bytes(twobytes, byteorder='little')


def _mks(single): return struct.pack("<f", single)


def _cvs(fourbytes): return struct.unpack("<f", fourbytes)[0]


def simulator_orb5res_parse(src, file_vars):
    """Block 300."""
    if file_vars['RCload'] != 0:
        src.seek(255, SEEK_SET)
        file_vars['Rt'] = _cvi(src.read(2)) + file_vars['RCload'] * 4


def simulator_orb5res_transform(file_contents, file_vars):
    """Block 320."""
    if file_vars['RCload'] != 0:
        file_contents[255:256] = _mki(file_vars['Rt'])
    if file_vars['FCenable'] == 0:
        file_contents[293:294] = _mki(3)


def HABeecom_gastelemetry_parse(src, file_vars):
    """Block 400."""
    # Note we're doing float/int equality. I dunno man, I just copy serverv.bas
    src.seek(323, SEEK_SET)
    file_vars['PROBEflag'] = _cvs(src.read(4))
    src.seek(251, SEEK_SET)
    file_vars['RCload'] = _cvs(src.read(4))
    src.seek(399, SEEK_SET)
    file_vars['O2a1'] = _cvs(src.read(4))
    file_vars['O2a2'] = _cvs(src.read(4))
    src.seek(415, SEEK_SET)
    file_vars['O2b1'] = _cvs(src.read(4))
    file_vars['O2b2'] = _cvs(src.read(4))
    if file_vars['O2a1'] > 0 and file_vars['O2a2'] == 1:
        file_vars['FCenable'] = 1
    if file_vars['O2b1'] > 0 and file_vars['O2b2'] == 1:
        file_vars['FCenable'] = 1


def HABeecom_gastelemetry_transform(file_contents, file_vars):
    """Block 420."""
    pass


def MCeecom_gasmc_parse(src, file_vars):
    """Block 500."""
    pass


def MCeecom_gasmc_transform(file_contents, file_vars):
    """Block 510 - 520."""
    pass


def SIMeecom_gassim_parse(src, file_vars):
    """Block 600."""
    pass


def SIMeecom_gassim_transform(file_contents, file_vars):
    """Block 610."""
    pass


def SIMeecom_doorsim_parse(src, file_vars):
    """Block 700."""
    pass


def SIMeecom_doorsim_transform(file_contents, file_vars):
    """Block 710."""
    file_contents[267:268] = _mki(file_vars['PACKblock'])
    file_contents[269:271] = _mki(file_vars['RCblock'])
    file_contents[271:274] = _mks(file_vars['IS2'])


def HABeng_orbitsse_parse(src, file_vars):
    """Block 800."""
    pass


def HABeng_orbitsse_transform(file_contents, file_vars):
    """Block 810 - 820."""
    pass
