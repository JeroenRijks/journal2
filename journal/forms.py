from django.forms import ModelForm
from journal.models import Resource, Tag


class ResourceForm(ModelForm):

    class Meta:
        model = Resource
        fields = ['name', 'link','tip','tags']


    def __init__(self, *args, **kwargs):
        super(ResourceForm, self).__init__(*args, **kwargs)
        self.fields['tags'].required = False

class TagForm(ModelForm):

    class Meta:
        model = Tag
        fields = ['name']