#  coding: utf-8 
import socketserver

# Copyright 2023 Zhi Liu
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
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    ROOT = './www'
    
    def handle(self):
        self.data = self.request.recv(1024).decode('utf-8')
        print("Got a request of:", self.data)
        
        if not self.data.startswith("GET "):
            self.send_response(405, "Method Not Allowed")
            return
        
        #rq =  self.data.splitlines()[0]
        #print(self.data)
        rq = self.data.split(' ')
        path = rq[1]
        #print(rq)
        #print("the path is"+path)
        
        #301 redirect
        if not path.endswith(".html") and not path.endswith(".css") and not path.endswith("/"):
            path += "/"
            self.send_redirect(path)
            return            

        # The webserver can return index.html from directories (paths that end in /)    
        if path.endswith("/"):
            path += "index.html"
            print("+index path"+path)
        
        final_path = MyWebServer.ROOT+path
        
        try:
            f = open(final_path,"rb")
        except:
            self.send_response(404, "Not Found")
        else:
            if path.endswith(".html"):
                self.send_response(200, "OK", "text/html", f.read())
            elif path.endswith(".css"):
                self.send_response(200, "OK", "text/css", f.read())
        
        
        
    def send_response(self, status_code, status_msg, content_type="text/plain", content=b""):
        response = f"HTTP/1.1 {status_code} {status_msg}\r\n"
        response += f"Content-Type: {content_type}\r\n"
        response += f"Content-Length: {len(content)}\r\n\r\n"
        self.request.sendall(response.encode('utf-8') + content)
    
    def send_redirect(self, new_path):
        response = f"HTTP/1.1 301 Moved Permanently\r\nLocation: {new_path}\r\n\r\n"
        self.request.sendall(response.encode('utf-8'))    
        
        

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
