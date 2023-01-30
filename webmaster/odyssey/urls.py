from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('safety', views.safety, name='safety'),
    path('register', views.register, name='register'),
    path('register/submit', views.register_view, name='submitOrder'),
    path('contact_us', views.contact_us, name='contact us'),
    path('sources', views.sources, name='sources')
]
