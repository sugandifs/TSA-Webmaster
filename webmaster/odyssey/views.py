from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

#google sheets api packages
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Create your views here.

gc = gspread.service_account(filename='odyssey/static/odyssey/credentials.json')
gsheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GwTC2kRQuuncIsxlGKaz68ynEZmeo49tzSszGuxmD0E/")


def index(request):
    return render(request, "odyssey/index.html")


def sources(request):
    return render(request, "odyssey/sources.html")


def program(request):
    return render(request, "odyssey/program.html")


def register(request):
    return render(request, "odyssey/order.html")

#Needs to update google spreadsheet
def register_view(request):
    if request.method == "POST":
        tourChoice = request.POST["tourChoice"]
        pass_fname = request.POST["firstName"]
        messages.success(request, "Congratulations! You've successfully booked the {tourChoice} for {pass_fname}")
        return HttpResponseRedirect(reverse('register'))
    messages.error(request, "Unsuccessful, try again.")
    return HttpResponseRedirect(reverse('register'))


def safety(request):
    return render(request, "odyssey/safety.html")


def contact_us(request):
    return render(request, "odyssey/contactus.html")