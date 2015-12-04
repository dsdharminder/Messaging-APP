#!/usr/bin/env python
import socket
import configparser
import unittest

#This is the unit testing class
#Line to enable/disable unit testing is in main -  unittest.main()
class TestChat(unittest.TestCase):
	def setUp(self):
		self.c=Chat("127.0.0.1", 40000, "test", "127.0.0.1", 40000)
		self.empty =""
		self.something="test123"


	def testSendReceive_msg(self):
		# test sending and receiving empty message
		self.c.send_msg(self.empty)
		self.assertEqual(self.empty,self.c.get_msg())

		# test sending and receiving message
		self.c.send_msg(self.something)
		self.assertEqual(self.something,self.c.get_msg())


class Chat:
	"""
	This class allows user to call methods for simple chatting with other user.
	"""
	
	def __init__(self, client_ip, client_port,friend_name,friend_ip,friend_port):
		"""
		This method takes following parameters:
		client_ip: is the ip of the current computer
		client_port: is the port current computer uses to communicate to other users
		friend_name: a name of the your chatting buddy
		friend_ip: an ip of your buddy 
		friend_port: a port number your buddy is using 
		Also, initialize the socket used to communicate with other users.
		"""
		# instance variables
		self.client_ip = client_ip
		self.client_port = int(client_port)
		self.friend_ip = friend_ip
		self.friend_port = int(friend_port)
		self.friend = friend_name

		# Running initializing methods and printing info to console
		self.sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
		self.sock.bind((self.client_ip,self.client_port))
		self.sock.settimeout(0.1)

	# Need improvement does not work properly
	def get_msg(self):
		"""
		This method receive the msg from friend with given by friend_name and returns
		the msg. If there is no message received before the socket timeouts, it returns
		empty string. Else returns nothing.
		"""
		msg=""
		try:
			while (True):
				data,addr = self.sock.recvfrom(1024)
				ip,port=addr
				if ip==self.friend_ip:
					msg += data.decode("utf-8")
		except socket.timeout:
			return msg

	def send_msg(self,message):
		"""
		This method take following parameter
		message: a message client sending to friend
		And send the message to friend_name
		"""
		self.sock.sendto(message.encode('utf-8'),(self.friend_ip,self.friend_port))
	
	def start_conversation(self):
		"""
		This method loop that allow user to continuously send and receive messages till
		:q is entered When it exits the loop.
		"""
		print ('Conversation started with ', self.friend, ' -- Send msg ":q to end')
		message = ''
		while message !=':q':
			message = input ('>> ')
			self.send_msg(message)
			print(self.get_msg())

if __name__ == "__main__":
	# Reading configuration from file name"server.ini"
	config = configparser.ConfigParser()
	config.read('client.ini')
	client_ip=config['ClientInfo']['CLIENT_IP']
	client_port=config['ClientInfo']['CLIENT_PORT']


	c=Chat(client_ip, client_port, client_ip, client_ip, client_port)

	#Uncomment below line to Disable Unit Testing
    #unittest.main()

	c.start_conversation()
