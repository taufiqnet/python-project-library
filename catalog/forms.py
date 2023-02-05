from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime  # for checking renewal date range.

from django import forms
from catalog.models import Author


class RenewBookForm(forms.Form):
    """Form for a librarian to renew books."""
    renewal_date = forms.DateField(
            help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        # Check date is not in past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        # Check date is in range librarian allowed to change (+4 weeks)
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(
                _('Invalid date - renewal more than 4 weeks ahead'))

        # Remember to always return the cleaned data.
        return 
    
class AuthorForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    date_of_birth = forms.DateField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    date_of_death = forms.DateField(widget=forms.TextInput(
        attrs={
            'class': 'form-control'
        }
    ))
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
        initial = {'date_of_death': '11/06/2020'}
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].label = 'First Name'
            self.fields['last_name'].label = 'Last Name'
            self.fields['date_of_birth'].label = 'Date of Birth'
            self.fields['date_of_death'].label = 'Date of Death'
        
        widget = {
            'first_name': forms.TextInput(attrs={'class':'form-control'}),
            'last_name': forms.TextInput(attrs={'class':'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class':'form-control'}),
            'date_of_death': forms.DateInput(attrs={'class':'form-control'})
        }
    