puppeteer = require('puppeteer');

const runBrowser = (async (userInput) => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent('<!--' + userInput + '-->');
  const xss = await page.evaluate(() => {
    return window.XSS;
  });
  await browser.close();
  return xss;
});

module.exports = {
  runBrowser: runBrowser
};
