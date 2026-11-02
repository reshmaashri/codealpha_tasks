from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import UserProfile, Post, Comment


ALLOWED_IMAGE_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif']
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


def validate_image_file(file):
    """Ensure uploaded file is an image and does not exceed 5MB."""
    if not file:
        return
    if file.size > MAX_IMAGE_SIZE:
        raise ValidationError(f"Image size must not exceed 5MB. Current size is {file.size / (1024 * 1024):.1f}MB.")
    
    # Check content type if available
    content_type = getattr(file, 'content_type', None)
    if content_type and content_type.lower() not in ALLOWED_IMAGE_TYPES:
        raise ValidationError("Unsupported file format. Please upload JPG, PNG, WebP, or GIF image.")


class UserRegistrationForm(forms.ModelForm):
    """User registration form with profile details."""
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'First Name',
            'autocomplete': 'given-name'
        })
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Last Name',
            'autocomplete': 'family-name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'name@example.com',
            'autocomplete': 'email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Create strong password (min 6 chars)',
            'autocomplete': 'new-password'
        }),
        min_length=6
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Repeat your password',
            'autocomplete': 'new-password'
        }),
        min_length=6
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input resize-none',
            'rows': 2,
            'placeholder': 'Tell the community about yourself (optional)'
        }),
        max_length=500
    )
    avatar = forms.ImageField(
        required=False,
        validators=[validate_image_file],
        widget=forms.FileInput(attrs={
            'class': 'file-input-hidden',
            'accept': 'image/*'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'username (letters, numbers, _)',
                'autocomplete': 'username'
            })
        }

    def clean_username(self):
        username = self.cleaned_data.get('username', '').strip()
        if not username:
            raise ValidationError("Username is required.")
        if len(username) < 3:
            raise ValidationError("Username must be at least 3 characters.")
        if not username.replace('_', '').isalnum():
            raise ValidationError("Username can only contain letters, numbers, and underscores.")
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError("This username is already taken. Please choose another.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("Email address is required.")
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match. Please verify.")
        return cleaned_data


class UserLoginForm(forms.Form):
    """User login form supporting username or email."""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Username or Email address',
            'autocomplete': 'username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your password',
            'autocomplete': 'current-password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-checkbox'})
    )


class PostCreateForm(forms.ModelForm):
    """Form to create a new post with image and caption."""
    image = forms.ImageField(
        required=True,
        validators=[validate_image_file],
        widget=forms.FileInput(attrs={
            'class': 'file-input-hidden',
            'accept': 'image/*',
            'id': 'post-image-input'
        })
    )
    caption = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input resize-none w-full',
            'rows': 3,
            'placeholder': "What's on your mind? Share thoughts, moments, or #hashtags...",
            'id': 'post-caption-input'
        }),
        max_length=2200
    )

    class Meta:
        model = Post
        fields = ['image', 'caption']


class PostEditForm(forms.ModelForm):
    """Form to edit an existing post's caption and optional image replacement."""
    image = forms.ImageField(
        required=False,
        validators=[validate_image_file],
        widget=forms.FileInput(attrs={
            'class': 'file-input-hidden',
            'accept': 'image/*',
            'id': 'edit-post-image-input'
        })
    )
    caption = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input resize-none w-full',
            'rows': 3,
            'placeholder': "Edit your post caption...",
            'id': 'edit-post-caption-input'
        }),
        max_length=2200
    )

    class Meta:
        model = Post
        fields = ['caption', 'image']


class ProfileEditForm(forms.ModelForm):
    """Form to edit user profile details and avatar."""
    first_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'First Name'})
    )
    last_name = forms.CharField(
        max_length=50,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Last Name'})
    )
    avatar = forms.ImageField(
        required=False,
        validators=[validate_image_file],
        widget=forms.FileInput(attrs={
            'class': 'file-input-hidden',
            'accept': 'image/*',
            'id': 'profile-avatar-input'
        })
    )
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-input resize-none',
            'rows': 3,
            'placeholder': 'Add a bio to your profile...'
        }),
        max_length=500
    )
    location = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'City, Country'}),
        max_length=100
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://yourwebsite.com'}),
        max_length=200
    )

    class Meta:
        model = UserProfile
        fields = ['avatar', 'bio', 'location', 'website']


class CommentForm(forms.ModelForm):
    """Quick comment submission form."""
    text = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'comment-input',
            'placeholder': 'Add a comment...',
            'autocomplete': 'off'
        }),
        max_length=1000
    )

    class Meta:
        model = Comment
        fields = ['text']
