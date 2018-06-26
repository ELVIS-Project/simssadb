from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from database.forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.mail import EmailMessage
from django.views.generic import (TemplateView, CreateView)
from database import forms
from django.urls import reverse
from haystack.query import SearchQuerySet
from haystack.generic_views import SearchView


class HomeView(TemplateView):  # show about page
    template_name = 'database/home.html'


class AboutView(TemplateView):  # show about page
    template_name = 'database/about.html'


class SignUp(CreateView):
    form_class = forms.UserCreateForm


class CreatePieceView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

    def get_success_url(self):
        return reverse('login')
    # success_url = reverse('about.html')  # cause "circular import" problem
    template_name = "registration/signup.html"


def signup(request):
    if request.method == 'POST':  # 'POST' means the client submits something as resources to the server
        form = UserCreateForm(request.POST)  # We get the form from the user
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # user can’t login without email confirmation.
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('registration/acc_active_email.html', { # Use this html template with the following variables
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token': account_activation_token.make_token(user),
            })  # this creates a body of email where you are specified using a html
            mail_subject = 'Activate your SIMSSA DB account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('A confirmation email has been sent to your email address. '
                                'Please confirm your email address to complete the registration by '
                                'clicking the activation link in the email.')
    else:
        form = UserCreateForm()  # display the form for the user to fill in, since we got a GET request
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user) # automatically log in
        return redirect('home')
    else:
        return HttpResponse('Invalid activation link. Please examine your activation link and try again!')
