import twitter
import time
import pytz
import datetime
import socket
import os

socket.setdefaulttimeout(10)

CONS_KEY = 'YmjPguNHsOmCpDgGJ82Gmw'
CONS_SEC = 'XdabDKXnDGcdXpDn9glgsCsCQYgafsyVF7KAWPTHo'
ACC_TOK = '55229276-H7Ae0RgERvBCroEn2W8CZDsKhxcouf4dIJpEkDMxQ'
ACC_TOK_SEC = 'VYvzuDMNOYTYsrhpERQD5VDmY81ZJDWODaL9FTJOg'

#SEARCH_TERM = ['#apple']
SEARCH_TERM = ['#apple OR osx OR #mac OR ipad OR ipod OR #lion']
FILE_OUT = 'apple3'
SLEEP = 60
AUTO_RESUME = False
RESUME_ID = 0 

api = twitter.Api(CONS_KEY,CONS_SEC,ACC_TOK,ACC_TOK_SEC)

def dt2format(dt):
    return str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)+' '+str(dt.hour)+'-'+str(dt.minute)+' '
    
def time_formatted():
    return str(time.localtime().tm_year)+'-'+str(time.localtime().tm_mon)+'-'+str(time.localtime().tm_mday)+' '+str(time.localtime().tm_hour)+'-'+str(time.localtime().tm_min)+' '

def twit2date(twit):
    return pytz.utc.localize(datetime.datetime.fromtimestamp(twit.created_at_in_seconds))
    
def write_twit(twit,dt):
    f = open(FILE_OUT+'.txt','a')
    f.write(dt2format(dt))
    f.write(str(twit.id)+' ')
    f.write(twit.text.encode('utf-8').replace('\n',' '))
    f.write('\n')
    f.close()

if (AUTO_RESUME==False):
	id = RESUME_ID
else:
	if (os.path.exists(FILE_OUT+'_lastid')==False): id = 0
	else:
		f = open(FILE_OUT+'_lastid','r')
		id = int(f.readline())
		f.close()

twit_counter=0

f = open(FILE_OUT,'r')
while True:

initialized=False
    #make twits in ascending order for better stats
    for t1 in range(0,len(x)):
        for t2 in range(t1,len(x)):
            if (x[t2].id < x[t1].id):
                bck = x[t1]
                x[t1]=x[t2]
                x[t2]=bck
    twit_counter = 0
    for t in x:
        twit_counter = twit_counter + 1
        if (twit2date(t).minute!=last_dt.minute):
            f = open(FILE_OUT+'_statn.txt','a')
            if (initialized==True): 
                f.write(dt2format(last_dt))
                f.write(str(twit_counter))
                f.write('\n')
            last_dt = twit2date(t)
            twit_counter = 0
            f.close()
            initialized = True
            
    time.sleep(SLEEP)

