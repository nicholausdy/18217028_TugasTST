
# coding: utf-8

# In[ ]:


#generate private key dan certifificate dulu di terminal:
#pastikan OpenSSL tersedia di komputer Anda (run cmd ini: openssl version)
#openssl req -newkey rsa:2048 -nodes -keyout "/home/jupyter/privkey2.pem" -x509 -days 9999 -out "/home/jupyter/certificate2.pem"
import ssl
import base64
from http.server import BaseHTTPRequestHandler,HTTPServer

USERS = [
    {
        "username":"user",
        "password":"1234",
        "hash":base64.b64encode("user:1234".encode('utf-8')).decode('utf-8')
    }
]
class CustomHandler(BaseHTTPRequestHandler):
    ''' Main class to present webpages and authentication. '''
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"Authentication needed\"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    def do_GET(self):
        auth = self.headers['Authorization']
        if not auth:
            return self.require_auth()

        hash_val = auth.split(' ')[1]
        for user in USERS:
            if user['hash'] == hash_val:
                self.send_response(200)
                self.end_headers()
                self.wfile.write("<html><body>Hi there, {}!</body></html>".format(user['username']).encode('utf-8'))
                return

        return self.require_auth()

def main():
    listen_target = ('192.168.56.110', 10400)  # https://192.168.56.110:10400/
    certificate_file = './certificate2.pem'
    private_key_file = './privkey2.pem'
    try:
        print ('started httpd...')
        httpd = HTTPServer(listen_target, CustomHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket,certfile=certificate_file, keyfile=private_key_file, server_side=True)
        httpd.serve_forever()
    except KeyboardInterrupt:
        print ('^C received, shutting down server')
        httpd.socket.close()

if __name__ == '__main__':
    main()
    


# In[ ]:




