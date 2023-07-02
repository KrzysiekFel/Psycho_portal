from django.shortcuts import render


def personality_test(request):
    return render(request, 'personality_test.html', {'title': 'Personality Test'})


def new_test(request):
    return render(request, 'personality_test.html', {'title': 'Personality Test'})


def test_result(request):
    return render(request, 'personality_test.html', {'title': 'Personality Test'})
