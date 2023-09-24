const puppeteer = require('puppeteer');


(async () => {
  // ._. https://stackoverflow.com/questions/22213980/could-someone-explain-what-process-argv-means-in-node-js-please
  const reported_url = process.argv[2];
  const login_url = `http://${process.env['APP_SERVER_HOSTNAME']}:${process.env['APP_SERVER_PORT']}/user/login`
  console.log('Login URL:', login_url);
  console.log('Reported URL:', reported_url);

  const browser = await puppeteer.launch({
    headless: 'new',
    executablePath: '/usr/bin/google-chrome',
    args: [
      "--no-sandbox",
      "--disable-gpu",
    ]
  });
  const page = await browser.newPage();

  // Login
  console.log("Trying login ...")
  await page.goto(login_url);
  await page.type('input[name=username]', 'admin')
  await page.type('input[name=password]', process.env['ADMIN_PASSWORD'])
  await Promise.all([
    page.click('button[type=submit]'),
    page.waitForNavigation({
      waitUntil: 'networkidle0',
    }),
  ]);

  // Visit page
  console.log("Visiting page ...")
  await page.goto(reported_url)
  await new Promise(r => setTimeout(r, 5*1000));
  await browser.close();
  console.log("Done!\n")
})();
