from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Q


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter your email',
            'style': 'width: 100%; padding: 8px; box-sizing: border-box;',
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'style': 'width: 100%; padding: 8px; box-sizing: border-box;',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['password1', 'password2']:
            if field_name in self.fields:
                self.fields[field_name].widget.attrs.update({
                    'placeholder': 'Enter password' if field_name == 'password1' else 'Confirm password',
                    'style': 'width: 100%; padding: 8px; box-sizing: border-box;',
                })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="Username or Email",
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username or email',
            'style': 'width: 100%; padding: 8px; box-sizing: border-box;',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter password',
            'style': 'width: 100%; padding: 8px; box-sizing: border-box;',
        })
    )

    def __init__(self, request=None, *args, **kwargs):
        if request is not None and not hasattr(request, 'user') and not hasattr(request, 'META'):
            kwargs['data'] = request
            request = None
        self.request = request
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username_or_email and password:
            # Check if user exists by username OR email
            user_obj = User.objects.filter(
                Q(username__iexact=username_or_email) | Q(email__iexact=username_or_email)
            ).first()

            if not user_obj:
                self.add_error('username', 'Account not found.')
                return cleaned_data

            # User found, now check password
            user = authenticate(self.request, username=user_obj.username, password=password)
            if user is None:
                self.add_error('password', 'Incorrect password.')
                return cleaned_data

            if not user.is_active:
                self.add_error('username', 'This account is inactive.')
                return cleaned_data

            self.user_cache = user

        return cleaned_data

    def get_user(self):
        return self.user_cache
