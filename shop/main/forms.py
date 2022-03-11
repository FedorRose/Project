from django import forms
from django.forms import ModelForm, TextInput, Textarea, widgets
from .models import *


class ContactForm(forms.Form):

    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Message'}))

    def __str__(self):
        return self.email


class ContactFormLetter(forms.Form):

    email = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Enter your email'}))

    def __str__(self):
        return self.email


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'text')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name'}),
            'text': forms.Textarea(attrs={'cols': 45, 'rows': 7, 'placeholder': 'Message'})
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Search'}))


def formfield_cb(field, **kwargs):
    if field.name == 'rating':
        kwargs["rating"] = RATING_CHOICES
    return field.formfield(**kwargs)


class ReviewForm(forms.ModelForm):
    formfield_callback = formfield_cb

    class Meta:
        model = Review
        fields = ('name', 'title', 'text', 'rating',)
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Name'}),
            'text': forms.Textarea(attrs={'rows': 7, 'placeholder': 'Message'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Title'}),
            'rating': forms.RadioSelect(attrs={'class': "rating-area"})
        }


sort_mapping = {
  "Rating": "-total_rating",
  "Price↑": "price",
  "Price↓": "-price",
  "Date": "-created",
}



