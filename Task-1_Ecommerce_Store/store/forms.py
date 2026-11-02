from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Order


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Create a password (min 6 chars)'}),
        min_length=6,
        label='Password'
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Confirm your password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Enter a unique username'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'Enter your email address'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email address already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please try again.")

        return cleaned_data


class UserLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Password'}),
        label='Password'
    )


class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('Credit/Debit Card (Simulated)', 'Credit / Debit Card (Instant Simulation)'),
        ('PayPal (Simulated)', 'PayPal (Simulated Express Checkout)'),
        ('Cash on Delivery', 'Cash on Delivery (Pay upon arrival)'),
    ]

    payment_method = forms.ChoiceField(
        choices=PAYMENT_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'payment-radio'}),
        initial='Credit/Debit Card (Simulated)'
    )

    # Simulated credit card fields for realistic experience
    card_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': '•••• •••• •••• ••••', 'maxlength': '19', 'id': 'card_number'})
    )
    card_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name on Card', 'id': 'card_name'})
    )
    card_expiry = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'MM / YY', 'maxlength': '7', 'id': 'card_expiry'})
    )
    card_cvv = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'CVV', 'maxlength': '4', 'id': 'card_cvv'})
    )

    class Meta:
        model = Order
        fields = [
            'full_name', 'email', 'phone', 'address', 'city', 'state', 'postal_code',
            'country', 'payment_method', 'notes'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'John Doe'}),
            'email': forms.EmailInput(attrs={'class': 'form-input', 'placeholder': 'john@example.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '+1 (555) 234-5678'}),
            'address': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '123 Market Street, Apt 4B'}),
            'city': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'San Francisco'}),
            'state': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'California'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-input', 'placeholder': '94103'}),
            'country': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'United States'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Special delivery instructions or gate code (optional)'}),
        }
