from django import forms
from .models import CsvFile
 
class PostForm(forms.ModelForm):
 
    class Meta:
        model = CsvFile
        fields = ['file', 'miner_type']