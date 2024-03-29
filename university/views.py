import random
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, get_user_model, update_session_auth_hash
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .models import UserProfile, Product, PurchaseHistory
from .forms import SignUpForm, LoginForm, ProfileUpdateForm, ForgotPasswordForm, OTPForm, ResetPasswordForm
import io
from django.http import FileResponse, HttpResponse, JsonResponse
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
    request.session['user'] = user.username
    print(user)
    request.session['verification_link'] = verification_link
    print(verification_link)
    return redirect('resend')


def resend(request):
    if request.method == 'POST':
        username = request.session.get('user')
        print(username)
        verification_link = request.session.get('verification_link')
        if username and verification_link:
            try:
                print('hello')
                user = User.objects.get(username=username)
                print(verification_link)
                send_verification_email(request, user, verification_link)
                return HttpResponse("Email Resent Successfully")
            except User.DoesNotExist:
                return HttpResponse("User does not exist.")
        else:
            return HttpResponse("Failed to resend Email")
    return render(request, 'resend.html')


def send_otp_mail(request, user, text):
    current_site = get_current_site(request)
    subject = 'OTP for forgot password request'
    message = f'Hello {user.username},\n\n' \
              f'Do not Share OTP to anyone:\n\n' \
              f'Your One Time Password is {text}\n\n' \
              f'Thank you,\n' \
              f'The Example Team\n\n' \
              f'This is an automated message, please do not reply.'

    send_mail(subject, message, 'yaswanth2813@gmail.com', [user.email])


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
            return redirect('resend')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


session_email = None


def forgot(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            # Process the form data, such as sending an OTP
            # For demonstration purposes, let's just print the data
            email = form.cleaned_data.get('email')
            user = get_object_or_404(User, email=email)
            request.session['email'] = email
            # session_user = request.session.get('user')
            if user is None:
                print("No User")
            if user is not None:
                otp = ''.join([str(random.randint(0, 9)) for _ in range(4)])
                request.session['otp'] = otp
                send_otp_mail(request, user, otp)
                return render(request, 'verify_otp.html', {'email': email})

    else:
        form = ForgotPasswordForm()

    return render(request, 'forgot.html', {'form': form})


def verify_otp(request):
    email = request.session.get('email', None)
    print(email)
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            # Get cleaned data for each digit
            digit1 = form.cleaned_data['digit1']
            digit2 = form.cleaned_data['digit2']
            digit3 = form.cleaned_data['digit3']
            digit4 = form.cleaned_data['digit4']

            # Combine digits to form OTP
            otp = digit1 + digit2 + digit3 + digit4
            session_otp = request.session.get('otp')
            print(session_otp)
            if otp == session_otp:
                del request.session['otp']

                return render(request, 'reset_password.html', {'email': email})
            else:
                return HttpResponse('Invalid OTP. Please try again.')

        else:
            # If the form is not valid, re-render the form with errors
            return render(request, 'verify_otp.html', {'form': form})
    else:
        form = OTPForm()
    return render(request, 'verify_otp.html', {'form': form})


def reset_password(request):
    form = ResetPasswordForm()
    email = request.session.get('email', None)
    print(email)
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']
            user = User.objects.get(email=email)
            # print(email)
            # Update the user's password
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
            else:
                return render(request, 'reset_password.html', {'form': form})
            # Update the user's password

            # Keep the user logged in after changing password
            update_session_auth_hash(request, user)

            # Optionally, you can add a success message
            messages.success(request, 'Your password has been successfully reset.')

            # Redirect the user to a success page or any desired page
            return redirect('login')  # Replace 'success_page' with your URL name
    return render(request, 'reset_password.html', {'form': form})


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
    if 'user' in request.session and request.method == 'POST':
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)

        if user.is_authenticated:
            product_id = request.POST.get('product_id')
            print(product_id)

            product = Product.objects.get(product_id=product_id)
            print(product.product_id)
            seller_name = product.seller_name
            customer_name = user.first_name
            purchase_history = PurchaseHistory.objects.create(
                user=user,
                product=product,
                seller_name=seller_name,
                customer_name=customer_name
            )

            messages.success(request, 'Product added to cart!')
            return redirect('home')
        else:
            return redirect('login')
    elif 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        products = Product.objects.all()
        return render(request, 'home.html', {'user': user, 'user_profile': user_profile, 'products': products})
    else:
        return redirect('login')


def navbar(request):
    return render(request, 'navbar.html')


def home_page_slider(request):
    return render(request, 'home_page_slider.html')


def products(request):
    return render(request, 'products.html')


def purchased_history(request):
    products = []
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        purchase_history = PurchaseHistory.objects.filter(user=user)

        for history in purchase_history:
            products.append(history.product)
    else:
        return redirect('login')
    return render(request, 'purchased_history.html',
                  {'user': user, 'products': products, 'purchase_history': purchase_history})


def add_to_cart(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        purchased_history = PurchaseHistory.objects.filter(user=user)
    else:
        return redirect('login')
    return render(request, 'add_to_cart.html',
                  {'user': user, 'user_profile': user_profile, 'purchased_history': purchased_history})


def profile(request):
    if 'user' in request.session:
        User = get_user_model()
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        print(user_profile.profile_pic)
    else:
        return redirect('login')
    return render(request, 'profile.html', {'user_profile': user_profile, 'user': user})


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
                if 'profile_pic' in request.FILES:
                    user_profile.profile_pic = request.FILES['profile_pic']
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
            seller_name = user.first_name

            product = Product.objects.create(
                user=user,
                product_id=product_id,
                product_name=product_name,
                product_description=product_description,
                product_price=product_price,
                product_rating=product_rating,
                product_image=product_image,
                seller_name=seller_name,
            )
    else:
        return redirect('login')
    return render(request, 'add_product.html', {'user': user, 'user_profile': user_profile})


def details(request):
    if 'user' in request.session:
        username = request.session.get('user')
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        if user_profile.roles == 'Seller':
            seller_details = UserProfile.objects.filter(roles='Seller').select_related('user')
    else:
        return redirect('login')
    return render(request, 'details.html',
                  {'user': user, 'user_profile': user_profile, 'seller_details': seller_details})


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
    return render(request, 'products_hist.html')


def update_seller(request):
    return render(request, 'update_seller.html')


def profile_seller(request):
    return render(request, 'profile_seller.html')


def verification(request):
    # Retrieve user and verification link from session
    user_id = request.session.get('user')
    verification_link = request.session.get('verification_link')

    # Get the user object using the user_id
    user = User.objects.get(username=user_id)

    # Render the verification template with user and verification link
    return render(request, 'resend.html', {'user': user, 'verification_link': verification_link})


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

    # Get the user from the session
    username = request.session.get('user')
    user = User.objects.get(username=username)

    # Retrieve the user's purchase history
    prods = PurchaseHistory.objects.filter(user=user)

    # Initialize variables for subtotal calculation
    subtotal = 0
    y = 680

    # Iterate over each purchased product
    for product in prods:
        # Retrieve product details
        title = product.product.product_name
        price = product.product.product_price
        quantity = product.quantity
        total = float(price) * quantity
        subtotal += total

        # Draw product details on the PDF
        y -= 20
        p.drawString(100, y, title)
        p.drawString(350, y, str(price))
        p.drawString(450, y, str(quantity))
        p.drawString(550, y, "${:.2f}".format(total))

    # Calculate tax, shipping, and grand total
    tax_rate = 0.05
    tax = subtotal * tax_rate
    shipping = 15.00
    grand_total = subtotal + tax + shipping

    # Draw subtotal, tax, shipping, and grand total
    p.drawString(100, y - 30, "Subtotal: ${:.2f}".format(subtotal))
    p.drawString(100, y - 50, "Tax (5%): ${:.2f}".format(tax))
    p.drawString(100, y - 70, "Shipping: ${:.2f}".format(shipping))
    p.drawString(100, y - 90, "Grand Total: ${:.2f}".format(grand_total))

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Set the file pointer back to the beginning of the buffer.
    buffer.seek(0)

    # Return the PDF as a FileResponse.
    return FileResponse(buffer, as_attachment=True, filename="shopping_cart.pdf")
