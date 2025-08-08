rm *funcs.py  CGI-BIN/*funcs.py CGI-BIN/ksta.py
cp /nfs/OGN/src/funcs/parserfuncs.py CGI-BIN
cp /nfs/OGN/src/funcs/dtfuncs.py     CGI-BIN
cp /nfs/OGN/src/funcs/ksta.py        CGI-BIN
git add .
git commit
git push origin master
