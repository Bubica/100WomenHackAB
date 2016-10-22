from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
# from optparse import OptionParser
from urlparse import urlparse

LOCAL_IP = '172.22.75.212'


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Test with:  curl http://localhost:8080?foo=bar

        request_path = self.path

        print("\n----- GET Request Start ----->\n")
        print("Full request path : {} ".format(request_path))
        print("Headers: ".format(self.headers))
        print("GET params : {} ".format(get_GET_params(request_path)))
        print("<----- GET Request End -----\n")

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("<html><head><title>100 Ladies 100 problems</title></head>")

    def do_POST(self):
        # Test with: curl --data "foo=bar&foo2=bar2" http://localhost:8080

        request_path = self.path
        request_headers = self.headers
        content_length = request_headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0

        print("\n----- POST Request Start ----->\n")
        print(request_headers)
        print(self.rfile.read(length))
        print("<----- POST Request End -----\n")

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("<html><head><title>POST Stuff</title></head>")

    do_PUT = do_POST
    do_DELETE = do_GET


def get_GET_params(request_path):
    query = urlparse(request_path).query
    return dict(qc.split("=") for qc in query.split("&"))


def main():
    port = 8080
    print('Listening on %s:%s' % (LOCAL_IP, port))
    server = HTTPServer((LOCAL_IP, port), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
