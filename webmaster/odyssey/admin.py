from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(Order)
admin.site.register(Account)
admin.site.register(Payment)
admin.site.register(LoginPing)
admin.site.register(HelpTicket)