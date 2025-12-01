#!/usr/bin/env python
"""
Email Configuration Test Script
Tests if your SMTP email settings are working correctly
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'marketplace.settings')
django.setup()

from django.core.mail import send_mail
from django.conf import settings
from decouple import config

def test_email_config():
    """Test email configuration and send a test email"""
    
    print("=" * 60)
    print("🔍 TESTING EMAIL CONFIGURATION")
    print("=" * 60)
    
    # Check configuration
    print("\n📋 Current Email Settings:")
    print(f"   EMAIL_HOST: {settings.EMAIL_HOST}")
    print(f"   EMAIL_PORT: {settings.EMAIL_PORT}")
    print(f"   EMAIL_HOST_USER: {settings.EMAIL_HOST_USER or '❌ NOT SET'}")
    print(f"   EMAIL_HOST_PASSWORD: {'✅ SET' if settings.EMAIL_HOST_PASSWORD else '❌ NOT SET'}")
    print(f"   EMAIL_USE_TLS: {settings.EMAIL_USE_TLS}")
    
    # Validate configuration
    if not settings.EMAIL_HOST_USER:
        print("\n❌ ERROR: EMAIL_HOST_USER is not set in .env file!")
        print("   Please add: EMAIL_HOST_USER=your-email@gmail.com")
        return False
    
    if not settings.EMAIL_HOST_PASSWORD:
        print("\n❌ ERROR: EMAIL_HOST_PASSWORD is not set in .env file!")
        print("   Please generate a Gmail App Password and add it to .env")
        print("   Guide: https://support.google.com/accounts/answer/185833")
        return False
    
    print("\n✅ Configuration looks good!")
    
    # Send test email
    print("\n📧 Sending test email...")
    print(f"   From: {settings.EMAIL_HOST_USER}")
    print(f"   To: {settings.EMAIL_HOST_USER}")
    
    try:
        send_mail(
            subject='✅ VHORLA Email Test - Success!',
            message='This is a test email from your Django application.\n\nIf you received this, your SMTP configuration is working correctly!',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        
        print("\n" + "=" * 60)
        print("✅ SUCCESS! Email sent successfully!")
        print("=" * 60)
        print(f"\n📬 Check your inbox at: {settings.EMAIL_HOST_USER}")
        print("   (Also check spam/junk folder)")
        print("\n✨ Your registration emails will work now!")
        return True
        
    except Exception as e:
        print("\n" + "=" * 60)
        print("❌ ERROR: Failed to send email")
        print("=" * 60)
        print(f"\n🔴 Error Type: {type(e).__name__}")
        print(f"🔴 Error Message: {str(e)}")
        
        # Provide specific help based on error
        error_str = str(e).lower()
        
        if 'authentication' in error_str or 'username and password' in error_str:
            print("\n💡 SOLUTION:")
            print("   1. Make sure you're using a Gmail App Password, not your regular password")
            print("   2. Enable 2-Factor Authentication on your Google Account")
            print("   3. Generate a new App Password: https://myaccount.google.com/apppasswords")
            print("   4. Update EMAIL_HOST_PASSWORD in your .env file")
            
        elif 'connection' in error_str or 'timed out' in error_str:
            print("\n💡 SOLUTION:")
            print("   1. Check your internet connection")
            print("   2. Make sure EMAIL_PORT=587 in .env")
            print("   3. Make sure EMAIL_USE_TLS=True in .env")
            print("   4. Check if firewall is blocking port 587")
            
        elif 'starttls' in error_str:
            print("\n💡 SOLUTION:")
            print("   1. Change EMAIL_PORT to 587 (not 465)")
            print("   2. Make sure EMAIL_USE_TLS=True")
            
        else:
            print("\n💡 COMMON SOLUTIONS:")
            print("   1. Double-check your EMAIL_HOST_USER (should be full email)")
            print("   2. Make sure you're using App Password, not regular password")
            print("   3. Restart your Django server after changing .env")
            print("   4. Check EMAIL_SETUP_GUIDE.md for detailed instructions")
        
        return False

if __name__ == '__main__':
    test_email_config()
