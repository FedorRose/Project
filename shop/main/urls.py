from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name='index'),
    path('shop/<slug:category_slug>', views.shop, name='shop'),
    path('shop/<slug:category_slug>/<slug:product_slug>', views.shop_single, name='shop_single'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('wishlist/', views.wishlist_view, name='wishlist_view'),
    path('wishlist/remove/<int:product_id>)', views.wishlist_remove, name='wishlist_remove'),
    path('wishlist/add/<int:product_id>', views.wishlist_add, name='wishlist_add'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:post_slug>', views.blog_single, name='blog_single'),
]
