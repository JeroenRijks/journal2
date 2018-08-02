from django.forms import ModelForm
from journal.models import Resource

class ResourceForm(ModelForm):
     class Meta:
         model = Resource
         fields = ['name', 'link']