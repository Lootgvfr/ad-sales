from django import forms

class FileForm(forms.Form):
    img = forms.FileField(label='Виберіть зображення макету ')