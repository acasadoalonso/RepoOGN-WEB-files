#!/usr/bin/python3
#
# gather the WX record from the APRS file and decode it
#

# example:   grep OGNDVS /nfs/OGN/DIRdata/DATA* | grep LEZS | tail -n 20 | python ~/src/APRSsrc/wx.py
#import cgi
import os
import sys
#import cgitb

import ksta
import sys
import datetime

from parserfuncs import parseraprs
import fileinput
msg={}
stations=[]				    # list of shown stations
html1 = """<HTML><TITLE>Get the meteo information</TITLE> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>The meteo observations for the selected ICAO station (%s) are: </H1> """
html2 = """<center><table><tr><td><pre>"""
html3 = """</pre></td></tr></table></center></html>"""

www = True
streq = sys.argv[1:]
if streq:
    sta = streq[0]                          # request the station
    sta = sta.upper()
    sta = sta.strip()
    #print("Station: ", sta)
else:
    sta = "Lillo"                            # take it as default
    print("Lillo (LELT) by default ...")

if www:
    print((html1 % sta))
if www:
    print(html2)
maxrecords=50

################
date = datetime.datetime.now()
dte = date.strftime("%y%m%d")       # today's date
filename="/nfs/OGN/DIRdata/DATA"+dte+".log"
filename="/nfs/OGN/DIRdata/DATA.active"
#
for line in reversed(list(open(filename))):
    #print(line.rstrip())
    #print ("LLL:", line)
    parseraprs(line, msg)
    if msg['source'] != 'WTX':
       continue
    station = msg['station']

    #print ("SSS", station, stations)          
    if sta == 'ALL' :
       if station in stations:
          continue
       else: 
          stations.append(station)
    else:
       if station.upper() != sta.upper():
          continue
       
    #print ("MMM", msg)
    windspeed=msg['windspeed']
    if windspeed == ' ':
       continue
    tempf=msg['temp']
    humidity=msg['humidity']
    rain=msg['rain']
    if tempf != ' ' and tempf != 0:
       #print ("TTT", tempf)
       tempc = round((float(tempf)-32)*5/9, 2)
    else:
       tempc=0.0
    message=""
    if tempc != 0.0:
       message += " Temp: %.2fºC"%tempc
    if humidity != ' ':
       message +=  " Humidity: "+msg['humidity']+"%"
    if rain != ' ':
       message +=  " Rain: "+msg['rain']+"mm/h"
    if station.upper() in ksta.ksta:
       print ("Station:", msg['station'], ksta.ksta[station.upper()], "Time (UTC):", msg['otime'], "Wind (dir/spd/burst):", msg['windspeed'], message)
    else:
       print ("Station:", msg['station'],                             "Time (UTC):", msg['otime'], "Wind (dir/spd/burst):", msg['windspeed'], message)
    maxrecords -= 1
    if maxrecords == 0:
       break

################
if www:
    print(html3)

