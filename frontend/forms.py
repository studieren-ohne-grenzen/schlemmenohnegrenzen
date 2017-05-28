from django import forms
from .choices import plz_choices

class HouseholdForm(forms.Form):
    name1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Dein Name*', 'class': 'form-control'}))
    handy1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Deine Handynummer*', 'class': 'form-control'}))
    email1 = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Deine E-Mail*', 'class': 'form-control'}))
    newsletter1 = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    name2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Sein/Ihr Name*', 'class': 'form-control'}))
    handy2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Seine/Ihre Handynummer*', 'class': 'form-control'}))
    email2 = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Seine/Ihre E-Mail*', 'class': 'form-control'}))
    newsletter2 = forms.BooleanField(initial=True, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    plz = forms.ChoiceField(choices=plz_choices, widget=forms.Select(attrs={'class': 'form-control'}))
    street = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Straße und Hausnummer*', 'class': 'form-control'}))
    note = forms.CharField(max_length=2000, required=False, widget=forms.Textarea(attrs={'placeholder': 'Vegetarisch? Allergien? Hier ist Platz für Nachrichten an eure Gastgeber.', 'class': 'form-control'}))
    accepted_tos = forms.BooleanField(initial=False, required=True, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    kontoinhaber = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'KontoinhaberIn*', 'class': 'form-control'}))
    iban = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'IBAN*', 'class': 'form-control'}))
    bic = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'BIC*', 'class': 'form-control'}))
    captcha = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    personal_payment = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))

    def clean(self):
        cleaned_data = super(HouseholdForm, self).clean()
        personal_payment = cleaned_data.get("personal_payment")
        iban = cleaned_data.get("iban")
        bic = cleaned_data.get("bic")
        kontoinhaber = cleaned_data.get("kontoinhaber")
        if not personal_payment:
            if not iban:
                self.add_error('iban', "Es muss eine gültige IBAN eingegeben werden.")
            if not bic:
                self.add_error('bic', "Es muss eine gültige BIC eingegeben werden.")
            if not kontoinhaber:
                self.add_error('kontoinhaber', "Es muss ein gültiger Kontoinhaber eingegeben werden.")

