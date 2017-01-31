/*
 * An XSS challenge: users sign a guestbook, and the server automatically
 * checks for a particular XSS payload.
 *
 * This is a PhantomJS script: run `phantomjs <filename>`.
 */


// Global constants
var ENV = require('system').env;
var FLAG = 'flag{be_our_guest_be_our_guest}';
var PORT = ENV.PORT || 8080;

// Send an HTML form in response to a GET request.
var FORM_HTML = [
    '<!DOCTYPE html>',
    '<html>',
    '<form method="POST" action="/">',
    '<input type="text" name="message" autofocus>',
    '<input type="submit" value="Sign the guestbook!">',
    '</form>',
    '</html>',
    ''
].join('\n');

// Run JavaScript in the context of a page to check for XSS.
var checkXss = function (flag) {
    if (window.XSS === undefined) {
        return 'The "XSS" JavaScript variable is still undefined.'
    } else {
        return 'The flag is: ' + flag
    }
};

// Load a web page with user input, then check for XSS.
var loadPage = function (input) {
    var result,
        page = require('webpage').create();

    page.setContent('<!-- ' + input + ' -->', 'http://localhost:8000');

    result = page.evaluate(checkXss, FLAG);

    // Clean up
    page.close();

    return result
};

// Helper method: send an HTTP response.
var sendResponse = function (response, statusCode, message) {
    response.statusCode = statusCode;
    response.write(message + '\n');
    response.close();
};

// Handle an HTTP POST: validate input, then check for XSS.
var payloadRegex = /^[<>A-Z=/-]+$/;
var handlePost = function(request, response) {
    var userPayload = request.post.message;

    if (userPayload === undefined) {
        sendResponse(response, 400, 'Please supply a message!');
    } else if (payloadRegex.test(userPayload) === false) {
        sendResponse(response, 400, 'Your message must match this regex: ' +
                     payloadRegex.source);
    } else {
        sendResponse(response, 200, loadPage(userPayload));
    }
}

// Main code: handle a request, and respond with the flag or an error.
var webserver = require('webserver');
var server = webserver.create();
var service = server.listen(PORT, function(request, response) {
    if (request.method === 'GET') {
        sendResponse(response, 200, FORM_HTML);
    } else if (request.method === 'POST') {
        handlePost(request, response);
    } else  {
        sendResponse(response, 405, 'Please send a GET or a POST.');
    }
});

// Check that the HTTP server started properly.
if (service === true) {
    console.log('Server started successfully.');
} else {
    console.log('Error: server failed to launch.');
    phantom.exit();
}

