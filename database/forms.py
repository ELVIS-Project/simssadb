from django import forms
from .models import MusicalWork

class PieceForm(forms.ModelForm):

    class Meta:
        model = MusicalWork
        fields = ('title', 'alternative_titles',)  # who posted it, the title and the text
        # By using these attributes, the author, title and text defined in Post, will automatically produce a form, when
        #form.as_p is required
        # the line above inherits from the model Post and present it as a form, and we want author, title and text to be
        # in the form

        widgets = {
            'title': forms.TextInput(attrs={'class': 'textinputclass'}), # 'textinputclass' this is css class
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}) # it contains 3 css classes

        }  # however, we can comment widgets area, and the form can still be displayed (maybe not as pretty as using CSS)
