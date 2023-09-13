import { expect } from '@playwright/test';

export async function iDRAC_login(page) {

    const IDRAC_HOST = process.env["IDRAC_HOST"] || 'https://192.168.0.120/'
    const IDRAC_USERNAME = process.env["IDRAC_USERNAME"] || 'root' // Default: root
    const IDRAC_PASSWORD = process.env["IDRAC_PASSWORD"] || 'calvin' // Default: calvin


		// Note: The IDRAC redirects visits to '/start.html' to
		// 'login.html' by default.
		await page.goto(`${IDRAC_HOST}/start.html`);
		await expect(page.getByText('Enterprise')).toBeVisible();
		await expect(page.locator('#user')).toBeVisible();
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
		await expect(page.frameLocator('frame[name="globalnav"]').getByText('Logout')).toBeVisible();
}
