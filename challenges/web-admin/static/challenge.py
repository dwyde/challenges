"""
A web challenge: get admin status, to read a flag.
"""
import json
import os.path
import xml.sax.saxutils

import tornado.ioloop
import tornado.web


# The port on which this application will listen
PORT = 8888


class MainHandler(tornado.web.RequestHandler):
    """ Handle web requests: check a user's status.
    """

    FORM_HTML = '\n'.join([
        '<html>',
        '<body>',
        '<form method="POST">',
        '   <label for="name">Who are you?</label>',
        '   <br>',
        '   <input id="name" name="name" autofocus>',
        '   <br>',
        '   <input type="submit">',
        '</form>',
        '</body>',
        '</html>',
    ])

    def get(self):
        """ Handle HTTP GET: return a simple HTML form.
        """
        self.write(self.FORM_HTML)

    def post(self):
        """ Handle HTTP POST: check the provided name.
        """
        name = self.get_argument('name', '')
        result = self.check(name)
        output = xml.sax.saxutils.escape(result)
        self.write(output)

    def check(self, user_input):
        """ Check if a user is an admin that can see the flag.
        """
        name = user_input.strip() 
        data = '{"name": "%s"}' % (name,)
        try:
            user = json.loads(data)
        except ValueError:
            return 'Invalid JSON'

        if user.get('admin'):
            return self.flag
        else:
            return 'Hi, %s!' % (name,)

    def initialize(self, flag):
        """ Set up the handler object.
        """
        self.flag = flag

    def set_default_headers(self):
        """ Do not send an informative Server header.
        """
        self.set_header('Server', 'CTF')


def read_flag():
    """ Read in this challenge's flag.
    """
    path = os.path.join(os.path.dirname(__file__), 'flag')
    with open(path) as fp:
        return fp.read().strip()


def make_app():
    """ Create the Tornado app.
    """
    return tornado.web.Application([
        (r'/', MainHandler, {'flag': read_flag()}),
    ])


def main():
    """ Run the application.
    """
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

