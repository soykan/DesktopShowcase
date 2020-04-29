from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from .myviews.register import RegisterView
from .myviews.login import LoginView
from .myviews.about import AboutView
from .myviews.index import IndexView
from .myviews.top_post_list import TopPostList
from .myviews.new_post_list import NewPostList
from .myviews.upload import UploadView
import time
import json
from myapp.models import User

def logout(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass
    return HttpResponseRedirect(reverse('index'))


registration_process_count = 0

def price(request):
    global registration_process_count
    if request.method == 'POST':
        registration_process_count += 1
        time.sleep(10 * registration_process_count)
        input_data = json.loads(request.session['input_data'])
        print(input_data)
        input_data = RegisterView.FormData(input_data['username'], input_data['password1'], input_data['password1'], input_data['email'])
        record = User(username=input_data.username, password=input_data.password1, email=input_data.email)
        record.save()
        return LoginView.login_success(request, input_data)
    return render(request, 'myapp/price.html')

    def finish_registration(input_data):
        RegisterView.save_to_database(input_data)
        return LoginView.login_success(self.request, self.input_data)      