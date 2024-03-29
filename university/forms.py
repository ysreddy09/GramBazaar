from django import forms
from .models import Product

class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    roles = forms.ChoiceField(choices=(('Customer', 'Customer'), ('Seller', 'Seller')))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(label="email", required=True)
    # phone_number = forms.CharField(label="phone_number", required=True)

class ResetPasswordForm(forms.Form):
    password = forms.CharField(label="Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(label="Confirm Password", widget=forms.PasswordInput)
class OTPForm(forms.Form):
    digit1 = forms.CharField(max_length=1,label="digit1")
    digit2 = forms.CharField(max_length=1,label="digit2")
    digit3 = forms.CharField(max_length=1,label="digit3")
    digit4 = forms.CharField(max_length=1,label="digit4")

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class ProfileUpdateForm(forms.Form):
    profile_image = forms.ImageField(label='Profile Picture', required=False)
    first_name = forms.CharField(max_length=100, label='First Name', required=True)
    last_name = forms.CharField(max_length=100, label='Last Name', required=True)
    postal_code = forms.CharField(max_length=6, label='Postal Code', required=True,
                                  widget=forms.TextInput(attrs={'pattern': '\d{6}', 'title': 'Please enter 6 digits'}))
    phone_number = forms.CharField(max_length=12, label='Phone Number', required=True, widget=forms.TextInput(
        attrs={'pattern': '\d{10}', 'title': 'Please enter 10 digits with 91 country code'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Address', required=True)


class ProductForm(forms.Form):
    product_id = forms.IntegerField(label='Product ID', required=True)
    product_name = forms.CharField(max_length=255, label='Product Name', required=True)
    product_description = forms.CharField(widget=forms.Textarea, label='Product Description', required=True)
    product_price = forms.DecimalField(label='Product Price', required=True)
    product_rating = forms.DecimalField(label='Product Rating', min_value=0, max_value=5, required=True)
    product_image = forms.ImageField(label='Product Image', required=True)
