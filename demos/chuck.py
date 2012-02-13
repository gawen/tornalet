import tornalet
import tornado.web
import random

URL = "http://chucknorrisfacts.fr/fortunes/fortunes.txt"

class MainHandler(tornado.web.RequestHandler):
    @tornalet.tornalet
    def get(self):
        http_client = tornado.httpclient.AsyncHTTPClient()
        facts = tornalet.asyncify(http_client.fetch)(URL).body.split("%")

        fact = facts[random.randrange(len(facts))]

        self.write("<pre>%s</pre>" % (fact, ))

import tornado.ioloop
import tornado.httpserver
from tornado.options import define, options

define("port", default = 8888, help = "run on the given port", type = int)

def main():
    tornado.options.parse_command_line()

    application = tornado.web.Application([
        (r"/", MainHandler),
    ], debug = True)

    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
