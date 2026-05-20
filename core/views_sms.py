from django.shortcuts import render, redirect
from django.contrib import messages
from .models_sms import SmsSubscriber
from .forms_sms import SmsSubscribeForm, SmsUnsubscribeForm

def sms_subscribe(request):
    if request.method == 'POST':
        form = SmsSubscribeForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            sub, created = SmsSubscriber.objects.get_or_create(phone=phone)
            sub.subscribed = True
            sub.save()
            messages.success(request, "Vous êtes inscrit aux notifications SMS !")
            return redirect('home')
    else:
        form = SmsSubscribeForm()
    return render(request, 'sms_subscribe.html', {'form': form})

def sms_unsubscribe(request):
    if request.method == 'POST':
        form = SmsUnsubscribeForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            try:
                sub = SmsSubscriber.objects.get(phone=phone)
                sub.subscribed = False
                sub.save()
                messages.success(request, "Vous êtes désinscrit des notifications SMS.")
            except SmsSubscriber.DoesNotExist:
                messages.error(request, "Numéro non trouvé.")
            return redirect('home')
    else:
        form = SmsUnsubscribeForm()
    return render(request, 'sms_unsubscribe.html', {'form': form})
