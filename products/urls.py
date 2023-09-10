from django.urls import path, include
from .views import ProductList, ProductHotList, ProductColdList, filter, ProductDetail, search

app_name = 'products'
urlpatterns = [
    path('', ProductList.as_view(), name='product-list'),
    path('hot/', ProductHotList.as_view(), name='product-hot'),
    path('cold/', ProductColdList.as_view(), name='product-cold'),
    path('s/', filter, name='filter'),
    path('<int:pk>/', ProductDetail.as_view(), name='product-detail'),
    path('search/', search, name='search'),
]