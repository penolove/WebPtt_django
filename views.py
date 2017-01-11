from django.shortcuts import render
import sqlite3
import time
from django.conf import settings
from datetime import datetime

ammount_dict={}
url_dict={}

# This tow dates should be handle properly
# Here I reamin it as fixed
endDate='2017.1.11'
#startDate='2015.7.09'
startDate='2017.1.10'

def get_article_ammount(date):
    """function for connect to DB and get today article ammount and save it in ammount_dict"""
    """if want to using different DB , check implement here"""
    def date_trans(x):
        """used for date transform """
        date_list=x.split('.')
        if(int(date_list[1])<10):
            return date_list[0]+'/ '+date_list[1]+'/'+date_list[2]
        else:
            return date_list[0]+'/'+date_list[1]+'/'+date_list[2]
    if(ammount_dict.get(date, None)==None):
        # this require the starbucks.sqlite
        conn=sqlite3.connect(settings.BASE_DIR+'/pttWeb/static/starbucks.sqlite')
        #conn=sqlite3.connect('/home/stream/Documents/kerkerman88/starbucks.sqlite')
        curs = conn.cursor()
        date_t=date_trans(date)
        get_length='SELECT hyperlink FROM webarticle where date = "'+date_t+'"' 
        curs.execute(get_length) 
        li=curs.fetchall()
        n=len(li)
        print "there are "+str(li)+" articles in "+date
        ammount_dict[date]=n
        url_dict[date]=li
        return ammount_dict[date]
    else:
        return ammount_dict[date]

def index(request):
    return render(request, 'WebPtt/index.html')

def index_if(request,id,date):
    """return correspondes image and render by id ,date"""
    #ammount=9
    ammount=get_article_ammount(date)
    article_url='https://www.ptt.cc'+ url_dict[date][int(id)-1][0]
    #pic_path
    path='worldcloud/'+date+'_'+id+'.png'
    #pic_path
    path='worldcloud/'+date+'_'+id+'.png'

    #info for display
    index_info=id+'/'+str(ammount)+' ('+str(int((float(id)/ammount*100)))+'% )'
    
    # check if last/first
    if(int(id)==1):
        P_N=-1
    elif(int(id)==ammount):
        P_N=1
    else:
        P_N=0
    return render(request, 'WebPtt/Gossip_index.html',{'pic_path':path,'index_info':index_info,'P_N':P_N,'date':date,'id':id,'startDate':startDate,'endDate':endDate , 'article_url':article_url})

def get_today():
    """return today date/most recently have been parse , check if today has article"""
    global endDate
    today=time.strftime("%m.%d")
    years=time.strftime("%Y")
    date_list=today.split(".")
    today=str(int(date_list[0]))+'.'+date_list[1]
    check_today=years+'.'+today
    if(get_article_ammount(check_today)>0):    
        a=datetime.strptime(check_today,'%Y.%m.%d')-datetime.strptime(endDate,'%Y.%m.%d')
        if(a.total_seconds()>=0):
            endDate=check_today
        print "get_today : "+ check_today
        return check_today
    else:
       print "get_today : "+ endDate
       return endDate 


def Gossip_index(request,id):
    """return correspondes image and render by id. check if today have data"""
    date=get_today()
    ammount=get_article_ammount(date)
    article_url='https://www.ptt.cc'+ url_dict[date][int(id)-1][0]
    #pic_path
    path='worldcloud/'+date+'_'+id+'.png'

    #info for display
    index_info=id+'/'+str(ammount)+' ('+str(int((float(id)/ammount*100)))+'% )'
    
    # check if last/first
    if(int(id)==1):
        P_N=-1
    elif(int(id)==ammount):
        P_N=1
    else:
        P_N=0
    return render(request, 'WebPtt/Gossip_index.html',{'pic_path':path,'index_info':index_info,'P_N':P_N,'date':date,'id':id,'startDate':startDate,'endDate':endDate , 'article_url':article_url})
