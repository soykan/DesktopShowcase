from django.views.generic.base import TemplateView
from .login import Login

class AboutView(TemplateView):

    template_name = "myapp/about.html"

    def get_context_data(self, **kwargs):
        context = {'active_about': 'active', 'height': True}
        Login.is_user_logged_on(self.request, context)
        return context