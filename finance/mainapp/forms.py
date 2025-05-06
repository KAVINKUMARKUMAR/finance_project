from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={'class': 'forms', 'placeholder': 'Name *'}),
            "email": forms.EmailInput(attrs={'class': 'forms', 'placeholder': 'Email Address *'}),
            "phone_code": forms.Select(attrs={'class': 'forms'}),
            "phone": forms.TextInput(attrs={'class': 'forms', 'placeholder': 'e.g. 0444444444 *'}),
            "service": forms.Select(attrs={'class': 'forms'}),
            "desc": forms.Textarea(attrs={'class': 'forms', 'placeholder': 'Your Message'}),
        }
