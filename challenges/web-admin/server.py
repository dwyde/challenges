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

    # Start of HTML
    HTML_START = '\n'.join([
        '<!DOCTYPE html>',
        '<html>',
        '<head>',
        '<meta charset="utf-8">',
        '<link rel="stylesheet" href="/static/style/challenge.css">',
        '</head>',
        '<body>',
        '<div id="wrapper">'
    ])

    # End of HTML
    HTML_END = '\n'.join([
        '</div>',
        '</body>',
        '</html>'
    ])

    # HTML form content
    HTML_FORM = '\n'.join([
        '<form method="POST">',
        '   <label for="name">Who are you?</label>',
        '   <br>',
        '   <input id="name" name="name" autofocus>',
        '   <br>',
        '   <input type="submit" value="Say hello">',
        '</form>'
    ])

    # The entire HTML form page
    FORM_CONTENT = HTML_START + HTML_FORM + HTML_END

    # A template for the output page
    OUTPUT_CONTENT = HTML_START + '<p>{}</p>' + HTML_END

    def get(self):
        """ Handle HTTP GET: return a simple HTML form.
        """
        self.write(self.FORM_CONTENT)

    def post(self):
        """ Handle HTTP POST: check the provided name.
        """
        name = self.get_argument('name', '')
        result = self.check(name)
        output = xml.sax.saxutils.escape(result)
        response = self.OUTPUT_CONTENT.format(output)
        self.write(response)

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

