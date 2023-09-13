export async function iDRAC_logout(page) {
    await page.frameLocator('frame[name="globalnav"]').getByRole('link', { name: 'Logout' }).click();
}