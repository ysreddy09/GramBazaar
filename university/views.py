from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import SignUpForm
from .forms import LoginForm


def index(request):
    return render(request, 'index.html')


# views.py


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()

    if form.errors:
        print(form.errors)
    return render(request, 'signup.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                error_message = "Invalid email or password. Please try again."
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home(request):
    return render(request, 'home.html')


def navbar(request):
    return render(request, 'navbar.html')


def home_page_slider(request):
    return render(request, 'home_page_slider.html')


def products(request):
    return render(request, 'products.html')


def add_to_cart(request):
    return render(request, 'add_to_cart.html')


def profile(request):
    return render(request, 'profile.html')


def footer(request):
    return render(request, 'footer.html')


def update(request):
    return render(request, 'update.html')


def about(request):
    return render(request, 'about.html')


def purchased_history(request):
    return render(request, 'purchased_history')
