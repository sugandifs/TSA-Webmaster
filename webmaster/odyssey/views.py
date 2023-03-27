from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from odyssey.models import *
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json


# Page rendering

def index(request):
    return render(request, "odyssey/index.html")


def sources(request):
    return render(request, "odyssey/sources.html")


def safety(request):
    return render(request, "odyssey/safety.html")


def contact_us(request):
    return render(request, "odyssey/contactus.html")


def error(request):
    return render(request, "odyssey/error.html")

# Tour booking


def register(request):
    if request.user.is_authenticated:
        payments = Payment.objects.filter(account = request.user)
        return render(request, "odyssey/order.html", context = {
            "payments":payments,
        })
    return render(request, "odyssey/order.html")

def add_payment(request):
    if request.method == "POST":
        #add functionality and json response
        p = Payment(cardName = request.POST.get("cc-nn"),firstNameBill = request.POST.get("bfname"), lastNameBill = request.POST.get("blname"), inputAddress = request.POST.get("baddress"), inputCity = request.POST.get("bcity"), inputState = request.POST.get("bstate"), inputZip = request.POST.get("bzip"), paymentMethod = request.POST.get("paymentMethod"),cc_name = request.POST.get("cc-name"), cc_number = request.POST.get("cc-num"), cc_expiration = request.POST.get("cc-exp"), cc_cvv = request.POST.get("cc-cvv"), account = request.user)
        p.save()
        print(p)
        messages.success(
            request, "Payment Method Added")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def register_view(request):
    if request.method == "POST":
        #add functionality and json response
        paymentChoice = Payment.objects.get(account = request.user, cardName = request.POST.get("cardSelection"))
        o = Order(tourChoice = request.POST.get("tourChoice"),departDate = request.POST.get("departDate"), ticketCount = request.POST.get("ticketCount"),account = request.user, payment = paymentChoice)
        o.save()
        print(o)
        messages.success(
            request, "Congratulations! You've successfully booked!")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@csrf_exempt
def fetch_url(request):
    data = {'url1': reverse('index')}
    return JsonResponse(data)

# Authentication System


def registration_view(request):
    return render(request, "odyssey/registration.html")


def create_account(request):
    if request.method == "POST":
        user = User.objects.create_user(username = request.POST.get("create-username"), email = request.POST.get("create-email"), password = request.POST.get("create-password"))
        user.first_name = request.POST.get("create-user-first-name")
        user.last_name = request.POST.get("create-user-last-name")
        user.save()
        account = Account(user=user, residentialAddress=request.POST.get("create-user-residential-address"), birthday=request.POST.get("create-user-birthday"),socialSecurity=request.POST.get("create-user-social-security"), securityAnswer1=request.POST.get("create-user-security-answer"))
        account.save()
        login(request,user)
        l = LoginPing(user = request.user, pingType = "Account Creation")
        l.save()
        messages.success(request, "Account Created")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status':'error'})


def log_in(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST.get(
            'username'), password=request.POST.get('password'))
        if user is not None:
            login(request, user)
            l = LoginPing(user = request.user, pingType = "Log In")
            l.save()
            # ADD REDIRECT
            return JsonResponse({'status': 'success'})
        return JsonResponse({'status': 'error'}, status=401)


def log_out(request):
    l = LoginPing(user = request.user, pingType = "Logout")
    l.save()
    logout(request)
    messages.success(request, "logged out")
    return HttpResponseRedirect(reverse("registration"))

# CHATBOT


@csrf_exempt
def chatbot(request):
    if request.method == 'POST':
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)
        message = data.get('message')

        # Generate a response
        response = generate_chatbot_response(message)
        # Return the bot's message as a JSON response
        return JsonResponse({'message': response})

    # If the request method is not POST, return an empty response
    return JsonResponse({})


def generate_chatbot_response(message):
    global conversation

    if message.lower() == "hi" or message.lower() == "hello":
        response = "Hi there! How can I help you today?"
    elif "about" in message.lower():
        response = "Odyssey is more than just a trip, it is an experience you will never forget for a lifetime. Experience space from a beautiful itinerary, while in the relief that your safety is guaranteed in our safety training program on top of or extra measures. Welcome to the Future."
    elif "info" in message.lower() or "tour" in message.lower() or "safety" in message.lower() or "program" in message.lower():
        response = "You get to choose from three of the best on Earth flights! To learn more, scroll down on our home page to see our tours, their safety procedures, and how to book them!"
    elif "order" in message.lower() or "status" in message.lower() or "book" in message.lower():
        response = "To book, visit the <strong>Book a Tour</strong> link at the top, you must be logged in. To check on the status of your order, you must be logged in and go into your profile."
    elif "cancel" in message.lower():
        response = "To cancel your order, a representative must cancel it for you. Please visit <strong>Contact Us</strong> to ask us to cancel your order and include a reason why."
    elif "thanks" in message.lower() or "thank you" in message.lower():
        response = "You're welcome! Is there anything else I can assist you with?"
    elif "more" in message.lower() or "help" in message.lower() or "human" in message.lower() or "representative" in message.lower():
        redirection = reverse("contact us")
        response = "Unfortunately, due to volume, there are no agents available at this time. To have an Odysseynaut help you, visit <strong><a href = '"+redirection+"' >Contact Us</a></strong> to submit a support ticket. Thank you for your patience."
    else:
        response = "I'm sorry, I didn't understand your message. How can I assist you?"
    return response
