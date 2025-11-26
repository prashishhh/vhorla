from django.contrib import admin
from . models import Banner, PromoBanner
from django.utils.html import format_html


class BannerAdmin(admin.ModelAdmin):
    list_display = ('banner_title', 'slug', 'created_date', 'updated_date', 'status','image_preview')
    readonly_fields = ('image_preview',)
    exclude = ('banner_title', 'slug', 'description')
    
    def image_preview(self, obj):
        if obj.banner_image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.banner_image.url)
        return "No image"
    
    image_preview.short_description = 'Image'
    

# Register your models here.
@admin.register(PromoBanner)
class PromoBannerAdmin(admin.ModelAdmin):
    list_display = ("__str__", "position", "is_active", "updated_date", "image_preview")
    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" height="80" style="object-fit:cover;" />', obj.image.url)
        return "No image"

    image_preview.short_description = "Image"


admin.site.register(Banner, BannerAdmin)
