from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.


def index(request):
    return render(request, "odyssey\index.html")


def sources(request):
    return render(request, "odyssey\sources.html")


def program(request):
    return render(request, "odyssey\program.html")


def register(request):
    return render(request, "odyssey\order.html")


def safety(request):
    return render(request, "odyssey\safety.html")


def contact_us(request):
    return render(request, "odyssey\contactus.html")
