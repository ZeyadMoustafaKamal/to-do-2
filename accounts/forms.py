from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='E-mail',error_messages={'required':'You have to enter the E-mail'})
    password = forms.CharField(widget=forms.PasswordInput(), label='Password',error_messages={'required':'You have to enter the password'})
    password1 = forms.CharField(required=False)
    password2 = forms.CharField(required=False)
    class Meta:
        model = CustomUser
        fields = ('email','password')
    def clean_email(self):
        email = self.cleaned_data['email']
        user = CustomUser.objects.filter(email=email)
        if user.exists():
            if user.filter(verified=True).exists():
                raise forms.ValidationError('This E-mail is already exists')
            else:
                user.delete()
        return email
    def clean_password(self):
        password = self.cleaned_data['password']
        if len(password) < 8:
            raise forms.ValidationError('The password should be at least 8 characters')
        return password


class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput(),label='Password')
    class Meta:
        model = CustomUser
        fields = ('email','password')
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        if email and password:
            user = authenticate(email=email,password=password)
            # Here I check if the user doen't exists or the user has an account but didn't verified it yet
            # in the two cases I will raise an error I willn't allow user to login to the account so the user
            # will have to create an account and in the form above if the account is exists but not verified the account will be deleted
            if not user or not user.verified:
                raise forms.ValidationError('Invalid E-mail or password')

        return cleaned_data
        
