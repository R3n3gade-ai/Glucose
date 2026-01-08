require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(__dirname));

// Configuration endpoint
app.get('/api/config.js', (req, res) => {
    res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
    const apiLogin = process.env.AUTHNET_API_LOGIN_ID || '';
    const publicKey = process.env.AUTHNET_PUBLIC_CLIENT_KEY || '';
    res.status(200).send(`window.AUTHNET_API_LOGIN_ID=${JSON.stringify(apiLogin)};window.AUTHNET_PUBLIC_CLIENT_KEY=${JSON.stringify(publicKey)};`);
});

// Charge endpoint
app.post('/api/charge', async (req, res) => {
    try {
        const {
            amount,
            opaqueData,
            firstName,
            lastName,
            email,
            address,
            city,
            state,
            zip,
            phone
        } = req.body || {};

        if (!opaqueData || !opaqueData.dataValue) {
            return res.status(400).json({ error: 'Missing opaqueData from Accept.js' });
        }
        if (!amount || Number(amount) <= 0) {
            return res.status(400).json({ error: 'Invalid amount' });
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
                        lastName: lastName || undefined,
                        address: address || undefined,
                        city: city || undefined,
                        state: state || undefined,
                        zip: zip || undefined,
                        phoneNumber: phone || undefined
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
            return res.status(402).json({ error: `${err?.code || 'ERROR'}: ${err?.text || 'Payment error'}` });
        }

        const txn = data?.transactionResponse;
        if (!txn || txn.responseCode !== '1') {
            const err = txn?.errors?.[0];
            return res.status(402).json({ error: `${err?.errorCode || 'DECLINED'}: ${err?.errorText || 'Transaction declined'}` });
        }

        res.status(200).json({ status: 'approved', authCode: txn.authCode, transactionId: txn.transId });
    } catch (e) {
        console.error(e);
        res.status(500).json({ error: e.message || 'Server error' });
    }
});

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
