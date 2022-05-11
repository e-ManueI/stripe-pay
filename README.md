# stripe-pay
Payment processing and gateway in Django using Stripe

### REQUIREMENT:
1. Clone the repository. Virtual environment using PIPENV is suitable for this project to install Django.

2. A test account at [stripe](dashboard.stripe.com) is required.

3. In the /container/settings.py, the STRIPE_PUBLIC_KEY, STRIPE_SECRET_KEY and the STRIPE_WEBHOOK_SECRET files should be altered into relevant key values obtained from the stripe developer dashboard. 
Facing problems?
[click here](https://www.appinvoice.com/en/s/documentation/how-to-get-stripe-publishable-key-and-secret-key-23) or  [here(official documentation)](https://stripe.com/docs/keys) to learn more.

4. When required, the stripe CLI is installed manually into the root directory to activate stripe webhooks (listening ports). Check this [here](https://stripe.com/docs/webhooks).