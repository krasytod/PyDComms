# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 09:50:30 2014

@author: krasytod
"""


## general imports
import urllib2,gzip
import random
import re
from bs4 import BeautifulSoup as BS
from comment import comment as comentar_class
import helper ,sqlites
import logging
from StringIO import StringIO
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
URL_DIRBG = "http://dnes.dir.bg/cat/all/"   #dnes.dir.bg/cat/all/?section=all&page=0&state=0&titles=
#URL_DIRBG = 'http://dnes.dir.bg//news_comments.php?id=17432461'
#http://dnes.dir.bg/comments/list.php?jnl_id=3&ctype_id=1&topic_id=17432461&list=all_s&page=1&ran=0.06207822563065157

def file_read_dir(name = 'something'):
    ''' четене на заглавната страница на новините в дира , ако са съхранени в текстови файл'''
    files = open(name, 'r')
    soup = BS(files.read())
    return soup



def read_dirbg(URL_DIRBG="http://dnes.dir.bg/cat/all/"):
    ''' четене на заглавната страница на новините в дира '''
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0')]
    urllib2.install_opener(opener)
    dirbg = urllib2.urlopen(URL_DIRBG)
    charset = dirbg.headers.getparam('charset')
    soup = BS(dirbg.read())
    
    return soup
    

def convert_url(url):
    '''конвертира УРЛто намерено в страницита с новините на дира, към това се генерира от comments.js
    URL_DIRBG = 'http://dnes.dir.bg//news_comments.php?id=17432461'
    http://dnes.dir.bg/comments/list.php?jnl_id=3&ctype_id=1&topic_id=17432461&list=all_s&page=1&ran=0.06207822563065157
    '''
    idx =  url.find('id=')
    if idx < 0: # нЕма такова нещо
        "търсения субстринг не съществува"
        return 1
    else:
        topic_id = url[idx+3:]        
    ran=  random.random()   #накрая на урлъто трябва да има рандъм генерирано число между 0 и 1
    url =  "http://dnes.dir.bg/comments/list.php?jnl_id=3&ctype_id=1&topic_id="+str(topic_id)+"&list=all_s&flat=1&page=1&ran="+str(ran)  
    return url   
    
def extract_comments(soup):
    ''' Връща сет с линкове към страниците с коментари към отделните новини.   Дали да не зарежда и допълнително информация
    като да търси определени тагове в новината (Борисов, герб , Украйна и тн) '''    
    comments = set()
    news = set()
    result = soup.find("div", {"id":"fullarticles"})  #списък с всичките заглавия
    for div_txt in result.findAll('div',attrs={'class':'txt'}):
        news.add(div_txt.find('a'))
        #print a_link.get('href'),a_link.getText()  # заглавие и линк на новините на Първа
    for data in result.findAll('div',attrs={'class':'coments'}):
        #print result.findAll('div',attrs={'class':'coments'})
        comments.add(convert_url("http://dnes.dir.bg/"+data.find_parent("a").get('href')))
       
    return comments,news
  

def read_comments(link,last_comm_link='',list_comentari=[]):
    ''' получава линка с коментарите към конкретна новина и Речник с коментарите, чийто ключове са интегър дата на коментара с добавени осем рандъм символа отзад,  втория параметър е  линка на последния коментар в базата данни. проверява за него когато създава нов коментар и ако има съвпадение прекратява (нататък всички коментари са вече обходени '''
    ### отваря първата страница , проверява дали има и други страници или е само една   -ИДЕЯ!!! Дали няма директно ходене на последна страница ? мммм ???и така да знам точно колко страници има ? Май да!
    page_list=[1]
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0')]
    urllib2.install_opener(opener)
    dirbg = urllib2.urlopen(link)
    soup = BS(dirbg.read())    
    pages =  soup.find('div', {'class':"pagingComments"})
    #print soup, "====++++++++++++++++"
    if pages != None:
        next_page = True
        result_set =  soup.find_all('a',{'href':"javascript:void(0)",'onclick': re.compile(r'loadComments*')})  
        
        for result in result_set:
            #print result
            try:
                page_list.append(int(result.text))
            except ValueError:
                pass
    ### край на сегмента с изчисляването на колко страници имат коментарите под тази новина
    
    
    def page_counter_builder(link,page_counter,time=''):
        '''инлайн функция, взима линка и номера на страницата , ъпдейтва линка и го връща '''
        if page_counter == 1:
            return link
        subs_string = 'page='+str(page_counter-1)
        try:
            index= link.index(subs_string)
            link =  link[:index]+'page='+str(page_counter)+ link [ len('page='+str(page_counter)) :]
        except ValueError:    
            pass #print "някаква грешка в суб стринга"
        return link
    for page_number in page_list:
        
        opener = urllib2.build_opener()
        opener.addheaders = [('User-agent', ' Mozilla/5.0 (Windows NT 6.1; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0')]
        urllib2.install_opener(opener)
        link = page_counter_builder(link,page_number)
        dirbg = urllib2.urlopen(link)
        soup = BS(dirbg.read())
        comments_list =  soup.find("form",{"name":"cformGuest"}).find_all("option")  # таблицата с коментарите и техните идентификатори
        for comment in comments_list:
            if comment.get("value") !='0':     # comment.get("value") =0 е идентификатора за "Обща дискусия"
                comment_class =  comment.get("class") ,   
                comment_text=   comment.text #.decode('cp1252').encode('utf_8')
                comment_name= comment_text[12:comment_text.find(',')] 
                comment_text = comment_text[comment_text.find(','):]
                comment_time = comment_text[comment_text.find('.')-2:]  # 
                comment_class_body = comment_class[0][0]  +"_body"
                comment_class_header = comment_class[0][0]
                comment_class_text= soup.find("p", {"id": comment_class_body}).text 
                comment_class_text = comment_class_text.strip()
                # вадене на вота от коментара. използването на regex може да пропусне отрицателни числа  / листа е във формат [+,-]
                votes = []
                class_header = soup.find("div", {"id": comment_class_header})
                user_profile =  class_header.find('span',{'class':"proInfo"})
                comm_user="NoReg"
                if user_profile != None:
                    comm_user =  user_profile.find_all('a')[1].get("href")[-10:]
                    
                class_voting = class_header.find("div",{'class':"voting"})
                for literal in class_voting.text.split():
                    try:
                        votes.append(int(literal))
                    except ValueError:
                        votes.append(0)
                _dummy1,_dummy2,news_id,comm_id,page_num= class_voting.find('a' ,{'href':"javascript:void(0);"}).get('onclick')[5:-1].split(',')
                
                #линк към коментара 
                comm_link="http://dnes.dir.bg/news_comments.php?id="+news_id+u'&page='+page_num+u'&comment='+comm_id
                #ако вече сме обходили коментарите нататък
                if last_comm_link == comm_link:
                    logging.debug(u'обходен')
                    return list_comentari
                time_key =   helper.dirbg_convert_time(comment_time)             #  Ключа който се образува от датата на коментара
                com_class = sqlites.comment(comm_id, comment_time,time_key,comment_name,comment_class_text,'Dir.bg',comm_link,comm_user ,"Sig- None",votes[0],votes[1],0,unicode(news_id),comm_id)  
                #print com_class
                #print news_id,comm_id
                if time_key != 666666:
                   list_comentari.append(com_class)  # 
    return list_comentari


#==============================================================================
# Секция с разни неща за тестване !!!!
#==============================================================================


def read_comments_test(link,last_comm_link='',list_comentari=[]):
    ''' тестване на нови функционалности. 
    '''
    print a_link.get('href'),a_link.getText()
    return 0

import datetime
def insert_in_db(all_comments,*args, **kwargs):
    logging.info('insert_in_db: %s, duljina %i',kwargs['db_name'],len(all_comments))
    #logging.info('insert_in_db: %s',kwargs['db_name'])
    date = datetime.datetime.now().date()
    from sqlalchemy import create_engine 
    if kwargs['db_name'] == "default":
         engine = create_engine('sqlite:///comments.db', echo=False)   #базата данни с която ще работим
    else:
         engine = create_engine('sqlite:///'+kwargs['db_name'], echo=False)     
    sqlites.Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker   # създава сесията 
    Session = sessionmaker(bind=engine)  #връзва сесията към базата данни
    session = Session()
    for comment in all_comments:
        session.merge(comment)
    session.commit()  #  ръга нещата в базата с данни
    session.close()

def  insert_news_in_db(all_news):
    '''Вкарва в таблиците с новините. Получава Соуп линк с новините, и текста '''
    from sqlalchemy import create_engine 
    engine = create_engine('sqlite:///comments.db', echo=False)   #базата данни с която ще работим
    sqlites.Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker   # създава сесията 
    Session = sessionmaker(bind=engine)  #връзва сесията към базата данни
    session = Session()
    import time
    current = time.localtime(time.time())
    current=helper.dir_convert_time(current)
    for link in all_news:
        match = re.findall(r'\d+\.nt',link.get('href') ) 
        if match:
          news_class= sqlites.news( match[0][:-3] ,link.getText(),link.get('href'),current )
          session.merge(news_class)
    session.commit()  #  ръга нещата в базата с данни
    session.close()

    
#*Коментарът е скрит, защото е етнически нетолерантен  - Трябва да се направи нещо с тези коментари

from sqlalchemy.sql.expression import func

###за вадене на неща от базата
def extract_from_db(topic_id=''):
    '''Вади от днешната база данни последния коментар за дадената новина '''
    date = datetime.datetime.now().date()
    from sqlalchemy import create_engine 
    engine = create_engine('sqlite:///comments.db', echo=False)   #базата данни с която ще работим
    sqlites.Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker   # създава сесията 
    Session = sessionmaker(bind=engine)  #връзва сесията към базата данни
    session = Session()
    #result = session.query(sqlites.comment).filter_by(_seconds=u'007').first()
    result_max = session.query  (func.max(sqlites.comment._seconds)).filter(sqlites.comment._url.like('%'+topic_id+'%'))
    result_min = session.query  (func.min(sqlites.comment._seconds))
    result_max= session.query(sqlites.comment).filter_by(_seconds=result_max)
    #result_min= session.query(sqlites.comment).filter_by(_seconds=result_min[0])
    session.close()
    return result_max#,result_min

###Взима линка на последния коментар , ако няма последен коментар, тоест новината се обхожда за първи път, то връща празен линк
def last_comment_link(topic_id=''):
    ''' Получава IDна новината, екстрактва от базата данни най-скорошния коментар от съответната новина. Ако новината не е
    била обходена, връща празен стринг'''    
    result = extract_from_db(topic_id)
    if  result.all() != []:
        last_comm_link = result.all()[0].get_url()
    else:
        last_comm_link = ''
    
    return last_comm_link

from sqlalchemy import and_, or_

def return_all_comments(since_time_opt=0):
    date = datetime.datetime.now().date()
    from sqlalchemy import create_engine 
    engine = create_engine('sqlite:///comments.db', echo=False)   #базата данни с която ще работим
    sqlites.Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker   # създава сесията 
    Session = sessionmaker(bind=engine)  #връзва сесията към базата данни
    session = Session()
    #result = session.query(sqlites.comment).filter_by(_seconds=u'007').first()

    if since_time_opt ==0:
        result =  session.query(sqlites.comment).order_by(sqlites.comment._seconds)
    else:
        result = session.query(sqlites.comment).filter(sqlites.comment._seconds>since_time_opt).order_by(sqlites.comment._seconds)
    return result,session#,result_min
    
def return_cenz_comms(time_shift,options):
    '''Връща коментарите които подлежат на проверка за цензуриране. Приема начало на смяна  и дикшънари с листа на имена и текстове с опции '''
    date = datetime.datetime.now().date()
    from sqlalchemy import create_engine 
    engine = create_engine('sqlite:///comments.db', echo=False)   #базата данни с която ще работим
    sqlites.Base.metadata.create_all(engine)
    from sqlalchemy.orm import sessionmaker   # създава сесията 
    Session = sessionmaker(bind=engine)  #връзва сесията към базата данни
    session = Session()    
    
    texts = options['text']    
    names = options['name'] 
    ###Създаване на условията които да бъдат филтрирани с OR
    conditions = []
    for name in names:
        conditions.append(sqlites.comment._name.ilike(u'%{}%'.format(name)))
    for text in texts:
        conditions.append(sqlites.comment._text.ilike(u'%{}%'.format(text)))
    result = session.query(sqlites.comment).filter(and_(or_(*conditions),sqlites.comment._seconds>time_shift,sqlites.comment._checked ==False ))      
    return result,session    
    
def vote_up(link,small_loop=10,big_loop=4,action=1):
    '''Гласува автоматично в коментарите под новините. Очаква линка за гласуване, брой гласувания, и типа гласуване. 1 - положителен,2 -отрицателен '''
    import time,cookielib
    #link ="https://panopticlick.eff.org/index.php?action=log&js=yes" 
    links= ["http://dnes.dir.bg/comments/voting.php?jnl_id=3&ctype_id=1&topic_id=18753004&comment_id=185917&action=2&ts=0.33454112514499024","http://dnes.dir.bg/comments/voting.php?jnl_id=3&ctype_id=1&topic_id=18753004&comment_id=185917&action=2&ts=0.4233232323234","http://dnes.dir.bg/comments/voting.php?jnl_id=3&ctype_id=1&topic_id=18753004&comment_id=185917&action=2&ts=0.55654112514499024"]
    user_agents= [u"Mozilla/6.0 (compatible; MSIE 11.0; Windows NT 6.1)",u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",u'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20102341 Firefox/32.0',u'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; de-de) AppleWebKit/523.10.3 (KHTML, like Gecko) Version/3.0.4 Safari/523.10',' Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; de-de) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16']
    user_ag =  u'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; de-de) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari'
    rand= random.randint(1,70)  # в случай, че се нареди повторно гласуване, да има малък шанс юзър агента да е същия
    for idx in range(small_loop):
      cj = cookielib.CookieJar()
      user_agent =  user_ag +unicode(rand)+ unicode(idx) + u'.'+unicode(big_loop)
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())  #,urllib2.HTTPHandler(debuglevel=1)
      #print idx
      opener.addheaders = [('User-Agent',user_agent ),('Referer', 'http://web-sniffer.net/'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Charset', 'UTF-8;q=0.7,*;q=0.7'),('Cache-Control', 'no-cache'),('Accept-encoding', 'gzip'),('Accept-Language','de,en;q=0.7,en-us;q=0.3')]
      #print link
      urllib2.install_opener(opener)
      dirbg = urllib2.urlopen(unicode(link))
      if dirbg.info().get('Content-Encoding') == 'gzip':
         buf = StringIO( dirbg.read())
         dirbg_decoded = gzip.GzipFile(fileobj=buf)
         soup = BS(dirbg_decoded.read()) 
      else:   
         soup = BS(dirbg.read())
      #print soup
      #print  dummy,link
      time.sleep(5.5)

def run_me(*args, **kwargs):
    '''подпрограмата която да бъде извиквана от основния файл.  '''
    db_name = "default"
    if 'db_name' in kwargs:
        db_name= kwargs['db_name']
    page =1 
    if 'page_num' in kwargs: 
        page = kwargs['page_num']
    url =    ["http://dnes.dir.bg/cat/all/?section=all&page=","&state=0&titles="]
    logging.info('run_me')
    for idx in range(page):
        soup= read_dirbg(url[0]+str(idx)+url[1])
        set_links,set_news = extract_comments(soup)
        if idx==0:
            insert_news_in_db(set_news) 
        for set_ in set_links:
            # last_comment_link( set_[67:74]  - topic_id което се подава на функцията която проверява базата данни и търси последния коментар към новината с това ID
            all_comments=read_comments( set_,last_comment_link( set_[67:74]))
            insert_in_db(all_comments,db_name = db_name)

    
    #return read_all_comments(set_links)   # връща всички коментари към всички новини на първа страница 
if __name__ == "__main__":
    #pass    
    run_me()    
    
def run_me_t(s=""):
    from time import sleep
    sleep(5)
    s="blaa"
