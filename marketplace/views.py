from django.shortcuts import render
from store.models import Product
from banner.models import Banner, PromoBanner
from category.models import Category

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
        or Product.objects.filter(status=True, is_approved=True)
                          .order_by('-updated_date', '-created_date')
                          .first()
    )

    context = {
        'products': products,
        'banners': banners,
        'categories': categories,
        'offer_product': offer_product,
        'promo_banner_left': promo_banner_left,
        'promo_banner_right': promo_banner_right,
    }

    return render(request, 'home/home.html', context)
