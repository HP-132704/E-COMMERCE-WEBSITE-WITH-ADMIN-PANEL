from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('collections/<str:name>/', views.collection_by_name, name='collection_by_name'),
    path('product/<str:cname>/<str:pname>/', views.product_details, name='product_details'),
    # Add your existing routes like:
    path('cart/', views.cart_page, name='cart'),
    path('remove_cart/<int:cid>/', views.remove_cart, name='remove_cart'),
    path('favviewpage/', views.favviewpage, name='favviewpage'),
    path('remove_fav/<int:fid>/', views.remove_fav, name='remove_fav'),
    path('fav_product/', views.fav_product, name='fav_product'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('logout/', views.logout_page, name='logout'),
    path('login/', views.login_page, name='login'),
    path('register/', views.register, name='register'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)