const express = require('express');
const bodyParser = require('body-parser');
const admin = require('firebase-admin');
const serviceAccount = require('./nutri-a-444113-firebase-adminsdk-16r9f-56c7715eef.json');

admin.initializeApp({
  credential: admin.credential.cert(serviceAccount)
});

const app = express();
app.use(bodyParser.json());

// Email validation function
function isValidEmail(email) {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

// Register API
app.post('/register', async (req, res) => {
  const { email, password } = req.body;
  if (!isValidEmail(email)) {
    return res.status(400).send('The email address is improperly formatted.');
  }
  try {
    const userRecord = await admin.auth().createUser({
      email: email,
      password: password,
    });
    res.status(200).send('User created successfully');
  } catch (error) {
    res.status(400).send(error.message);
  }
});

// Login API
app.post('/login', async (req, res) => {
  const { email, password } = req.body;
  if (!isValidEmail(email)) {
    return res.status(400).send('The email address is improperly formatted.');
  }
  try {
    const userRecord = await admin.auth().getUserByEmail(email);
    res.status(200).send('Login successful');
  } catch (error) {
    res.status(400).send(error.message);
  }
});

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
