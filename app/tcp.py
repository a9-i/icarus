import socketserver  # https://docs.python.org/3.5/library/socketserver.html
from app.abuseipdb import prereport
from app.memoryfile import lastattacker
import logging


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        # self.data = self.request.recv(1024).strip()
        (host, port) = self.server.server_address
        prereport(self.client_address[0], port, 'TCP')
        lastattacker(self.client_address[0])  # From memoryfile.py


def runtcp(port):
    try:
        HOST, PORT = "0.0.0.0", port
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        server.allow_reuse_address = True
        server.serve_forever()

    except BaseException as e:  # should be more specific.
        logging.basicConfig(filename='logs.txt', level=logging.INFO)
        logging.info(e)
