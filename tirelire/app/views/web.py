from django.shortcuts import render


def tirelire(request):
    return render(request, 'index.html')
