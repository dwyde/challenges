puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setContent('<script>XSS=JSON</script>');
  const xss = await page.evaluate(() => {
    return window.XSS;
  });
  console.log('XSS: ' + xss);
  await browser.close();
})();
