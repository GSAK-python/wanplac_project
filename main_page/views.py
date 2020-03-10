import datetime
from django.views.generic import TemplateView


class MainPageView(TemplateView):
    template_name = 'main_page/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        if self.request:
            context['client_panel_date'] = datetime.datetime.now().date()
            context['app2'] = datetime.datetime.now().date() + datetime.timedelta(days=1)
            return context




