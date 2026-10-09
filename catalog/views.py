from django.shortcuts import render

from .models import Product


def home(request):
    products = (
        Product.objects.filter(is_active=True)
        .select_related('category')
        .prefetch_related('images')[:12]
    )
    return render(request, 'home.html', {'products': products})