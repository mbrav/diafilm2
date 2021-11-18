from django.core.mail import EmailMultiAlternatives
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page

from diafilm.settings import EMAIL_HOST_USER

from .forms import ContactForm


@cache_page(60 * 15)
def author(request):
    return render(request, 'about/author.html')


@cache_page(60 * 15)
def contact(request):
    contact_form = ContactForm()
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)

        subject, from_email = 'hello', EMAIL_HOST_USER
        to = str(contact_form['email'].value())
        subject = contact_form['subject'].value()
        name = contact_form['name'].value()
        text_content = contact_form['message'].value()

        context = {
            'name': name,
            'email': to,
            'subject': subject,
            'message': text_content,
        }

        html_template = 'about/emails/contact.html'
        html_content = render_to_string(html_template, context)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return render(request, 'about/author.html', {'recepient': to})

    context = {
        'form': contact_form,
    }
    return render(request, 'about/contact.html', context)
