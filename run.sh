# A small shell script that runs the server

srcdir=./src

# run
python3 $srcdir/server.py "$@";
# once done, clean up junk files
rm -f $srcdir/*.pyc;

