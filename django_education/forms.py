from django import forms
from .models import item_synthese
from django.forms import ModelForm
from captcha.fields import CaptchaField

class ContactForm(forms.Form):
    subject = forms.CharField(label="Sujet du message ")
    sender = forms.EmailField(label="Expéditeur (à modifier si besoin) ")
    cc_myself = forms.BooleanField(required=False, label="Envoyer une copie sur mon mail ")
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()
    
class ReponseItemSyntheseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fiche = kwargs.pop('fiche')
        super(ReponseItemSyntheseForm, self).__init__(*args, **kwargs)
        items=item_synthese.objects.filter(fiche_synthese=fiche)
        for item in items:
            self.fields[item.reference()] = forms.CharField(widget=forms.Textarea, required=False)
            self.fields[item.reference()] .widget.attrs['class'] = 'form-control'
            self.fields[item.reference()].help_text = [item.question,item.couleur,item.image]
