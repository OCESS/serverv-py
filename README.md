### Setup:

    git clone https://github.com/OCESS/serverv-py
    virtualenv -p python3 serverv-py
    cd serverv-py
    source bin/activate
    pip install -r requirements.txt
    # Optional, view diffs to .RND files in git diff:
    echo '[diff "rnd"]\n\ttextconv = xxd\n\tcachetextconv = true\n\tbinary = true' >> .git/config

### Usage:

    # source bin/activate if you haven't done so in the current session
    ./serverv-py/server.py --sevpath orbit-files/sevpath.RND
