from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

# google sheets api packages
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Create your views here.

# gc = gspread.service_account(filename='odyssey/static/odyssey/credentials.json')
# sheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1GwTC2kRQuuncIsxlGKaz68ynEZmeo49tzSszGuxmD0E/")
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
creds = ServiceAccountCredentials.from_json_keyfile_name(
    'odyssey/static/odyssey/credentials.json', scope)
client = gspread.authorize(creds)
sheet = client.open("tsa-webmaster").sheet1


def index(request):
    return render(request, "odyssey/index.html")


def sources(request):
    return render(request, "odyssey/sources.html")


def register(request):
    return render(request, "odyssey/order.html")

# Needs to update google spreadsheet


def isEmptyData(row):
    return sheet.cell(row, 1).value is None


def register_view(request):
    if request.method == "POST":
        info_arr = []
        info_arr.append(request.POST["tourChoice"])
        info_arr.append(request.POST["firstName"])
        info_arr.append(request.POST["lastName"])
        info_arr.append(request.POST["birthday"])
        info_arr.append(request.POST["firstNameBill"])
        info_arr.append(request.POST["lastNameBill"])
        info_arr.append(request.POST["inputAddress"])
        info_arr.append(request.POST["inputAddress2"])
        info_arr.append(request.POST["inputCity"])
        info_arr.append(request.POST["inputState"])
        info_arr.append(request.POST["inputZip"])
        info_arr.append(request.POST["paymentMethod"])
        info_arr.append(request.POST["cc-name"])
        info_arr.append(request.POST["cc-number"])
        info_arr.append(request.POST["cc-expiration"])
        info_arr.append(request.POST["cc-cvv"])
        row = 1
        while True:
            if isEmptyData(row):
                break
            row += 1
        for i in info_arr:
            sheet.update_cell(row, info_arr.index(i)+1, i)
        messages.success(
            request, "Congratulations! You've successfully booked!")
        return HttpResponseRedirect(reverse('register'))
    messages.error(request, "Unsuccessful, try again.")
    return HttpResponseRedirect(reverse('register'))


def safety(request):
    return render(request, "odyssey/safety.html")


def contact_us(request):
    return render(request, "odyssey/contactus.html")
