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
    ./serverv-py/server.py --sevpath orbit-files/sevpath.RND --piloting 127.0.0.1:31415

### Testing:

    # Will run server.py for a few seconds, then exit.
    # Also checks that no .RND files were changed after running,
    # and spins up a very basic server to receive network messages.
    ./test.bash

### Source files:

There are a few sources in `serverv-py/serverv-py`. The most important is
`server.py`, which contains the main event loop and calls other modules.

- `server.py`: Actually runs everything asynchronously.
- `filetransforms.py`: Generalized helper logic for copying files between legacy
  QB clients.
- `qb_communication.py`: Actually does the copying of files between
  legacy QB clients
- `piloting_state.py`: Reads and keeps track of the piloting state, i.e.
  `STARSr` data file.
- `utility.py`: A few common helper functions used by different modules.
