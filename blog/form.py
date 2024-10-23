from django import forms
from .models import Comments, Subscriber

class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ('name', 'email', 'text_comments')




class SubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']


