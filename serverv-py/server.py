#!/usr/bin/env python3
"""Aims to clone serverv.bas."""
import argparse
from pathlib import PureWindowsPath, PurePath, Path
import asyncio
import signal
import functools
import warnings

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
        assert self._srcpath.stat().st_size == self._filesize
        with self._srcpath.open('rb') as src:
            file_contents = bytearray(src.read(self._filesize))
            assert file_contents[0] == file_contents[-1]
        precontents_len = len(file_contents)
        self._transform(file_contents, file_vars)
        assert len(file_contents) == precontents_len
        for destpath in self._destpaths:
            with destpath.open('wb') as dest:
                dest.write(file_contents)
            assert destpath.stat().st_size == self._filesize


file_vars = {}

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
    FileConnector('SIMeecom', ['HABeecom'], 'DOORSIM.RND', 276),
    # Block 800
    FileConnector('HABeng', ['flight', 'telemetry',
                             'simulator', 'SIMmirror'], 'ORBITSSE.RND', 1159),
    # Block 900
    FileConnector('display', ['flight', 'mirror'], 'MST.RND', 26),
    # Block 930
    FileConnector('MCeecom', ['HABeecom', 'MCeecom'], 'TIME.RND', 26)
]


def update_orbit_files(event_loop):
    """Read, update all .RND files at 1 Hz. Helper for event loop."""
    reschedule_time = event_loop.time() + 1.0
    print('Updating orbit_files at', event_loop.time())
    for connector in file_connectors:
        connector.process_src()
    for connector in file_connectors:
        connector.write_to_dest()
    event_loop.call_at(reschedule_time, update_orbit_files, event_loop)


def request_exit(signal=None):
    """Ask event loop to finish all callbacks and exit."""
    if signal is not None:
        print("Got signal", signal, "and shutting down.")
    event_loop.stop()


# Set up signal handler and call update_orbit_files.
event_loop = asyncio.get_event_loop()
for signame in ('SIGINT', 'SIGTERM'):
    event_loop.add_signal_handler(getattr(signal, signame),
                                  functools.partial(request_exit, signame))
event_loop.call_soon(update_orbit_files, event_loop)

# Debug mode gives us useful information for development.
event_loop.set_debug(True)
warnings.simplefilter('always', ResourceWarning)

# Run until event_loop.stop() is called.
event_loop.run_forever()
event_loop.close()

print(file_vars)
