from django.contrib import admin
from .models import SiteSetting, ContactSetting

from django.utils.html import format_html


# Register your models here.

class SettingAdmin(admin.ModelAdmin):
    list_display = ('site_title', 'address', 'phone_number', 'logo_preview', 'favicon_preview', 'default_image_preview')
    readonly_fields = ('logo_preview','favicon_preview', 'default_image_preview')
    
    def logo_preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.logo.url)
        return "No Logo"
    
    def favicon_preview(self, obj):
        if obj.favicon:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.favicon.url)
        return "No Favicon"
    
    def default_image_preview(self, obj):
        if obj.default_image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.default_image.url)
        return "No Favicon"
    
    logo_preview.short_description = 'Logo'
    favicon_preview.short_description = 'Favicon'
    default_image_preview.short_description = 'Default Image'
    

class ContactSettingAdmin(admin.ModelAdmin):
    list_display = ('primary_email', 'primary_phone', 'support_phone')
    fieldsets = (
        ('Primary Office', {
            'fields': ('primary_email', 'primary_phone', 'primary_address')
        }),
        ('Support & Inquiries', {
            'fields': ('support_phone', 'support_address')
        }),
        ('Social Media', {
            'fields': ('instagram_url', 'whatsapp_url', 'facebook_url', 'tiktok_url', 'youtube_url', 'wechat_url')
        }),
    )
    

admin.site.register(SiteSetting, SettingAdmin)
admin.site.register(ContactSetting, ContactSettingAdmin)