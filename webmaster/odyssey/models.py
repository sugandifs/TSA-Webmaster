from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, datetime, date

# Create your models here.
class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    residentialAddress = models.CharField(max_length = 100)
    birthday = models.CharField(max_length = 16)
    socialSecurity = models.CharField(max_length = 20)
    securityAnswer1 = models.CharField(max_length = 64)

    def __str__(self):
        return f"{self.user}"

class Payment(models.Model):
    cardName = models.CharField(max_length = 64)
    firstNameBill = models.CharField(max_length = 64)
    lastNameBill = models.CharField(max_length = 64)
    inputAddress = models.CharField(max_length = 64)
    inputCity = models.CharField(max_length = 64)
    inputState = models.CharField(max_length = 64)
    inputZip = models.CharField(max_length = 64)
    paymentMethod = models.CharField(max_length = 64)
    cc_name = models.CharField(max_length = 64)
    cc_number = models.CharField(max_length = 64)
    cc_expiration = models.CharField(max_length = 64)
    cc_cvv = models.CharField(max_length = 64)
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.cc_name}"

STATUS_CHOICES = (
    ("pending", "pending"),
    ("failed", "failed"),
    ("processed", "processed"),
    ("reviewing", "reviewing"),
    ("approved", "approved"),
    ("redeemed", "redeemed"),
    ("completed", "completed"),
)

class Order(models.Model):
    tourChoice = models.CharField(max_length = 64)
    payment = models.ForeignKey(Payment, on_delete = models.CASCADE)
    account = models.ForeignKey(User, on_delete = models.CASCADE)
    depart_date = models.DateField(default = date.today() + timedelta(days = 64))
    numTickets = models.IntegerField(default = 1)
    status = models.CharField(
        max_length = 20,
        choices = STATUS_CHOICES,
        default = "pending",
    )
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.date} {self.account} {self.tourChoice}"

class LoginPing(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE)
    pingType = models.CharField(max_length = 16, null = True, default = "Admin Login")
    date= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.user) + " " + str(self.pingType) + ': ' + str(self.date)
    
class HelpTicket(models.Model):
    email = models.EmailField()
    subject = models.TextField()
    question = models.TextField()
    account = models.ForeignKey(User, on_delete=models.CASCADE, null = True)

    def __str__(self):
        return f"{self.email}: {self.subject}"