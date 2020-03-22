from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from myapp.models import User

class Login:
    def __init__(self, request):
        self.request = request
        self.context = {'active_login': 'active', 'height': True}

    class FormData:
        def __init__(self, username=None, password=None):
            self.username = username
            self.password = password

        def __str__(self):
            return 'Username: {self.username}, Password: {self.password}'.format(self=self)
    
    def response(self):
        if self.is_user_logged_on(self.request, self.context):
            return self.redirect_to_index()
        if self.request.method == 'POST':
            return self.post()
        else:
            return self.get()
    
    def post(self):
        input_data = self.get_input_data()
        if self.check_login_credentials(input_data):
            return self.login_success(self.request, input_data)
        else:
            return self.incorrect_login_credentials()

    def get(self):
        return render(self.request, 'myapp/login.html', self.context)
    
    def incorrect_login_credentials(self):
        self.context['incorrect'] = True
        return render(self.request, 'myapp/login.html', self.context)     

    def get_input_data(self):
        username = self.request.POST.get('username').strip()
        password = self.request.POST.get('password').strip()
        input_data = Login.FormData(username, password)
        return input_data

    def redirect_to_index(self):
        return HttpResponseRedirect(reverse('index'))    

    def check_login_credentials(self, input_data):
        username = input_data.username
        password = input_data.password
        try:
            data = User.objects.get(username=username, password=password)
            return True
        except User.DoesNotExist:
            return False  
    
    @classmethod
    def login_success(cls, request, input_data):
        username = input_data.username
        request.session['user_id'] = cls.get_user_id(username)
        return HttpResponseRedirect(reverse('index'))  

    @classmethod
    def get_user_id(cls, username):
        try:
            user = User.objects.get(username=username)
            return user.id
        except User.DoesNotExist:
            pass
    
    @classmethod
    def is_user_logged_on(cls, request, context):
        if 'user_id' not in request.session:
            context['not_logged_on'] = True
            return False
        return True      
