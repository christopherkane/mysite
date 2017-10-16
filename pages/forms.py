from django import forms
from django.core.validators import MaxLengthValidator, RegexValidator
from django.core.mail import send_mail
from django.template.loader import get_template
from django.conf import settings
from smtplib import SMTPException
import logging

# our new form
class ContactForm(forms.Form):
    contact_name = forms.CharField(
        required=True,
        validators = [
            MaxLengthValidator(50),
            RegexValidator(
                regex='^[a-zA-Z ,.\'-]+$',
                message='Ensure you only use letters, spaces, apostrophes, hyphens,  periods.',
                code='invalid_contact_name'
            ),
        ]
    )
    contact_email = forms.EmailField(
        required=True,
        validators=[
            MaxLengthValidator(50),
        ]
    )
    content = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'rows':7}),
        validators = [
            MaxLengthValidator(2500)
        ]
    )

    def send_email(self):
        contact_name = self.cleaned_data['contact_name']
        contact_email = self.cleaned_data['contact_email']
        form_content = self.cleaned_data['content']

        # Email the cmessage body from the supplied info and a template
        template = get_template('pages/contact.txt')
        content = template.render({
            'contact_name': contact_name,
            'contact_email': contact_email,
            'form_content': form_content,
        })

        try:
            send_mail(
                'You\'ve got mail',
                content,
                settings.SERVER_EMAIL,
                [a[1] for a in settings.ADMINS],
                fail_silently=False,
            )
        except SMTPException as e:
            logger = logging.getLogger(__name__)
            logger.error('Failed to send email: {}\n{}'.format(e, content))