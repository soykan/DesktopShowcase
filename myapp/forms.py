from django import forms

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=255, min_length=4)
    content = forms.CharField(widget=forms.Textarea, max_length=1000, required=False)
    photo = forms.ImageField()