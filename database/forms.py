from django import forms
from database.models.musical_work import MusicalWork
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


class PieceForm(forms.ModelForm):

    class Meta:
        model = MusicalWork
        fields = ('variant_titles', )  # who posted it, the title and
        # the text
        # By using these attributes, the author, title and text defined in Post, will automatically produce a form, when
        #form.as_p is required
        # the line above inherits from the model Post and present it as a form, and we want author, title and text to be
        # in the form

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}), # 'textinputclass' this is css class
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}) # it contains 3 css classes

        }  # however, we can comment widgets area, and the form can still be displayed (maybe not as pretty as using CSS)


class UserCreateForm(UserCreationForm):
    class Meta:  # define the field you want to exposer to the form
        fields = ("username", "email", "password1", "password2")
        model = get_user_model()  # A 'to-be-created' user will sumbit this form

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
<<<<<<< HEAD
        self.fields["username"].label = "Display name"  # shows when the blank is empty. If not used, the blank will show the name of field as default

=======
        self.fields["username"].label = "Display name"
        self.fields["email"].label = "Email address"
>>>>>>> develop
