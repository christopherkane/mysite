from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from .forms import ContactForm

def index(request):
    # Get from from session if it exists, otherwise create a blank form
    form = request.session.get('invalid_form', ContactForm())
    # Purge invalid form from session if it exists
    request.session.pop('invalid_form', None)

    return render(request, 'pages/index.html', {'form': form})

def contact(request):
    # If this is a POST request we need to process the form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = ContactForm(request.POST)
        # If valid, send as email
        if form.is_valid():
            form.send_email()
            return HttpResponseRedirect(reverse('pages:thanks'))
        else:
            # Add form message to be used in next request
            request.session['invalid_form'] = form
            # Redirect to a index once more, with contact form fragment identifier
            return HttpResponseRedirect(reverse('pages:index') + '#contact')
    return HttpResponseRedirect(reverse('pages:index'))