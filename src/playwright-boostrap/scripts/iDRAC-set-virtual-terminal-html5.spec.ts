import { test, expect } from '@playwright/test';

test.use({
  ignoreHTTPSErrors: true
});

let IDRAC_PASSWORD = process.env["IDRAC_PASSWORD"]; // Default: root
let IDRAC_USERNAME = process.env["IDRAC_USERNAME"]; // Default: calvin

test('test', async ({ page }) => {
  await page.goto('https://192.168.0.120/start.html');
  await page.goto('https://192.168.0.120/login.html');
  await page.locator('#user').click();
  await page.locator('#user').press('Tab');
  await page.locator('#user').dblclick();
  await page.locator('#user').press('Control+a');
  await page.locator('#user').fill(IDRAC_USERNAME);
  await page.locator('#user').press('Tab');
  await page.locator('#password').fill(IDRAC_PASSWORD);
  await page.getByRole('link', { name: 'Submit' }).click();
  await page.locator('#keeppassword').check();
  await page.getByRole('link', { name: 'Continue' }).click();


  await page.frameLocator('frame[name="da"]').frameLocator('iframe[name="help"]').getByRole('link', { name: 'Settings' }).click();
  await page.frameLocator('frame[name="da"]').locator('#kvmPluginType').selectOption('2');
  await page.frameLocator('frame[name="da"]').getByRole('link', { name: 'Apply' }).click();
  await page.frameLocator('frame[name="globalnav"]').getByRole('link', { name: 'Logout' }).click();
});
