#!/usr/bin/python
from daemonClass import Daemon
import socket               # Import socket module
import logging
logging.basicConfig(filename='log.log',level=logging.DEBUG)

#logging.debug('This message should go to the log file')
#logging.info('So should this')
#logging.warning('And this, too')


class App(Daemon):
    
    def run(self):
        logging.info('run')
        soc = socket.socket()         # Create a socket object
        host = socket.gethostname() # Get local machine name
        port = 12345                # Reserve a port for your service.
        soc.bind((host, port))        # Bind to the port
        soc.listen(5)                 # Now wait for client connection.
        while True:
            c, addr = soc.accept()     # Establish connection with client.
            print 'Got connection from', addr
            c.send('Thank you for connecting')
        c.close()                # Close the connection
#Appa = App('test.bla')
#Appa.run()
'''
s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
port = 22345                # Reserve a port for your service.
s.bind((host, port))        # Bind to the port
s.listen(5)                 # Now wait for client connection.
while True:
    c, addr = s.accept()     # Establish connection with client.
    print 'Got connection from', addr
    c.send('Thank you for connecting')
c.close()                # Close the connection
'''