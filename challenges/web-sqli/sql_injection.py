#!/usr/bin/env python
"""
A Python puzzle: SQL injection (on an HTTP server).
"""
import http.server
import socketserver
import os
import sqlite3
import urllib.parse


# The flag.
FLAG_STRING = 'flag{pr3p4r3d_stmts_r_th3_b3st}'

# Template of HTML to display
BASE_HTML = '''
<!DOCTYPE html>
<html>
<head>
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


class MyHttpServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    """ Use a very simple threaded HTTP server, with no thread pooling :-(
    """
    pass


class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    """ Handle HTTP requests to allow SQL injection.
    """

    def do_HEAD(self):
        """ Send an HTTP HEAD response.
        """
        self._start_response()

    def do_GET(self):
        """ Take input from a GET parameter, and respond to the user.
        """
        self._start_response()
        query = urllib.parse.urlparse(self.path).query
        pairs = urllib.parse.parse_qs(query)
        try:
            value = pairs['belt_color'][-1]
        except (KeyError, IndexError):
            text = 'Please choose a belt color!'
            self.send(text)
        else:
            sql_injection = SqlInjection()
            result = sql_injection.query(value)
            html_safe_value = _html_escape(value)

            if not result:
                message_template = ("You want the '{color}' belt?"
                                   " There's no such thing!")
                text = message_template.format(color=html_safe_value)
                self.send(text)
            elif len(result) == 1:
                message_template = 'Yes, you can earn a {color} belt!'
                text = message_template.format(color=html_safe_value)
                self.send(text)
            else:
                text = 'Multiple results? Impossible!<br>' + '<br>'.join(result)
                self.send(text)

    def send(self, text):
        message = BASE_HTML.format(message=text)
        self.wfile.write(message.encode())


    def _start_response(self):
        """ Send a response code and headers.
        """
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()

def _html_escape(value):
    return value.replace('&', '&amp;').replace(
                         '>', '&gt;').replace(
                         '<', '&lt;').replace(
                         '"', '&quot;').replace(
                         "'", '&#x27;').replace(
                         '/', '&#x2F;')

def run(server_address,
        server_port,
        server_class=MyHttpServer,
        handler_class=MyHttpRequestHandler):
    """ Run an HTTP server that's vulnerable to SQL injection.
    """
    server_address = (server_address, server_port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

def main():
    """ Read the PORT environment variable, and listen on localost.
    """
    env_port = os.getenv('PORT')
    try:
        port = int(env_port)
    except (TypeError, ValueError):
        print('Please specify a valid PORT environment variable.')
        exit(1)
    else:
        print('Starting server on port %s.' % port)
        run('', port)

if __name__ == '__main__':
    main()
