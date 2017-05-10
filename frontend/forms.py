from django import forms

class HouseholdForm(forms.Form):
    name1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Dein Name'}))
    handy1 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Deine Handynummer'}))
    email1 = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Deine E-Mail'}))
    newsletter1 = forms.BooleanField(required=False)
    name2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Sein/Ihr Name'}))
    handy2 = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Seine/Ihre Handynummer'}))
    email2 = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Seine/Ihre E-Mail'}))
    newsletter2 = forms.BooleanField(required=False)
    plz = forms.IntegerField()
    street = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Straße und Hausnummer'}))
    note = forms.CharField(max_length=2000, widget=forms.Textarea(attrs={'placeholder': 'Vegetarisch? Allergien? Hier ist Platz für Nachrichten an eure Gastgeber.'}))
    accepted_tos = forms.BooleanField()
