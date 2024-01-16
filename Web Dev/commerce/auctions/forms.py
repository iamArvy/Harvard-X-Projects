from django import forms
from .models import Listings, Categories, Comments

class CreateListingForm(forms.ModelForm):
    cat = forms.ModelChoiceField(queryset=Categories.objects.all(), empty_label="Select a category")

    class Meta:
        model = Listings
        fields = ['title', 'img', 'cat', 'startprice', 'desc']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comments']
