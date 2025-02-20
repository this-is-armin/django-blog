from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views import View

from .forms import SignUnForm, SignInForm, UpdateProfileForm


class SignUpView(View):
    template_name = 'account/signup.html'
    form_class = SignUnForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})
    
    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = User.objects.create_user(username=cd['username'], email=cd['email'], password=cd['password1'])
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'You have successfully signed up.', 'info')
            return redirect('account:signin')
        return render(request, self.template_name, {'form' : form})


class SignInView(View):
    template_name = 'account/signin.html'
    form_class = SignInForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form' : form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'You have successfully signed in.', 'info')
                return redirect('home')
            messages.error(request, 'Username or Password is wrong.', 'danger')
            return redirect('account:signin')
        return render(request, self.template_name, {'form' : form})


def signout_view(request):
    if not request.user.is_authenticated:
        return redirect('home')
    logout(request)
    messages.success(request, 'You have successfully signed out.', 'info')
    return redirect('home')


class ProfileView(View):
    template_name = 'account/profile.html'

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, **kwargs):
        user = self.user_instance
        return render(request, self.template_name, {'user' : user})


def delete_account_view(request, username):
    user = get_object_or_404(User, username=username)
    if not request.user.is_authenticated:
        return redirect('home')
    if request.user != user:
        messages.error(request, 'You can`t delete this user.', 'danger')
        return redirect('account:profile', user.username)
    user.delete()
    messages.success(request, 'You have successfully deleted the account.', 'info')
    return redirect('home')


class UpdateProfileView(View):
    template_name = 'account/update.html'
    form_class = UpdateProfileForm

    def setup(self, request, *args, **kwargs):
        self.user_instance = get_object_or_404(User, username=kwargs['username'])
        return super().setup(request, *args, **kwargs)
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('home')
        if request.user != self.user_instance:
            messages.error(request, 'You can`t update the user profile.', 'danger')
            return redirect('account:profile', self.user_instance.username)
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, **kwargs):
        user = self.user_instance
        INITIAL = {'email':user.email, 'first_name':user.first_name, 'last_name':user.last_name}
        form = self.form_class(initial=INITIAL)

        return render(request, self.template_name, {'user':user, 'form':form})
    
    def post(self, request, **kwargs):
        form = self.form_class(request.POST)
        user = self.user_instance

        if form.is_valid():
            cd = form.cleaned_data
            user.email = cd['email']
            user.first_name = cd['first_name']
            user.last_name = cd['last_name']
            user.save()
            messages.success(request, 'You have successfully updated the profile.', 'info')
            return redirect('account:profile', user.username)
        return render(request, self.template_name, {'user':user, 'form':form})