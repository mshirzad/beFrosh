from django.urls import path
from django.contrib import admin
from product import views

app_name = 'product'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('add-product/', views.addProduct, name='add-product'),
    path('add-fav/', views.add_fav, name='add-fav'),
    path('my-listings/', views.my_listings, name='my-listings'),
    path('favorites/', views.favorites, name='favorites'),
    path('product-details/<str:prod_pk>/',
         views.productDetails, name='product-details'),
    path('search/', views.search_products, name='search-products'),

    path('add-comment/', views.add_comment, name='add-comment'),
    path('delete-product/', views.delete_item, name='delete-product'),
    path('delete-fave/', views.delete_fave, name='delete-fave'),



]
