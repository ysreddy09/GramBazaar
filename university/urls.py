from django.urls import path
from . import views
from .views import verify_email

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name='signup'),
    path('home/', views.home, name='home'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
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
    path('add_product/', views.add_product, name='add_product'),
    path('details/', views.details, name='details'),
    path('products_hist/', views.products_hist, name='products_hist'),
    path('update_seller/', views.update_seller, name='update_seller'),
    path('generate-pdf/', views.generate_pdf, name='generate_pdf'),
    path('verification/', views.verification, name='verification'),
    path('send_verification_email', views.send_verification_email, name='send_verification_email'),
    path('verify_email/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('forgot/',views.forgot, name='forgot'),
    path('verify_otp/', views.verify_otp, name='verify_otp')
]
