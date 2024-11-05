import socket
import threading
import signal
import sys

def get_ip():
    # Create a temporary socket to connect to an external server
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # We don't actually connect, just use this to determine interface
        s.connect(('8.8.8.8', 80))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

HOST = get_ip()
PORT = 65432

connections = []
threads = []
addrs = []
def broadcast_msg(from_addr,msg):
	for i in range(len(connections)):
		conn = connections[i]
		addr = addrs[i]
		if addr == from_addr:
			continue
		try:
			conn.sendall(msg.encode())
		except Exception:
			connections.pop(i)

def listen_for_messages(clientconn, addr):
	print(f"connected: {addr}")
	while True:
		try:
			msg = clientconn.recv(1024).decode('utf-8')
			if not msg:
				continue
			print(f"{addr}: {msg}")
			broadcast_msg(addr, f"{addr}: {msg}")
		except Exception:
			return

def signal_handler_wrapper(s):
	def signal_handler(sig, frame):
		print("bye bye")
		s.close()
		sys.exit(0)
	return signal_handler

def main():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		signal.signal(signal.SIGINT, signal_handler_wrapper(s))
		print(f"Starting Server on: {HOST}")
		s.bind((HOST, PORT))
		s.listen()
		while True:
			conn, addr = s.accept()
			connections.append(conn)
			addrs.append(addr)
			thread = threading.Thread(target=listen_for_messages, args=(conn, addr))
			thread.start()
	except Exception:
		print("panic quitting...")
		s.close()

if __name__ == "__main__":
	main()
