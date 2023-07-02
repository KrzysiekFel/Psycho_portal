from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FearTracker
from .forms import FearTrackerForm
from django.contrib import messages
import matplotlib.pyplot as plt
from django.conf import settings
import os


def fear_tracker(request):
    return render(request, 'fear_tracker.html', {'title': 'Fear Tracker'})


class FearCreateView(LoginRequiredMixin, CreateView):
    model = FearTracker
    form_class = FearTrackerForm
    template_name = 'fear_tracker_form.html'
    success_url = reverse_lazy('fear-tracker')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Record added successfully.')
        return super().form_valid(form)


class YourChartView(TemplateView):
    template_name = 'plot_fear.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        queryset = FearTracker.objects.filter(author_id=user_id).order_by('date')

        x = [f.date.strftime('%Y-%m-%d') for f in queryset]
        y = [f.fear_level for f in queryset]

        plt.plot(x, y, 'xb-')
        plt.xlabel('Date')
        plt.ylabel('Fear level')
        plt.title('Fear level plot')

        chart_image = 'media/chart_image.jpg'
        plt.savefig(chart_image)
        plt.close()

        context['chart_image'] = os.path.join(settings.MEDIA_URL, 'chart_image.jpg')

        return context
