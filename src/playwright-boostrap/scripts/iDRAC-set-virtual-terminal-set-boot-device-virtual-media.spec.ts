import { test, expect } from '@playwright/test';
import { iDRAC_login } from './utils/iDRAC-login';
import { iDRAC_logout } from './utils/iDRAC-logout';

require('dotenv').config()

test.use({
  ignoreHTTPSErrors: true
});


test('test', async ({ page }) => {
  // Login
  await iDRAC_login(page);

  await page.waitForTimeout(6000);
  // Go to setup page
  await page.frameLocator('frame[name="treelist"]').getByRole('link', { name: 'Setup' }).click();
  // Click First bootdevice
  await page.frameLocator('frame[name="da"]').locator('#firstBootDevice').selectOption('8');
  // Apply
  await page.frameLocator('frame[name="da"]').locator('#btn_apply_lbl').click();

  // Log out
  await iDRAC_logout(page);
});
