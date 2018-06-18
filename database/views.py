from django.shortcuts import render
from django.views.generic import (TemplateView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import MusicalWork
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import *
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.contrib import messages
from django.core.mail import EmailMessage
from database.models import *
from django.views.generic import ListView
from django.views.generic import ListView
from rest_framework import generics
from database.serializers import *
from rest_framework import viewsets

# Create your views here.


class HomeView(TemplateView):  # show about page
    template_name = 'home.html'

class AboutView(TemplateView):  # show about page
    template_name = 'about.html'

# This function
# searches for post_form page!
# you cannot create a post unless logged in


<<<<<<< HEAD
class CreatePieceView(LoginRequiredMixin, CreateView):
    login_url = '/login/'

    redirect_field_name = 'database/musicalwork_detail.html'  # save the new
    #  post, and it redirects to post_detail page

    form_class = PieceForm  # This creates a new PostForm,
    # and PostForm already specifies which fields we need to create
    model = MusicalWork


class MusicalWorkDetailView(DetailView):  # show the content
    # of the post when clicking
    model = MusicalWork  #


class MusicalWorkListView(ListView):  # home page: show a list of post
    model = MusicalWork  # what do you want to show
    # in this list: post, so model = Post

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
=======
class SignUp(CreateView):
    form_class = forms.UserCreateForm

    def get_success_url(self):
        return reverse('login')
    # success_url = reverse('about.html')  # cause "circular import" problem
>>>>>>> 9a0a8d5... New: Changed detail views to view sets for, removed old views
    template_name = "registration/signup.html"


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


<<<<<<< HEAD

class GeographicAreaDetail(generics.RetrieveAPIView):
=======
class GeographicAreaViewSet(viewsets.ModelViewSet):
>>>>>>> 9a0a8d5... New: Changed detail views to view sets for, removed old views
    queryset = GeographicArea.objects.all()
    serializer_class = GeographicAreaSerializer


class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer


class MusicalWorkViewSet(viewsets.ModelViewSet):
    queryset = MusicalWork.objects.all()
    serializer_class = MusicalWorkSerializer


class PartViewSet(viewsets.ModelViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer


class SourceViewSet(viewsets.ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class CollectionOfSourcesViewSet(viewsets.ModelViewSet):
    queryset = CollectionOfSources.objects.all()
    serializer_class = CollectionOfSourcesSerializer


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
