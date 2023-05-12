# Setup

Install [nvm node version manager](https://github.com/nvm-sh/nvm)
Install node lts , use node lts

```
npm install
```

# Run

> On Dell servers, the default username and password for iDRAC is `root`/`calvin`.

```
IDRAC_USERNAME=root IDRAC_PASSWORD=calvin npx playwright test scripts/iDRAC-set-virtual-terminal-html5.spec.ts --debug
```

# Test generation / writing new scripts/tests

```
PWDEBUG=console npx playwright codegen --ignore-https-errors https://192.168.0.120
```
