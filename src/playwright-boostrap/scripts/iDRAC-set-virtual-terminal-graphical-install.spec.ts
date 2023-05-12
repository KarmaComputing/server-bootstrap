import { test, expect } from '@playwright/test';

test.use({
  ignoreHTTPSErrors: true
});

test('test', async ({ page }) => {

  await page.goto('https://192.168.0.120/start.html');
  await page.goto('https://192.168.0.120/login.html');
  await page.locator('#user').click();
  await page.locator('#user').fill('root');
  await page.locator('#user').press('Tab');
  await page.locator('#password').fill('valvin');
  await page.locator('#user').dblclick();
  await page.locator('#user').press('Control+a');
  await page.locator('#user').fill('root');
  await page.locator('#user').press('Tab');
  await page.locator('#password').fill('calvin');
  await page.getByRole('link', { name: 'Submit' }).click();
  await page.locator('#keeppassword').check();
  await page.getByRole('link', { name: 'Continue' }).click();


  const page2Promise = page.waitForEvent('popup');
  await page.frameLocator('frame[name="da"]').frameLocator('iframe[name="help"]').getByRole('link', { name: 'Launch' }).click();
  const page2 = await page2Promise;
  await page2.locator('#kvmCanvas').click({
    position: {
      x: 509,
      y: 405
    }
  });
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');
  await page2.locator('body').press('ArrowUp');

  // ---------------------

});
