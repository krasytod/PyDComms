# -*- coding: utf-8 -*-
"""


@author: krasytod
"""


## general imports
import urllib2,gzip,cookielib, requests
#from requests import session
import random,re, shelve
from cookielib import LWPCookieJar
from bs4 import BeautifulSoup as BS
import helper,dirbg 
import logging,time #,cookielib
from StringIO import StringIO
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
URL_DIRBG = "http://dnes.dir.bg/cat/all/"   #dnes.dir.bg/cat/all/?section=all&page=0&state=0&titles=
import datetime

def soupufy(response_text):
	''' Да извадим всички коментари и техните атрибути от админ екстърнал панела'''
	soup = BS(response_text)
	list_comms = soup.find("div", {"id":"list"})  #списък с всичките коментари
	comments_list = list_comms.findAll("tr")
	comments_list_return = list() # сет с всички коменти
	news_dict= dict()
	for comment in comments_list:
		comm_id ,type_comm = comment.get('id'),comment.get('bgcolor')  # comment id и цвета на коментара
		comm_type = 0
		if type_comm =="red":
			#print "cherven" 
			comm_type = 2
		elif type_comm =="pink":
			#print "pink" 
			comm_type = 3
		
		
		elif comm_id == None:
			continue
		else:
			comm_type = 1
		list_td = comment.findAll("td") 
		#list_td[1]   - Журнал
		_com_reason =  comment.find("input",{"type":"radio"}).get("name")[9:] #        r_reason_
		comm_topic= list_td[2].get_text()  #от това се вадят интересните неща за топика                  #,"BRRRRRRRRRRRRRRRR\n" 
		news_id = re.search(r'\b\d+\b',comm_topic).group(0)       #   ,"::::::",comm_topic
		news_link = list_td[2].find("a",{"target":"_blank"}).get("href")
		#print news_link
		news_name = list_td[2].findAll("a")[1].get_text()
		comm_user = list_td[3].get_text()   #заглавие
		comm_date = list_td[4].get_text()
		comm_ip = list_td[5].get_text()
		comm_post = list_td[7].get_text()
		comm_edit_url = list_td[8].find("a").get("href")
		#print list_td[8], comm_edit_url
		comm_secs = helper.dirbg_convert_time_admin_ext("2015-04-27 20:49:32")
		#print comm_id ,comm_type,news_id ,news_link,news_name,comm_user,comm_date,comm_ip,comm_post,comm_secs,  "\n\n\n::::::::\n\n\n"
		one_comm_list = list([comm_date,comm_id ,comm_secs,comm_post,comm_user,comm_type,news_id ,0,comm_ip,"http://dnes.dir.bg/comments/"+comm_edit_url,_com_reason])
		comments_list_return.append(one_comm_list)
		news_dict [news_id ] = [news_link ,news_name,list_td[1].get_text()]
	#comments_list_return.append([ news_id,news_name, news_link])
	#print comments_list_return[0],len(comments_list_return[0])
		

		
		
	return comments_list_return,news_dict

def soupufy_brote(response_text,comments_list =[]):
	''' Да извадим всички коментари и техните атрибути от едитор екстърнал панела.Връща лист от дикшънарита'''
	soup = BS(response_text)
	#comments_list = []
	list_comms = soup.findAll("div", {"class":"AppComm_coment _comment"})  #списък с всичките коментари
	
	for comment_div in list_comms:
		#print comment_div.find("span",{'class': 'commentDate'}).get_text().split("-")[0]            #comment_div.find("br",{"clear":"all"}).get_text()
		commentar_dict = dict()
		commentar_dict['user'] = comment_div.find("div",{"class":"left"}).find("img").get("title") 
		commentar_dict['ip'] =  comment_div.find("span",{'class': 'commentDate'}).get_text().split("-")[1]     #user         # comment_div.get("id").split("_")  - id На новина и коментар
		commentar_dict['news_id']=comment_div.get("id").split("_")[3]
		commentar_dict['comm_id']=comment_div.get("id").split("_")[4]
		commentar_dict['id']=comment_div.get("id")
		commentar_dict['text'] =  comment_div.find("br",{"clear":"all"}).get_text()
		commentar_dict['date'] = comment_div.find("span",{'class': 'commentDate'}).get_text().split("-")[0]  
		comments_list.append(commentar_dict)
		#print comments_list
		#print comment_div.get("id").split("_"),comment_div.find("div",{"class":"left"}).find("img").get("title") 
	return 0 #comments_list


def extact_comment_brote (links = ['http://dnes.dir.bg/comments/list_ed.php?jnl_id=3&ctype_id=1&topic_id=19068162&list=all&page=1&ran=0.08729374515991262']):
	'''Екстрактва коментарите от едиторс панела и ги връща като лист от дикшинърита'''
	#print links
	#links = {'11': {'url': u'http://dnes.dir.bg/comments/list_ed.php?jnl_id=3&ctype_id=1&topic_id=19080958&list=all&page=1&ran=0.08729374515991262', 'text': u'\u0410\u0442\u0438\u043d\u0430 \u043d\u044f\u043c\u0430 \u0434\u0430 \u043e\u0442\u0441\u0442\u044a\u043f\u0438 \u0437\u0430 \u043e\u0440\u044f\u0437\u0432\u0430\u043d\u0435 \u043d\u0430 \u0437\u0430\u043f\u043b\u0430\u0442\u0438 \u0438 \u043f\u0435\u043d\u0441\u0438\u0438', 'br': 0}}
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	comments_list = []
	
	
	for link in links.values():
		response=season_dir.get(link['url'], headers  = headers)
		soupufy_brote(response.text,comments_list) 
	#print "ii: " ,len(comments_list)
	return  comments_list#comm_list , news_dict
	
def Brote_stop_this(comentar_za_spirane):
	'''Получава коментара  дикшънари и спира коментара с основание спам'''
	
	# filter:"0" , allow[]:"0",select[]:"0",unselect[]:"0",reject[]:"0",unflag[]:"0",revise[]:"4_1_19075213_95295" , reject[]:"13_1_19076304_94239"     r_reason_13_1_19076304_94239:"5"  - спам
	#",20150517105955_3_1_19068162_94627_1740068_5,20150517114119_3_1_19068162_94773_1740068_5"
	payload = { "jnl_id":"3","ctype_id":"1","topic_id":comentar_za_spirane["news_id"],"allow":"","reject":","+comentar_za_spirane['id']+"_5","select":"","unselect":"","move":"","move_selected":"","move_to":"0","action":"submit_all"}
	#print payload
	#payload ["reject[]"] = comentar_za_spirane["id"]
	#payload ["r_reason_"+comentar_za_spirane["id"]] = "5"
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","X-Requested-With":"XMLHttpRequest",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive","Referer":"http://dnes.dir.bg/news_comments.php?id="+comentar_za_spirane["news_id"]}
	response=season_dir.post("http://dnes.dir.bg/comments/admin.php", data=payload,headers  = headers)
	#print response.status_code,response.text 
	
	
def Brote_restore_this(comentar_za_puskane):
	'''Получава коментара като дикшънари и го връща '''
	# filter:"0" , allow[]:"0",select[]:"0",unselect[]:"0",reject[]:"0",unflag[]:"0",revise[]:"4_1_19075213_95295" , reject[]:"13_1_19076304_94239"     r_reason_13_1_19076304_94239:"5"  - спам
	#
	payload = { "jnl_id":"3","ctype_id":"1","topic_id":comentar_za_puskane._news_id,"allow":"","reject":","+comentar_za_puskane._id+"_5","select":"","unselect":"","move":"","move_selected":"","move_to":"0","action":"submit_all"}
	#print payload
	#payload ["reject[]"] = comentar_za_spirane["id"]
	#payload ["r_reason_"+comentar_za_spirane["id"]] = "5"
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","X-Requested-With":"XMLHttpRequest",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive","Referer":"http://dnes.dir.bg/news_comments.php?id="+comentar_za_puskane._news_id}
	response=season_dir.post("http://dnes.dir.bg/comments/admin.php", data=payload,headers  = headers)
	

def post_admin_ext(payload):
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	predifined_payload = { "action":"update","list":"awaiting","page":"1","jnl_id":"0","ctype_id":"0","topic_id":"0","thread_id":"0","hobby_id":"","journals":"3,4,5,7,8,13,14,15,16,17,23,24,25,29,33,35,43"
	,"ctypes":"1,2,3,4,5,6,7,11,13,16,17,18,19,20,21","latest_by_topic":"","filter":"0"}
	payload.update(predifined_payload)
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","X-Requested-With":"XMLHttpRequest",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive","Referer":"http://dnes.dir.bg/comments/admin_list_ext.php"}
	response=season_dir.post("http://dnes.dir.bg/comments/admin_list_ext.php", data=payload,headers  = headers)
	#print payload
	if response.status_code == 200:
		return 0
	else:
		print "post_admin_ext error:",response.status_code
		return 1







def get_news_text_by_id(link):
	''' по получен линк към коментарите на новината , връща нейното заглавие'''
	#http://dnes.dir.bg/news_comments.php?id=19103710
	#http://dnes.dir.bg/comments/list_ed.php?jnl_id=3&ctype_id=1&topic_id=19101072&list=all&page=1&ran=0.08729374515991262
	return  "http://dnes.dir.bg/news_comments.php?id="+re.findall('\d+',link)[2]
	
	
def get_news_text_by_link(link):
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	u'User-Agent':u"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	season_dir = requests.session()
	## създаване на кукитата, така че да могат да се съхпанят във файл, после извикваме гет или пост на рекуест сешъна
	cookie_file = 'cookies.txt'
	cj = cookielib.LWPCookieJar(cookie_file)
	season_dir.cookies = cj
	response =season_dir.get(link,headers = headers)
	soup = BS(response.text)
	h3 = soup.find("h3").get_text()
	#print h3
	return h3


def brote_moderate(comments_list,users_ban=[u'Мулетаров'] ,ip_ban=["127.0.0.1"]):
	'''Подпрограмата за спиране на брут коментари '''
	#mod_duma = u'Мулетаров'  #http://dnes.dir.bg/comments/list_ed.php?jnl_id=3&ctype_id=1&topic_id=19080958&list=all&page=1&ran=0.08729374515991262
	
	com_stoped= []   #лист със спряните коментари
	#print users_ban.keys()
	#print "ebb: ",len(comments_list)
	for comment in comments_list:
		for user in users_ban.keys():
			#print user,comment['user']
			if user in comment['user']:
			#print comment['id']
				comment['stoped_time'] = datetime.datetime.now().strftime("%H:%M:%S")
				Brote_stop_this(comment)
				#print "h"
				com_stoped.append( comment)
		for ip in ip_ban.keys():
			#print "bs: ", comment['ip']
			if ip in comment['ip']:
			#print comment['id']
				comment['stoped_time'] = datetime.datetime.now().strftime("%H:%M:%S")
				Brote_stop_this(comment)
				#print comment['ip']
				com_stoped.append( comment)
	return com_stoped
    
def vote_up(link,small_loop=10,big_loop=4,action=1):
    #print "vote",link
    '''Гласува автоматично в коментарите под новините. Очаква линка за гласуване, брой гласувания, и типа гласуване. 1 - положителен,2 -отрицателен '''
    import time
    #link ="https://panopticlick.eff.org/index.php?action=log&js=yes" 
    links= ["http://dnes.dir.bg/comments/voting.php?jnl_id=3&ctype_id=1&topic_id=18753004&comment_id=185917&action=2&ts=0.33454112514499024","http://dnes.dir.bg/comments/voting.php?jnl_id=3&ctype_id=1&topic_id=18753004&comment_id=185917&action=2&ts=0.4233232323234","http://dnes.dir.bg/comments/voting.php?jnl_id=3&ctype_id=1&topic_id=18753004&comment_id=185917&action=2&ts=0.55654112514499024"]
    user_agents= [u"Mozilla/6.0 (compatible; MSIE 11.0; Windows NT 6.2)",u"Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)",u'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20102341 Firefox/32.0',u'Mozilla/5.0 (Macintosh; U; Intel Mac OS X; de-de) AppleWebKit/523.10.3 (KHTML, like Gecko) Version/3.0.4 Safari/523.10',' Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; de-de) AppleWebKit/533.16 (KHTML, like Gecko) Version/5.0 Safari/533.16']
    user_ag =  u'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; de-de) AppleWebKit/633.16 (KHTML, like Gecko) Version/6.0 Safari'
    rand= random.randint(1,70)  # в случай, че се нареди повторно гласуване, да има малък шанс юзър агента да е същия
    for idx in range(small_loop):
      cj = cookielib.CookieJar()
      user_agent =  user_ag +unicode(rand)+ unicode(idx) + u'.'+unicode(big_loop)
      opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj),urllib2.HTTPRedirectHandler())  #,urllib2.HTTPHandler(debuglevel=1)
      #print idx
      opener.addheaders = [('User-Agent',user_agent ),('Referer', 'http://dnes.dir.bg/'),('Accept','text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),('Accept-Charset', 'UTF-8;q=0.7,*;q=0.7'),('Cache-Control', 'no-cache'),('Accept-encoding', 'gzip'),('Accept-Language','de,en;q=0.7,en-us;q=0.3')]
      #print link
      urllib2.install_opener(opener)
      dirbg = urllib2.urlopen(unicode(link))
      if dirbg.info().get('Content-Encoding') == 'gzip':
         buf = StringIO( dirbg.read())
         dirbg_decoded = gzip.GzipFile(fileobj=buf)
         soup = BS(dirbg_decoded.read()) 
      else:   
         soup = BS(dirbg.read())
      time.sleep(5.5)
      
def login(user=u'bla',password=u'bla'):
	'''Функцията за логване в дира '''
	 ## Първо да заредим началната страница на клубовете и да приберем кукитата
	 ## Необходимите параметри
	url_first= "http://clubs.dir.bg"
	url_login = 'https://id.dir.bg/login_site.php'
	headers  = {"Host":"clubs.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	u'User-Agent':u"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	season_dir = requests.session()
	## създаване на кукитата, така че да могат да се съхпанят във файл, после извикваме гет или пост на рекуест сешъна
	cookie_file = 'cookies.txt'
	cj = cookielib.LWPCookieJar(cookie_file)
	season_dir.cookies = cj
	response =season_dir.get(url_first,headers = headers)
	season_dir.cookies.save(ignore_discard=True, ignore_expires=True)
	#print response.cookies,"\n\n", response.text
	#print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa"
	payload = {"username": 'chlen1', "password": 'supatopcheta'}
	headers2  = {"Host":"id.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	'Referer': "http://clubs.dir.bg/",
	u'User-Agent':u"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	## създаваме сийзън и използваме за да заредим началната страница на клубовете и после да се логнем
	season_dir.cookies.load()
	response = season_dir.post(url_login, data=payload,headers  = headers2)
	#response = season_dir.get('http://dnes.dir.bg/comments/admin_list_ext.php')                   #http://clubs.dir.bg/login.php?Cat=
	response = season_dir.get("http://clubs.dir.bg/login.php", headers  = headers)
	#print response.status_code, response.headers,response.history,response.url
	season_dir.cookies.save()
	
	#print season_dir
	return "Login Complete"





def postclubs(mnenie,tema,link="http://clubs.dir.bg/newreply.php?Cat=171&Board=gumeniglavi&Number=1953487464&page=0&view=collapsed&what=showflat&sb=5&part=&vc=1"):
	'''Поства в клуб Горна '''
	#print season_dir
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	
	get_url="http://clubs.dir.bg/newreply.php?Cat=171&Board=gumeniglavi&Number=1953755017&page=0&view=collapsed&what=showflat&sb=5&part=&vc=1"
	headers  = {"Host":"clubs.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	'Referer': "http://clubs.dir.bg/",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	action =  "http://clubs.dir.bg/addpost.php"
	response=season_dir.get(get_url,headers =headers)
	#print response.history,response.url
	#print response.status_code, response.headers,response.history,response.url, "\n########################\n\n",response.text
	payload = {"postername":"sm01","icon":"book.gif","Cat":"171","Reged":"y","Board":"gumeniglavi","Main":"1953487464","Parent":"1953755017","page":"0","view":"collapsed",
				"what":"showflat","oldnumber":"1953755017","sb":"5","part":"","vc":"1","replyto":"sm01","Subject":"Trompet","Body":"KUR"}
	headers  = {"Host":"clubs.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	'Referer': "http://clubs.dir.bg/newreply.php?Cat=171&Board=gumeniglavi&Number=1953755017&page=0&view=collapsed&what=showflat&sb=5&part=&vc=1",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	response=season_dir.post("http://clubs.dir.bg/addpost.php", data=payload,headers  = headers)
	
	#response = session.get('http://dnes.dir.bg/comments/admin_list_ext.php')                   #http://clubs.dir.bg/login.php?Cat=
	#print response.status_code, response.headers,response.history,response.url
	#print "\n\n|||||||||||||||||||||||||||||||\n\n",response.history,response.url,'\n\n\n',response.text
	#with open("fff.txt",'w<') as f:
	#	f.write(response.text)  Cat=171&Board=gumeniglavi&Number=1953754262&page=0&view=collapsed&what=showflat&sb=5&part=&vc=1
    
	#print "\n\n\n\n"
	 ### http://clubs.dir.bg/start_page.php?Cat=&fp=1&f_room_id=1&option=Âõîä&toMess=/&GDirId=e506a2827ec0eb390f5ca84ae1c1bdc6
	 
	 
def admin_list_ext(link = 'http://dnes.dir.bg/comments/admin_list_ext.php'):
	'''Зарежда страницата с коментарите за модерация от системата '''
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	response=season_dir.get(link, headers  = headers)
	#print response.status_code,response.text
	result = soupufy(response.text)  #comm_list , news_dict
	return result

def helper_extract_edit_comment(response_text):
	'''Помощна функция която получава текста от гет заявката и връща необхидимите данни. <form action="/comments/edit_ext.php" method="post" name="form1">
  <input type="hidden" name="action" value="update">
  <input type="hidden" name="jnl_id" value="3">
  <input type="hidden" name="ctype_id" value="1">
  <input type="hidden" name="topic_id" value="18964694">
  <input type="hidden" name="is_selected" value="0">
  <input type="hidden" name="url" value="/comments/admin_list_ext.php#18964694_177536">
  <input type="hidden" name="translit" value="0">
  <input type="hidden" name="id" value="177536">
   <input type="checkbox" name="hide_nickname" value="1"/>
   <textarea id="cbody" name="body" style="width: 500px; height: 200px">Ако си карал по цариградско шосе или южната дъга с 55 трябва да ти отнемат книжката</textarea>
'''
	soup = BS(response_text)
	soup_form = soup.find("form")  #списък с всичките коментари
	form_action= soup_form.get("action")
	form_name= soup_form.get("name")
	action = soup_form.find("input",{'name':'action'}).get("value")
	jnl_id = soup_form.find("input",{'name':'jnl_id'}).get("value")
	ctype_id = soup_form.find("input",{'name':'ctype_id'}).get("value")
	topic_id = soup_form.find("input",{'name':'topic_id'}).get("value")
	is_selected = soup_form.find("input",{'name':'is_selected'}).get("value")
	url = soup_form.find("input",{'name':'url'}).get("value")
	translit = soup_form.find("input",{'name':'translit'}).get("value")
	_id = soup_form.find("input",{'name':'id'}).get("value")
	checkbox = soup_form.find("input",{'name':'hide_nickname'}).get("value")
	area = soup_form.find("textarea",{'name':'body'}).get_text()
	area_id = soup_form.find("textarea",{'name':'body'}).get("id")

	
	return (form_action,action,jnl_id,ctype_id ,topic_id ,is_selected,url ,translit,_id ,checkbox ,area )

def hide_user(_id="177536",topic_id="18964694",ctype_id="1",jnl_id="3",link = 'http://dnes.dir.bg/comments/edit_ext.php'):
	'''Зарежда страницата с редакция на отделен коментар(скриване на име) '''
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	payload = {'id':_id,'topic_id':topic_id,'ctype_id':ctype_id,'jnl_id':jnl_id}
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	response=season_dir.get(link, headers  = headers,params = payload)
	#print response.url
	###да извадим от върнатия отговор нещата които ни интересуват
	form_action,action,jnl_id,ctype_id ,topic_id ,is_selected,url ,translit,_id ,checkbox ,area  = helper_extract_edit_comment(response.text)  #comm_list , news_dict
	form_action = 'http://dnes.dir.bg/'+form_action
	payload = {'id':_id,'topic_id':topic_id,'ctype_id':ctype_id,'jnl_id':jnl_id,'action':action,'is_selected':is_selected,'translit':translit,'hide_nickname':"1",'body':area,'url':url,'subject':"" }
	response=season_dir.post(link, headers  = headers,data = payload)
	#print response.status_code
	return response.status_code


def get_news(link="http://dnes.dir.bg/?&state=2"):
	'''Връща списък от линкове с най-популярните новини под формата на лист от речници с ключове text и url  '''
	season_dir = requests.session()
	season_dir.cookies = LWPCookieJar('cookies.txt')
	season_dir.cookies.load()
	headers  = {"Host":"dnes.dir.bg", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
	'User-Agent':"Mozilla/5.0 (X11; Linux x86_64; rv:39.0) Gecko/20100101 Firefox/39.0","Connection":"keep-alive"}
	response=season_dir.get(link, headers  = headers)
	soup = BS(response.text)
	comments = set()
	news = dict()
	result = soup.find("div", {"id":"fullarticles"})  #списък с всичките заглавия
	br = 0 # counter
	for div_txt in result.findAll('div',attrs={'class':'txt'}):
		#<div class="txt"><h2><a href="/news/oon-kristalina-georgieva-generalen-sekretar-19057381?nt=10">”Политико” слага Кристалина Георгиева начело на ООН</a></h2>
           # Престижното американско издание “Политико” пише, че предвид бързия ѝ възход все повече гласове в Брюксел виждат Кристалина Георгиева в... <b><a href="/news/oon-kristalina-georgieva-generalen-sekretar-19057381?nt=10">прочети още »</a></b>
		#print div_txt, "\n\n"
		one_news_dict = dict()
		one_news_dict['text'] =  div_txt.find('a').get_text()
		news_id =   re.findall(r'\d+\?nt', div_txt.find('a').get('href'))[0][:-3]  # така взимаме IDто на новината
		if news_id == None:
			continue
		one_news_dict['url'] = "http://dnes.dir.bg/comments/list_ed.php?jnl_id=3&ctype_id=1&topic_id="+news_id + "&list=all&page=1&ran=0.08729374515991262"
		#one_news_dict['counter'] = str(br)
		one_news_dict['br'] = 0
		news[str(br)] = one_news_dict
		br +=1
 		
		#print a_link.get('href'),a_link.getText()  # заглавие и линк на новините на Първа

	return news



def mark_cenzor_wrods(comments,cenz_words,cenzor_names):
	'''Получава лист от коментари и лист от цензорни думи. Обикаля и маркира цензорните думи в коментарите. Връща променените коментари  PS. Името на функцията е сгрешено, но вече го има написана на твърде много места  восновния модул'''
	for comment in comments:
		for word in cenz_words:
			idx =  -6 
			len_comment = len(comment._text)
			cenz_html_str = '<font size="'+str(word.weight )+'" color="red">'  # стринга за вмъкване
			#print "/n " + word.text 
			while  comment._text.find( word.text,idx+6) !=-1:
				if  comment._text.find('"red">'+ word.text,idx+6) !=-1: break   # в случай че се подава един и същ коментар втори път
				idx=comment._text.find( word.text,idx+6) 
				comment._text = comment._text[:idx]+ cenz_html_str+ comment._text[idx:idx + len (word.text)]+"</font>"+comment._text[idx + len (word.text):]  
				#print idx , res._text , " blaaaa"
				if idx+7>len_comment : break   # когато превърти 
		for name in cenzor_names:
			#print name.text
			if comment._user.find(name.text) !=-1: # and comment._status == 1:
				comment._status =7 
				print comment._status
				#comment._user = '<font color="red">'+comment._user +"</font>"
				
def perform_premoderation_admin_ext(comments_lst):
	'''Изпълнява опциите от модшелфа по модериране по юзър и айпи '''
	mod_shelve = shelve.open('moderation.db')
	temp_user = mod_shelve['mod_user']
	#1#### Да намерим дали потребителя е в условията ма модерация по име
	comments_lst_loop = list(comments_lst)  # правиме копие на оригиналния лист
	comments_lst = comments_lst.all()
	#print type(comments_lst)
	for comment in comments_lst_loop:
		for key in temp_user.keys():
			if key in comment._user:  #1КРАЙ####
				#print key ,(temp_user[key]) 
				#print type(temp_user[key]) 
				#Да проверим какво трябва да направим с коментара, да го извадим от мястото му в  листа, да извършим необходимите десйтвия и да го върнем най-отзад
				if int(temp_user[key]) == 1:  # Наблюдавай само
					comment._status = 7
					comment._text = u'<font size="6" color=#551112> ПОТРЕБИТЕЛЯ Е СЛЕДЕН </font> <br>' + comment._text
				elif int(temp_user[key]) == 2:  # коментара да е готов за реджект и скрит в див
					comment._status = 8
					#print comment._user
					#comments_lst.append(comment)
	#comments_lst= list(comments_lst_return)
	

if __name__ == "__main__":
    pass    
    
    
def run_me_t(s=""):
    from time import sleep
    sleep(5)
    s="blaa"
