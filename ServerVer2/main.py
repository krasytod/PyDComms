#!flask/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  6 13:32:24 2015

@author: krasytod
"""
from daemonClass import Daemon
#import socket               # Import socket module
import logging, threading,time
logging.basicConfig(filename='log.log',level=logging.DEBUG)
import dirbg
import run
#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')

def PeriodCheck(times = 60*5*5):  #5 minutes
        while True:
            logging.info('checkfunc period is: '+str(times))
            dirbg.run_me()
            time.sleep(times)   

def FlaskStart ():
    run.run_flask()
    



class ServerDaemon(Daemon):
    def PeriodCheck(self,times = 60*5):  #5 minutes   # това май е за махане
        while True:
            logging.info('checkfunc period is: '+str(times))
            dirbg.run_me()
            time.sleep(times)   

    def run(self):
        logging.info('run')
        scraper_thread = threading.Thread(target=PeriodCheck,args = (45,))
        scraper_thread.daemon = True
        scraper_thread.start()
        logging.info('after scraper')
        #FlaskStart()
        logging.info('after flask')
          #
        
        
if __name__ == "__main__":
    main_thread = ServerDaemon('test.bla')
    main_thread.run()
