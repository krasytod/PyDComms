# -*- coding: utf-8 -*-
"""
Различни допълнителни функции 
Created on Mon Sep 29 12:11:35 2014

@author: krasytod
"""
import datetime

def dir_convert_time(time_struct):
    '''Конвертира времето върнато от date.time в секунди по подобие на дирбгконверттайма.  '''
    return (time_struct.tm_year-2000)*12*24*3600*31  + time_struct.tm_mon*24*3600*31 + time_struct.tm_mday*24*3600 + time_struct.tm_hour*3600 + time_struct.tm_min*60


def dirbg_convert_time(time_string):
    ''' конвертира дата/час стринг в интиджър с int = 0  01.01.2000 00:00
    пример date_string  = "23.09.2014 16:09  , date_int = 476122140
    '''
    total_seconds = 0
    if  len(time_string) < 17:     # понякога тайм стринга съдържа и други символи(нещо с кодировката) които крашват функцията
        try:
            pt =datetime.datetime.strptime(time_string ,'%d.%m.%Y %H:%M')
            total_seconds = pt.minute*60+pt.hour*3600 +  (pt.year-2000)*12*24*3600*31+ pt.month*24*3600*31  + pt.day*24*3600  # * забележка най-отдолу
        except ValueError:
            print "pt"
    else: 
        total_seconds = 666666
    #==============================================================================
    # *забележка -   очевидно кода е бъгав, месеца се приема автоматично че е 31 дни зав сички месеци, годините не се съобразява че може и да са високосни.  Ще работи за текущата цел но в бъдеще се налагат промени
    #==============================================================================

    return total_seconds

def dnevnik_convert_time(time_string):
    ''' конвертира датата и часа взети от коментара в дневник, особено спрямо дира е че използва букви за месец, "окт= октомври и тн"
    #22:28 01 окт, 2014  
    '''
    #print time_string
    correct_date = time_string[:8]+time_string[14:]
    month = time_string[9:12]
    month_dict = {u"окт":10,u"сеп":9,u"авг":8,u"юли":7,u"юни":6,u"май":5,u"апр":4,u"мар":3,u"фев":2,u"яну":1,u"ное":11,u"дек":12}  #Речник за мап-ване на стринга от дневник към числово представяне на месеца, 
    #print correct_date
    month =  month_dict[month]
    pt =datetime.datetime.strptime(correct_date,u'%H:%M %d%Y')
    total_seconds = pt.minute*60+pt.hour*3600 +  (pt.year-2000)*12*24*3600*31+ month*24*3600*31  + pt.day*24*3600
    return total_seconds

#print dnevnik_convert_time(u"14:46 01 окт, 2014")