from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product
from .forms import ProductFilterForm

class ProductList(ListView):
    model = Product

class ProductDetail(DetailView):
    model = Product
    
def search(request):
    return render(request, 'products/search.html')

def filter(request):
    products = Product.objects.all()
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        data = form.cleaned_data
        sensitive = data.get('sensitive', False)
        name = data.get('name')
        description = data.get('description')
        price_from = data.get('price_from')
        price_to = data.get('price_to')

        if name:
            if sensitive:
                products = products.filter(name__contains=name)
            else:
                products = products.filter(name__icontains=name)

        if description:
            if sensitive:
                products = products.filter(desc__contains=description)
            else:
                products = products.filter(desc__icontains=description)

        if price_from and price_to:
            products = products.filter(price__range=(price_from, price_to))

    context = {
        'products': products,
        'form': form,
    }
    return render(request, 'products/product_filter.html', context)