from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import json

from urlparse import urlparse

from .request_handler import process_request

LOCAL_IP = '172.22.75.212'
LOCAL_PORT = 8080

fixture = json.dumps({
    "user":
    {
        'firstname': 'Tina',
        'surname': 'Yellow',
        'age': 15,
    },
    "matches": {
        'by_age':
        {
            "name": "Anne",
            "surname": "Brown",
            "age": 13,
            'nationality': 'british'
        },
        'by_location':
        {
            "name": "Vida",
            "surname": "Sugar",
            "age": 56,
            'nationality': 'french'
        }
    }
})


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        # Test with:  curl http://172.22.75.212:8080?foo=bar

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
        request_path = self.path
        payload = self.get_POST_payload()

        print("\n----- POST Request Start ----->\n")
        print(payload)
        print("<----- POST Request End -----\n")

        # process_request()
        # matches = process_request(payload)
        matches = fixture
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
        return self.rfile.read(length)


def get_GET_params(request_path):
    query = urlparse(request_path).query
    return dict(qc.split("=") for qc in query.split("&"))


def main():
    print('Listening on %s:%s' % (LOCAL_IP, LOCAL_PORT))
    server = HTTPServer((LOCAL_IP, LOCAL_PORT), RequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
