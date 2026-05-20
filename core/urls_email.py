from django.urls import path
from .views_email import email_subscribe, email_unsubscribe

urlpatterns = [
    path('email/subscribe/', email_subscribe, name='email-subscribe'),
    path('email/unsubscribe/', email_unsubscribe, name='email-unsubscribe'),
]
