from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from myapp.models import User
from .login import LoginView

class Register:
    def __init__(self, request):
        self.request = request
        self.context = {'active_register': 'active', 'height': True}
        
    
    class FormData:
        def __init__(self, username=None, password1=None, password2=None, email=None):
            self.username = username
            self.password1 = password1
            self.password2 = password2
            self.email = email
        
        def __str__(self):
            return 'Username: {self.username}, Password1: {self.password1}, \
                    Password2: {self.password2}, email: {self.email}'.format(self=self)

    def response(self):
        if self.is_user_logged_on():
            return self.redirect_to_index()
        if self.request.method == 'POST':
            return self.post()
        else:
            return self.get()

    def get(self):
        return render(self.request, 'myapp/register.html', self.context)

    def post(self):
        input_data = self.get_input_data()
        if not self.is_password_correctly_typed(input_data):
            return self.password_is_mistyped()
        if self.is_all_input_data_supplied(input_data):
            if not self.is_username_long_enough(input_data.username):
                return self.username_is_short()
            if not self.is_password_long_enough(input_data.password1):
                return self.password_is_short()
            if not self.is_email_valid(input_data.email):
                return self.email_not_valid()
            if self.is_username_exists(input_data.username):
                return self.username_exists()
            if self.is_email_exists(input_data.email):
                return self.email_exists()
            return self.register_the_new_user(input_data)
        else:
            return self.required_data_not_fully_supplied()

    def register_the_new_user(self, input_data):
        self.save_to_database(input_data)
        return LoginView.login_success(self.request, input_data)

    def email_not_valid(self):
        self.context['email_not_valid'] = True
        return render(self.request, 'myapp/register.html', self.context)

    def email_exists(self):
        self.context['email_exists'] = True
        return render(self.request, 'myapp/register.html', self.context)

    def username_exists(self):
        self.context['username_exists'] = True
        return render(self.request, 'myapp/register.html', self.context)

    def password_is_mistyped(self):
        self.context['different'] = True
        return render(self.request, 'myapp/register.html', self.context)
    
    def required_data_not_fully_supplied(self):
        self.context['empty'] = True
        return render(self.request, 'myapp/register.html', self.context)
    
    def username_is_short(self):
        self.context['username_short'] = True
        return render(self.request, 'myapp/register.html', self.context)

    def password_is_short(self):
        self.context['password_short'] = True
        return render(self.request, 'myapp/register.html', self.context)

    def get_input_data(self):
        request = self.request
        username = request.POST.get('username').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()
        email = request.POST.get('email').strip()
        input_data = Register.FormData(username, password1, password2, email)
        return input_data
    
    def is_password_correctly_typed(self, input_data):
        password1 = input_data.password1
        password2 = input_data.password2
        if password1 == password2:
            return True
        return False
    
    def is_all_input_data_supplied(self, input_data):
        username = input_data.username
        password1 = input_data.password1
        password2 = input_data.password2
        email = input_data.email
        if username and password1 and password2 and email:
            return True
        return False

    def is_username_long_enough(self, username):
        if len(username) > 2:
            return True
        return False
    
    def is_password_long_enough(self, password):
        if len(password) > 3:
            return True
        return False
    
    def is_username_exists(self, username):
        try:
            record = User.objects.get(username=username)
            return True
        except User.DoesNotExist:
            return False

    def is_email_exists(self, email):
        try:
            record = User.objects.get(email=email)
            return True
        except User.DoesNotExist:
            return False
    
    def is_email_valid(self, email):
        try:
            validate_email(email)
            return True
        except ValidationError:
            return False
        
    def save_to_database(self, input_data):
        username = input_data.username
        password = input_data.password1
        email = input_data.email
        record = User(username=username, password=password, email=email)
        record.save()

    def is_user_logged_on(self):
        return LoginView.is_user_logged_on(self.request, self.context)
    
    def redirect_to_index(self):
        return HttpResponseRedirect(reverse('index'))    
