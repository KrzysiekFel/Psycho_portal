from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import FearTracker
from.forms import FearTrackerForm
from django.contrib import messages


def fear_tracker(request):
    return render(request, 'fear_tracker.html', {'title': 'Fear Tracker'})


def plot_fear(request):
    return render(request, 'plot_fear.html', {'title': 'Plot fear'})


class FearCreateView(LoginRequiredMixin, CreateView):
    model = FearTracker
    form_class = FearTrackerForm
    template_name = 'fear_tracker_form.html'
    success_url = reverse_lazy('fear-tracker')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Record added successfully.')
        return super().form_valid(form)
