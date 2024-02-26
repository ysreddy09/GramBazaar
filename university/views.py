import random, io
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, logout
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import UserProfile, Product
from .forms import SignUpForm, LoginForm, ProfileUpdateForm
from django.http import FileResponse
from reportlab.pdfgen import canvas


def logout(request):
    request.session.flush()
    return render(request, 'login.html')


def index(request):
    return render(request, 'index.html')


def send_verification_email(request, user, verification_link):
    current_site = get_current_site(request)
    subject = 'Verify your email address'
    message = f'Hello {user.username},\n\n' \
              f'Please click the link below to verify your email address:\n\n' \
              f'{verification_link}\n\n' \
              f'If you did not sign up for an account on our website, you can safely ignore this email.\n\n' \
              f'Thank you,\n' \
              f'The Example Team\n\n' \
              f'This is an automated message, please do not reply.'

    send_mail(subject, message, 'yaswanth2813@gmail.com', [user.email])

    # Set session variables if needed
    request.session['user_id'] = user.id
    request.session['verification_link'] = verification_link

    return redirect('verification')


def verify_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_verified = True
        user.is_active = True
        user_profile.save()
        user.save()
        messages.success(request, 'Your email has been successfully verified.')
    else:
        messages.error(request, 'Failed to verify your email.')

    return redirect('login')


def signup(request):
    form = SignUpForm()
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            roles = form.cleaned_data['roles']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            if password != confirm_password:
                return render(request, 'signup.html', {'form': form, 'error_message': 'Passwords do not match'})

            username = first_name.lower() + str(random.randint(1000, 9999))
            while User.objects.filter(username=username).exists():
                username = first_name.lower() + str(random.randint(1000, 9999))
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.is_active = False
            user.save()
            user_profile = UserProfile(user=user, roles=roles)
            user_profile.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain
            verification_link = f'http://{domain}{reverse("verify_email", kwargs={"uidb64": uidb64, "token": token})}'
            send_verification_email(request, user, verification_link)
            return redirect('verification')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            if user is None:
                # Attempt authentication with email
                try:
                    from django.contrib.auth import get_user_model
                    User = get_user_model()
                    user = User.objects.get(email=username)
                    user = authenticate(request, username=user.username, password=password)
                except User.DoesNotExist:
                    pass

            if user is not None:
                request.session['user'] = user.username
                return redirect('home')
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid email or password.'})
    return render(request, 'login.html', {'form': form})


def home(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        products = Product.objects.all()
    else:
        redirect('login')
    return render(request, 'home.html', {'user': user, 'user_profile': user_profile, 'products': products})


def navbar(request):
    return render(request, 'navbar.html')


def home_page_slider(request):
    return render(request, 'home_page_slider.html')


def add_to_cart(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
    else:
        return redirect('login')
    return render(request, 'add_to_cart.html', {'user': user, 'user_profile': user_profile})


def footer(request):
    return render(request, 'footer.html')


def update(request):
    if 'user' in request.session:
        username = request.session['user']
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if request.method == 'POST':
            form = ProfileUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                user.first_name = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                user_profile.postal_code = form.cleaned_data['postal_code']
                user_profile.phone_number = form.cleaned_data['phone_number']
                user_profile.address = form.cleaned_data['address']
                # Check if a new profile picture was uploaded
                if 'profile_pic' in request.FILES:
                    # If a new image is uploaded, delete the existing one
                    if user_profile.profile_pic:
                        user_profile.profile_pic.delete(save=False)
                    user_profile.profile_pic = request.FILES['profile_pic']

                if request.POST.get('remove_photo', False):
                    # If requested, delete the existing photo
                    if user_profile.profile_pic:
                        user_profile.profile_pic.delete(save=False)
                user.save()
                user_profile.save()
                return redirect('profile')
    else:
        return redirect('login')
    return render(request, 'update.html', {'user': user, 'user_profile': user_profile})


def about(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
    else:
        return redirect('login')
    return render(request, 'about.html', {'user': user, 'user_profile': user_profile})


def purchased_history(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
    else:
        return redirect('login')
    return render(request, 'purchased_history.html', {'user': user})


def side_nav(request):
    return render(request, 'side_nav.html')


def add_product(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if request.method == 'POST':
            product_id = request.POST['product_id']
            product_name = request.POST['product_name']
            product_description = request.POST['product_description']
            product_price = request.POST['product_price']
            product_rating = request.POST['product_rating']
            product_image = request.FILES['product_image']
            product = Product.objects.create(
                user=user,
                product_id=product_id,
                product_name=product_name,
                product_description=product_description,
                product_price=product_price,
                product_rating=product_rating,
                product_image=product_image
            )
            print(product)
    else:
        return redirect('login')
    return render(request, 'add_product.html', {'user': user, 'user_profile': user_profile})


def details(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.roles in ('Seller', 'Admin'):
            if request.GET.get('type') == 'buyer':
                page_type = 'buyer'
            else:
                page_type = 'seller'
    else:
        return redirect('login')
    return render(request, 'details.html', {'user': user, 'user_profile': user_profile, 'page_type': page_type})


def products_hist(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        products = Product.objects.all()
        if user_profile.roles in ('Seller', 'Admin'):
            if request.GET.get('type') == 'ava_products':
                page_type = 'ava_products'
            else:
                page_type = 'pur_products'
        return render(request, 'products_hist.html',
                      {'user': user, 'user_profile': user_profile, 'page_type': page_type, 'products': products})


def update_seller(request):
    return render(request, 'update_seller.html')


def profile_seller(request):
    return render(request, 'profile_seller.html')


def verification(request):
    # Retrieve user and verification link from session
    user_id = request.session.get('user_id')
    verification_link = request.session.get('verification_link')

    # Get the user object using the user_id
    user = User.objects.get(id=user_id)

    # Render the verification template with user and verification link
    return render(request, 'verification.html', {'user': user, 'verification_link': verification_link})


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


def profile(request):
    if 'user' in request.session:
        User = get_user_model()
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
    else:
        return redirect('login')
    return render(request, 'profile.html', {'user_profile': user_profile, 'user': user})

