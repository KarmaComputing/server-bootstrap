import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  timeout: 5 * 60 * 1000,
  // expect timeout is different from test timeout ( https://playwright.dev/docs/test-timeouts#expect-timeout )
  expect: {
      timeout: 120 * 1000,
  },
  // Look for test files in the "tests" directory, relative to this configuration file.
  testDir: 'scripts',

  // Run all tests in parallel.
  fullyParallel: true,

  // Fail the build on CI if you accidentally left test.only in the source code.
  forbidOnly: !!process.env.CI,

  // Retry on CI only.
  retries: process.env.CI ? 2 : 0,

  // Opt out of parallel tests on CI.
  workers: process.env.CI ? 1 : undefined,

  // Reporter to use
  reporter: 'html',

  use: {
    // Base URL to use in actions like `await page.goto('/')`.
    baseURL: 'http://127.0.0.1:3000',

    // Collect trace when retrying the failed test.
    trace: 'on-first-retry',
  },
  // Configure projects for major browsers.
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
  ],
});
