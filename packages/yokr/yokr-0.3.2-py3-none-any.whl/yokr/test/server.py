import json
import logging
import pprint
import traceback
from wsgiref.simple_server import make_server

PORT = 5000
logging.basicConfig(level=logging.DEBUG)


def simple_app(environ, start_response):
    print(environ['REMOTE_ADDR'])
    print(environ['REQUEST_METHOD'], environ['PATH_INFO'], environ['SERVER_PROTOCOL'])
    print(environ['HTTP_HOST'])
    print(environ.get('CONTENT_TYPE'))
    print(environ.get('CONTENT_LENGTH'))
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)
    try:
        request_body_str = request_body.decode('UTF-8')
        request_body_obj = json.loads(request_body_str)
        x_string = request_body_obj['x']
        payload = json.loads(x_string)
    except:
        print(request_body)
        traceback.print_exc()
        start_response(500)
        return []

    pprint.pprint(payload)

    response_text = 'OK'
    response_body = response_text.encode('UTF-8')

    status = '200 OK'
    headers = [
        ('Content-type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]
    start_response(status, headers)
    return [response_body]


with make_server(host='', port=PORT, app=simple_app) as httpd:
    print("Serving on port %d..." % PORT)
    httpd.serve_forever()
