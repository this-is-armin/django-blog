from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class SignUnForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter username...', 'class':'form-control'}))
    email = forms.EmailField(label='', max_length=200, widget=forms.TextInput(attrs={'placeholder':'Enter email...', 'class':'form-control'}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter first name...', 'class':'form-control'}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter last name...', 'class':'form-control'}))
    password1 = forms.CharField(label='', max_length=180, widget=forms.PasswordInput(attrs={'placeholder':'Enter password...', 'class':'form-control'}))
    password2 = forms.CharField(label='', max_length=180, widget=forms.PasswordInput(attrs={'placeholder':'Enter password(Confirm)...', 'class':'form-control'}))

    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)

        invalid_chars = ['<', '>', '(', ')', '{', '}', '[', ']', '\\', '/', '|', '.', ',', '?', '-', '=', '+', '!', '`', '~', '@', '#', '$', '%', '^', '&', '*', ';', ':', '"', "'"]
        for char in invalid_chars:
            if char in username:
                raise ValidationError('Your username have invalid characters..!')

        if user.exists():
            raise ValidationError('This username already exists.')
        return username
    
    def clean(self):
        cd = self.cleaned_data
        p1 = cd.get('password1')
        p2 = cd.get('password2')

        if p1 and p2 and p1 != p2:
            raise ValidationError('Passwords don`t match. Try again.')
        
        if len(p1) < 8 or len(p2) < 8:
            raise ValidationError('The length of passwords must be 8 or more characters.')


class SignInForm(forms.Form):
    username = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter username...', 'class':'form-control'}))
    password = forms.CharField(label='', max_length=180, widget=forms.PasswordInput(attrs={'placeholder':'Enter password...', 'class':'form-control'}))
    

class UpdateProfileForm(forms.Form):
    email = forms.EmailField(label='', max_length=200, widget=forms.TextInput(attrs={'placeholder':'Enter email...', 'class':'form-control'}))
    first_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter first name...', 'class':'form-control'}))
    last_name = forms.CharField(label='', max_length=100, widget=forms.TextInput(attrs={'placeholder':'Enter last name...', 'class':'form-control'}))
    
