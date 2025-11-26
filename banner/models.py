from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Banner(models.Model):
    banner_title = models.CharField(max_length=100, unique=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(blank=True)
    url = models.CharField(max_length=200, blank=True, null=True)
    banner_image = models.ImageField(upload_to="photos/banners", blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    
    
    class Meta:
        verbose_name = 'banner'
        verbose_name_plural = 'banners'
        
    def __str__(self):
        return self.banner_title or "Homepage Banner"

    def save(self, *args, **kwargs):
        if not self.banner_title:
            timestamp = timezone.now().strftime("%Y%m%d%H%M%S")
            self.banner_title = f"Banner {timestamp}"

        if not self.slug:
            base_slug = slugify(self.banner_title) or f"banner-{timezone.now().strftime('%Y%m%d%H%M%S')}"
            unique_slug = base_slug
            counter = 1
            while Banner.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = unique_slug

        super().save(*args, **kwargs)


class PromoBanner(models.Model):
    POSITION_CHOICES = [
        ("left", "Left"),
        ("right", "Right"),
    ]

    title = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=10, choices=POSITION_CHOICES, default="left", unique=True)
    image = models.ImageField(upload_to="photos/promo_banners")
    url = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Featured Promo Banner"
        verbose_name_plural = "Featured Promo Banner"

    def __str__(self):
        return self.title or "Promo Banner"
