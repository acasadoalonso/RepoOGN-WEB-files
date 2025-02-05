#!/usr/bin/python3
import json
#import cgi
#import cgitb
import os
from socket import gethostbyname, gethostname
import urllib.request, urllib.error, urllib.parse
import sqlite3
import os
import sys
import config
import datetime
from datetime import timedelta
import ksta
#cgitb.enable()
# --------------------------------------#
# -*- coding: UTF-8 -*-

# --------------------------------------#
def fixcoding(addr):
        if addr != None:
                addr=addr.replace('á', 'a')
                addr=addr.replace('à', 'a')
                addr=addr.replace('â', 'a')
                addr=addr.replace('Á', 'A')
                addr=addr.replace('é', 'e')
                addr=addr.replace('è', 'e')
                addr=addr.replace('ê', 'e')
                addr=addr.replace('É', 'E')
                addr=addr.replace('í', 'i')
                addr=addr.replace('ì', 'i')
                addr=addr.replace('î', 'i')
                addr=addr.replace('Í', 'I')
                addr=addr.replace('ó', 'o')
                addr=addr.replace('ò', 'o')
                addr=addr.replace('ô', 'o')
                addr=addr.replace('Ó', 'O')
                addr=addr.replace('Ò', 'O')
                addr=addr.replace('ú', 'u')
                addr=addr.replace('ù', 'u')
                addr=addr.replace('û', 'u')
                addr=addr.replace('Ú', 'U')
                addr=addr.replace('ü', 'u')
                addr=addr.replace('ñ', 'n')
                addr=addr.replace('Ñ', 'N')
                addr=addr.replace('Ø', 'O')
                addr=addr.replace('Ã', 'a')
                addr=addr.replace('ƒ', 'f')
                addr=addr.replace('Â', 'a')
                addr=addr.replace('¶', '-')
                addr=addr.replace('…', '-')
                addr=addr.replace('Ë', 'E')
                addr=addr.replace('†', '-')
                addr=addr.replace('ä', '-')
                addr=addr.replace('Ł', 'L')
                addr=addr.replace('ł', 'l')
                addr=addr.replace('ł', '-')
        return addr


#
# Handling functions
#
def getrecdesc(receivers, rg):
    for rec in receivers:
       if rec["callsign"] == rg:
          descr=rec["description"]
          descr=fixcoding(descr)
          if len(descr) > 36:
             descr=descr[0:36]
          return (descr)

def getreccountry(receivers, rg):
    for rec in receivers:
       if rec["callsign"] == rg:
          country=rec["country"]
          return (country)

def getaprsip(aprsclients, rg):
    i=0
    while i < 5:
        aprs=aprsclients[i]
    
        for rec in aprs:
           if rec["username"].upper()  == rg.upper():
              ip=rec["addr_rem"]
              p=ip.index(':')
              ip=ip[0:p]
              return (ip)
        i += 1

def getaprsserver(aprsclients, rg, aprsservers):
    i=0
    while i < 5:
        aprs=aprsclients[i]
    
        for rec in aprs:
           if rec["username"].upper() == rg.upper():
              ip=rec["addr_loc"]
              p=ip.index(':')
              ip=ip[0:p]
              if ip in aprsservers:
                 return (aprsservers[ip])
              else:
                 return(ip)
        i += 1

def getaprstconnect(aprsclients, rg):
    i=0
    while i < 5:
        aprs=aprsclients[i]
    
        for rec in aprs:
           if rec["username"].upper() == rg.upper():
              tc=rec["t_connect"]
              tt=datetime.datetime.fromtimestamp(tc)
              return (tt)
        i += 1

def getaprsslr(aprsclients, rg):
    i=0
    while i < 5:
        aprs=aprsclients[i]
    
        for rec in aprs:
           if rec["username"].upper() == rg.upper():
              slr=rec["since_last_read"]
              td=timedelta(seconds=slr)
              return (td)
        i += 1
def getaprsrec(aprsclients, rg):
    i=0
    while i < 5:
        aprs=aprsclients[i]
    
        for rec in aprs:
           if rec["username"].upper() == rg.upper():
              return (rec)
        i += 1
def upddescri(key, curs):
    descri=''
    if key in ksta.ksta:
       gid = ksta.ksta[key]   	# report the station name
       updcmd = "update RECEIVERS SET descri='"+gid+"' where idrec='"+key+"';"
       print ("Desc:", key, gid, updcmd)
       curs.execute(updcmd)
       descri=gid
    return (descri)
##############################################################################################################
#
# Main program
#

www = True
streq = sys.argv[1:]
if streq:
    sta = streq[0]                        # request the station
    sta = sta.upper()
    rg = sta.strip()
else:
    rg = "ALL"                            # take it as default
dbpath = config.DBpath
#
# get the stations info for the WIKI page
#
s_obj=""
receivers="{}"
s = urllib.request.urlopen('http://ogn.peanutpod.de/receivers.json')
ss= s.read().decode('utf-8')
if ss[0] == '{':
   s_obj = json.loads(ss)

if "receivers" in s_obj:
   receivers=s_obj["receivers"]
else:
   print ("no data from peanutpod ...")

#
# Get the information for the APRS servers
#
i=1					# the names of the servers go from 1 to 5 (so far)
upd = False
aprsclients=[]
hostname=gethostname()
ipaddr=gethostbyname(hostname)
aprsipaddrs={"172.31.9.13":"glidern4"}
while i < 6:
      aprsname='glidern'+str(i)+'.glidernet.org'
      ipaddr=gethostbyname(aprsname)
      ipaddro={ipaddr:'glidern'+str(i)}
      aprsipaddrs.update(ipaddro)
      aprs = urllib.request.urlopen('http://'+aprsname+':14501/status.json')
      ss= aprs.read().decode('utf-8')
      s_obj = json.loads(ss)
      clients=s_obj["clients"]
      aprsclients.append(clients)
      i += 1
#print ("APRS IP addrs:",aprsipaddrs)
#print ("APRS IP clients:",aprsclients)
s = json.dumps(s_obj, indent=4)
if rg != "ALL":
   print (getaprsrec(aprsclients,rg))
   print ("\n\n===================================================================================\n\n")

#
# the HTML formats
#
html1 = """<header> <TITLE>Get the flights</TITLE> <meta charset="UTF-8"></header><body> <IMG src="../gif/ogn-logo-150x150.png" border=1 alt=[image]><H1>Status of the OGN receiver stations: </H1> <HR> <P> %s </P> </HR> """
html2 = """<center><table><tr><td><pre>"""
html3 = """</pre></td></tr></table></center></body>"""
filename = dbpath+config.DBSQLite3        # open th DB in read only mode
fd = os.open(filename, os.O_RDONLY)
conn = sqlite3.connect('/dev/fd/%d' % fd)
cursD = conn.cursor()
cursU = conn.cursor()
vd = ('Valid station: %-s:' % rg)         # prepate the literal to show
print((html1 % vd))                       # tell that
print(html2)                              # cursor for the ogndata table
print("<a> ID          Description                                                         Country   IP addr      Server        Connected           Last heartbeat </a>")
if rg == "UPD":
    # get all the receivers
    cursD.execute('select idrec, descri from RECEIVERS order by idrec;')
    upd = True
elif rg == "ALL":
    # get all the receivers
    cursD.execute('select idrec, descri from RECEIVERS order by idrec;')
else:
    cursD.execute('select idrec, descri from RECEIVERS where idrec = ? ', [rg])             # get all the receivers

for row in cursD.fetchall():              # search all the rows
    id = row[0].rstrip()
    desc = row[1]
    if (id == None or id == "NONE" ):
        continue
    if len(receivers) > 2:
       descri=getrecdesc(receivers,id)
       country=getreccountry(receivers,id)
    else:
       if upd:
          descri=upddescri(id, cursU)
       else:
          descri=" "
       country=" "
    aprsip      =getaprsip(aprsclients,id)
    aprsserver  =getaprsserver(aprsclients,id, aprsipaddrs)
    aprstconnect=getaprstconnect(aprsclients,id)
    aprsslr     =getaprsslr(aprsclients,id)
    if desc != None and descri != None:
        descri=descri.encode('utf-8').decode('utf-8')
        print("<a>", "%-9s : %-30s %-36s %-6s %-15s  %-12s "% (id, desc, descri, country, aprsip, aprsserver), aprstconnect, "     ", aprsslr, "</a>")
print(html3)
conn.commit()
cursD.close()
cursU.close()
os.close(fd)

