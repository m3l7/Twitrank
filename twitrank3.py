import twitter
import time
import pytz
import datetime
import socket


SEARCH_TERM = ['#apple OR osx OR #mac OR ipad OR ipod OR #lion']
FILE_OUT = 'out/apple3'
DAEMON=False            
SLEEP = 720
DEBUG = True


CONS_KEY = 'YmjPguNHsOmCpDgGJ82Gmw'
CONS_SEC = 'XdabDKXnDGcdXpDn9glgsCsCQYgafsyVF7KAWPTHo'
ACC_TOK = '55229276-H7Ae0RgERvBCroEn2W8CZDsKhxcouf4dIJpEkDMxQ'
ACC_TOK_SEC = 'VYvzuDMNOYTYsrhpERQD5VDmY81ZJDWODaL9FTJOg'

USE_PAGES=True
AUTO_RESUME = False #set always false FIXME
RESUME_ID = 0
SYNC_OLD_TWITS = False

socket.setdefaulttimeout(10)
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
twit_counter=0

last_dt = datetime.datetime.today() 
init=False

while (True):
    
    if (DEBUG==True): print(time_formatted()+' new search')
    x = []
    last_id=id
    for i in SEARCH_TERM:
        for pg in range(1,16):
            try:
                src = api.GetSearch(i, geocode=None, since_id=id, per_page=100,page=pg )
            except Exception, err:
                print('Warning: '+time_formatted()+str(err))
                break
            for twit in src:
                add = True
                for oldtwit in x:
                    if (twit.id==oldtwit.id):
                        add=False
                        break
                if (add==True):
                    x.append(twit)
                    dt = twit2date(twit) 
                    if (twit.id>last_id): last_id=twit.id
            if (DEBUG==True): print('Fetching page '+str(pg)+'. Length: '+str(len(src)))
            if ((USE_PAGES==False) or (len(src)<100)): break
            if ((init==False) and (SYNC_OLD_TWITS==False)): break  
    id=last_id

    #make twits in ascending order
    for t1 in range(0,len(x)):
        for t2 in range(t1,len(x)):
            if (x[t2].id < x[t1].id):
                bck = x[t1]
                x[t1]=x[t2]
                x[t2]=bck
    for t in x:
        write_twit(t,twit2date(t))
        
    if (DAEMON==False): break               
    init=True
    time.sleep(SLEEP)