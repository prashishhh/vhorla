from django.db import models

# Create your models here.
class SiteSetting(models.Model):
    site_title = models.CharField(max_length=200, default="Vohrla")
    meta_description = models.TextField(blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    logo = models.ImageField(upload_to="photos/logos/", blank=True, null=True)
    favicon = models.ImageField(upload_to="photos/favicons/", blank=True, null=True)
    default_image = models.ImageField(upload_to="photos/default/", blank=True, null=True)
    site_url = models.CharField(max_length=200, blank=True, null=True)
    copyright = models.CharField(max_length=200, blank=True, null=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)

    # Hero Section
    hero_title_line1 = models.CharField(max_length=200, blank=True, null=True, default="A place to discover")
    hero_title_line2 = models.CharField(max_length=200, blank=True, null=True, default="your marketplace.")
    hero_subtitle = models.TextField(blank=True, null=True, default="Buy, sell, or book services — student merch, second-hand textbooks, project services, snacks, and more.")
    
    # Contact Page - Primary Office
    contact_email = models.EmailField(blank=True, null=True, default="contact@monetatech.com")
    contact_phone_1 = models.CharField(max_length=200, blank=True, null=True, default="+1 (555) 123-4567")
    contact_address_1 = models.TextField(blank=True, null=True, default="123 Innovation Avenue, Suite 456\nSan Francisco, CA 94107, USA")
    
    # Contact Page - Support & Inquiries
    contact_phone_2 = models.CharField(max_length=200, blank=True, null=True, default="+1 (555) 987-6543 (Support)")
    contact_address_2 = models.TextField(blank=True, null=True, default="789 Digital Plaza, Floor 10\nNew York, NY 10001, USA")
    
    def __str__(self):
        return "Site Setting"

    class Meta:
        verbose_name = "Site Setting"
        verbose_name_plural = "Site Settings"


class ContactSetting(models.Model):
    # Primary Office
    primary_email = models.EmailField(default="contact@monetatech.com")
    primary_phone = models.CharField(max_length=200, default="+1 (555) 123-4567")
    primary_address = models.TextField(default="123 Innovation Avenue, Suite 456\nSan Francisco, CA 94107, USA")
    
    # Support & Inquiries
    support_phone = models.CharField(max_length=200, default="+1 (555) 987-6543 (Support)")
    support_address = models.TextField(default="789 Digital Plaza, Floor 10\nNew York, NY 10001, USA")
    
    # Social Media Links
    instagram_url = models.URLField(blank=True, null=True, default="https://www.instagram.com/companyname")
    whatsapp_url = models.URLField(blank=True, null=True, default="https://wa.me/15551234567")
    facebook_url = models.URLField(blank=True, null=True, default="https://www.facebook.com/companyname")
    tiktok_url = models.URLField(blank=True, null=True, default="https://www.tiktok.com/@companyname")
    youtube_url = models.URLField(blank=True, null=True, default="https://www.youtube.com/@companyname")
    wechat_url = models.URLField(blank=True, null=True, default="mailto:contact@monetatech.com")
    
    def __str__(self):
        return "Contact Settings"
    
    class Meta:
        verbose_name = "Contact Setting"
        verbose_name_plural = "Contact Settings"