import socket
import os

# Number of bites written to the socket at a time
BUFFER_SIZE = 1024
# Default socket name
DEF_SOCK = "socket"

# Send a file via socket.
def SendFile(input_file, socket_name=DEF_SOCK):

	sock = socket.socket(socket.AF_UNIX)
	sock.connect(socket_name)
	print ("Sender connected")

	# Open input file in read-only binary
	inFile = open(input_file, 'rb')
	writer = inFile.read(BUFFER_SIZE)
	while (writer):
		sock.sendall(writer)
		writer = inFile.read(BUFFER_SIZE)

	inFile.close()
	sock.close()

# Receive a file via socket.
def ReceiveFile(output_file="out", socket_name=DEF_SOCK):

	sock = socket.socket(socket.AF_UNIX)
	sock.bind(socket_name)
	sock.listen(0)
	connect, address = sock.accept()
	print ("Receiver connected")

	# Open output file in write-only binary
	outFile = open(output_file, 'wb')
	while (True):
		reader = connect.recv(BUFFER_SIZE)
		if not reader: break	# Escape while loop at end of file
		while (reader):
			outFile.write(reader)
			reader = connect.recv(BUFFER_SIZE)

	outFile.close()
	connect.close()
	sock.close
	os.remove(socket_name)
