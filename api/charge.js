// Serverless function to capture a payment via Authorize.Net using opaqueData from Accept.js
// Do NOT hardcode secrets; use environment variables in Vercel.

module.exports = async (req, res) => {
  if (req.method !== 'POST') {
    res.status(405).json({ error: 'Method Not Allowed' });
    return;
  }

  try {
    const {
      amount,
      opaqueData,
      firstName,
      lastName,
      email
    } = req.body || {};

    if (!opaqueData || !opaqueData.dataValue) {
      res.status(400).json({ error: 'Missing opaqueData from Accept.js' });
      return;
    }
    if (!amount || Number(amount) <= 0) {
      res.status(400).json({ error: 'Invalid amount' });
      return;
    }

    const payload = {
      createTransactionRequest: {
        merchantAuthentication: {
          name: process.env.AUTHNET_API_LOGIN_ID,
          transactionKey: process.env.AUTHNET_TRANSACTION_KEY
        },
        transactionRequest: {
          transactionType: 'authCaptureTransaction',
          amount: Number(amount),
          payment: {
            opaqueData: {
              dataDescriptor: opaqueData.dataDescriptor || 'COMMON.ACCEPT.INAPP.PAYMENT',
              dataValue: opaqueData.dataValue
            }
          },
          customer: email ? { email } : undefined,
          billTo: {
            firstName: firstName || undefined,
            lastName: lastName || undefined
          }
        }
      }
    };

    const resp = await fetch('https://api.authorize.net/xml/v1/request.api', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await resp.json();

    const resultCode = data?.messages?.resultCode;
    if (resultCode !== 'Ok') {
      const err = data?.messages?.message?.[0];
      res.status(402).json({ error: `${err?.code || 'ERROR'}: ${err?.text || 'Payment error'}` });
      return;
    }

    const txn = data?.transactionResponse;
    if (!txn || txn.responseCode !== '1') {
      const err = txn?.errors?.[0];
      res.status(402).json({ error: `${err?.errorCode || 'DECLINED'}: ${err?.errorText || 'Transaction declined'}` });
      return;
    }

    res.status(200).json({ status: 'approved', authCode: txn.authCode, transactionId: txn.transId });
  } catch (e) {
    res.status(500).json({ error: e.message || 'Server error' });
  }
};
