#!/usr/bin/env python
import configparser
import sys
import os
import Authentication
import Chat
import unittest

#This is the unit testing class
#Line to enable/disable unit testing is in main -  unittest.main()
class TestRun(unittest.TestCase):
	def setUp(self):
		self.a=Run("127.0.0.1", 40000, "127.0.0.1", 40000)

class Run:
	def __init__(self, server_ip, server_port, client_ip, client_port ):
		self.client_ip = client_ip
		self.client_port = int(client_port)
		self.server_ip = server_ip
		self.auth =Authentication.Authentication(self.server_ip,server_port,self.client_ip,self.client_port)

	def find_friend(self):
		found = False
		while not found:
			try:
				text =input("Enter your friend name: ")
				if self.auth.get_friendinfo(text):
					self.friend_ip,self.friend_port =self.auth.get_friendinfo(text)
					self.friend_name=text
					found = True
			except LookupError as e:
				print(e)

	def start_chat(self):
		chat=Chat.Chat(self.client_ip, self.client_port,self.friend_name,self.friend_ip,self.friend_port)
		chat.start_conversation()

	def start_client(self):
		print("starting client application on "+os.name+" ...")
		print("starting authentication ...")
		self.auth.login()
		text=''
		while text is not ':q':
			self.find_friend()
			self.start_chat()
			text = input(">")
			print("':q' to quit or enter any key for keep chatting")

if __name__ == "__main__":
	# Reading configuration from file name"server.ini"
	config = configparser.ConfigParser()
	config.read('client_b.ini')
	server_ip=config['ServerInfo']['SERVER_IP']
	server_port=config['ServerInfo']['SERVER_PORT']
	client_ip=config['ClientInfo']['CLIENT_IP']
	client_port=config['ClientInfo']['CLIENT_PORT']

	# Making object and calling start method
	try:
		r =Run(server_ip, server_port, client_ip, client_port)

		#Uncomment below line to Disable Unit Testing
    	#unittest.main()

		r.start_client()
	except Exception as e:
		sys.exit(e)
