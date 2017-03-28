# What is this?

This project is a rewrite of OCESS' server program in the
kind-of distributed client-server model that is Spacesim's
collective QuickBasic infrastructure. To maintain some
backwards compatibility, but not restrict ourselves to
old software, this Python server will be able to mediate
the existing legacy communication and also use modern
communication e.g. communication with a `node.js` server.

Since the legacy logic of this server has been mostly cloned
from the legacy server (`serverv.bas`), there will be a bit
of code smell so be aware. It should mostly be contained.

For the legacy server, see the `notes` directory. My chicken
scratchings of understanding the legacy code are also in there.

### Setup:

    git clone https://github.com/OCESS/serverv-py
    ./setup.bash
    source bin/activate

### Usage:

    # source bin/activate if you haven't done so in the current session
    ./serverv-py/server.py --sevpath orbit-files/sevpath.RND

### Testing:

    # Will run server.py for a few seconds, then exit.
    # Also checks that no .RND files were changed after running.
    ./test.sh
