const http = require('http');
const url = require('url');
const { execFile } = require('child_process');

const hostname = '0.0.0.0';
const port = 8888;

const writeOut = function(res, message) {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/plain');
  res.end(`${message}\n`);
};

const server = http.createServer((req, res) => {
  requestUrl = url.parse(req.url, true);
  userInput = requestUrl.query.input || '';

  execFile('./wrapper.sh', [userInput], (error, stdout, stderr) => {
    if (error) {
      writeOut(res, error);
    } else {
      writeOut(res, stdout);
    }
  });
});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}/`);
});

