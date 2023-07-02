from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from .models import PersonalityTest
from .forms import PersonalityForm
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


def personality_test(request):
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


class TestResultView(LoginRequiredMixin, ListView):
    template_name = 'personality_test_result.html'
    model = PersonalityTest

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset().filter(author=user).values('question_1', 'question_2', 'question_3',
                                                                     'question_4', 'question_5', 'question_6',
                                                                     'question_7').order_by('-date_posted').first()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = self.get_queryset()

        total_sum = sum(data.values())
        personality_type = 'Introvert'
        if total_sum > 10:
            personality_type = 'Extravert'
        context['personality_type'] = personality_type

        return context
