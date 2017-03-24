### Setup:

    git clone https://github.com/OCESS/serverv-py
    ./setup.sh
    source bin/activate

### Usage:

    # source bin/activate if you haven't done so in the current session
    ./serverv-py/server.py --sevpath orbit-files/sevpath.RND

### Testing:

    # Will run server.py for a few seconds, then exit.
    # Also checks that no .RND files were changed after running.
    ./test.sh
