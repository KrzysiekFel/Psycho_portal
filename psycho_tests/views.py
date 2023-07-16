from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .models import PsychoTest, TestResult, Answer
from .forms import TestForm, TestFillForm
from django.views.generic import CreateView, ListView, View, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PsychoTestsListView(ListView):
    model = PsychoTest
    template_name = 'psycho_tests/psycho_tests_home.html'
    context_object_name = 'tests'
    ordering = ['-date_creation']


class CreateTestView(LoginRequiredMixin, CreateView):
    model = PsychoTest
    form_class = TestForm
    template_name = 'psycho_tests/psycho_tests_create.html'
    success_url = reverse_lazy('psycho-tests')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Test added successfully.')
        return super().form_valid(form)


class TestFillView(View):
    def get(self, request, test_id):
        answers = Answer.objects.filter(psycho_test=test_id)
        test = PsychoTest.objects.get(pk=test_id)
        questions = test.questions.all()
        form = TestFillForm(questions=questions, answers=answers)
        return render(request, 'psycho_tests/psycho_tests_detail.html', {'test': test, 'form': form})

    def post(self, request, test_id):
        answers = Answer.objects.filter(psycho_test=test_id)
        test = PsychoTest.objects.get(pk=test_id)
        questions = test.questions.all()
        form = TestFillForm(request.POST, questions=questions, answers=answers)

        if form.is_valid():
            score = 0
            id_number_of_first_answer = int(Answer.objects.filter(psycho_test=test_id).first().id)

            for question in questions:
                choice = form.cleaned_data.get(f'question_{question.id}')
                score += int(choice) - id_number_of_first_answer  # this subtraction is needed to start counting from 0
                # because choice value is answer id from table and id value will not start from 0

            user = request.user
            result = TestResult(score=score, test=test, user=user)
            result.save()

            return redirect('test-result', result_id=result.id)

        return render(request, 'psycho_tests/psycho_tests_detail.html', {'test': test, 'form': form})


class TestResultView(View):
    def get(self, request, result_id):
        result = TestResult.objects.get(pk=result_id)
        test = result.test

        if result.score >= test.threshold:
            result_description = test.result_above_threshold
        else:
            result_description = test.result_below_threshold

        context = {
            'result': result,
            'test': test,
            'result_description': result_description
        }

        return render(request, 'psycho_tests/psycho_tests_result.html', context)


class AllTestResultView(LoginRequiredMixin, ListView):
    model = TestResult
    template_name = 'psycho_tests/psycho_tests_all_test_results.html'
    context_object_name = 'results'
    ordering = ['-date_creation']


class DeleteTestView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = PsychoTest
    template_name = 'psycho_tests/psycho_tests_delete.html'
    success_url = reverse_lazy('psycho-tests')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Record deleted successfully.')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
