from django.urls import path
from .views import HomeView, AboutView, CoffeeView

app_name = 'pages'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('coffee/', CoffeeView.as_view(), name='coffee'),
]