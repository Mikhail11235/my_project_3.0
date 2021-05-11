from django import forms
from .models import CsvFile
 
class Form(forms.ModelForm):
    class Meta:
        model = CsvFile
        fields = ['file', 'miner_type']