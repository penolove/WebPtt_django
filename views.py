from django.shortcuts import render
import sqlite3
import time
from django.conf import settings
from datetime import datetime
import simplejson
import glob

ammount_dict={}
url_dict={}

# This tow dates should be handle properly
# Here I reamin it as fixed
endDate='2017.1.11'
startDate='2015.7.09'
#startDate='2017.1.10'


def date_trans_z(x):
    """used for date transform """
    """2017.01.09->2017/01/09 """
    date_list=x.split('.')
    return date_list[0]+'/'+date_list[1]+'/'+date_list[2]


def get_article_ammount(date):
    """function for connect to DB and get today article ammount and save it in ammount_dict"""
    """if want to using different DB , check implement here"""
    def date_trans(x):
        """used for date transform """
        """2017.1.09->2017/ 1/09 """
        date_list=x.split('.')
        if(int(date_list[1])<10):
            return date_list[0]+'/ '+str(int(date_list[1]))+'/'+date_list[2]
        else:
            return date_list[0]+'/'+date_list[1]+'/'+date_list[2]

    if(ammount_dict.get(date, None)==None):
        # this require the starbucks.sqlite
        #conn=sqlite3.connect(settings.BASE_DIR+'/pttWeb/static/starbucks.sqlite')
        conn=sqlite3.connect('/home/stream/Documents/kerkerman88/starbucks.sqlite')
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

def index_if_back(request,id,date):
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
    return render(request, 'WebPtt/Gossip_index_back.html',{'pic_path':path,'index_info':index_info,'P_N':P_N,'date':date,'id':id,'startDate':startDate,'endDate':endDate , 'article_url':article_url})

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

def Gossip_index_back(request,id):
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
    return render(request, 'WebPtt/Gossip_index_back.html',{'pic_path':path,'index_info':index_info,'P_N':P_N,'date':date,'id':id,'startDate':startDate,'endDate':endDate , 'article_url':article_url})

def Gossip_index(request,id):
    """return correspondes image and render by id. check if today have data"""
    date=get_today()
    ammount=get_article_ammount(date)
    article_url_list=['https://www.ptt.cc'+i[0] for i in url_dict[date]]
    article_url=article_url_list[int(id)-1]
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

    #dump article_url pass to Web
    url_list = simplejson.dumps(article_url_list)

    return render(request, 'WebPtt/Gossip_index.html',{'pic_path':path,'index_info':index_info,'P_N':P_N,'date':date,'id':id,'startDate':startDate,'endDate':endDate , 'article_url':article_url, 'url_list':url_list ,'ammount':ammount})

class Week_Image(object):
    def __init__(self,filename):
        self.filename=filename
        self.date=Week_Image.name2date(filename)
    @staticmethod
    def name2date(filename):
        date=filename.split('/')[1].split('_')[2].replace('.png','')
        return datetime.strptime(date,'%Y.%m.%d')

def get_sorted_img_list():
    """return path and date"""
    dirPath=settings.BASE_DIR
    imgdir="/pttWeb/static/topicmodel"
    fileID=glob.glob(dirPath+imgdir+"/*.png")
    fileID=[i.replace('/home/stream/Documents/minimum_django/pttWeb/static/','') for i in fileID]
    fileID=[Week_Image(i) for i in fileID]
    fileID.sort(key=lambda x: x.date, reverse=True)
    #translate . to / since javascript parsing date has some issue!
    fileID=[(i.filename,date_trans_z(i.date.strftime("%Y.%m.%d"))) for i in fileID]
    return fileID

def Topic_index(request):
    """render for topic model , very simple rule"""
    """return path,date of images of topic to javascript"""
    fileID=get_sorted_img_list()
    week_img_list = simplejson.dumps(fileID)
    #latest
    path=fileID[0][0]
    date=fileID[0][1]
    print date
    return render(request, 'WebPtt/Gossip_topic_model.html',{'pic_path':path,'week_img_list':week_img_list,'date':date})

def index_if(request,id,date):
    """return correspondes image and render by id ,date"""
    ammount=get_article_ammount(date)
    article_url_list=['https://www.ptt.cc'+i[0] for i in url_dict[date]]
    article_url=article_url_list[int(id)-1]
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

    #dump article_url pass to Web
    url_list = simplejson.dumps(article_url_list)

    return render(request, 'WebPtt/Gossip_index.html',{'pic_path':path,'index_info':index_info,'P_N':P_N,'date':date,'id':id,'startDate':startDate,'endDate':endDate , 'article_url':article_url, 'url_list':url_list ,'ammount':ammount})
