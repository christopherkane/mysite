from django import forms
from django.core.validators import MaxLengthValidator, RegexValidator

# our new form
class ContactForm(forms.Form):
    contact_name = forms.CharField(
        required=True,
        validators = [
            MaxLengthValidator(50),
            RegexValidator(
                regex='^[a-zA-Z ,.\'-]+$',
                message='Ensure you only use letters, spaces, apostrophes, hyphens, commas, and periods.',
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
        # TODO send email using the self.cleaned_data dictionary
        pass
