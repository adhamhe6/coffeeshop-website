from django.shortcuts import render
from django.views.generic import TemplateView
from products.models import Product

class HomeView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return context

class AboutView(TemplateView):
    template_name = 'pages/about.html'

class CoffeeView(TemplateView):
    template_name = 'pages/coffee.html'