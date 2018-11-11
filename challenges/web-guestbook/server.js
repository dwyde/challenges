const http = require('http');
const url = require('url');

const xss = require('./xss.js')

const hostname = '0.0.0.0';
const port = 8888;

const MAX_LENGTH = 30;

// The flag string
const FLAG = (() => {
  const fs = require('fs');
  const contents = fs.readFileSync('flag').toString();
  return contents.trim();
})();

// A callback to write responses
const writeOut = function(res, message) {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end(`${message}\n`);
};

// An HTTP server
const server = http.createServer((request, response) => {
  const urlData = url.parse(request.url, true);
  const userInput = urlData.query.input || '';
  const payloadRegex = /^[<>A-Z=/-]+$/;

  if (userInput.length > MAX_LENGTH) {
    // Input is too long
    writeOut(response, `Messages can be at most ${MAX_LENGTH} characters.`);
  } else if (payloadRegex.test(userInput) === false) {
    // Input does not match the whitelist filter.
    writeOut(response, 'Your message must match this regex: ' +
             payloadRegex.source);
  } else {
    // Run the input through the HTML injection.
    xss.runBrowser(userInput).then((result) => {
      if (result === undefined) {
        writeOut(response, 'The XSS variable is still undefined.');
      } else {
        writeOut(response, 'The flag is ' + FLAG); 
      }
    });
  }
});

// Main code
server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

