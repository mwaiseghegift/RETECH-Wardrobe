from django.shortcuts import render


def Handleerr404(request, exception):
    return render(request, '404.html')