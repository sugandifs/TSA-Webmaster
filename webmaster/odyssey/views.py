from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from odyssey.models import *
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import random
import json
from datetime import timedelta, datetime, date

# Page rendering

def index(request):
    return render(request, "odyssey/index.html")


def sources(request):
    return render(request, "odyssey/sources.html")


def safety(request):
    return render(request, "odyssey/safety.html")


def contact_us(request):
    return render(request, "odyssey/contactus.html")

def contact_us_send(request):
    if not request.user.is_authenticated:
        h = HelpTicket(email = request.POST["email"], subject = request.POST["subject"], question = request.POST["question"])
        h.save()
        return render(request, "odyssey/contactus.html", context = {"message_success":"Message sent! Check your message center in your profile in 24 hours!"})
    if request.method == "POST":
        h = HelpTicket(email = request.POST["email"], subject = request.POST["subject"], question = request.POST["question"], account = request.user)
        h.save()
        messages.success(request, "message sent")
        return render(request, "odyssey/contactus.html", context = {"message_success":"Message sent! Check your message center in your profile in 24 hours!"})
    return HttpResponseRedirect(reverse("contact_us"))

def faq(request):
    return render(request, "odyssey/faq.html")

def error(request):
    return render(request, "odyssey/error.html")

# Tour booking

def register_param(request, checked):
    if request.user.is_authenticated:
        payments = Payment.objects.filter(account = request.user)
        return render(request, "odyssey/order.html", context = {
            "payments":payments,
            "checked":checked,
        })
    return render(request, "odyssey/order.html", context = {
        "checked":checked,
    })

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
        messages.success(
            request, "Payment Method Added")
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})

def register_view(request):
    if request.method == "POST":
        #add functionality and json response
        paymentChoice = Payment.objects.get(account = request.user, cardName = request.POST.get("cardSelection"))
        tour_choice = request.POST.get("tourChoice")
        if tour_choice is None:
            tour_choice = "Next Available Tour"
        tickets_date_request = request.POST.get("tickets_date")
        if str(tickets_date_request) == "":
            tickets_date_request = str(date.today())
        o = Order(tourChoice = request.POST.get("tourChoice"),account = request.user, payment = paymentChoice, depart_date =datetime.strptime(tickets_date_request, "%Y-%m-%d")+timedelta(days = 64),numTickets = request.POST.get("num_tickets"))
        o.save()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'})


@csrf_exempt
def fetch_url(request):
    data = {'url1': reverse('index')}
    return JsonResponse(data)

# Authentication System

@login_required
def profile(request):
    if not request.user.is_authenticated:
        messages.error(request, "Please Log In")
        return HttpResponseRedirect(reverse("registration"))
    account = Account.objects.get(user = request.user)
    payment_methods = Payment.objects.filter(account = request.user)
    orders = Order.objects.filter(account = request.user).order_by('depart_date')
    message_center = HelpTicket.objects.filter(account = request.user).order_by('-id')
    context = {
        "account":account,
        "payments":payment_methods,
        "orders":orders,
        "user_info":request.user,
        "message_center":message_center,
    }
    return render(request, "odyssey/profile.html", context)

@login_required
def edit_profile(request):
    account = Account.objects.get(user = request.user)
    payment_methods = Payment.objects.filter(account = request.user)
    orders = Order.objects.filter(account = request.user).order_by('depart_date')
    message_center = HelpTicket.objects.filter(account = request.user).order_by('-id')
    if request.method == "POST":
        if request.user.check_password(request.POST["conf_password"]):
            u = request.user
            account.birthday = request.POST["birthday"]
            account.socialSecurity = request.POST["ssn"]
            account.residentialAddress = request.POST["address"]
            account.securityAnswer1 = request.POST["security"]
            u.first_name = request.POST["fname"]
            u.last_name = request.POST["lname"]
            u.email = request.POST["email"]
            u.save()
            account.save()
            context = {
                "message_center":message_center,
                "function_message":"Success! Profile Saved.",
                "account":account,
                "payments":payment_methods,
                "orders":orders,
                "user_info":request.user
            }
            return render(request, "odyssey/profile.html", context)
        context = {
            "message_center":message_center,
            "account":account,
            "payments":payment_methods,
            "orders":orders,
            "user_info":request.user,
            "function_message":"You entered an invalid password. Try again."
        }
    return render(request, "odyssey/profile.html", context)

def edit_payments(request):
    if request.method == "POST":
        p = Payment(cardName = request.POST.get("cc-nn"),firstNameBill = request.POST.get("bfname"), lastNameBill = request.POST.get("blname"), inputAddress = request.POST.get("baddress"), inputCity = request.POST.get("bcity"), inputState = request.POST.get("bstate"), inputZip = request.POST.get("bzip"), paymentMethod = request.POST.get("paymentMethod"),cc_name = request.POST.get("cc-name"), cc_number = request.POST.get("cc-num"), cc_expiration = request.POST.get("cc-exp"), cc_cvv = request.POST.get("cc-cvv"), account = request.user)
        p.save()
        account = Account.objects.get(user = request.user)
        payment_methods = Payment.objects.filter(account = request.user)
        message_center = HelpTicket.objects.filter(account = request.user).order_by('-id')
        orders = Order.objects.filter(account = request.user).order_by('depart_date')
        context = {
                    "function_message":"Success! Payments Updated.",
                    "message_center":message_center,
                    "account":account,
                    "payments":payment_methods,
                    "orders":orders,
                    "user_info":request.user
                }
        return render(request, "odyssey/profile.html", context)
    return HttpResponseRedirect(reverse("profile"))

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
