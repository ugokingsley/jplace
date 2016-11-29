from django import forms
from django.contrib.auth.models import User

from .models import *





class TestimonySaveForm(forms.Form):
    title = forms.CharField(
        label='Title',
        widget=forms.TextInput(attrs={'size': 64})
    )

    testimony = forms.CharField(
        label='Testimony',
        widget=forms.Textarea (attrs={'id':'ck'})
    )
    tags = forms.CharField(
        label='Tags',
        required=False,
        widget=forms.TextInput(attrs={'size': 64})
    )

    share = forms.BooleanField(
        label='Share on the main page',
        required=False
    )






class SearchForm(forms.Form):
    query = forms.CharField(
        label='Search Jplace',
        widget=forms.TextInput(attrs={'placeholder': 'Enter a keyword to search for'})
    )

class FriendInviteForm(forms.Form):
    name = forms.CharField(label='Friend\'s Name')
    email = forms.EmailField(label='Friend\'s Email')


