#!/usr/bin/python3
import cgi
import os
import cgitb
import sys
import config
from geopy.geocoders import Nominatim
#
# Get all the flight by date
#
if config.MySQL:

    import MySQLdb                  # the SQL data base routines^M
    conn = MySQLdb.connect(host=config.DBhost, user=config.DBuser,
                           passwd=config.DBpasswd, db=config.DBname)
else:
    import sqlite3
    conn = sqlite3.connect(config.DBpath+config.DBSQLite3)
curs  = conn.cursor()
curs2 = conn.cursor()

setcmd1 = "set global sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
setcmd2 = "set session sql_mode='STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';"
if config.MySQL:

    curs.execute(setcmd1)
    curs.execute(setcmd2)


cgitb.enable()
datereq = sys.argv[1:]                  # first parameter
if datereq:
    dt = datereq[0]                     # get the registration
else:
    dt = ''
#                    select count(*), max(altitude), max(distance) from OGNDATA where idflarm = 'DDE48A' and date = '260815' ;

html1 = """<head><meta charset="UTF-8"></head><TITLE>Get the flights</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The flights for the selected date are: </H1> <HR> <P> %s </P> </HR> """
#html1="""<TITLE>Get the flights</TITLE> <H1>The OGN flights for the selected date are: </H1> <HR> <P> %s </P> </HR> """
html2 = """<center><table><tr><td><pre>"""
html3 = """</pre></td></tr></table></center>"""
html4 = '<a href="http://cunimb.net/igc2map.php?lien=http://' + \
    config.reposerver+'/DIRdata/fd/'

rootdir = config.DBpath+"/fd"
nlines = 0

if dt == '':
    print((html1 % 'Invalid date'))
else:
    dd = dt[0:2]
    mm = dt[2:4]
    yy = dt[4:6]
    dir = rootdir+'/Y'+yy+'/M'+mm
    if int(dd) > 0 and int(dd) < 32 and int(mm) > 0 and int(mm) < 13 and int(yy) > 14 and int(yy) < 23  and os.path.isdir(dir):
        vd = ('Valid date: %s-%s-%s. </br>Select now the flight to display:' %
              (dd, mm, yy))
    else:
        vd = "Invalid date ...==> "+dd+mm+yy
    print((html1 % vd))
    print(html2)
    if os.path.isdir(dir):   
        ld = os.listdir(dir)
    else:
        ld=''
    for f in ld:
        if f[0:2] == "FD" and f[2:4] == yy and f[4:6] == mm and f[6:8] == dd:
            if f[-3:] == '.gz':
               id = f[-16:-7]
            else:
               id = f[-13:-4]
            dte = yy+mm+dd
            cnt = 0
            alt = 0.0
            dst = 0.0
            addr = ''
            lati = 0.0
            longi = 0.0
            selcmd = "select count(*), max(altitude) as maxa, max(distance) as maxd from OGNDATA where idflarm = '%s' and date = '%s' " % (id, dte)
            curs.execute(selcmd)
            reg = curs.fetchone()
            #print ( ">>>>", id , reg , selcmd)
            if reg and reg != None:
                cnt = reg[0]
                if cnt == None:
                    cnt = 0
                alt = reg[1]
                if alt == None:
                    alt = 0.0
                dst = reg[2]
                if dst == None:
                    dst = 0.0
                #geolocator = Nominatim(timeout=20)
                geolocator = Nominatim(user_agent="Repoogn",timeout=20)

                execmd = "select max(altitude) as maxa, latitude, longitude from OGNDATA where idflarm = '%s' and date = '%s' " % (id, dte)
                curs2.execute(execmd)
                reg = curs2.fetchone()
                if reg and reg != None:
                    malt = reg[0]
                    if malt == alt:
                        lati = reg[1]
                        longi = reg[2]
                        #loc = geolocator.reverse([lati,long])
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
                 
                 ff = '/nfs/OGN/DIRdata/fd/Y' + yy + '/M' + mm + '/' + f.lstrip()
                 os.system('gunzip '+ff)
                 fn = html4 + 'Y' + yy + '/M' + mm + '/' + f[0:-3].lstrip()
            else:
                 ff=''
                 fn = html4 + 'Y' + yy + '/M' + mm + '/' + f.lstrip()
 
            fname = ("FN:%-33s %s" % (f, ff))
            fname = ("FN:%-33s " % f)
            print(fn, '">MAP</a>', "<a>", fname, details,  "</a>")
    if nlines == 0:
        print("No flights found")
    print(html3)
exit(0)
