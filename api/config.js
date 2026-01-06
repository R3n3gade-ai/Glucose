// Returns public config for the browser (no secrets)
module.exports = async (req, res) => {
  res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
  const apiLogin = process.env.AUTHNET_API_LOGIN_ID || '';
  const publicKey = process.env.AUTHNET_PUBLIC_CLIENT_KEY || '';
  res.status(200).send(`window.AUTHNET_API_LOGIN_ID=${JSON.stringify(apiLogin)};window.AUTHNET_PUBLIC_CLIENT_KEY=${JSON.stringify(publicKey)};`);
};
