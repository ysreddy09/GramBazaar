import random

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import UserProfile
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from django.contrib.auth.decorators import login_required
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas


def index(request):
    return render(request, 'index.html')


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            role = form.cleaned_data['role']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                return render(request, 'signup.html', {'form': form, 'error_message': 'Passwords do not match'})

            username = first_name.lower() + str(random.randint(100, 999))

            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            print("User created:", user)

            pro = UserProfile.objects.create(user=user, roles=role)
            print("UserProfile created:", pro)

            return redirect('login')

    return render(request, 'signup.html', {'form': form})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid email or password.'})
    return render(request, 'login.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def navbar(request):
    return render(request, 'navbar.html')


def home_page_slider(request):
    return render(request, 'home_page_slider.html')


def products(request):
    return render(request, 'products.html')


def generate_pdf(request):
    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)

    # Draw content on the PDF.
    p.drawString(100, 750, "Shopping Cart")
    p.drawString(100, 700, "Image")
    p.drawString(200, 700, "Product")
    p.drawString(350, 700, "Price")
    p.drawString(450, 700, "Quantity")
    p.drawString(550, 700, "Total")

    # Example product details (replace with actual data)
    prods = [
        {"title": "Dingo Dog Bones", "price": "$12.99", "quantity": "2", "total": "$25.98"},
        {"title": "Nutro™ Adult Lamb and Rice Dog Food", "price": "$45.99", "quantity": "1", "total": "$45.99"},
        {"title": "Nutro™ Adult Lamb and Rice Dog Food", "price": "$45.99", "quantity": "1", "total": "$45.99"}
    ]
    y = 680
    for product in prods:
        y -= 20
        p.drawString(100, y, product["title"])
        p.drawString(350, y, product["price"])
        p.drawString(450, y, product["quantity"])
        p.drawString(550, y, product["total"])

    # Add subtotal, tax, shipping, and grand total
    p.drawString(100, y - 30, "Subtotal: $71.97")
    p.drawString(100, y - 50, "Tax (5%): $3.60")
    p.drawString(100, y - 70, "Shipping: $15.00")
    p.drawString(100, y - 90, "Grand Total: $90.57")

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Set the file pointer back to the beginning of the buffer.
    buffer.seek(0)

    # Return the PDF as a FileResponse.
    return FileResponse(buffer, as_attachment=True, filename="shopping_cart.pdf")


def add_to_cart(request):
    return render(request, 'add_to_cart.html')


@login_required
def profile(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)


def footer(request):
    return render(request, 'footer.html')


def update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            postal_code = form.cleaned_data['postal_code']
            phone_number = form.cleaned_data['phone_number']
            address = form.cleaned_data['address']
            profile_picture = form.cleaned_data['profile_picture']

            # Get or create the user's profile
            User_profile, created = UserProfile.objects.get_or_create(user=request.user)

            # Update profile fields
            User_profile.first_name = first_name
            User_profile.last_name = last_name
            User_profile.postal_code = postal_code
            User_profile.phone_number = phone_number
            User_profile.address = address

            # Update profile picture if provided
            if profile_picture:
                User_profile.profile_pic = profile_picture

            User_profile.save()
            return redirect('profile')
    else:
        # If it's a GET request, initialize the form with user data
        initial_data = {
            'first_name': request.user.userprofile.first_name,
            'last_name': request.user.userprofile.last_name,
            'postal_code': request.user.userprofile.postal_code,
            'phone_number': request.user.userprofile.phone_number,
            'address': request.user.userprofile.address,
        }
        form = ProfileUpdateForm(initial=initial_data)

    return render(request, 'update.html', {'form': form})


def about(request):
    return render(request, 'about.html')


def purchased_history(request):
    return render(request, 'purchased_history.html')


def side_nav(request):
    return render(request, 'side_nav.html')


def seller_home(request):
    return render(request, 'seller_home.html')


def add_product(request):
    return render(request, 'add_product.html')


def details(request):
    return render(request, 'details.html')


def products_hist(request):
    return render(request, 'products_hist.html')


def update_seller(request):
    return render(request, 'update_seller.html')


def profile_seller(request):
    return render(request, 'profile_seller.html')


def admin_home(request):
    return render(request, 'admin_home.html')


def admin_details(request):
    return render(request, 'admin_details.html')


def admin_side_nav(request):
    return render(request, 'admin_side_nav.html')
