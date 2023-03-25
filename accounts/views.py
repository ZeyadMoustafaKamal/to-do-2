from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.views.generic import FormView,RedirectView,TemplateView
from django.urls import reverse_lazy, reverse
import random
import string
from .forms import SignUpForm, LoginForm
from .models import CustomUser
from django.http import HttpResponseRedirect
from django.conf import settings
import hashlib

def get_random_code():
    slug = ''.join(random.choice(string.ascii_letters) for x in range(25))
    if CustomUser.objects.filter(code=slug).exists():
        slug = get_random_code()
    return slug

def send_verify_link(email,code ,request):
    user = CustomUser.objects.filter(email=email).first()
    # This will n't generate the code using the get_random_code funtion because sometimes I want to send a code and then get that code
    # but this shows an error as the code isn't beind changed in the database yet but it sent to the user so I will generate the random code
    # and I will pass it into this function to be able to use it later
    if user is not None:
        hashed_code = hashlib.sha256(code.encode()).hexdigest()
        user.code = hashed_code
        user.save()
        subject = 'Here is the link to verify your E-mail'
        link = request.build_absolute_uri( reverse('verify', args=[code]) )
        message = f'Hello verify your E-mail using this link {link}'
        send_mail(from_email=settings.DEFAULT_FROM_EMAIL, subject=subject, message=message, recipient_list=[email])

class SignUp(FormView):

    form_class = SignUpForm
    template_name = 'accounts/signup.html'
    def dispatch(self, request,*args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super().dispatch(request, *args, **kwargs)
    def form_valid(self, form):
        # First create the user
        user = form.save(commit=False)
        user.set_password(form.cleaned_data.get('password'))
        user.save()  # Save the user object before sending the verification link
        # Send the verification url
        code = get_random_code()
        send_verify_link(form.cleaned_data['email'],code,self.request)
        return HttpResponseRedirect(reverse('verify_email',args=[CustomUser.objects.get(email=form.cleaned_data['email']).code]))

    def form_invalid(self, form):
        if 'email' in form.errors:
            messages.error(self.request, form.errors['email'][0])
        if 'password' in form.errors:
            messages.error(self.request, form.errors['password'][0])
        return super().form_invalid(form)
    def post(self, request, *args: str, **kwargs):
        return super().post(request, *args, **kwargs)

class Login(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = reverse_lazy('index')
    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = auth.authenticate(email=email,password=password)
        auth.login(self.request,user)
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,'Invalid email or password')
        return super().form_invalid(form)
    

class VerifyEmail(TemplateView):
    template_name = 'accounts/email_verify.html'
    def post(self, request,*args,**kwargs):
        user = CustomUser.objects.filter(code=kwargs.get('code')).first()
        code = get_random_code()
        if user: 
            send_verify_link(user.email,code,request)
        return redirect(reverse('verify_email',args=[hashlib.sha256(code.encode()).hexdigest()]))

def logout(request):
    # This is a simple function just log the user out
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('index')


class Verify(RedirectView):
    pattern_name = 'index'
    query_string = False
    def get_redirect_url(self, *args, **kwargs):
        hashed_code = hashlib.sha256(kwargs.get('code').encode()).hexdigest()
        print(hashed_code)
        user_to_verify = CustomUser.objects.filter(code=hashed_code).first()
        print(user_to_verify)
        if user_to_verify and user_to_verify.validate_code(hashed_code) and user_to_verify.code != '0':
            auth.login(self.request,user_to_verify)
            user_to_verify.code = '0'
            user_to_verify.verified = True
            user_to_verify.save()
            messages.success(self.request,'Successfully verified your account')
        else:
            messages.error(self.request,'Error while checking the link !! The link may be incorrect of invlid')
        return reverse('index')