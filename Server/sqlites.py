# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 13:43:06 2014

@author: krasytod
"""

#import sqlite3
#from sqlalchemy import create_engine
#engine = create_engine('sqlite:///test4.db', echo=True)
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
#Now that we have a “base”, we can define any number of mapped classes in terms of it.
from sqlalchemy import Column, Integer, String, Boolean



class comment(Base):
    '''клас контейнер за  "коментите".   '''    
    __tablename__ = 'comments'
    _date=   Column(String)
    _id = Column(Integer, primary_key=True) 
    _seconds=Column(Integer)  # seconds since the Milenium
    _name=Column(String)
    _text=Column(String)   
    _site=Column(String)
    _url=Column(String) 
    _sig=Column(String) 
    _user=Column(String) 
    _votes_plus= Column(Integer) 
    _votes_minus= Column(Integer)
    _checked = Column(Boolean, unique=False, default=False)
    
    
    def __init__(self,_id=0,date='',seconds='',name='',text='',site='None',url='',user='', sig='',votes_plus=0,votes_minus=0,checked = False):
        self._id = _id
        self._date=date
        self._seconds = seconds
        self._name = name
        self._text= text
        self._site= site
        self._url= url
        self._user=user
        self._sig=sig
        self._votes_plus=votes_plus
        self._votes_minus=votes_minus
        self._checked = checked
    def __str__(self):
        #return u"Име: "+ self.get_name()+ u" дата: "+self.get_date()+u" сайт: "+self.get_site() +u" Коментар: "+ self._text+u"\n"  
        print u"Име: ", self.get_name(), u" дата: ",self.get_date(),u" сайт: ",self.get_site() ,u" Коментар: ", self._text+u"\n" ,u"    положителен вот: ", self._votes_plus, u"    отрицателен вот: ", self._votes_minus, u"Проверен за нецензурност: ",self._checked 
        return ""       
        
    def set_name(self,name):
        self._name = name
        
    def set_seconds(self,seconds):
        self._seconds = seconds
        
    def set_date(self,date):
        self._date = date
    
    def set_text(self,text):
        self._text = text
    
    def set_site(self,site):
        self._site = site
    
    def set_url(self,url):
        self._url = url
        
    def set_votes(self,plus,minus):
        '''връща тюпъл от вотовете +/-/разлика '''
        self._votes_plus=plus
        self._votes_minus= minus
    
    def set_checked(self,state):
        self._checked =state 
        
    def set_id(self,id):
        self._id = id    
    
    def get_name(self):
        return self._name
        
    def get_user(self):    
        return self._user  
    
    def get_date(self):
        return self._date
    
    def get_text(self):
        return self._text
    
    def get_site(self):
        return self._site
    
    def get_url(self):
        return self._url  
        
    def get_seconds(self):
        return self._seconds     
        
    def get_votes(self):
        '''Връща общата оценка като разлика между положителния и отрицателния вот '''
        return self.votes_plus - self.votes_minus
        
    def get_sig(self):
        return self.sig
  
    def get_votes(self):
        '''връща тюпъл от вотовете +/-/разлика '''
        return (self._votes_plus,self._votes_minus,self._votes_plus-self._votes_minus)
    
    def get_checked(self):
        return self._checked     
    
    def get_id(self):
        return self._id
    
        
        
    def get_all(self):
        return [self._date,self._seconds, self._name, self._text, self._site, self._url,self._user,self._sig,self._votes_plus, self._votes_minus, self._checked]
        
        
        
#==============================================================================
# Base.metadata.create_all(engine)
# from sqlalchemy.orm import sessionmaker
# Session = sessionmaker(bind=engine)
# session = Session()
# 
# 
# 
# 
# #(self,date='',seconds='',name='',text='',site='None',url='',user='', sig='',votes_plus=0,votes_minus=0):
# bla = comment('20-12',10111,'krasy')
# session.add(bla) # фактическо свързване към базата данни 
# #second_comment = session.query(comment).filter_by(_seconds=10111).first()  # тук вече прави флъш на първия клас към базата и извършва заявката
# session.commit()
# 
# #print second_comment.get_date()
##==============================================================================
#session.close()