import twitter
import time


CONS_KEY = 'YmjPguNHsOmCpDgGJ82Gmw'
CONS_SEC = 'XdabDKXnDGcdXpDn9glgsCsCQYgafsyVF7KAWPTHo'
ACC_TOK = '55229276-H7Ae0RgERvBCroEn2W8CZDsKhxcouf4dIJpEkDMxQ'
ACC_TOK_SEC = 'VYvzuDMNOYTYsrhpERQD5VDmY81ZJDWODaL9FTJOg'

SEARCH_TERM = ['#apple','#osx','#mac','#ipad','#ipod','#lion']
FILE_OUT = 'apple_tag'
SLEEP = 10

api = twitter.Api(CONS_KEY,CONS_SEC,ACC_TOK,ACC_TOK_SEC)

def time_formatted():
    return str(time.localtime().tm_year)+'-'+str(time.localtime().tm_mon)+'-'+str(time.localtime().tm_mday)+' '+str(time.localtime().tm_hour)+'-'+str(time.localtime().tm_min)+' '

def write_twit(twit):
    f = open(FILE_OUT+'.txt','a')
    f.write(time_formatted())
    f.write(str(twit.id)+' ')
    f.write(twit.text.encode('utf-8').replace('\n',' '))
    f.write('\n')
    f.close()

id=0
twit_counter=0
last_min = time.localtime().tm_min
while (True):
    x = []
    last_id=id
    for i in SEARCH_TERM:
        try:
            src = api.GetSearch(i, geocode=None, since_id=id, per_page=200)
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
                if (twit.id>last_id): last_id=twit.id
                twit_counter = twit_counter + 1
                write_twit(twit)
    id=last_id
    time.sleep(SLEEP)
    if (time.localtime().tm_min!=last_min):
        last_min = time.localtime().tm_min
        f = open(FILE_OUT+'_statn.txt','a')
        f.write(time_formatted())
        f.write(str(twit_counter))
        f.write('\n')
        twit_counter=0
        f.close()


