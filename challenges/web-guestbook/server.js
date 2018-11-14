const http = require('http');
const url = require('url');

const xss = require('./xss.js')

// A host and port on which this server will listen
const hostname = '0.0.0.0';
const port = 8888;

// The maximum length of input
const MAX_LENGTH = 30;

// HTML content to display an input form
const FORM_HTML = `<form>
   <label for="message">Write a message:</label>
   <br>
   <input id="message" name="message" type="text" autofocus>
   <br>
   <input type="submit" value="Click here to sign the guestbook!">
</form>`;

// The flag string
const FLAG = (() => {
  const fs = require('fs');
  const contents = fs.readFileSync('flag').toString();
  return contents.trim();
})();

// A callback to write responses
const writeOut = function(res, message) {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.end(
`<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="/static/style/challenge.css">
<link rel="stylesheet" href="/static/style/guestbook.css">
</head>
<body>
<div>${message}</div>
</body>
</html>`
  );
};

const regexReject = (response, regex) => {
  pattern = regex.replace(/&/g, '&amp;')
                 .replace(/</g, '&lt;')
                 .replace(/>/g, '&gt;');
  writeOut(response, 'Your message must match this regex: ' + pattern);
};

const runBrowser = (response, userInput) => {
  xss.runBrowser(userInput).then((result) => {
    if (result === undefined) {
      writeOut(response, 'The XSS variable is still undefined.');
    } else {
      writeOut(response, 'The flag is ' + FLAG);
    }
  });
};

const processInput = (response, userInput) => {
  const payloadRegex = /^[<>A-Z=/-]+$/;

  if (userInput.length > MAX_LENGTH) {
    // Input is too long
    writeOut(response, `Messages can be at most ${MAX_LENGTH} characters.`);
  } else if (payloadRegex.test(userInput) === false) {
    // Input does not match the whitelist filter.
    regexReject(response, payloadRegex.source)
  } else {
    // Run the input through the HTML injection.
    runBrowser(response, userInput);
  }
};

// An HTTP server
const server = http.createServer((request, response) => {
  const urlData = url.parse(request.url, true);
  const userInput = urlData.query.message || '';

  if (userInput) {
    processInput(response, userInput);
  } else {
    writeOut(response, FORM_HTML);
  }
});

// Main code
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

