from django import forms
from .models import Document


class DocumentForm(forms.ModelForm):
    file = forms.FileField(label='Upload File', max_length=100)

    class Meta:
        model = Document
        fields = ['title', 'description', 'file']