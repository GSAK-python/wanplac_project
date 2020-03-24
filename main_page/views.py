import datetime
from django.views.generic import TemplateView
import app1
import app2
import client_panel
from client_panel.models import DateList
from app2.models import DateList
from app1.models import DateList


class MainPageView(TemplateView):
    template_name = 'main_page/main.html'

    def get_context_data(self, **kwargs):
        context = super(MainPageView, self).get_context_data(**kwargs)
        if self.request:
            context['current_day'] = datetime.datetime.now().date()
            context['next_day'] = datetime.datetime.now().date() + datetime.timedelta(days=1)
            context['next_next_day'] = datetime.datetime.now().date() + datetime.timedelta(days=2)
            context['next_next_next_day'] = datetime.datetime.now().date() + datetime.timedelta(days=3)
            context['client_panel_date_list'] = client_panel.models.DateList.objects.values_list('date', flat=True)
            context['app2_date_list'] = app2.models.DateList.objects.values_list('date', flat=True)
            context['app1_date_list'] = app1.models.DateList.objects.values_list('date', flat=True)
            context['current_time'] = datetime.datetime.now().time()
            context['start_break'] = datetime.time(11, 45)
            context['stop_break'] = datetime.time(12, 15)
            return context
