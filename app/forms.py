from django.forms import ModelForm
from api.models import *

class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'image']

    # def get_fields(self):
    #     user = self.context['request'].user
    #     if user.groups.filter(name='Manager').exists():
    #         self.Meta.fields = '__all__'
    #     else:
    #         self.Meta.fields = ['name', 'image']

    #     return super().get_fields()
