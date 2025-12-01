# Quick Fix Guide: Login/Register Issues on Hosting

## What I Fixed

### 1. Added Production Security Settings ✅
- Secure cookies for HTTPS
- CSRF protection for your domain
- Session security
- SSL/TLS settings

### 2. Fixed Database Configuration ✅
- Now uses `DATABASE_URL` environment variable
- Falls back to local database for development
- Added connection pooling for better performance

### 3. Installed Required Package ✅
- Added `dj-database-url` to requirements.txt

## Most Common Issues & Solutions

### Issue: "CSRF verification failed" on login/register

**Symptoms:**
- Form submission fails
- Error message about CSRF token
- 403 Forbidden error

**Solutions:**
1. **Check your hosting environment variables:**
   ```
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   ```

2. **Verify CSRF_TRUSTED_ORIGINS in settings.py:**
   ```python
   CSRF_TRUSTED_ORIGINS = [
       'https://your-domain.com',
       'https://www.your-domain.com',
   ]
   ```

3. **Make sure DEBUG=False in production**

### Issue: Login works locally but not on hosting

**Possible Causes:**
1. **Cookies not being set** - Check browser DevTools > Application > Cookies
2. **HTTPS redirect issues** - Ensure `SECURE_PROXY_SSL_HEADER` is set (already done)
3. **Database not migrated** - Run migrations on production

**Quick Test:**
```bash
# On your hosting platform
python manage.py migrate
python manage.py createsuperuser
```

### Issue: "DisallowedHost" error

**Fix:** Add your domain to ALLOWED_HOSTS environment variable:
```
ALLOWED_HOSTS=summerclass-ghxx.onrender.com
```

### Issue: Static files (CSS/JS) not loading

**Fix:**
```bash
python manage.py collectstatic --noinput
```

Make sure WhiteNoise is in MIDDLEWARE (already configured ✅)

## Environment Variables You MUST Set on Hosting

```bash
# Critical
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=summerclass-ghxx.onrender.com

# Database (get from your hosting provider)
DATABASE_URL=postgresql://user:password@host:port/database

# Email (for registration verification)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

## Testing Your Login/Register

### 1. Test Registration
```
1. Go to /accounts/register/
2. Fill in the form
3. Submit
4. Check email for verification link
5. Click verification link
6. Should redirect to login
```

### 2. Test Login
```
1. Go to /accounts/login/
2. Enter credentials
3. Submit
4. Should redirect to dashboard
```

### 3. Check Browser Console
- Open DevTools (F12)
- Go to Console tab
- Look for JavaScript errors
- Go to Network tab
- Look for failed requests (red)

## Debugging Steps

### Step 1: Check Server Logs
Look for errors related to:
- CSRF
- Database connection
- Email sending
- Session/cookies

### Step 2: Temporarily Enable DEBUG
**WARNING: Only do this briefly for debugging**
```
DEBUG=True
```
This will show detailed error pages

### Step 3: Test Database Connection
```python
python manage.py shell
>>> from django.contrib.auth import get_user_model
>>> User = get_user_model()
>>> User.objects.all()
```

### Step 4: Check Email Configuration
```python
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])
```

## Still Not Working?

### Check These:

1. **Is your domain in CSRF_TRUSTED_ORIGINS?**
   - Must include `https://`
   - Must match exactly

2. **Are cookies being set?**
   - Check browser DevTools > Application > Cookies
   - Should see `sessionid` and `csrftoken`

3. **Is the database accessible?**
   - Check DATABASE_URL is correct
   - Verify database exists
   - Check migrations are applied

4. **Are static files loading?**
   - Check browser Network tab
   - Look for 404 errors on CSS/JS files

5. **Is email configured correctly?**
   - Gmail requires App Password
   - Check EMAIL_HOST_USER and EMAIL_HOST_PASSWORD

## Contact Form Example (if needed)

If you need to test the contact form separately:

```python
# In views.py
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        try:
            send_mail(
                f'Contact from {name}',
                message,
                email,
                ['your-email@example.com'],
                fail_silently=False,
            )
            messages.success(request, 'Message sent successfully!')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    # ... rest of your code
```

## Need More Help?

Share these details:
1. Exact error message
2. Browser console errors
3. Server logs
4. What you've already tried
