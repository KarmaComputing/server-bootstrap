import { test, expect } from '@playwright/test';
import { iDRAC_login } from './utils/iDRAC-login';
import { iDRAC_logout } from './utils/iDRAC-logout';

test.use({
  ignoreHTTPSErrors: true
});

let IDRAC_PASSWORD = process.env["IDRAC_PASSWORD"]; // Default: root
let IDRAC_USERNAME = process.env["IDRAC_USERNAME"]; // Default: calvin
let IDRAC_HOST     = process.env["IDRAC_HOST"]; // E.g. https://192.168.0.120/

test('test', async ({ page }) => {

  // Login
  await iDRAC_login(page);

  // Set console plugin type to html not java
  await page.frameLocator('frame[name="da"]').frameLocator('iframe[name="help"]').getByRole('link', { name: 'Settings' }).click();
  await page.frameLocator('frame[name="da"]').locator('#kvmPluginType').selectOption('2');
  await page.frameLocator('frame[name="da"]').getByRole('link', { name: 'Apply' }).click();

  // Logout
  await iDRAC_logout(page);
});
