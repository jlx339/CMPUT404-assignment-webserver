#  coding: utf-8 
import SocketServer
import os

# Copyright 2016 Abram Hindle, Eddie Antonio Santos, Lixin Jin
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2016 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

	# Checkout if the request action is "GET", otherwise 405
	requestAction = self.data.split(' ')[0]
	## http version?
	if (requestAction == "GET"):
		request = "www" + self.data.split(' ')[1]
	else:
		request = "Invalid Action"
		response = "HTTP/1.1 405 Method Not Allowed\n\n"
		self.request.sendall(response)

	##self.request.sendall(request)
	if (os.path.exists(request) == False):
		response = "HTTP/1.1 404 Not Found\n\n"
		##self.request.sendall("notnotnot")
		self.request.sendall(response)
	elif (".." in request):
		response = "HTTP/1.1 404 Not Found\n\n"
		##self.request.sendall("notnotnot")
		self.request.sendall(response)
		return
	else:
		if (os.path.isdir(request)):
			if (request.endswith("/")):
				request = request + "index.html"
			else:
				request = request + "/index.html"
			

		# Checkout the type
		if (request.endswith(".css")):
			contentType = "text/css\r\n\r\n"
		if (request.endswith(".html")):
			contentType = "text/html\r\n\r\n"

		f = open(request, 'r')
		content = f.read()
		f.close()
		header = "HTTP/1.1 200 OK\r\nContent-Type: " + contentType
		content = header + content + "\r\n"
		self.request.sendall(content)


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
