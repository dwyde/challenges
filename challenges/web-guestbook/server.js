const http = require('http');
const url = require('url');

const xss = require('./xss.js')

const hostname = '0.0.0.0';
const port = 8888;

const MAX_LENGTH = 30;

const FORM_HTML = `<!DOCTYPE html>
<html>
<head>
<style>
    p {white-space: pre-wrap}
</style>
<meta charset="utf-8">
</head>
<body>
<form>
   <label for="input">Input:</label>
   <br>
   <input id="input" name="input">
   <br>
   <input type="submit" value="Submit">
</form>
</body>
</html>`;

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
  res.end(`${message}\n`);
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
  const userInput = urlData.query.input || '';

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

