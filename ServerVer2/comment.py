# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 16:09:59 2014

@author: krasytod

Клас комент
"""

class comment:
    '''клас контейнер за  "коментите".   '''    
    
    _date='' 
    _seconds=0  # seconds since the Milenium
    _name=''
    _text=''    
    _site='None'
    _url=''    
    
    def __init__(self,date='',seconds='',name='',text='',site='None',url='',user='', sig='',votes_plus=0,votes_minus=0,news_id="3",comm_id="0"):
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
        self._news_id=news_id
        self._comm_id=comm_id
        
    def __str__(self):
        #return u"Име: "+ self.get_name()+ u" дата: "+self.get_date()+u" сайт: "+self.get_site() +u" Коментар: "+ self._text+u"\n"  
        print u"Име: ", self.get_name(), u" дата: ",self.get_date(),u" сайт: ",self.get_site() ,u" Коментар: ", self._text+u"\n" ,u"    положителен вот: ", self._votes_plus, u"    отрицателен вот: ", self._votes_minus
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
    
        
        
    def get_all(self):
        return [self._date,self._seconds, self._name, self._text, self._site, self._url,self.user,self.sig,self.votes_plus, self.votes_minus]
        
        
#asd= comment("2","bla","tralallala")
