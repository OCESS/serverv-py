#!/usr/bin/env python3
"""Aims to clone serverv.bas."""
import argparse
from pathlib import PureWindowsPath, PurePath, Path

import filetransforms


parser = argparse.ArgumentParser()
parser.add_argument("--sevpath", default="sevpath.RND",
                    help="Path to sevpath.RND")
args = parser.parse_args()


# Get paths to clients from sevpath.RND
clients = [
    "flight",
    "mirror",
    "telemetry",
    "simulator",
    "HABeecom",
    "MCeecom",
    "SIMeecom",
    "display",
    "HABeng",
    "SIMmirror",
    "HABdisplay"
]

client_path = {}
with open(args.sevpath, "r") as sevpaths:
    for client in clients:
        client_path[client] = Path(
            args.sevpath).parent / PureWindowsPath(sevpaths.read(25).strip())
del clients  # all information is now in client_path as the keys


# 1 flight (OSbackup.RND, ORBITSSE.RND, MST.RND, lastly RESTART.RND)
# 2 mirror (OSbackup.RND, MST.RND)
# 3 telemetry (OSbackup.RND, ORB5res.RND, ORBITSSE.RND)
# 4 simulator (OSbackup.RND, ORB5res.RND, ORBITSSE.RND, lastly engsimrs.RND)
# 5 hab eecom (GASTELEMETRY.RND, GASMC.RND, GASSIM.RND, DOORSIM.RND, TIME.RND, lastly EECOMrs.RND) # noqa: E501
# 6 MC eecom (GASTELEMETRY.RND, GASMC.RND, TIME.RND, lastly GASMCrs.RND)
# 7 sim eecom (OSbackup.RND, GASTELEMETRY.RND, GASMC.RND, GASSIM.RND, DOORSISM.RND, lastly gasRS1.RND and gasRS2.RND) # noqa: E501
# 8 display (OSbackup.RND, MST.RND, lastly MSTrs.RND)
# 9 hab eng (OSbackup.RND, ORB5res.RND, ORBITSSE.RND, lastly resetSSE.RND)
# 10 sim mirror (OSbackup.RND, ORBITSSE.RND)
# 11 hab display (OSbackup.RND)

def simplify_filename(filename):
    """Return the lowercase filename, no extensions."""
    return PurePath(filename.lower()).stem


class FileConnector:
    """Writes contents of src/filename to dest/filename.

    I noticed that serverv.bas does a lot of the following:
        read from path1/filename
        set global var based on file contents
        write to path2/filename

    This class seeks to generalize this logic.

    Call self.parsesrc to update 'global variables' (I know) in file_vars
    based on the contents of src/filename and then
    call self.write_to_dest to write the contents for src/filename
    to dest/filename, with a predefined transformation.
    """

    def __init__(self, src, dests, filename, filesize):
        """Simply set up instance."""
        self._srcpath = client_path[src] / filename
        self._destpaths = [client_path[dest] / filename for dest in dests]
        self._filesize = filesize
        # Programmatically get parse, transform functions from filetransforms
        # e.g. _parsesrc = simulator_orb5res_parse
        self._parsesrc = getattr(
            filetransforms,
            src + '_' + simplify_filename(filename) + '_parse')
        self._transform = getattr(
            filetransforms,
            src + '_' + simplify_filename(filename) + '_transform')

    def process_src(self):
        """Read src/filename and possibly changes variables in file_vars."""
        global file_vars
        with self._srcpath.open('rb') as src:
            self._parsesrc(src, file_vars)

    def write_to_dest(self):
        """Write src/filename to dest/filename with a transformation."""
        global file_vars
        if self._srcpath.stat().st_size != self._filesize:
            raise IOError(str(self._srcpath) + ' filesize was not ' +
                          str(self._filesize) + ' as expected')
        with self._srcpath.open('rb') as src:
            file_contents = bytearray(src.read(self._filesize))
            if file_contents[0] != file_contents[-1]:
                raise IOError(
                    'chkCAR check failed when reading ' + str(self._srcpath))
        self._transform(file_contents, file_vars)
        for destpath in self._destpaths:
            with destpath.open('wb') as dest:
                dest.write(file_contents)


file_vars = {'RCload': 0, 'Rt': 0, 'FCenable': 0,
             'PACKblock': 0, 'RCblock': 0, 'IS2': 0.0}

file_connectors = [
    # Block 300
    FileConnector('simulator', ['HABeng'], 'ORB5res.RND', 412),
    # Block 400
    FileConnector('HABeecom', ['MCeecom', 'SIMeecom'],
                  'GASTELEMETRY.RND', 800),
    # Block 500
    FileConnector('MCeecom', ['HABeecom', 'SIMeecom'], 'GASMC.RND', 82),
    # Block 600
    FileConnector('SIMeecom', ['HABeecom'], 'GASSIM.RND', 182),
    # Block 700
    FileConnector('SIMeecom', ['HABeecom'], 'DOORSIM.RND', 276)
]

for connector in file_connectors:
    connector.process_src()
for connector in file_connectors:
    connector.write_to_dest()

print(file_vars)
