# SMTP Email Setup Guide for Django Registration

## ⚠️ CRITICAL: Your Email Settings Are Empty!

Your `.env` file shows:
```
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

**This WILL NOT WORK!** You need to configure these properly.

## 🔧 Step-by-Step Gmail SMTP Setup

### Step 1: Enable 2-Factor Authentication on Gmail

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** (left sidebar)
3. Under "How you sign in to Google", click **2-Step Verification**
4. Follow the steps to enable it

### Step 2: Generate App Password

1. Go to: https://myaccount.google.com/apppasswords
   - Or: Google Account → Security → 2-Step Verification → App passwords
2. Select app: **Mail**
3. Select device: **Other (Custom name)**
4. Enter name: **Django VHORLA**
5. Click **Generate**
6. **COPY THE 16-CHARACTER PASSWORD** (you won't see it again!)

### Step 3: Update Your .env File

Open your `.env` file and update:

```bash
# Email Configuration
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop  # The 16-char app password (spaces don't matter)
EMAIL_USE_TLS=True
```

**IMPORTANT:**
- Use your **full Gmail address** for EMAIL_HOST_USER
- Use the **16-character App Password**, NOT your regular Gmail password
- Keep the spaces in the app password or remove them - both work

### Step 4: Test Email Sending

Run this test script:

```bash
python test_email.py
```

## 🧪 Test Email Script

I've created `test_email.py` for you. Run it to verify email works:

```bash
python test_email.py
```

If successful, you'll see:
```
✅ Email sent successfully!
Check your inbox at: your-email@gmail.com
```

If it fails, you'll see the exact error message.

## 🚨 Common Issues & Solutions

### Issue 1: "SMTPAuthenticationError: Username and Password not accepted"

**Causes:**
- Using regular Gmail password instead of App Password
- 2-Factor Authentication not enabled
- Wrong email address

**Solution:**
- Enable 2FA on Google Account
- Generate new App Password
- Use the App Password in .env

### Issue 2: "SMTPServerDisconnected: Connection unexpectedly closed"

**Causes:**
- Wrong EMAIL_PORT (should be 587)
- EMAIL_USE_TLS not set to True
- Firewall blocking port 587

**Solution:**
```bash
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

### Issue 3: "SMTPException: STARTTLS extension not supported"

**Cause:** Using wrong port (465 instead of 587)

**Solution:** Use port 587 with TLS

### Issue 4: Email sends but never arrives

**Causes:**
- Email in spam folder
- Wrong recipient email
- Gmail blocking the email

**Solution:**
- Check spam/junk folder
- Check Gmail's "Sent" folder
- Add your domain to Gmail's safe senders

## 📧 Production Email Settings (for Hosting)

### Option 1: Gmail (Development & Small Scale)
```bash
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

**Limits:** 500 emails/day

### Option 2: SendGrid (Recommended for Production)
```bash
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
EMAIL_USE_TLS=True
```

**Limits:** 100 emails/day (free), unlimited (paid)

### Option 3: Mailgun
```bash
EMAIL_HOST=smtp.mailgun.org
EMAIL_PORT=587
EMAIL_HOST_USER=postmaster@your-domain.mailgun.org
EMAIL_HOST_PASSWORD=your-mailgun-password
EMAIL_USE_TLS=True
```

## 🔍 Debugging Email Issues

### Enable Email Logging

Add to `settings.py`:

```python
# Email Backend for Development (prints to console)
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
```

This will print emails to console during development instead of sending them.

### Check Django Logs

Look for email-related errors in your Django logs:

```bash
# In your Django shell
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail(
...     'Test Subject',
...     'Test message',
...     'from@example.com',
...     ['to@example.com'],
...     fail_silently=False,
... )
```

## ✅ Verification Checklist

Before deploying:

- [ ] 2-Factor Authentication enabled on Gmail
- [ ] App Password generated
- [ ] EMAIL_HOST_USER set to your Gmail address
- [ ] EMAIL_HOST_PASSWORD set to App Password (16 chars)
- [ ] EMAIL_PORT set to 587
- [ ] EMAIL_USE_TLS set to True
- [ ] Test email script runs successfully
- [ ] Registration email received in inbox
- [ ] Verification link works
- [ ] Password reset email works

## 🎯 Quick Test Commands

### Test 1: Basic Email
```bash
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'This is a test', 'from@example.com', ['your-email@gmail.com'])
```

### Test 2: Registration Flow
1. Go to `/accounts/register/`
2. Fill in the form
3. Submit
4. Check email for verification link
5. Click link
6. Should activate account

### Test 3: Password Reset
1. Go to `/accounts/password-reset/`
2. Enter email
3. Check email for reset link
4. Click link
5. Set new password

## 📝 Example .env File

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,summerclass-ghxx.onrender.com

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/myproject_db

# Email Configuration (REQUIRED!)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-actual-email@gmail.com
EMAIL_HOST_PASSWORD=abcd efgh ijkl mnop
EMAIL_USE_TLS=True

# eSewa
ESEWA_PRODUCT_CODE=EPAYTEST
ESEWA_SECRET_KEY=your-secret-key
ESEWA_FORM_URL=https://rc-epay.esewa.com.np/api/epay/main/v2/form
```

## 🆘 Still Not Working?

1. **Check your .env file** - Make sure EMAIL_HOST_USER and EMAIL_HOST_PASSWORD are filled
2. **Restart Django server** - Changes to .env require restart
3. **Check spam folder** - Gmail might mark it as spam
4. **Try test_email.py** - See the exact error
5. **Check Google Account** - Make sure 2FA is enabled
6. **Generate new App Password** - Old one might be revoked

## 📞 Need Help?

Share:
1. Error message from test_email.py
2. Django server logs
3. Whether 2FA is enabled
4. Whether you're using App Password or regular password
