require('dotenv').config();
const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3000;

// Debug: Check if Environment Variables are loaded
console.log('------------------------------------------------');
console.log('Server Starting...');
console.log('Environment Variable Check:');
console.log('AUTHNET_API_LOGIN_ID exists:', !!process.env.AUTHNET_API_LOGIN_ID);
console.log('AUTHNET_PUBLIC_CLIENT_KEY exists:', !!process.env.AUTHNET_PUBLIC_CLIENT_KEY);
// masked log for verification (show first 4 chars only if exists)
if (process.env.AUTHNET_API_LOGIN_ID) console.log('AUTHNET_API_LOGIN_ID (starts with):', process.env.AUTHNET_API_LOGIN_ID.substring(0, 4) + '...');
if (process.env.AUTHNET_PUBLIC_CLIENT_KEY) console.log('AUTHNET_PUBLIC_CLIENT_KEY (starts with):', process.env.AUTHNET_PUBLIC_CLIENT_KEY.substring(0, 4) + '...');
console.log('------------------------------------------------');

app.use(cors());
app.use(bodyParser.json());

const fs = require('fs');
const DATA_DIR = path.join(__dirname, 'data');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR);
}

const LEADS_FILE = path.join(DATA_DIR, 'leads.json');
const ORDERS_FILE = path.join(DATA_DIR, 'orders.json');
const VISITORS_FILE = path.join(DATA_DIR, 'visitors.json');

// Helper to append data to JSON file
function appendToDataFile(filePath, newData) {
    let data = [];
    try {
        if (fs.existsSync(filePath)) {
            const fileContent = fs.readFileSync(filePath, 'utf8');
            data = JSON.parse(fileContent);
        }
    } catch (e) {
        console.error('Error reading data file:', e);
    }

    // Add timestamp
    newData.timestamp = new Date().toISOString();
    data.push(newData);

    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

// Configuration endpoint
app.get('/api/config.js', (req, res) => {
    res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
    const apiLogin = process.env.AUTHNET_API_LOGIN_ID || '';
    const publicKey = process.env.AUTHNET_PUBLIC_CLIENT_KEY || '';
    res.status(200).send(`window.AUTHNET_API_LOGIN_ID=${JSON.stringify(apiLogin)};window.AUTHNET_PUBLIC_CLIENT_KEY=${JSON.stringify(publicKey)};`);
});

// Admin Data endpoint
app.get('/api/admin-data', (req, res) => {
    let leads = [];
    let orders = [];
    let visitorCount = 0;
    try {
        if (fs.existsSync(LEADS_FILE)) leads = JSON.parse(fs.readFileSync(LEADS_FILE, 'utf8'));
        if (fs.existsSync(ORDERS_FILE)) orders = JSON.parse(fs.readFileSync(ORDERS_FILE, 'utf8'));
        if (fs.existsSync(VISITORS_FILE)) {
            const visitors = JSON.parse(fs.readFileSync(VISITORS_FILE, 'utf8'));
            visitorCount = visitors.length;
        }
    } catch (e) {
        console.error('Error reading admin data:', e);
    }
    res.json({ leads, orders, visitorCount });
});

// Visitor tracking endpoint
app.post('/api/visitor', (req, res) => {
    const { page } = req.body || {};
    appendToDataFile(VISITORS_FILE, { page: page || 'unknown' });
    res.status(200).json({ status: 'tracked' });
});

// Capture Lead endpoint
app.post('/api/lead', (req, res) => {
    const { firstName, lastName, email, phone } = req.body || {};
    if (!email && !phone) {
        return res.status(400).json({ error: 'Email or phone required' });
    }

    appendToDataFile(LEADS_FILE, { firstName, lastName, email, phone, type: 'lead' });
    res.status(200).json({ status: 'saved' });
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

        // Save Order
        const orderData = {
            txnId: txn.transId,
            authCode: txn.authCode,
            amount,
            firstName,
            lastName,
            email,
            phone,
            address,
            city,
            state,
            zip,
            status: 'approved'
        };
        appendToDataFile(ORDERS_FILE, orderData);

        res.status(200).json({ status: 'approved', authCode: txn.authCode, transactionId: txn.transId });
    } catch (e) {
        console.error(e);
        res.status(500).json({ error: e.message || 'Server error' });
    }
});

// Serve static files AFTER all API routes
app.use(express.static(__dirname));

app.listen(PORT, () => {
    console.log(`Server running at http://localhost:${PORT}`);
});
