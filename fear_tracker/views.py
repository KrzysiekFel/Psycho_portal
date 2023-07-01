from django.shortcuts import render


def fear_tracker(request):
    return render(request, 'fear_tracker.html', {'title': 'Fear Tracker'})
