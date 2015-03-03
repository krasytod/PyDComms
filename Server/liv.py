# -*- coding: utf-8 -*-
"""
Created on Mon Sep 22 09:52:35 2014

@author: Vonodna
"""

#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import division
import string
import sys
import math

def load_comment_list(filename):
    lst=[]
    f=open(filename,'r')
    while True:
        line = f.readline()
        if not line: break
        lst.append(line.strip())
    f.close()
    return lst

def compare_texts(s1, s2):
    if len(s1)<1 or len(s2)<1:
        return 1    
    translate_to=u','    
    not_letters_or_digits = u'!"#%\'()*+,-./:;<=>?@[\]^_`{|}~'
    translate_table = dict((ord(char), translate_to) for char in not_letters_or_digits)  
    # s1=s1.translate(string.maketrans("",""), string.punctuation) #removing punctuation   не работи с уникод!!!
    s1=s1.translate(translate_table)
    s1=s1.upper()
    s1=s1.strip()
    s1=s1.split() #split the sentence in words
    s2=s2.upper().translate(translate_table).strip().split()
    
    #if abs(len(s1)-len(s2))>100: #magic number, I know
        #print "Continue"
        #continue
    l=[[0] * (len(s2)+1) for i in range(len(s1)+1)]
    for i in range(len(s1)+1):
        l[i][0]=i

    for i in range(len(s2)+1):
        l[0][i]=i

    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            #print "comparing",  s1[i-1], s2[j-1]
            if s1[i-1]==s2[j-1]:
                repl=0
            else:
                repl=1
            l[i][j]=min(l[i-1][j-1]+repl,l[i-1][j]+1,l[i][j-1]+1)
    #print "Levenstein distance is",l[len(s1)-1][len(s2)-1]
    #print l[len(s1)-1][len(s2)-1]/len(s1)
    #print '==========================================='
    mindistance=l[len(s1)][len(s2)]/max(len(s1),len(s2))
    return mindistance    


'''
s='"Мутрата" води най-голямата партия в България! Може да е тиква, може да е бандит, но е абсолютно прав, няма ли мнозинство в Парламента, нищо няма да зависи от него и ще има избори до дупка! И РБ и Бардаков са гола вода, въздух под налягане! Плямпане, плямпане, плямпане! Плюят Бойко, че прерязал 1000 лентички! Да не си ги е рязал за кеф в къщи! Първо строиш, после режеш! 1000 обекта - 1000 лентички, кой е построил повече от него! Уж критикуват, а всъшност го хвалят! 1000 лентички за 3 години, а "великия" Путин за 14 години нито една!'#.decode("cp1251")#.encode('utf8')
s1=s[:]
enw=load_comment_list('comments.txt') #loading comments

mindst=1000
most_similar=''

for ww in enw:
    mindistance=compare_texts(s, ww)
    if mindistance<mindst:
        mindst=mindistance
        most_similar=ww
        
print "Compared to\n"
print s
print "The most similar text is to:\n"
print most_similar
print "\n with levenstein distance of:",mindst
'''
