from django import forms
from .models import item_synthese
from django.forms import ModelForm
from captcha.fields import CaptchaField
from datetime import datetime

today = datetime.now()
date_today=today.strftime("%Y-%m-%d")
    
class ContactForm(forms.Form):
    subject = forms.CharField(label="Sujet du message ")
    sender = forms.EmailField(label="Expéditeur (à modifier si besoin) ")
    cc_myself = forms.BooleanField(required=False, label="Envoyer une copie sur mon mail ")
    message = forms.CharField(widget=forms.Textarea)
    captcha = CaptchaField()

CHOICES=[('1','Premier ordre (K,\u03C4)'),('2',u'Second ordre (K,\u03BE,\u03C90)'),('3','Second ordre (K,\u03C91,\u03C92)'),('4','Forme générale'),('5','Exercice simple'),('6','Exercice pas simple')]

class TraceBodeForm(forms.Form):
    format = forms.ChoiceField(choices=CHOICES, widget = forms.RadioSelect(attrs = {
            'onclick' : "this.form.submit();",}))
    
class TraceBodeForm1erordre(forms.Form):
    K = forms.FloatField(label="K", required=False)
    tau = forms.FloatField(label="\u03C4", required=False)

class TraceBodeForm2ndordre1(forms.Form):
    K = forms.FloatField(label="K", required=False)
    xi = forms.FloatField(label="\u03BE", required=False)
    w0 = forms.FloatField(label="\u03C90", required=False)

class TraceBodeForm2ndordre2(forms.Form):
    K = forms.FloatField(label="K", required=False)
    w1 = forms.FloatField(label="\u03C91", required=False)
    w2 = forms.FloatField(label="\u03C92", required=False)

class TraceBodeFormGenerale(forms.Form):
    numerateur = forms.CharField(label="Num", required=False)
    denominateur = forms.CharField(label="Dén", required=False)

class TraceBodeRandom(forms.Form):
    visible = forms.ChoiceField(choices=[('1','Caché'),('2','Visible')], widget = forms.RadioSelect(attrs = {
            'onclick' : "ShowHideAnswer();",}))
    
class ReponseItemSyntheseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        fiche = kwargs.pop('fiche')
        super(ReponseItemSyntheseForm, self).__init__(*args, **kwargs)
        items=item_synthese.objects.filter(fiche_synthese=fiche)
        for item in items:
            self.fields[item.reference()] = forms.CharField(widget=forms.Textarea, required=False)
            self.fields[item.reference()] .widget.attrs['class'] = 'form-control'
            self.fields[item.reference()].help_text = [item.question,item.couleur,item.image]

class FicheSuiviForm(forms.Form):
    date = forms.DateTimeField(
            widget=forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'value': date_today
            })
        )
    note = forms.CharField(label="Note",widget=forms.Textarea)
