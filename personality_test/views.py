from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from .models import PersonalityTest
from .forms import PersonalityForm
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin


def personality_test(request):
    return render(request, 'personality_test.html', {'title': 'Personality Test'})


def test_result(request):
    return render(request, 'personality_test.html', {'title': 'Personality Test'})


class PersonalityTestView(LoginRequiredMixin, CreateView):
    model = PersonalityTest
    form_class = PersonalityForm
    template_name = 'personality_test_form.html'
    success_url = reverse_lazy('personality-test')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Test added successfully.')
        return super().form_valid(form)
