from django import forms
from django.core.validators import MaxLengthValidator, RegexValidator
from django.core.mail import send_mail
from django.template.loader import get_template

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

        send_mail(
            'You\'ve got mail',
            content,
            'donotreply@chriskane.xyz',
            ['chris@chriskane.xyz'],
            fail_silently=False,
        )