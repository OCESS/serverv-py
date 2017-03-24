#!/bin/sh

if [ "`basename $PWD`" != serverv-py ] || [ ! -d '.git' ]; then
  echo 'Need to source this in the serverv-py repo, exiting'
  exit 1
fi

echo ''
echo 'Installing python virtualenv...'
virtualenv -p python3 --prompt '(serverv-py)' .
VENV_EXIT=$?

echo ''
echo 'Installing python packages...'
. bin/activate
pip install -r requirements.txt
REQ_EXIT=$?

echo ''
echo 'wgetting large blobs...'
# Too big to store on github, and it's just the same file x9, really.
wget 'https://csclub.uwaterloo.ca/~pj2melan/OSbackup.RND'
WGET_EXIT=$?
for dir in a b c d g h i j k; do
  cp -v OSbackup.RND "orbit-files/$dir/"
  cpresult=$?
  [ $cpresult -eq 0 ] || WGET_EXIT=$cpresult
done
rm -v OSbackup.RND
rmresult=$?
[ $rmresult -eq 0 ] || WGET_EXIT=$rmresult

# Optional, for textual diffs of .RND files.
echo '[diff "rnd"]\n\ttextconv = xxd\n\tcachetextconv = true\n\tbinary = true' >> .git/config

echo ''
[ $VENV_EXIT -eq 0 ] || echo "virtualenv setup failed, exitcode=$VENV_EXIT."
[ $REQ_EXIT -eq 0 ] || echo "Installing of python packages failed, exitcode=$REQ_EXIT."
[ $WGET_EXIT -eq 0 ] || echo "Getting of large blobs failed: exitcode=$WGET_EXIT."
