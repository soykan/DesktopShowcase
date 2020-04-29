from django.views.generic import TemplateView
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from myapp.models import User
from .login import LoginView
from datetime import datetime
import time
import json

class RegisterView(TemplateView):
    template_name = 'myapp/register.html'
    """
    def quirky_randomizer():
        ms = datetime.now().strftime("%f")
        #print("Microsecond: " + ms)
        codes = []
        count = 0

        for i in range(0, int(len(ms)/2)):
            val1 = ms[i]
            val2 = ms[len(ms) - (i + 1)]
            if i % 2 != 0:
                c1 = val1 + val2
            else:
                c1 = val2 + val1
            c21 = abs(int(val1) - int(val2))
            c22 = abs(int(val1) + int(val2)) % 10
            c2 = str(c21) + str(c22)
            codes.append(c1)
            codes.append(c2)
            count = abs(int(codes[0]) - int(codes[len(codes) - 1])) % 3

        codes = '{0}'.format(str(count) * count).join(codes)
        return codes
    """
    def post(self, request):
        input_data = self.get_input_data()
        context = self.get_context_data()
        if not self.is_password_correctly_typed(input_data):
            return self.password_is_mistyped(context) 
        if self.is_all_input_data_supplied(input_data):
            if not self.is_username_long_enough(input_data.username):
                return self.username_is_short(context)
            if not self.is_password_long_enough(input_data.password1):
                return self.password_is_short(context)
            if not self.is_email_valid(input_data.email):
                return self.email_not_valid(context) 
            if self.is_username_exists(input_data.username):
                return self.username_exists(context) 
            if self.is_email_exists(input_data.email):
                return self.email_exists(context) 
            return self.register_the_new_user(input_data)
        else:
            return self.required_data_not_fully_supplied()

    def get(self, request):
        context = self.get_context_data()
        if not LoginView.is_user_logged_on(request, context):
            return render(request, self.template_name, context)
        return self.redirect_to_index()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_register'] = 'active'
        context['height'] = True
        return context

    def redirect_to_index(self):
        return HttpResponseRedirect(reverse('index'))    

    def register_the_new_user(self, input_data):
        self.request.session['input_data'] = input_data.toJSON()
        
        return HttpResponseRedirect(reverse('price'))
        #self.save_to_database(input_data)
        #return LoginView.login_success(self.request, input_data)
    


    def email_not_valid(self, context):
        context['email_not_valid'] = True
        return render(self.request, 'myapp/register.html', context)

    def email_exists(self, context):
        context['email_exists'] = True
        return render(self.request, 'myapp/register.html', context)

    def username_exists(self, context):
        context['username_exists'] = True
        return render(self.request, 'myapp/register.html', context)

    def password_is_mistyped(self, context):
        context['different'] = True
        return render(self.request, 'myapp/register.html', context)
    
    def required_data_not_fully_supplied(self, context):
        context['empty'] = True
        return render(self.request, 'myapp/register.html', context)
    
    def username_is_short(self, context):
        context['username_short'] = True
        return render(self.request, 'myapp/register.html', context)

    def password_is_short(self, context):
        context['password_short'] = True
        return render(self.request, 'myapp/register.html', context)

    def get_input_data(self):
        request = self.request
        username = request.POST.get('username').strip()
        password1 = request.POST.get('password1').strip()
        password2 = request.POST.get('password2').strip()
        email = request.POST.get('email').strip()
        input_data = RegisterView.FormData(username, password1, password2, email)
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
        
    def save_to_database(input_data):
        username = input_data.username
        password = input_data.password1
        email = input_data.email
        record = User(username=username, password=password, email=email)
        record.save()

    class FormData:
        def __init__(self, username=None, password1=None, password2=None, email=None):
            self.username = username
            self.password1 = password1
            self.password2 = password2
            self.email = email
        
        def __str__(self):
            return 'Username: {self.username}, Password1: {self.password1}, \
                    Password2: {self.password2}, email: {self.email}'.format(self=self)
        
        def toJSON(self):
            return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)