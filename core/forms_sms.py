from django import forms

class SmsSubscribeForm(forms.Form):
    phone = forms.CharField(
        label="Numéro de téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '06 12 34 56 78',
            'class': 'lo-sms-input',
            'type': 'tel',
            'pattern': '[0-9 +]{10,15}',
            'required': True,
        })
    )

class SmsUnsubscribeForm(forms.Form):
    phone = forms.CharField(
        label="Numéro de téléphone",
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': '06 12 34 56 78',
            'class': 'lo-sms-input',
            'type': 'tel',
            'pattern': '[0-9 +]{10,15}',
            'required': True,
        })
    )
