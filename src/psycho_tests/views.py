from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib import messages
from .models import PsychoTest, TestResult, Answers
from .forms import TestForm, TestFillForm
from django.views.generic import CreateView, ListView, View, DeleteView
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
    PermissionRequiredMixin,
)
from typing import Type, List, Dict, Any
from django.http import HttpRequest, HttpResponse


class PsychoTestsListView(ListView):
    model: Type[PsychoTest] = PsychoTest
    template_name: str = "psycho_tests/psycho_tests_home.html"
    context_object_name: str = "tests"

    ordering: List[str] = ["-date_creation"]

    def get_queryset(self):
        return super().get_queryset().filter(status="published")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_publisher"] = self.request.user.groups.filter(
            name="Publisher"
        ).exists()
        return context


class CreateTestView(LoginRequiredMixin, CreateView):
    model: Type[PsychoTest] = PsychoTest
    form_class = TestForm
    template_name: str = "psycho_tests/psycho_tests_create.html"
    success_url = reverse_lazy("psycho-tests")

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Test added successfully.")
        return super().form_valid(form)


class TestFillView(View):
    def get(self, request: HttpRequest, test_id: int) -> HttpResponse:
        print(type(test_id))
        test = get_object_or_404(PsychoTest, pk=test_id)
        answers = get_object_or_404(Answers, pk=test.answers_id)
        questions = test.questions.all()
        form = TestFillForm(questions=questions, answers=answers)
        return render(
            request,
            "psycho_tests/psycho_tests_detail.html",
            {"test": test, "form": form},
        )

    def post(self, request: HttpRequest, test_id: int) -> HttpResponse:
        test = PsychoTest.objects.get(pk=test_id)
        answers_id: int | None = test.answers_id
        answers = Answers.objects.get(pk=answers_id)
        questions = test.questions.all()
        form = TestFillForm(request.POST, questions=questions, answers=answers)

        if form.is_valid():
            score: int = 0

            for question in questions:
                choice = form.cleaned_data.get(f"question_{question.id}")
                score += int(choice)

            user = request.user
            result = TestResult(score=score, test=test, user=user)
            result.save()

            return redirect("test-result", result_id=result.id)

        return render(
            request,
            "psycho_tests/psycho_tests_detail.html",
            {"test": test, "form": form},
        )


class TestResultView(View):
    def get(self, request: HttpRequest, result_id: int) -> HttpResponse:
        result = TestResult.objects.get(pk=result_id)
        test = result.test

        if result.score >= test.threshold:
            result_description = test.result_above_threshold
        else:
            result_description = test.result_below_threshold

        context: Dict[str, Any] = {
            "result": result,
            "test": test,
            "result_description": result_description,
        }

        return render(request, "psycho_tests/psycho_tests_result.html", context)


class AllTestResultView(LoginRequiredMixin, ListView):
    model: Type[TestResult] = TestResult
    template_name: str = "psycho_tests/psycho_tests_all_test_results.html"
    context_object_name: str = "results"
    ordering: List[str] = ["-date_creation"]

    def get_queryset(self):
        return TestResult.objects.filter(user=self.request.user)


class DeleteTestView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model: Type[PsychoTest] = PsychoTest
    template_name: str = "psycho_tests/psycho_tests_delete.html"
    success_url = reverse_lazy("psycho-tests")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Record deleted successfully.")
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class PendingPsychoTestListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = "psycho_tests.change_psychotest"
    model: Type[PsychoTest] = PsychoTest
    template_name: str = "psycho_tests/psycho_tests_to_publish.html"
    context_object_name: str = "pending_tests"
    ordering = ["-date_creation"]

    def get_queryset(self):
        return super().get_queryset().filter(status="pending")


def publish_test(request, test_id):
    test = PsychoTest.objects.get(pk=test_id)
    test.status = "published"
    test.save()
    messages.success(request, "Test published successfully!")
    return redirect("psycho-tests")
