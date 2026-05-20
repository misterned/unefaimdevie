from django.shortcuts import render, redirect
from django.contrib import messages
from .models_email import EmailSubscriber
from .forms_email import EmailSubscribeForm, EmailUnsubscribeForm

def email_subscribe(request):
    if request.method == 'POST':
        form = EmailSubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            sub, created = EmailSubscriber.objects.get_or_create(email=email)
            sub.subscribed = True
            sub.save()
            messages.success(request, "Vous êtes inscrit aux notifications email !")
            return redirect('home')
    else:
        form = EmailSubscribeForm()
    return render(request, 'email_subscribe.html', {'form': form})

def email_unsubscribe(request):
    if request.method == 'POST':
        form = EmailUnsubscribeForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                sub = EmailSubscriber.objects.get(email=email)
                sub.subscribed = False
                sub.save()
                messages.success(request, "Vous êtes désinscrit des notifications email.")
            except EmailSubscriber.DoesNotExist:
                messages.error(request, "Adresse non trouvée.")
            return redirect('home')
    else:
        form = EmailUnsubscribeForm()
    return render(request, 'email_unsubscribe.html', {'form': form})
