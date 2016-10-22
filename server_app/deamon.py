from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json

from urlparse import urlparse

from .request_handler import process_request

LOCAL_IP = '172.22.75.212'
LOCAL_PORT = 8080


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Test with:  curl http://172.22.75.212:8080?foo=bar

        request_path = self.path
        params = get_GET_params(request_path)

        print("\n----- GET Request Start ----->\n")
        print("GET params : {} ".format(params))
        print("<----- GET Request End -----\n")

        if not params or 'map' not in params:
            self.send_response(404)
        else:
            self.send_response(200)
            self.send_header("Content-type", "img/png")
            self.end_headers()
            with open(params.get('map'), 'r') as f:
                self.wfile.write(f.read())
                # self.wfile.write("<html><head><title>100 Ladies 100 problems</title></head>")

    def do_POST(self):
        request_path = self.path
        payload = self.get_POST_payload()

        print("\n----- POST Request Start ----->\n")
        print(payload)
        print("<----- POST Request End -----\n")

        matches = process_request(payload)
        self.send_matches(matches)

    def send_matches(self, matches):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "http://www.100women.com:8000")
        self.end_headers()
        self.wfile.write(matches)

    do_PUT = do_POST
    do_DELETE = do_GET

    def get_POST_payload(self):
        content_length = self.headers.getheaders('content-length')
        length = int(content_length[0]) if content_length else 0
        # return self.rfile.read(length)
        return '{"birthday": "04/16/1983","hometown": { "id": "116619061681465", "name": "Zagreb, Croatia" },"first_name": "Agata", "last_name": "Brajdic", "id": "10154711934932119", "picture":{"data":{"is_silhouette":false,"url":"https://fbcdn-profile-a.akamaihd.net/hprofile-ak-prn1/v/t1.0-1/c63.64.795.795/s50x50/534067_10151387453072119_1860096328_n.jpg?oh=e619774a131044e779df005c641f8ea8&oe=588C4A4E&__gda__=1482895449_afebc340b65ede0646fc193f27922626"}}}'


def get_GET_params(request_path):
    query = urlparse(request_path).query
    print query
    if not query:
        return {}
    return dict(qc.split("=") for qc in query.split("&"))


def main():
    print('Listening on %s:%s' % (LOCAL_IP, LOCAL_PORT))
    server = HTTPServer((LOCAL_IP, LOCAL_PORT), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
