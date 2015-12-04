#!/usr/bin/env python
#This file is xmlrpc server for "Run.py".
from xmlrpc.server import SimpleXMLRPCServer
import configparser
import sqlite3
import unittest
import logging
import subprocess
from time import gmtime, strftime
import sys

#This is the unit testing classs 
#Line to enable/disable unit testing is in main -  unittest.main()

class TestServer(unittest.TestCase):

    #THe IP and Port inputs are already sanitized from client input 
    #Only usernames and passwords need to be checked 
    def test_add_user(self):
        logging.debug('Testing add_user()')
        #Valid Credentials to add
        self.assertTrue(db.add_user('joe', 'pw5', '127.0.0.202', 3333))
        self.assertTrue(db.add_user('baaarefs', 'asdfasaw', '127.0.0.302', 6666))
        self.assertTrue(db.add_user('^&*(@#$@#$@#$@#$', '@#$*&@#($*&@#*$&', '127.0.0.4', 42))
        #Username already taken       
        self.assertFalse(db.add_user('joe', 'pw5', '127.0.0.420', 123123123))
        self.assertFalse(db.add_user('Arevor', 'wronglol', '127.0.0.2', 12453))
        #2 or less character username
        self.assertFalse(db.add_user('', '565', '127.0.0.420', 123123123))
        #2 or less character password
        self.assertFalse(db.add_user('Jimbob', '5', '127.0.0.420', 123123123))
        #No Username or password
        self.assertFalse(db.add_user('', '', '127.0.0.1', 1))
        self.assertFalse(db.add_user('  ', '  ', '127.0.0.1', 1))

    def test_update_userinfo(self):
        logging.debug('Testing update_userinfo()')
        #Valid user supplied to update
        self.assertTrue(db.update_userinfo('joe', 'pw6', '127.0.0.420', 4444)) 
        self.assertTrue(db.update_userinfo('Arevor', 'pw1', '127.0.0.422', 4422))
        #Invalid user supplied to update
        #Returns true, but nothing is updated 
        self.assertTrue(db.update_userinfo('jimbo','pw6', '127.0.0.420', 4444)) 
        #No user supplied to update
        self.assertFalse(db.update_userinfo('', 'abc', '127.0.0.1', 4))
        #blank user 
        self.assertFalse(db.update_userinfo('  ', '123', '127.0.4.1', 234234))
        #Under x Charcaters 
        self.assertFalse(db.update_userinfo('x', 'y', '127.0.4.1', 234234))

    def test_check_user(self):
        logging.debug('Testing check_user()')
        #Valid user/pw 
        self.assertTrue(db.check_user('Arevor', 'pw1'))
        self.assertTrue(db.check_user('Dharm', 'pw2'))
        #invlid username and password
        self.assertFalse(db.check_user('Jerome', '123'))
        #Valid username, not password
        self.assertFalse(db.check_user('Arevor', 'asdhf73'))
        #Valid password, not username
        self.assertFalse(db.check_user('Jerome', 'pw1'))
        self.assertFalse(db.check_user('Jerome', 'pw3'))
        #case senitive 
        self.assertFalse(db.check_user('arevor', 'pw1'))

    def test_check_friend(self):
        logging.debug('Testing check_friend')
        #Valid friend
        self.assertTrue(db.check_friend('joe'))
         #invalid friend
        self.assertFalse(db.check_friend('abgguhr') )
        self.assertFalse(db.check_friend('')) 
        self.assertFalse(db.check_friend('  ')) 

    def test_lookup_friend(self):
        logging.debug('Testing lookup_friend()')
        #Valid friend to lookup
        self.assertEqual(db.lookup_friend('Arevor'),('127.0.0.220', '42020'))
        self.assertEqual(db.lookup_friend('joe'),('127.0.0.202', '3333'))#is not using updated joe values? con.commit ?
        #Username does not exist
        self.assertFalse(db.lookup_friend('Arev'))
        self.assertFalse(db.lookup_friend('  '))

    def test_isBlank(self):
        logging.debug('Testing isBlank()')
        #blank lines
        self.assertTrue(db.isBlank(''))
        self.assertTrue(db.isBlank(' '))
        self.assertTrue(db.isBlank(""))
        self.assertTrue(db.isBlank('                               '))
        #before/after whitespace 
        self.assertFalse(db.isBlank('bobobboob      '))
        self.assertFalse(db.isBlank('   bobobo   '))
        self.assertFalse(db.isBlank('  bobob'))

    def test_isValidLen(self):
        self.assertFalse(db.isValidLen('abcabcabc'))
        self.assertTrue(db.isValidLen(''))
        self.assertTrue(db.isValidLen('xy'))

    #This method is not accessible to the user, ie an existing account cannot be deleted
    def test_remove_user(self):
        logging.debug('Testing remove_user()')
        #Valid User to remove
        self.assertTrue(db.remove_user('joe'))
        #User does not exist
        self.assertTrue(db.remove_user('ripdude'))
        #Under 2 Characters or blank 
        self.assertFalse(db.remove_user(''))
        self.assertFalse(db.remove_user('x '))
        self.assertFalse(db.remove_user('x'))

    def test_send_offlinemsg(self):
        logging.debug('Testing send_offlinemsg()')
        #invalid usernames 
        self.assertFalse(db.send_offlinemsg('', 'message goes here', ''))
        self.assertFalse(db.send_offlinemsg('xx', 'message goes here', ''))
        self.assertFalse(db.send_offlinemsg('', 'message goes here', 'xx'))
        #valid usernames 
        #self.assertTrue(db.send_offlinemsg('Arevor', 'offline message text', 'Calvin'))
        #self.assertTrue(db.send_offlinemsg('Nolan', 'offline message text', 'Arevor'))
        #self.assertTrue(db.send_offlinemsg('Arevor', 'offline message text', 'Nolan'))

    def test_get_offlinemsg(self):
        logging.debug('Testing get_offlinemsg')
        #Valid usernames 
        self.assertEqual(db.get_offlinemsg('Arevor'),[('offline message text', 'Nolan'),('offline message text 2', 'Nolan')])
        self.assertEqual(db.get_offlinemsg('Nolan'),[('offline message text', 'Arevor'),('offline message text 2', 'Arevor')])
    


 
#This class requires database called 'users.db' on the same folder as the 'server.py'
#For unittesting, createLogins.sql is used to create a new database named with appropriate timestamp
class Server_db:
    """ 
    The class allows operations with data in database.The class uses sqlite3 module.
    """
    def __init__(self,dbname,server_ip,server_port):
        """
        Create the database with given dbname. Then connect to the database
        and create a cursor for executing sqlite3 commands. 
        """
        self.dbname = dbname
        self.con = sqlite3.connect(dbname)
        self.cur = self.con.cursor()
        self.server_ip=server_ip
        self.server_port=server_port

        # The access method from server initialization
        self.server = SimpleXMLRPCServer((server_ip, int(server_port)))
        logging.info('Server started on %s %s', server_ip, server_port)


    def add_user(self, username, password, ip, port):
        """
        Take username, password, user's ip and user's port number and add the new user to the database.
        """
        if (self.isBlank(username) or self.isBlank(password)):
            return False
        if (self.isValidLen(username) or self.isValidLen(password)):
            return False
               
        safe_input = (username, password, ip, port)
        try:
            self.cur.execute("INSERT INTO Users(Username,Password, Client_IP, Client_Port) VALUES (?, ?, ?, ? )" , safe_input)
            self.con.commit()
            logging.info('%s was added', username)
            return True
        except sqlite3.IntegrityError: #If Unique Key already exists
            logging.info('Failed attempt to add %s', username)
            return False

    def remove_user(self, username):
        """
        Param - username - ID to be deleted from table 
        this method is not served to the clients. 
        """
        if(self.isBlank(username) or self.isValidLen(username)):
            return False
        safe_input = (username,)
        #this method should be secured ie. need more than just username to call it 
        self.cur.execute("DELETE FROM Users WHERE Username = ?" , safe_input)
        self.con.commit()
        logging.info('%s was removed', username)
        return True

    def update_userinfo(self, username, password, ip, port):
        """
        Param - Username - update password/ip/port for given username 
        """
        if (self.isBlank(username) or self.isBlank(password)):
            return False
        if (self.isValidLen(username) or self.isValidLen(password)):
            return False
        safe_input1 = (password, username)
        safe_input2 = (ip, username)
        safe_input3 = (port, username)
        self.cur.execute("UPDATE Users SET Password = ? WHERE Username = ?", safe_input1)
        self.cur.execute("UPDATE Users SET Client_IP = ? WHERE Username = ?" , safe_input2)
        self.cur.execute("UPDATE Users SET Client_Port = ? WHERE Username = ?" , safe_input3)
        self.con.commit()
        logging.info('%s user information was updated', username)
        return True

    def check_user(self,username, password):
        """
        This method take username and password of the user and check whether 
        the password and user name match with the database. Returns true if match is found 
        else returns false.
        """
        safe_input = (username, password)
        vals = self.cur.execute("SELECT Username, Password FROM Users WHERE Username=? AND Password=?",safe_input).fetchone()
        if vals:
            logging.info('%s was authenticated', username)
            return True
        else:
            logging.info('Failed login for %s', username)
            return False

    def check_friend(self, username):
        """
        Param - Username - Returns true is username exists in table, else false. 
        """
        if (self.isBlank(username) or self.isValidLen(username)):
            return False

        safe_input = (username,)
        
        vals = self.cur.execute("SELECT Username, Password FROM Users WHERE Username=?" ,safe_input).fetchone()
        if vals:
            return True
        else:
                return False

    def lookup_friend(self,username):
        """
        Param - Username - Returns tuple of (IP, Port) Assigned to current username 
        """
        if self.isBlank(username) or self.isValidLen(username):
            return False
        safe_input = (username,)
        try:
            vals = self.cur.execute("SELECT Client_IP, Client_Port FROM Users WHERE Username=?" ,safe_input).fetchone()
            if vals:
                return vals[0],str(vals[1])
            else:
                return False
        except LookupError as e:
            return False

    def send_offlinemsg(self, username, message, receiver):
        if self.isBlank(username) or self.isValidLen(username):
            return False
        if self.isBlank(receiver) or self.isValidLen(receiver):
            return False

        safe_input = (username, message, receiver)
        self.cur.execute("INSERT INTO OfflineMsgs(Username, Msg, MsgSender) VALUES (?,?,?)", safe_input)
        self.con.commit()
        logging.info('New offline for %s', username)
        return True

    def get_offlinemsg(self, username,):
        #This is a privilied method in the sense that I am assuming the user's identity has already been verified 
        #Ie you cannot receieve offline messages for another user 
        logging.debug('testing get offlinemsgs')
        safe_input = (username,)
        vals = self.cur.execute("SELECT Msg, MsgSender FROM OfflineMsgs WHERE Username=?" ,safe_input).fetchall()
        self.cur.execute("DELETE FROM OfflineMsgs WHERE Username=?", safe_input) #delete the messages once they have been retrieved
        self.con.commit()
        if vals:
            return vals 
        else:
            return False

          

    @staticmethod #does not receive implicit first agrument (no reference to self) 
    def isBlank (myString):
        if myString and myString.strip():
            #myString is not None AND myString is not empty or blank
            return False
        #myString is None OR myString is empty or blank
        return True

    @staticmethod
    def isValidLen(myString):
        if len(myString) < 3:
            return True 
        else:
            return False

    def start_xmlserver(self):
        print("Listening on port "+str(self.server_port)+"...")
        self.server.register_function(self.add_user, "add_user")
        self.server.register_function(self.check_user, "check_user")
        self.server.register_function(self.check_friend, "check_friend")
        self.server.register_function(self.lookup_friend, "lookup_friend")
        self.server.register_function(self.update_userinfo, "update_userinfo")
        self.server.register_function(self.send_offlinemsg, "send_offlinemsg")
        self.server.register_function(self.get_offlinemsg, "get_offlinemsg")
        self.server.serve_forever()

if __name__ == "__main__":
    #Initialize logging facility, format timestamp 
    logging.basicConfig(filename='server.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt='%d/%m/%y-%H:%M:%S')
    logging.debug('Server.py started')

    # Reading configuration from file name"server.ini"
    config = configparser.ConfigParser()
    config.read('server.ini')
    ip=config['HostInfo']['IP']
    port=config['HostInfo']['PORT']
    prod_dbname =config['DatabaseInfo']['production']
    
    #Comment the below 5 Lines to DISABLE unit testing for the server class. 
    #Unit Testing will always use a fresh database called 'TestDB-%H%M%S'
    #test_db_name = "TestDB-"+strftime("%H%M%S")
    #print ('Unit Testing server.py with '+ test_db_name)
    #strargs = "sqlite3 " + test_db_name + " < createLogins.sql"
    #subprocess.call([strargs], shell=True)
    #db = Server_db(test_db_name,ip,port)
    #unittest.main()

    #intialize database
    db = Server_db(prod_dbname,ip,port)
    # XMLRPC server starts
    db.start_xmlserver()
