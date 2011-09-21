import twitter
import time
import pytz
import datetime


CONS_KEY = 'YmjPguNHsOmCpDgGJ82Gmw'
CONS_SEC = 'XdabDKXnDGcdXpDn9glgsCsCQYgafsyVF7KAWPTHo'
ACC_TOK = '55229276-H7Ae0RgERvBCroEn2W8CZDsKhxcouf4dIJpEkDMxQ'
ACC_TOK_SEC = 'VYvzuDMNOYTYsrhpERQD5VDmY81ZJDWODaL9FTJOg'

#SEARCH_TERM = ['#apple']
SEARCH_TERM = ['#apple','osx','#mac','ipad','ipod','#lion']
FILE_OUT = 'apple2'
SLEEP = 2
AUTO_RESUME = False
RESUME_ID = 114496823313436672 

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
print(str(id))
#print('lol')
last_dt = twit2date(api.GetSearch(SEARCH_TERM[0], geocode=None, since_id=id, per_page=1)[0])
print(dt2format(last_dt))  
while (True):
    x = []
    last_id=id
    for i in SEARCH_TERM:
        try:
            src = api.GetSearch(i, geocode=None, since_id=id, per_page=100,page=1 )
        except Exception, err:
            print('Warning: '+time_formatted()+str(err))
            break
        #print(len(src))
        for twit in src:
            print (twit.id)
            add = True
            for oldtwit in x:
                if (twit.id==oldtwit.id):
                    add=False
                    break
            if (add==True):
                x.append(twit)
                dt = twit2date(twit) 
                if (twit.id>last_id): last_id=twit.id                
                write_twit(twit,dt)
    id=last_id
    
    
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
        if (twit2date(t).minute!=last_dt.min):
            
            f = open(FILE_OUT+'_statn.txt','a')
            f.write(dt2format(last_dt))
            f.write(str(twit_counter))
            f.write('\n')
            last_dt = twit2date(t)
            twit_counter = 0
            f.close()
            
    time.sleep(SLEEP)

