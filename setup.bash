#!/usr/bin/env bash
# This script is idempotent. i.e. if you want to run it
# again and again, you can.

set -eo pipefail

if [[ "`basename $PWD`" != serverv-py ]] || [[ ! -d '.git' ]]; then
  echo 'Need to source this in the serverv-py repo, exiting'
  exit 1
fi

echo ''
echo 'Installing python virtualenv...'
virtualenv -p python3 --prompt '(serverv-py)' .

echo ''
echo 'Installing python packages...'
source bin/activate
pip install -r requirements.txt

# Error on unused variables, but after bin/activate because it would fail.
set -u

#  We don't do anything with OSbackup.RND right now, we'll not care about it.
# echo ''
# echo 'wgetting large blobs into orbit-files...'
# # Too big to store on github, and it's just the same file x9, really.
# # If this link ever goes dead, get it from the spacesim.org website.
# wget 'https://csclub.uwaterloo.ca/~pj2melan/OSbackup.RND'
# for dir in a b c d g h i j k; do
#   cp -v OSbackup.RND "orbit-files/$dir/"
# done
# rm -v OSbackup.RND

# Optional, for textual diffs of .RND files.
if ! grep -qF '[diff "rnd"]' .git/config; then
  printf '[diff "rnd"]\n\ttextconv = xxd\n\tcachetextconv = true\n\tbinary = true\n' >> .git/config
fi
