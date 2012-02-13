# Tornalet

[Tornado](http://www.tornadoweb.org/) is great, if you can code asynchronously ...

[Greenlet](http://pypi.python.org/pypi/greenlet) is cool to create asynchronous programs using micro-threads.

What about a mix of the two ?

## Howto

To install tornalet, you can clone this repository or use PyPI:

    easy_install tornalet
    pip install tornalet

To enable tornale, prefix each of your handler's method the decorator ``@tornalet.tornalet``.

Then decorate with ``tornalet.asyncify`` each of your *blocking* function. This will make your function asynchronous.

## Example

    import tornalet
    import tornado.web
    import random

    URL = "http://chucknorrisfacts.fr/fortunes/fortunes.txt"

    class MainHandler(tornado.web.RequestHandler):
        @tornalet.tornalet
        def get(self):
            http_client = tornado.httpclient.AsyncHTTPClient()
            
            # Here's the magic : this line is not synchronous.
            facts = tornalet.asyncify(http_client.fetch)(URL).body.split("%")

            fact = facts[random.randrange(len(facts))]

            self.write("<pre>%s</pre>" % (fact, ))
    
    ...

## License

Tornadolet is licensed under the Apache Licence, Version 2.0 ([http://www.apache.org/licenses/LICENSE-2.0.html](http://www.apache.org/licenses/LICENSE-2.0.html)).

