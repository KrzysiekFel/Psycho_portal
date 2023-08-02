from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import FearTracker
from .forms import FearTrackerForm
from django.contrib import messages
from plotly.offline import plot
from plotly.graph_objs import Scatter
from typing import Dict, Any, List, Type
from django.http import HttpRequest, HttpResponse
from django.db.models.query import QuerySet


class FearCreateView(LoginRequiredMixin, CreateView):
    model: Type[FearTracker] = FearTracker
    form_class: Type[FearTrackerForm] = FearTrackerForm
    template_name: str = "fear_tracker/fear_tracker_form.html"
    success_url = reverse_lazy("fear-tracker")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Record added successfully.")
        return super().form_valid(form)


class FearListView(LoginRequiredMixin, ListView):
    model: Type[FearTracker] = FearTracker
    template_name: str = "fear_tracker/fear_tracker_list.html"
    context_object_name: str = "records"
    ordering: List[str] = ["-date"]
    paginate_by: int = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(author=self.request.user)


class FearDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model: Type[FearTracker] = FearTracker
    template_name: str = "fear_tracker/fear_tracker_delete.html"
    success_url = reverse_lazy("fear-list")

    def delete(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        messages.success(self.request, "Record deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def test_func(self) -> bool:
        record = self.get_object()
        return self.request.user == record.author


class YourChartView(LoginRequiredMixin, TemplateView):
    template_name: str = "fear_tracker/fear_tracker.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        queryset: QuerySet[FearTracker] = FearTracker.objects.filter(
            author_id=user_id
        ).order_by("date")

        x: List[str] = [f.date.strftime("%Y-%m-%d") for f in queryset]
        y: List[int] = [f.fear_level for f in queryset]

        plot_div = plot(
            [
                Scatter(
                    x=x,
                    y=y,
                    mode="lines",
                    name="test",
                    opacity=0.8,
                    marker_color="green",
                )
            ],
            output_type="div",
        )
        context["plot_div"] = plot_div

        return context
