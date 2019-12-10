#!/usr/bin/python3
import cgi
import os
import cgitb
import sqlite3
import sys
import config
from geopy.geocoders import Nominatim


#
# Get IGC file by registration
#

def scandir(dir, rpath, html4, curs, curs2):
    nlines = 0
    ld = os.listdir(dir)
    ld.sort()
    for f in ld:
        if f[0:2] == "FD" and f.find(rg) != -1:
            id = f[-13:-4]
            dte = f[2:8]
            alt = 0.0
            dst = 0.0
            cnt = 0
            addr = ''
            selcmd = "select count(*), max(altitude) as maxa, max(distance) as maxd from OGNDATA where idflarm = '%s' and date = '%s' " % (id, dte)
            curs.execute(selcmd)
            reg = curs.fetchone()
            if reg and reg != None:
                cnt = reg[0]
                if cnt > 0:
                    alt = reg[1]
                    dst = reg[2]
                #geolocator = Nominatim(timeout=5)
                execmd = "select max(altitude) as maxa, latitude, longitude from OGNDATA where idflarm = '%s' and date = '%s' " % (id, dte)
                curs2.execute(execmd)
                reg = curs2.fetchone()
                if reg and reg != None:
                    malt = reg[0]
                    if malt == alt:
                        lati = reg[1]
                        longi = reg[2]
                        addr = ''
                        #loc = geolocator.reverse([lati,long])
                        # if loc.address != None:
                        # addr=(loc.address).encode('utf8')
                        addr = ' '
                    else:
                        lati = 0.0
                        longi = 0.0
                        addr = ''
            nlines += 1
            if cnt > 0:
                details = (" ==> Count(%4d) MDist(%5.1f) MAlt(%6.1f) Lat(%7.4f) Long(%7.4f) %s " % (cnt, dst, alt, lati, longi, addr))
            else:
                details = " "
            if f[-3:] == '.gz':
                 
                 ff = '/nfs/OGN/DIRdata/fd/' + rpath + '/' + f.lstrip()
                 os.system('gunzip '+ff)
                 fn = html4 + rpath + '/' + f[0:-3].lstrip()
            else:
                 ff=''
                 fn = html4 + rpath + '/' + f.lstrip()

            fname = ("FN:%-33s %s" % (f, ff))
            fname = ("FN:%-33s " % f)
            print(fn, '">MAP</a>', "<a>", fname, details,  "</a>")
        elif (os.path.isdir(dir+'/'+f)):
            nlines += scandir(dir+'/'+f, rpath+'/'+f, html4, curs, curs2)
    return(nlines)
#
# Main code
#

setcmd1 = "set global sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';"
setcmd2 = "set session sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION';"
rootdir = config.DBpath+"/fd"
if config.MySQL:

    import MySQLdb                  # the SQL data base routines^M
    conn = MySQLdb.connect(host=config.DBhost, user=config.DBuser,
                           passwd=config.DBpasswd, db=config.DBname)
else:

    import sqlite3
    conn = sqlite3.connect(config.DBpath+config.DBSQLite3)

curs  = conn.cursor()
curs2 = conn.cursor()

if config.MySQL:
    curs.execute(setcmd1)
    curs.execute(setcmd2)

cgitb.enable()
# select distinct date  from OGNDATA where idflarm=(select idglider from GLIDERS where registration = 'D-2520') ;
regist = sys.argv[1:]			# first parameter
if regist:
    rr = regist[0]                      # get the registration
else:
    rr = ''
html1 = """<head><meta charset="UTF-8"></head><TITLE>Get the flights</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The flights for the selected registration are: </H1> <HR> <P> %s </P> </HR> """
html2 = """<center><table><tr><td><pre>"""
html3 = """</pre></td></tr></table></center>"""
html4 = '<a href="http://cunimb.net/igc2map.php?lien=http://' + \
    config.reposerver+'/DIRdata/fd'
nlines = 0

if rr == '':
    print((html1 % 'Invalid  registration'))
else:
    rg = rr.strip()
    rg = rg.upper()
    cmd = "select cn from GLIDERS where registration = '%s' " % rg
    curs.execute(cmd)
    reg = curs.fetchone()
    if reg and reg != None:
        cn = reg[0]
    else:
        cn = ''
    vd = ('Valid registration: %-s %s:' % (rg, cn))
    print((html1 % vd))
    print(html2)
    nlines = scandir(rootdir, "", html4, curs, curs2)
    if nlines == 0:
        print("No flights found for:", rg)
    print(html3)
exit(0)
