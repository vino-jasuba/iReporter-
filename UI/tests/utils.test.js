const utils = require('../js/utils')
var faker = require('faker')
const puppeteer = require('puppeteer')

var data = []
var eaCountries = ['kenya', 'uganda']

for (var i = 0; i <= 10; i++) {
  data.push({
    name: faker.name,
    address: faker.address,
    country: faker.random.arrayElement(eaCountries)
  })
}

test('it groups given collection by specified key', () => {
  expect(utils.groupBy(data, 'country')).toHaveProperty('kenya')
  expect(utils.groupBy(data, 'country')).toHaveProperty('uganda')
})

test('home page loads correctly', async () => {
  let browser = await puppeteer.launch({})
  let page = await browser.newPage()

  await page.goto('file:///home/vino/Repo/Andela/frontend-ireporter/UI/index.html')

  const html = await page.$eval('.text-largest', e => e.innerHTML)

  expect(html).toBe('See corruption, Report immediately.')

  browser.close()
})

test('user login redirects to dashboard', async () => {
  let browser = await puppeteer.launch({})
  let page = await browser.newPage()

  await page.goto('file:///home/vino/Repo/Andela/frontend-ireporter/UI/login.html')
  await page.click('input[name="username"]')
  await page.type('input[name="username"]', 'vino')

  await page.click('input[name="password"]')
  await page.type('input[name="password"]', 'PaSsw0rd')

  await Promise.all([
    page.click('button[name="submit"]'),
    page.waitForNavigation({ waitUntil: 'networkidle0' })
  ])

  var url = await page.url()

  expect(url).toBe('file:///home/vino/Repo/Andela/frontend-ireporter/UI/dashboard.html')

  browser.close()
})

test('user logout redirects to index page', async () => {
  let browser = await puppeteer.launch({})
  let page = await browser.newPage()

  // login first
  await page.goto('file:///home/vino/Repo/Andela/frontend-ireporter/UI/login.html')
  await page.click('input[name="username"]')
  await page.type('input[name="username"]', 'vino')

  await page.click('input[name="password"]')
  await page.type('input[name="password"]', 'PaSsw0rd')

  // wait for redirect to dashboard
  await Promise.all([
    page.click('button[name="submit"]'),
    page.waitForNavigation({ waitUntil: 'networkidle0' })
  ])

  // click logout button
  await Promise.all([
    page.click('#logout'),
    page.waitForNavigation({ waitUntil: 'networkidle0' })
  ])

  var url = await page.url()

  expect(url).toBe('file:///home/vino/Repo/Andela/frontend-ireporter/UI/index.html')

  browser.close()
}, 30000)
