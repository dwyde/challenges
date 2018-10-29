"""
SQL injection (on an HTTP server).
"""
import sqlite3
import urllib.parse
import xml.sax.saxutils

import tornado.ioloop
import tornado.web


# The port on which this application will listen
PORT = 8888

# The flag.
FLAG_STRING = 'flag{prepared_statements_make_the_web_go_round}'


class SqlInjection(object):
    """ The main class for this module: allow SQL injection.
    """

    # Values to initially load into the database.
    INITIAL_VALUES = ('white', 'green', 'blue', 'brown', 'black',
                      FLAG_STRING)

    def __init__(self):
        """ Initialize an in-memory SQLite database of users. """
        self.conn = sqlite3.connect(':memory:')
        with self.conn:
            self.conn.execute('''CREATE TABLE belts (name TEXT COLLATE NOCASE)''')
            for val in self.INITIAL_VALUES:
                self.conn.execute('''INSERT INTO belts VALUES (?)''', (val,))

    def query(self, value):
        """ The main entry point for this class: return an SQL result set.
        """
        query_string = "SELECT * FROM belts WHERE name='%s'" % value
        results = self._run_query(query_string)
        return [row[0] for row in results]

    def _run_query(self, query_string):
        """ Run a query.
        """
        cursor = self.conn.cursor()
        try:
            cursor.execute(query_string)
        except (sqlite3.OperationalError, sqlite3.Warning):
            pass
        results = cursor.fetchall()
        cursor.close()
        return results


class MainHandler(tornado.web.RequestHandler):
    """ Handle HTTP requests to allow SQL injection.
    """

    # Template of HTML to display
    BASE_HTML = '''
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <title>SQL Injection Dojo</title>
    </head>
    <body>
    <p>
    What color belt would you like?
    </p>
    <form>
        <input name="belt_color">
        <input type="submit" value="Choose!">
    </form>
    <p>{message}</p>
    </body>
    </html>
    '''

    def get(self):
        value = self.get_argument('belt_color', '')
        if not value:
            text = 'Please choose a belt color!'
            self._send_message(text)
        else:
            sql_injection = SqlInjection()
            result = sql_injection.query(value)
            html_safe_value = xml.sax.saxutils.escape(value)
            if not result:
                message_template = ("You want the '{color}' belt?"
                                   " There's no such thing!")
                text = message_template.format(color=html_safe_value)
                self._send_message(text)
            elif len(result) == 1:
                message_template = 'Yes, you can earn a {color} belt!'
                text = message_template.format(color=html_safe_value)
                self._send_message(text)
            else:
                text = 'Multiple results? Impossible!<br>' + '<br>'.join(result)
                self._send_message(text)

    def set_default_headers(self):
        """ Do not send an informative Server header.
        """
        self.set_header('Server', 'CTF')

    def _send_message(self, message):
        """ Write a response to the client.
        """
        text = self.BASE_HTML.format(message=message)
        self.write(text)


def make_app():
    """ Create the Tornado app.
    """
    return tornado.web.Application([
        (r'/', MainHandler)
    ])


def main():
    """ Run the application.
    """
    app = make_app()
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()


if __name__ == '__main__':
    main()

