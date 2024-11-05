import socket
import threading
import signal 
import sys 

SERVER  = input("paste server ip: ")
SERVER_PORT = 65432


def send_data(s):
	while True:
		msg = input("enter a message:\n")
		s.sendall(msg.encode())

def recv_data(s):
	while True:
		data = s.recv(1024).decode('utf-8')
		if not data:
			continue
		print(f"Recieved: {data}")

def signal_handler_wrapper(s):
	def signal_handler(sig, frame):
		print("bye bye")
		s.close()
		sys.exit(0)
	return signal_handler

def main():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	signal.signal(signal.SIGINT, signal_handler_wrapper(s))
	try:
		print("connecting to server")
		s.connect((SERVER, SERVER_PORT))
		listening_thread = threading.Thread(target=recv_data, args=(s,))
		listening_thread.start()
		send_data(s)
	except Exception:
		print("huh, panic, bye bye....")
		s.close()

if __name__ == "__main__":
	main()
