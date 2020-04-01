import os
from django.views.generic.edit import FormView
from myapp.forms import UploadFileForm
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from myapp.models import Post
from myapp.myviews.login import LoginView
from pathlib import Path

class UploadView(FormView):
    template_name = 'myapp/upload.html'
    form_class = UploadFileForm
    success_url = '/new/'

    def get(self, request):
        if not self.is_user_logged_on():
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context) 

    def post(self, request):
        if not self.is_user_logged_on():
            return HttpResponseRedirect(reverse('index'))
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_not_valid()
    
    def form_not_valid(self):
        context = self.get_context_data()
        context['form_not_valid'] = True
        return render(self.request, self.template_name, context)

    def form_valid(self, form):
        self.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_upload'] = 'active'
        context['height'] = True
        return context

    def handle_uploaded_file(self, file):
        current_path = os.path.dirname(os.path.realpath(__file__))
        parent_path = Path(current_path).parent.parent
        photo_path = str(parent_path) + "/photos/" + str(file.name)
        with open(photo_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
    
    def save(self):
        request = self.request
        record = Post(title=request.POST.get('title'), content=request.POST.get('content'), photo=request.FILES['photo'].name)
        self.handle_uploaded_file(request.FILES['photo'])
        record.save()   

    def is_user_logged_on(self):
        context = self.get_context_data()
        return LoginView.is_user_logged_on(self.request, context)
    