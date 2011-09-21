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
FILE_OUT = 'out/apple3'
SLEEP = 60
AUTO_RESUME = True
RESUME_ID = 0 

api = twitter.Api(CONS_KEY,CONS_SEC,ACC_TOK,ACC_TOK_SEC)

def dt2format(dt):
    return str(dt.year)+'-'+str(dt.month)+'-'+str(dt.day)+' '+str(dt.hour)+'-'+str(dt.minute)+' '

def format2dt(frm):
    dt = datetime
    dt.year = frm.split(' ')[0].split('-')[0]
    dt.month = frm.split(' ')[0].split('-')[1]
    dt.day = frm.split(' ')[0].split('-')[2]
    dt.hour = frm.split(' ')[1].split('-')[0]
    dt.minute = frm.split(' ')[1].split('-')[1]
    return dt
    
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
    
def write_twit_per_min(dt,count):
    f_min = open(FILE_OUT+'_stat_per_min.txt','a')
    f_min.write(dt2format(dt)+' '+str(count)+'\n')
    f_min.close()
def write_last_id(id):
    f_l = open(FILE_OUT+'_lastid.txt','w')
    f_l.write(str(id))
    f_l.close()


if (AUTO_RESUME==False):
    id = RESUME_ID
else:
    if (os.path.exists(FILE_OUT+'_lastid.txt')==False): id = 0
    else:
        f = open(FILE_OUT+'_lastid.txt','r')
        id = int(f.readline())
        f.close()

twit_counter=0

f = open(FILE_OUT+'.txt','r+')
f.seek(0)
while (True):
    line = f.readline()
    if (int((line.split(' ')[2]))>=id): break

init = False
count_twit_per_min = 0
last_dt = datetime.datetime.today()

while (True):
    try:
        line = f.readline()
    except:
        break
    
    words = line.split(' ')
    
    try:
        datefrm = words[0]+' '+words[1]
        id = int(words[2])
        author = words[3][:-1]
        text = line.split(words[3])[1][1:].replace('\n',' ')
    except:
        break
    
    if (init==False):
        last_dt = format2dt(datefrm)
        init = True
    if (last_dt.minute!=format2dt(datefrm).minute):
        write_twit_per_min(format2dt(datefrm),count_twit_per_min)
        count_twit_per_min = 0
        last_dt = format2dt(datefrm)
        write_last_id(id)
    else:
        count_twit_per_min = count_twit_per_min + 1
        
        


