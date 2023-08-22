from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('safety', views.safety, name='safety'),
    path('register', views.register, name='register'),
    path('register/<int:checked>', views.register_param ,name = "register_param"),
    path('register/submit', views.register_view, name='submitOrder'),
    path('contact_us', views.contact_us, name='contact us'),
    path('contact_us/send', views.contact_us_send, name = 'contact_send'),
    path('sources', views.sources, name='sources'),
    path('error', views.error, name="error"),
    path('create-account/', views.create_account, name="create_account"),
    path('log-in/', views.log_in, name="log_in"),
    path('log-out', views.log_out, name="log_out"),
    path('profile',views.profile, name = "profile"),
    path('chatbot/', views.chatbot, name="chatbot"),
    path('registration', views.registration_view, name="registration"),
    path('fetch_url/', views.fetch_url, name="fetch_url"),
    path('add-payment', views.add_payment,name = "add_payment"),
    path('edit-profile', views.edit_profile, name = "edit_profile"),
    path('edit-payments', views.edit_payments, name = "edit_payments"),
    path('faq', views.faq, name = "faq")
]