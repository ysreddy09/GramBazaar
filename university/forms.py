from django import forms


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=(('customer', 'Customer'), ('seller', 'Seller')))
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)


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
        attrs={'pattern': '^91\d{10}$', 'title': 'Please enter 10 digits with 91 country code'}))
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), label='Address', required=True)
