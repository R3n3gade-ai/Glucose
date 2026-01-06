GLP1

Complete sales funnel with Authorize.Net payment processing + Vercel deployment.

**Live Site**: https://glp-1-git-main-joshuas-projects-95d2d3ba.vercel.app/

## Features

- ✅ Responsive landing page (glp-clone.html)
- ✅ Multi-package checkout (1, 3, 6 bottle options)
- ✅ Order bump ($19 premium guide)
- ✅ Upsell flow (post-purchase offers)
- ✅ Secure payment via Authorize.Net Accept.js
- ✅ Serverless API for payment processing
- ✅ Thank you pages with tracking

## Local Preview

```bash
python -m http.server 5500
# Open http://localhost:5500/glp-clone.html
```

## Vercel Deployment

### 1. Repository Setup
Ensure your repo contains:
- `index.html` (root redirect)
- `glp-clone.html` (main landing page)
- `public/` folder (checkout, thank-you, upsells)
- `api/` folder (charge.js, config.js)
- `vercel.json` (routing config)
- `package.json`

### 2. Environment Variables
In Vercel → Project Settings → Environment Variables, add:

```
AUTHNET_API_LOGIN_ID=your_api_login_id
AUTHNET_TRANSACTION_KEY=your_transaction_key
AUTHNET_PUBLIC_CLIENT_KEY=your_public_client_key
AUTHNET_SIGNATURE_KEY=your_signature_key
```

**Security**: Never commit actual credentials. Use `.env.example` as a template.

### 3. Authorize.Net Configuration
- Log into Authorize.Net dashboard
- Go to Account → Security Settings → Manage Accept Client Keys
- Add your Vercel domain to **Allowed Origins**:
  - Production: `https://your-site.vercel.app`
  - Preview: `https://your-site-*.vercel.app`

### 4. Deploy
```bash
git add .
git commit -m "Complete checkout funnel with Authorize.Net"
git push origin main
```

Vercel will auto-deploy from GitHub.

## Sales Funnel Flow

1. **Landing Page** (`/`) → redirects to `glp-clone.html`
2. **Checkout** (`/checkout`) → 3 package options + order bump
3. **Thank You** (`/thank-you`) → confirmation + upsell offer
4. **Upsell 1** (`/upsell-1`) → $49 advanced formula (optional)
5. **Final Thank You** (`/thank-you-final`) → order complete

## Payment Processing

- **Client-side**: Accept.js tokenizes card data (no PCI compliance needed)
- **Server-side**: `/api/charge` creates authCaptureTransaction via Authorize.Net API
- **Security**: All card data stays in Accept.js modal; only payment tokens reach your server

## Testing

### Sandbox Mode
Use Authorize.Net sandbox credentials for testing:
- Test card: 4111111111111111
- CVV: 123
- Exp: any future date

### Production
Switch to production credentials in Vercel env vars when ready for live transactions.

## Support

Questions? Check Authorize.Net docs or contact support@glucoboost.com
