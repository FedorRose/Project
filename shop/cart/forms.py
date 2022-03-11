from django import forms
from .models import *

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 51)]


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'email', 'address', 'postal_code', 'city')
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last lame'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal_code'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
        }
