from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('navbar/', views.navbar, name='navbar'),
    path('home_page_slider/', views.home_page_slider, name='home_page_slider'),
    path('products/', views.navbar, name='products'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('profile/', views.profile, name='profile'),
    path('footer/', views.footer, name='footer'),
    path('about/', views.about, name='about'),
    path('update/', views.update, name='update'),
    path('purchased_history/', views.purchased_history, name='purchased_history'),
    path('side_nav/', views.side_nav, name='side_nav'),
    path('seller_home/', views.seller_home, name='seller_home'),
    path('add_product/', views.add_product, name='add_product'),
    path('details/', views.details, name='details'),
    path('products_hist/', views.products_hist, name='products_hist'),
    path('profile_seller/', views.profile_seller, name='profile_seller'),
    path('update_seller/', views.update_seller, name='update_seller'),
    path('admin_home/', views.admin_home, name='admin_home'),
    path('admin_side_nav/', views.admin_side_nav, name='admin_side_nav'),
    path('admin_details/', views.admin_details, name='admin_details'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
]
