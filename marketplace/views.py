from django.shortcuts import render
from store.models import Product
from banner.models import Banner, PromoBanner
from category.models import Category
from sitesetting.models import SiteSetting, ContactSetting

def home(request):
    # Show only the 4 newest approved products
    products = (
        Product.objects
        .filter(status=True, is_approved=True)
        .order_by('-updated_date', '-created_date')[:4]
    )

    # Active banners
    banners = Banner.objects.filter(status=True)
    promo_banner_left = PromoBanner.objects.filter(is_active=True, position='left').first()
    promo_banner_right = PromoBanner.objects.filter(is_active=True, position='right').first()

    # Show only 4 categories on homepage
    categories = Category.objects.filter(status=True)[:4]

    # Great Offer: newest featured product, or fallback to newest product
    offer_product = (
        Product.objects
        .filter(status=True, is_approved=True, is_featured=True)
        .order_by('-updated_date', '-created_date')
        .first()
    )

    # Site Settings for Hero Section
    site_setting = SiteSetting.objects.first()

    context = {
        'products': products,
        'banners': banners,
        'categories': categories,
        'offer_product': offer_product,
        'promo_banner_left': promo_banner_left,
        'promo_banner_right': promo_banner_right,
        'site_setting': site_setting,
    }

    return render(request, 'home/home.html', context)

def contact(request):
    if request.method == 'POST':
        # Handle form submission here (e.g., send email)
        pass
    
    site_setting = SiteSetting.objects.first()
    # Get or create ContactSetting to ensure it always exists
    contact_setting, created = ContactSetting.objects.get_or_create(pk=1)
    
    # Debug output
    print(f"DEBUG: contact_setting = {contact_setting}")
    print(f"DEBUG: primary_email = {contact_setting.primary_email}")
    print(f"DEBUG: primary_phone = {contact_setting.primary_phone}")
    
    context = {
        'site_setting': site_setting,
        'contact_setting': contact_setting,
    }
    return render(request, 'home/contactus.html', context)



