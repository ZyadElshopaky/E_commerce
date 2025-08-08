# forms.py

from django import forms
from .models import Product
from django.utils import timezone
# forms.py

class ProductForm(forms.ModelForm):
    created_at = forms.DateTimeField(disabled=True, required=False ,initial=timezone.now())
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['created_by']
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['created_at'].disabled = True
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
