from django import forms

class EmailSubscribeForm(forms.Form):
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'votre@email.fr',
            'class': 'lo-email-input',
            'required': True,
        })
    )

class EmailUnsubscribeForm(forms.Form):
    email = forms.EmailField(
        label="Adresse email",
        widget=forms.EmailInput(attrs={
            'placeholder': 'votre@email.fr',
            'class': 'lo-email-input',
            'required': True,
        })
    )
