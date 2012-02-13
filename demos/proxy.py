import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.options import define, options

from urlparse import urljoin

import tornalet

define("port", default = 8888, help = "run on the given port", type = int)
define("url", default = u"http://maps.google.com/", help = "base URL for the proxy", type = unicode)

class ProxyHandler(tornado.web.RequestHandler):
    @tornalet.tornalet
    def get(self, path):
        url = urljoin(options.url, path)

        http_client = tornado.httpclient.AsyncHTTPClient()
        body = tornalet.asyncify(http_client.fetch)(url).body

        self.write(body)

def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/(.*)", ProxyHandler),
    ], debug = True)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
