from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FearTracker
from .forms import FearTrackerForm
from django.contrib import messages
from django.conf import settings
import os
from plotly.offline import plot
from plotly.graph_objs import Scatter


def fear_tracker(request):
    return render(request, 'fear_tracker/fear_tracker.html', {'title': 'Fear Tracker'})


class FearCreateView(LoginRequiredMixin, CreateView):
    model = FearTracker
    form_class = FearTrackerForm
    template_name = 'fear_tracker/fear_tracker_form.html'
    success_url = reverse_lazy('fear-tracker')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Record added successfully.')
        return super().form_valid(form)


class YourChartView(LoginRequiredMixin, TemplateView):
    template_name = 'fear_tracker/fear_tracker_plot.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        queryset = FearTracker.objects.filter(author_id=user_id).order_by('date')

        x = [f.date.strftime('%Y-%m-%d') for f in queryset]
        y = [f.fear_level for f in queryset]

        plot_div = plot([Scatter(x=x, y=y, mode='lines', name='test', opacity=0.8, marker_color='green')],
                        output_type='div')
        context['plot_div'] = plot_div

        return context
