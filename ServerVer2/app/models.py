# -*- coding: utf-8 -*-
from app import db


class cenzor(db.Model):
    __tablename__ = 'cenzor'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(32), unique=True, index=True)
    weight = db.Column(db.Integer, index=True)
    _type = db.Column(db.Integer, index=True)  # 0 - name only, 1 - text only , 2 Both
     
    def __init__(self, text=u"test" ,weight="1",_type="1"):
        self.text = text
        self.weight = int(weight)
        self._type = int(_type)
    def __unicode__ (self):
        return u'<Дума: %r>' % (self.text)
    def __repr__(self):
        return '<Дума: %r>' % (self.text)


class comments(db.Model):
    '''клас контейнер за  "коментите".   '''    # Трябва да го направим да взима и заглавието на новината, може би ?
    _date=   db.Column(db.String, index=True)    #(db.DateTime)
    _id = db.Column(db.Integer, primary_key=True) 
    _seconds=db.Column(db.Integer)  # seconds since the Milenium
    _name=db.Column(db.String, index=True)
    _text=db.Column(db.String, index=True)   
    _site=db.Column(db.String, index=True)
    _url=db.Column(db.String, index=True) 
    _sig=db.Column(db.String) 
    _user=db.Column(db.String, index=True) 
    _votes_plus= db.Column(db.Integer) 
    _votes_minus= db.Column(db.Integer)
    _checked = db.Column(db.Boolean, unique=False, default=False)
    _news_id=db.Column(db.String, db.ForeignKey('news._id'))
    _comm_id=db.Column(db.String, unique=True, default=False)
    _flag = db.Column(db.Boolean, unique=False, default=False)
   
    def __unicode__(self):
        #return u"Име: "+ self.get_name()+ u" дата: "+self.get_date()+u" сайт: "+self.get_site() +u" Коментар: "+ self._text+u"\n"  
        return u"Име: " +  unicode(self._text)+ u" дата: "+unicode(self._date) +u" Коментар: "+ unicode(self._text)+u"\n"
       
class comments_shodni(db.Model):
	'''Клас съдържащ коментарите които ще се търсят, че  се пускат редовно като спам '''
	_id = db.Column(db.Integer, primary_key=True)
	_text=db.Column(db.String, index=True)
	
	def __init__(self, text=u"test" ):
		self._text = text
	
	
	def __unicode__(self):
		return self._text


class news(db.Model):
	'''Клас съдържащ данни за всяка новина '''
	_id = db.Column(db.Integer, primary_key=True)
	_text=db.Column(db.String, index=True)
	_url = db.Column(db.String, index=True)
	_seconds=db.Column(db.Integer)  # seconds since the Milenium
	_posts = db.relationship('comments', backref='news', lazy='dynamic')
	
	def __unicode__(self):
		return u'<Заглавие: %r>' % (self._text)
