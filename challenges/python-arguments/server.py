import os.path
import urllib.parse
import xml.sax.saxutils

import tornado.ioloop
import tornado.web

import challenge


# The port on which this application will listen
PORT = 8888


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        self.write('\n'.join([
            '<html>',
            '<head>',
            '<style>',
            '   p {white-space: pre-wrap}',
            '</style>',
            '<meta charset="utf-8">',
            '</head>',
            '<body>',
            '<form method="POST">',
            '   <label for="input">Input:</label>',
            '   <br>',
            '   <input id="input" name="input">',
            '   <br>',
            '   <input type="submit" value="Submit">',
            '</form>',
            '</body>',
            '</html>',
        ]))

    def post(self):
        """ Handle HTTP POST: check the provided name.
        """
        user_input = self._read_user_input()
        try:
            result = challenge.main(user_input)
        except Exception as ex:
            result = 'Error: {}'.format(ex)
        self._write_result(result)

    def _read_user_input(self):
        """ Parse a value from user-supplied data.
        """
        body = self.request.body.decode()
        cleaned = body.rstrip('\r\n')
        query = urllib.parse.parse_qs(cleaned)
        user_input = query.get('input', [''])
        return user_input[0]

    def _write_result(self, result):
        """ Write a result to the client.
        """
        text_out = str(result)
        output = xml.sax.saxutils.escape(text_out)
        self.write(output)

    def set_default_headers(self):
        """ Do not send an informative Server header.
        """
        self.set_header('Server', 'CTF')

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

