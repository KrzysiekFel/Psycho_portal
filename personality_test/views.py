from django.shortcuts import render
from django.urls import reverse_lazy
from django.contrib import messages
from .models import PersonalityTest
from .forms import PersonalityForm
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin


INTROVERT_INFO = "Being an introvert means that you gain energy and find solace through internal reflection and " \
                 "solitude. Introverted individuals prefer quieter, more peaceful environments and tend to feel " \
                 "drained by excessive social stimulation. They enjoy spending time alone or with a few close friends " \
                 "or family members. Introverts are often deep thinkers and observers, valuing meaningful connections " \
                 "and engaging in introspection. They may prefer one-on-one conversations or smaller group settings " \
                 "where they can have more in-depth interactions. Introverts need time alone to recharge and may find " \
                 "too much social interaction overwhelming. While they may appear reserved or shy, introverts can be " \
                 "excellent listeners and possess a rich inner world of thoughts and ideas."
EXTRAVERT_INFO = "Being an extrovert means that you draw energy and feel more alive through external stimuli and " \
                 "social interactions. Extroverted individuals thrive in social settings and enjoy being around " \
                 "people. They tend to be outgoing, sociable, and enjoy engaging in conversations and group " \
                 "activities. Extroverts feel energized when surrounded by others and may seek out social situations " \
                 "to fulfill their need for interaction. They are often comfortable in the spotlight, enjoy being the " \
                 "center of attention, and find it easy to strike up conversations and make new connections. " \
                 "Extroverts may have a wide circle of friends and acquaintances, as they are naturally inclined to " \
                 "engage with others."


def personality_test(request):
    return render(request, 'personality_test/personality_test.html', {'title': 'Personality Test'})


class PersonalityTestView(LoginRequiredMixin, CreateView):
    model = PersonalityTest
    form_class = PersonalityForm
    template_name = 'personality_test/personality_test_form.html'
    success_url = reverse_lazy('personality-test')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Test added successfully.')
        return super().form_valid(form)


class TestResultView(LoginRequiredMixin, ListView):
    template_name = 'personality_test/personality_test_result.html'
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

        if total_sum > 10:
            personality_type = 'Extravert'
            personality_detailed = EXTRAVERT_INFO
        else:
            personality_type = 'Introvert'
            personality_detailed = INTROVERT_INFO

        context['personality_type'] = personality_type
        context['personality_detailed'] = personality_detailed

        return context
