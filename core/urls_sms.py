from django.urls import path
from .views_sms import sms_subscribe, sms_unsubscribe

urlpatterns = [
    path('sms/subscribe/', sms_subscribe, name='sms-subscribe'),
    path('sms/unsubscribe/', sms_unsubscribe, name='sms-unsubscribe'),
]
