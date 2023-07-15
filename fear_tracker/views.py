from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import FearTracker
from .forms import FearTrackerForm
from django.contrib import messages
from plotly.offline import plot
from plotly.graph_objs import Scatter


class FearCreateView(LoginRequiredMixin, CreateView):
    model = FearTracker
    form_class = FearTrackerForm
    template_name = 'fear_tracker/fear_tracker_form.html'
    success_url = reverse_lazy('fear-tracker')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Record added successfully.')
        return super().form_valid(form)


class FearListView(LoginRequiredMixin, ListView):
    model = FearTracker
    template_name = 'fear_tracker/fear_tracker_list.html'
    context_object_name = 'records'
    ordering = ['-date']
    paginate_by = 10


class FearDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = FearTracker
    template_name = 'fear_tracker/fear_tracker_delete.html'
    success_url = reverse_lazy('fear-list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Record deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class YourChartView(LoginRequiredMixin, TemplateView):
    template_name = 'fear_tracker/fear_tracker.html'

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
