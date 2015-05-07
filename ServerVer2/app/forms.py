# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, BooleanField,IntegerField,TextAreaField,RadioField,SelectField,FormField,SelectMultipleField
from wtforms.validators import DataRequired,Length,ValidationError



class LoginForm(Form):
    openid = StringField('openid', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class SingleCenzorForm(Form):
    #choices_m = StringField('избор')
    cenzor = StringField('Цензорна дума', validators=[DataRequired(message=u'This field is required.')])
    cenType = RadioField('Тип',choices=[(0,u'Име'),(1,u'Текст'),(2,u'Двете')],coerce=int,default=1, validators=[DataRequired(message=u'This field is required1.')])    
    weight = SelectField(u'Тежест', choices=[(1,1), (2,2), (3,3),(4,4),(5,5)],coerce=int)
    #multiple = FormField(SubForm, label="Multiple: ")
    #weight = IntegerField(u'Тежест',validators=[DataRequired()])
  
class MultiCenzorForm(Form):
	choices = TextAreaField('Цензорно поле','style="display:none"')

class DeleteCenzorForm(Form):
	choice_for_del = SelectMultipleField('изтрийване',choices = [])
	
class News_field_Form(Form):
	News= SelectField(u'Новини:', choices=[(0,u"Всички")],coerce=int)

class add_shoden_Form(Form):
	shoden_m_field =   TextAreaField('Цензорно поле','style="display:none"')        #TextAreaField(u"shoden")
