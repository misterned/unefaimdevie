
import logging
from django.core.mail import send_mail
from django.conf import settings
from core.models_email import EmailSubscriber

logger = logging.getLogger(__name__)

def notify_new_post(post):
    subject = f"[Une faim de vie au Croisic] Nouvel article : {post.title}"
    url = f"{settings.SITE_URL}{post.get_absolute_url()}"
    message = f"Un nouvel article vient d'être publié sur une faim de vie au Croisic : {post.title}\n\nLire l'article : {url}"
    html_message = (
        f"<p>Chers affamés du Croisic</p>"
        f"<p>Un nouvel article vient d'être publié sur <em>Une faim de vie au Croisic</em> :</p>"
        f"<p><strong>{post.title}</strong></p>"
        f"<p><a href=\"{url}\">Lire l'article</a></p>"
        f"<p>Stéphane Nédélec</p>"
    )
    from_email = settings.DEFAULT_FROM_EMAIL
    recipients = list(EmailSubscriber.objects.filter(subscribed=True).values_list('email', flat=True))
    logger.info(f"Tentative d'envoi d'email à {len(recipients)} abonnés : {recipients}")
    if recipients:
        try:
            result = send_mail(subject, message, from_email, recipients, fail_silently=False, html_message=html_message)
            logger.info(f"Email envoyé avec succès à {recipients}. Résultat send_mail: {result}")
        except Exception as e:
            logger.error(f"Erreur d'envoi email: {e}")
