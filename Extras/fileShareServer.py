import socket

# Number of bytes read from the socket at a time
BUFFER_SIZE = 1024

# Receive and write a file via socket.
def ReceiveFile(output_file, socket_name="socket"):

	sock = socket.socket(socket.AF_UNIX)
	sock.bind(socket_name)
	sock.listen(0)
	connect, address = sock.accept()
	print "Receiver connected"

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

if __name__ == "__main__":
	ReceiveFile("out")
