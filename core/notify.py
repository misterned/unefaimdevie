from django.core.mail import send_mail
from django.conf import settings
from core.models_email import EmailSubscriber

def notify_new_post(post):
    subject = f"Nouvel article : {post.title}"
    message = f"Un nouvel article vient d'être publié sur une faim de vie au Croisic : {post.title}\n\nLire l'article : {settings.SITE_URL}{post.get_absolute_url()}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = list(EmailSubscriber.objects.filter(subscribed=True).values_list('email', flat=True))
    if recipients:
        send_mail(subject, message, from_email, recipients, fail_silently=True)
