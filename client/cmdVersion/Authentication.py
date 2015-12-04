#!/usr/bin/env python
import xmlrpc.client
import configparser
import getpass
import sys
import unittest

#This is the unit testing class
#Line to enable/disable unit testing is in main -  unittest.main()
class TestAuthentication(unittest.TestCase):
	def setUp(self):
		self.a=Authentication("127.0.0.1", 40000, "127.0.0.1", 40000)


# Need improvement:
# This file uses database methods from 'User_db' through xmlrpc server. It requires 'User_db.py' file runnung.
"""
This class allow user to login if they have account else ask them to make new account. Account information is 
stored in database on server.
"""
class Authentication:
	def __init__(self, server_ip, server_port, client_ip, client_port):
		self.client_ip = client_ip
		self.client_port = int(client_port)
		
		self.username =""
		self.password =""

		# the auth from database but it is going to from server
		try:
			print("Connecting to server ...")
			self.db = xmlrpc.client.ServerProxy("http://"+server_ip+":"+str(server_port)+"/")
		except Exception as e:
			sys.exit(e)

	def get_userinfo(self):
		try:
			self.username = input("Username: ")
			if self.username.isalnum():
				self.password = getpass.getpass()
			if not self.username and not self.password and not self.username.isalnum() and not self.password.isalnum():
				raise ValueError('invalid username or password')		
		except ValueError as e:
			print(e)

	def get_friendinfo(self,username):
		try:
			if self.db.check_friend(username):
				friendinfo = self.db.lookup_friend(username)
				return friendinfo
			else:
				raise LookupError("user does not exits")
		except LookupError as e:
			print(e)

	def new_user(self):
		print("Create new Account")
		self.get_userinfo()
		if not self.db.check_friend(self.username):
			if self.password.isalnum():
				print("Confirm")
				text=getpass.getpass()
			if self.username and self.password and self.username.isalnum() and self.password.isalnum() and text == self.password:
				self.db.add_user(self.username,self.password,self.client_ip,self.client_port)
				if self.db.check_user(self.username,self.password):
					print("successful")
			else:
				if not self.username.isalnum():
					print("use mix of alphabets and numbers in username")
				elif not self.password.isalnum():
					print("use mix of alphabets and numbers in password")
				elif text != self.password :
					print("password did not match")
		else:
			print ("user already exit")

	def login(self):
		msg =""
		while not self.db.check_user(self.username,self.password):
			print("':l' for login or ':s' sign up")
			msg = input("Enter the command: ")
			if msg == ':l':
				self.get_userinfo()
				if not self.db.check_user(self.username,self.password):
					print("No match found")
			elif msg == ':s':
				self.new_user()
		print("Logging in ...")
		

if __name__ == "__main__":
	# Reading configuration from file name"server.ini"
	config = configparser.ConfigParser()
	config.read('client_b.ini')
	server_ip=config['ServerInfo']['SERVER_IP']
	server_port=config['ServerInfo']['SERVER_PORT']
	client_ip=config['ClientInfo']['CLIENT_IP']
	client_port=config['ClientInfo']['CLIENT_PORT']

	try:
		auth = Authentication(server_ip, server_port, client_ip, client_port)

		#Uncomment below line to Disable Unit Testing
    	#unittest.main()

		auth.login()
	except Exception as e:
		sys.exit(e)
