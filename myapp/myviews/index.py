from django.views.generic.base import TemplateView
from .login import LoginView

class IndexView(TemplateView):
    template_name = "myapp/index.html"

    def get_context_data(self, **kwargs):
        context = {'active_home': 'active', 'height': True}
        LoginView.is_user_logged_on(self.request, context)
        return context