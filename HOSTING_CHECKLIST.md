# Django Login/Register Hosting Checklist

## ✅ Issues Fixed

### 1. Security Settings Added
- Added production security settings in `settings.py`
- HTTPS redirect enabled for production
- Secure cookies for sessions and CSRF
- HSTS headers configured
- Proxy SSL header support for hosting platforms

### 2. Current Configuration Status

**✓ Already Correct:**
- CSRF tokens present in login.html and register.html
- CSRF_TRUSTED_ORIGINS configured for your domain
- ALLOWED_HOSTS uses environment variables
- Email settings configured

**⚠️ Needs Attention:**
- Database credentials are hardcoded (see below)

## 🔧 Required Environment Variables for Hosting

Make sure these are set in your hosting platform (Render/Heroku/etc):

```bash
# Required
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database (use your hosting provider's database URL)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# eSewa
ESEWA_PRODUCT_CODE=your-product-code
ESEWA_SECRET_KEY=your-secret-key
ESEWA_FORM_URL=https://epay.esewa.com.np/api/epay/main/v2/form
```

## 📝 Database Configuration for Production

**Current Issue:** Database credentials are hardcoded in settings.py

**Fix:** Update `settings.py` to use DATABASE_URL from environment:

```python
import dj_database_url

# Replace the current DATABASES configuration with:
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default='postgresql://prashish:ilovepostgres@1@localhost:5432/myproject_db')
    )
}
```

**Install required package:**
```bash
pip install dj-database-url
pip freeze > requirements.txt
```

## 🚀 Deployment Steps

### 1. Update requirements.txt
```bash
pip freeze > requirements.txt
```

### 2. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 3. Run Migrations on Production
```bash
python manage.py migrate
```

### 4. Create Superuser (if needed)
```bash
python manage.py createsuperuser
```

## 🔍 Common Login/Register Issues on Hosting

### Issue 1: CSRF Verification Failed
**Cause:** Missing CSRF_TRUSTED_ORIGINS or wrong domain
**Fix:** Ensure `CSRF_TRUSTED_ORIGINS` includes your full domain with https://

### Issue 2: Static Files Not Loading
**Cause:** collectstatic not run or wrong STATIC_ROOT
**Fix:** Run `python manage.py collectstatic` and ensure WhiteNoise is configured

### Issue 3: Database Connection Error
**Cause:** Wrong database credentials or DATABASE_URL
**Fix:** Check your hosting provider's database credentials

### Issue 4: Email Verification Not Working
**Cause:** Email settings incorrect or Gmail blocking
**Fix:** 
- Use Gmail App Password (not regular password)
- Enable "Less secure app access" or use OAuth2

### Issue 5: Session/Cookie Issues
**Cause:** Secure cookies not working with HTTP
**Fix:** Ensure your site uses HTTPS (should be automatic on Render)

## 🧪 Testing Checklist

Before deploying:
- [ ] Test login with correct credentials
- [ ] Test login with wrong credentials
- [ ] Test registration with new email
- [ ] Test registration with existing email
- [ ] Test email verification link
- [ ] Test password reset
- [ ] Test "Remember Me" functionality
- [ ] Test logout

After deploying:
- [ ] Test all above on production URL
- [ ] Check browser console for errors
- [ ] Check server logs for errors
- [ ] Test on different browsers
- [ ] Test on mobile devices

## 📊 Debugging on Production

### View Logs
```bash
# On Render
render logs

# Check Django logs
tail -f /path/to/logs/django.log
```

### Common Log Errors

**"CSRF verification failed"**
- Check CSRF_TRUSTED_ORIGINS
- Ensure form has {% csrf_token %}
- Check if cookies are being set

**"DisallowedHost"**
- Add your domain to ALLOWED_HOSTS

**"OperationalError: FATAL: password authentication failed"**
- Check DATABASE_URL
- Verify database credentials

## 🔐 Security Best Practices

1. **Never commit .env file** - Add to .gitignore
2. **Use strong SECRET_KEY** - Generate new one for production
3. **Enable 2FA for admin** - Use django-two-factor-auth
4. **Rate limit login attempts** - Already have loginattempt app
5. **Use HTTPS only** - Configured in settings
6. **Regular security updates** - Keep Django and packages updated

## 📞 Support

If issues persist:
1. Check server logs
2. Enable DEBUG=True temporarily to see detailed errors
3. Check browser Network tab for failed requests
4. Verify all environment variables are set correctly
