# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, \
    login_required
from sqlalchemy import desc
from app import app, db
from .forms import LoginForm, SingleCenzorForm, MultiCenzorForm,DeleteCenzorForm,News_field_Form,add_shoden_Form
from .models import comments ,cenzor,comments_shodni, news
import db_create,dirbg, helper,liv
from .decorators import async
import logging,datetime,os ,time, random
from wtforms import SelectField
logger = logging.getLogger(__name__)
logging.basicConfig(filename='log.txt',level=logging.DEBUG)


### CONSTANTS ###
DB_STRING_NAME = 'comments.db'
PAGE_SIZE = 20
SHIFT_START_STRING =u"Натисти за начало на смяна" 
SHIFT_START=0  #От началото на света в секунди 


@app.route('/')
@app.route('/index')
def index():
    ##### да проверя дали съществува база данни и да я върна ако съществува, ако не да кажа че няма база данни
    db_base_info = u""
    import os
    db_exists = os.path.isfile(DB_STRING_NAME)   #връща Истина ако базата данни съществува
    if db_exists:
     db_base_info +=u"Базата данни съществува."
     file_info = os.stat(DB_STRING_NAME)
     file_size= dict()
     #file_size['bites'] = file_info.st_size % 1024
     file_size['kbs'] = (file_info.st_size % (1024*1024)) //1024
     file_size['mbs'] = file_info.st_size / (1024*1024)
     #print file_size
     mbs_str = unicode (file_size['mbs']) + u"."
     db_base_info += u" Размер: " + mbs_str + unicode(file_size['kbs'] ) + u" Mibs("+ unicode(file_info.st_size) + u")"
    else:
     db_base_info +=u"Несъществува база данни"	
    return render_template('index.html', db_name =db_base_info,title='Home')


@async
def start_async_scrapper():
	dirbg.run_me(db_name=DB_STRING_NAME,page_num= 3)
	return 0
	
@async
def vote_manipulation(url):
	'''Манипулиране на вота в дир бг. КУР Мурзилки!!! '''
	#f= open('loop.txt','w+')
	big_loop = random.randint(2,6)
	if big_loop < 5:
		small_loop = random.randint(5,12)  #За да не се получава твърде голям Вот
	else:
		small_loop = random.randint(4,9)
	

	for idx in range (big_loop):
		f= open('/loop.txt','w+')
		for idy in range (small_loop):
			dirbg.vote_up( unicode(request.form['url']),idy,idx)
			
			f.write('m: ')
			f.write(idx)
			f.write(idy)
			
			time.sleep(idy)
		f.close()
		time.sleep(idx*30*3)
		#print "minava"
	return "0"
			
	
@app.route('/vote',methods=['POST']) 
def make_vote():
	if "url"  in request.form.keys():
		dirbg.vote_up( unicode(request.form['url']))
	return "0"
	
@app.route('/add-shoden',methods=['POST',"GET"]) 
def add_shoden():
	'''Добавяне на сходен коментар със собствена форма и пост метод '''
	shoden_form = add_shoden_Form()
	if shoden_form.is_submitted():
		comment_text=request.form["shoden_m_field"]
		new_row = comments_shodni(comment_text)
		db.session.add(new_row)
		db.session.commit()
		return  render_template('redirect.html', text = u"Добавено към сходни " , link="/add-shoden", timer = 5)
	return render_template("add-shoden.html",form2 = shoden_form)
	


@app.route('/shodni/',methods=['GET']) 
def shodni():
	comm_id = request.args['comm_id']
	result = comments.query.filter_by(_comm_id=comm_id).first() 
	result = result._text
	new_row = comments_shodni(result)
	db.session.add(new_row)
	db.session.commit()
	return result
	
	
@app.route('/post',methods=['GET', 'POST']) 
def take_post():
	global SHIFT_START_STRING,SHIFT_START
	if "time_shift" in request.form.keys():
		if request.form["time_shift"]=="No_click":
			return  SHIFT_START_STRING
		if request.form["time_shift"]=="click_start":
			SHIFT_START = helper.dir_convert_time(time.localtime(time.time()))
			SHIFT_START_STRING= u"Начало на текущата смяна: "+request.form["begin_shift"]
			return  SHIFT_START_STRING
		g.shift_start =  helper.dir_convert_time(time.localtime(time.time()))
	#dir_convert_time
	return "blala"
	
	
@app.route('/newdb')    
def newdb():
	if not os.path.isfile(DB_STRING_NAME):
		db_create.create()
	else:
		today = datetime.date.today()
		now = datetime.datetime.now()
		# Да вземем таблицата с цензурните думи за да можем да я прехвърлим в новата база данни
		cenz = cenzor.query.all()
		os.rename(DB_STRING_NAME, DB_STRING_NAME + "-"+str(today)+"-"+str(now))
		db_create.create()
		#подаваме на функцията за включване на коментари, името на базата и  редовете от таблицата цензор
		dirbg.insert_in_db(cenz,db_name = "comments.db")
	return render_template('redirect.html', text = u"Базата е създадена.Автоматично връщане след " , link="/",timer= 10)


@app.route('/redirect/')
def redirect_func():
	'''Обработва командването на софтуера, когато е с кликане върху линкове '''
	url = request.args.get('url')
	page = request.args.get('page')
	comment = request.args.get('comment')
	id_comm = request.args.get('id')
	redirect_m= True
	url= url+u"&page="+page+u"&comment="+comment
	cenz = comments.query.filter_by(_id=id_comm ).first()          #
	cenz._checked = True
	logging.info(u"Маркирана като прочетена %s" , url )  
	db.session.commit()
	if url== None:
		redirect_m= False
		logging.info(u"Url не е подаден" )
		return render_template('redirect-close.html' )
	return redirect(url, code=302)
	#return render_template('redirect-command.html',redirect = redirect, url = url )

@app.route('/cenzor-edit',methods=['GET', 'POST'])   
@app.route('/cenzor-edit/<option>',methods=['GET', 'POST'])    
def cenzorEdit(option="None"):
    g.cenzor_lst=[ text_tup[0]  for text_tup  in cenzor.query.with_entities(cenzor.text).all()]
    Singleform = SingleCenzorForm()
    Multiform = MultiCenzorForm()
    if option == "None":
            return render_template('cenzor-edit.html', form=Singleform,Multiform=Multiform   )
    elif option== "single":
        #print "single",g.cenzor_lst
        if Singleform .validate_on_submit():                #validate_on_submit():
            flash(u'Your changes have been saved ')  # + c+u" " +c+ u" "+unicode(Singleform.weight.data)
            cenzor_word = cenzor(unicode(Singleform.cenzor.data),unicode(Singleform.weight.data),unicode(Singleform.cenType.data))
            if unicode(Singleform.cenzor.data) in g.cenzor_lst:
                logging.debug(u"повтаря се")
            else: 
                db.session.add(cenzor_word )
            db.session.commit()
            return redirect('/index')   #'cenzor-edit'
        else:
            if (Singleform .errors !={}):
                flash(Singleform .errors)
            #form.cenzor.data = "b"
            return render_template('cenzor-edit.html', form=Singleform,Multiform=Multiform   )
    elif option== "multi":
        flash(u'Your changes have been saved ')  # + unicode(Singleform.cenzor.data)+u" " +unicode(Singleform.cenType.data)+ u" "+unicode(Singleform.weight.data)
        #g.user.about_me = form.about_me.data
        for elem in Multiform.choices.data.split('|-|'):
            _cenzor=tuple(unicode(el) for el in elem.split("-|-"))
            if len(_cenzor[0])>0:
                if _cenzor[0] in g.cenzor_lst:
                    c 
                    
                else:
                    logging.info(u"Не се повтаря  мулти %s",_cenzor[0] )   
                    cenzor_word = cenzor(_cenzor[0],_cenzor[1],_cenzor[2])
                    db.session.add(cenzor_word )
        db.session.commit()
        # db.session.add(g.user)
        #db.session.commit()
        #flash('Your changes have been saved %b.' ,form.validate_on_submit())
        return redirect('/index')   #'cenzor-edit'    

    else:
        flash ("problmeatic URL")  
        return render_template('cenzor-edit.html', form=Singleform,Multiform=Multiform   )

@app.route('/cenzor-delete',methods=['GET', 'POST']) 
def cenzorDelete():
	g.cenzor_lst=[ text_tup[0]  for text_tup  in cenzor.query.with_entities(cenzor.text).all()]
	Singleform = DeleteCenzorForm()
	enumur_choice_list=list(enumerate (g.cenzor_lst))
	#print Singleform.is_submitted()
	if Singleform.is_submitted():
		for choice in Singleform.choice_for_del.data:
			 cenz = cenzor.query.filter_by(text=unicode(enumur_choice_list[int(choice)][1])).first()          #
			 logging.info(u"цензорни думи набелязани за триене %s",cenz )  
			 db.session.delete(cenz)
		db.session.commit()
		return render_template('redirect.html', text = u" Изтрито " , link="/", timer = 5)
	Singleform.choice_for_del.choices = enumur_choice_list
	return render_template('cenzor-delete.html', form=Singleform,num = len(Singleform.choice_for_del.choices )  )

@app.route('/scrapper')
def scrapper():
	status =  start_async_scrapper()
	return render_template('redirect.html', text = u"Базата се подновява.Моля за малко търпение " , link="/", timer = 60)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    #print request.args, form.is_submitted()
    if form.validate_on_submit():
        flash('Login requested for OpenID="%s", remember_me=%s' %
              (form.openid.data, str(form.remember_me.data)))
        return redirect('/index')
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])
                           
                           
@app.route('/comments/')
def comments_all():
    g.cenzor_lst=[ text_tup[0]  for text_tup  in cenzor.query.with_entities(cenzor.text).all()] 
    page = request.args.get('page')
    all_comms = request.args.get('all_comms')
    cenzor_arg = request.args.get('cenzor')
    search_text = request.args.get('search_text')
    search_name = request.args.get('search_name')
    news_arg= request.args.get('news')
    shodni = request.args.get('shodni')
    if shodni ==None:
         shodni = "0"
    if news_arg ==None:
         news_arg = "0"
    if search_text ==None:
        search_text ="" 
    if search_name ==None:
        search_name =""     
    if cenzor_arg == None:
         cenzor_arg = "0"
    
    if shodni =="1" :    
        comments_lst= comments.query.all()
        shodni_lst= comments_shodni.query.all()
        shoden_found_lst = helper.search_shodni(comments_lst,shodni_lst) 
        news_field = News_field_Form(News=news_arg)
        if page == None:
            page = "0"
        return render_template('comments.html',blas=shoden_found_lst, num_comments = len(shoden_found_lst),page = int(page),cenzor = 0,news_choice = news_field )         
        
    current = time.localtime(time.time())
    current=helper.dir_convert_time(current) - 60*60*24*3 # минута*час*ден*3
    news_list_query = news.query.filter(news._seconds >current).order_by(news._seconds.desc())
    news_field = News_field_Form(News=news_arg)
    news_field.News.choices=[(0,u"Всички")]
    for news_elem in news_list_query.all():
        #print news_elem._text[:10]
        news_field.News.choices.append((news_elem._id,news_elem._text))
    #print news_list
    #news_field.default=news_arg
    if cenzor_arg == "0":
       #print "0000000000"
       num_rows_db=comments.query.count()
       #print num_rows_db
       comments_lst = None
       #comments_lst = comments.query.order_by(comments._seconds.desc()).filter( (comments._text.contains(search_text )) &((comments._name.contains(search_name ))) )
       if news_arg =="0":
          comments_lst= comments.query.join(news, (news._id == comments._news_id)).order_by(comments._seconds.desc()).filter( (comments._text.contains(search_text )) &((comments._name.contains(search_name ))) )
       else:
           comments_lst= comments.query.join(news, (news._id == comments._news_id)).order_by(comments._seconds.desc()).filter( (comments._text.contains(search_text )) &((comments._name.contains(search_name ))) & ((comments._news_id==news_arg )))
       #print comments_lst[0].news._id 
       if all_comms :
           #print "bla"
           comments_lst =  comments_lst.all() #comments.query.order_by(comments._seconds.desc()).all()
           #print comments_lst
       elif page != None:
           page = int(page)
           comments_lst =  comments_lst.limit(PAGE_SIZE).offset(page*PAGE_SIZE)    #comments.query.order_by(comments._seconds.desc()).limit(PAGE_SIZE).offset(page*PAGE_SIZE)
           #print comments_lst.filter(comments._text.contains("trlala"))
           #comments_lst = comments_lst[page*20:page*20+20]   # по 20 коментара на страница 
       if comments_lst == None:
           flash('Comments not found.')
           return redirect(url_for('index'))
       if page == None:
            page = 0
       return render_template('comments.html',blas=comments_lst, num_comments = num_rows_db,page = page,cenzor = cenzor_arg,news_choice = news_field )
    else:
        cenzor_comments_list = []
        cenzor_class_words = cenzor.query.order_by(cenzor.weight.desc()).all()
        shodni_words = comments_shodni.query.all()
        for word in cenzor_class_words:
            #print word.text,
            result = comments.query.filter( (comments._text.contains(word.text)) & (comments._checked ==False ) &(comments._seconds>SHIFT_START )  ).all()
            #print len(result)
            for res in result:
                for shodna in  shodni_words:
                    shodstvo = liv.compare_texts(shodna._text,res._text)
                    if shodstvo < 0.3:
                        res._flag=True                #маркирам ,че е флагната. В случая заради повтаряне ( спам)
                for word in cenzor_class_words:
                    idx =  -6 
                    len_comment = len(res._text)
                    cenz_html_str = '<font size="'+str(word.weight )+'" color="red">'  # стринга за вмъкване
                    #print "/n " + word.text 
                    while  res._text.find( word.text,idx+6) !=-1:
                        if  res._text.find('"red">'+ word.text,idx+6) !=-1: break   # в случай че се подава един и същ коментар втори път
                        idx=res._text.find( word.text,idx+6) 
                        res._text = res._text[:idx]+ cenz_html_str+ res._text[idx:idx + len (word.text)]+"</font>"+res._text[idx + len (word.text):]  
                        #print idx , res._text , " blaaaa"
                        if idx+7>len_comment : break   # когато превърти 
                    
                res._text = res._text+u' <a href="/redirect/?mark_read=1&id='+ unicode(res._id)+ u'" target="_blank" class = "check">Маркирай за проверено</a>'         #/redirect/?mark_read=1&url={{ bla._url|safe }}&id={{ bla._id|safe }} 
            #print unicode(result)                      
            #да проверявам дума по дума в result и да маркирам цензурните думи в червено
            
            cenzor_comments_list.extend(result)
        #print "test /n",cenzor_comments_list[0] 
        #print   len( cenzor_comments_list),int(page)
        return render_template('comments.html' ,blas = cenzor_comments_list[int(page)*PAGE_SIZE:int(page)*PAGE_SIZE+PAGE_SIZE], num_comments = len(cenzor_comments_list),page = int(page),cenzor = 1,news_choice = news_field ) 
         
         
         
         
         
@app.route('/user/<nickname>')
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.before_request
def before_request():
    '''Този декоратор е предназначен да сe извиква функцията преди всеки рикуест '''
    
    #print len(g.cenzor_lst)
    pass
    #g.cenzor_lst_full=[ text_tup[0]+text_tup[1]+text_tup[2]  for text_tup  in cenzor.query.with_entities(cenzor.text).all()]
    #print g.cenzor_lst
     


@app.route('/test')
def test():
	return render_template('bootstraptest.html')
