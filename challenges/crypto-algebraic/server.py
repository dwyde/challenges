import os.path

import tornado.ioloop
import tornado.web


# The filesystem path to the folder containing this file
THIS_FOLDER = os.path.dirname(__file__)

# The coveted flag
FLAG = 'flag{you_figured_out_the_coordinate_system}'


class FenHandler(tornado.web.RequestHandler):
    """ Check if the user's FEN notation matches our desired position.
    """

    def get(self):
        fen = self.get_argument('fen', None)
        if fen == 'r1b1k2r/ppppqppp/2n5/8/1PP2B2/3n1N2/1P1NPPPP/R2QKB1R':
            self.write(FLAG)

    def set_default_headers(self):
        """ Do not send an informative Server header.
        """
        self.set_header('Server', 'CTF')


class FileHandler(tornado.web.StaticFileHandler):

    def set_default_headers(self):
        """ Do not send an informative Server header.
        """
        self.set_header('Server', 'CTF')


if __name__ == '__main__':
    application = tornado.web.Application([
        (r'/fen', FenHandler),
        (r'/(.*)', FileHandler,
            {'path': THIS_FOLDER, 'default_filename': 'index.html'}),
    ])
    application.listen(8888)
    tornado.ioloop.IOLoop.current().start()

