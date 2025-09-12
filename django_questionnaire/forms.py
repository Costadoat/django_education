from django import forms
from django.forms.widgets import CheckboxSelectMultiple, Textarea
from django_questionnaire.models import Work_Picture,Work_QCM

class QuestionForm(forms.Form):

    def __init__(self, question, utilisateur, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        choice_list = [x for x in question.get_answers_list()]
        self.fields["answers"] = forms.ChoiceField(choices=choice_list,
                                                   widget=CheckboxSelectMultiple)
        self.fields["status_eleve"] = forms.ChoiceField(choices=question.list_status_eleve)
        if utilisateur.is_teacher:
            self.fields["status_prof"] = forms.ChoiceField(choices=question.list_status_prof)

class QuestionPictureForm(forms.ModelForm):

    class Meta:
        model = Work_Picture
        fields = [
            'commentaire',
            'image',
            'status_eleve',
            'status_prof'
        ]
        widgets = {
            'commentaire': forms.Textarea(attrs={'class': 'form-label rounded'})
        }

    def __init__(self, question, utilisateur, *args, **kwargs):
        super(QuestionPictureForm, self).__init__(*args, **kwargs)
        #if not utilisateur.is_teacher:
        #    field = self.fields['status_prof']
        #    field.widget = field.hidden_widget()

class EssayForm(forms.Form):
    def __init__(self, question, utilisateur, *args, **kwargs):
        super(EssayForm, self).__init__(*args, **kwargs)
        self.fields["answers"] = forms.CharField(
            widget=Textarea(attrs={'style': 'width:100%'}))
