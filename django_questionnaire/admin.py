from django import forms
from django.contrib import admin
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.translation import gettext_lazy as _

from django_questionnaire.models import Quiz, Question, Question_QCM, Question_QCM_Proposition, Question_Picture, Question_QCM_Proposition, Work_QCM,\
    Work_QCM_Proposition, Job, Work_Picture

class PropositionInline(admin.TabularInline):
    model = Question_QCM_Proposition

class QuestionnaireAdminForm(forms.ModelForm):

    class Meta:
        model = Quiz
        exclude = []

    questions = forms.ModelMultipleChoiceField(
        queryset=Question_QCM.objects.all(),
        required=False,
        label=_("Questions"),
        widget=FilteredSelectMultiple(
            verbose_name=_("Questions"),
            is_stacked=False))

    def __init__(self, *args, **kwargs):
        super(QuestionnaireAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['questions'].initial =\
                self.instance.question_set.all()

    def save(self, commit=True):
        quiz = super(QuestionnaireAdminForm, self).save(commit=False)
        quiz.save()
        quiz.question_set.set(self.cleaned_data['questions'])
        self.save_m2m()
        return quiz

def duplicate_questionnaire(ModelAdmin, request, queryset):

    for object in queryset:
        object.duplicate()

    duplicate_questionnaire.short_description = "Dupliquer l'enregistrement"

class QuestionnaireAdmin(admin.ModelAdmin):
    form = QuestionnaireAdminForm

    list_display = ('title', 'sequence', )
    list_filter = ('sequence',)
    search_fields = ('description', 'sequence', )
    actions = [duplicate_questionnaire]

def duplicate_question_qcm(ModelAdmin, request, queryset):

    for object in queryset:
        object.duplicate(object.quiz)

    duplicate_question_qcm.short_description = "Dupliquer l'enregistrement"

def duplicate_question_picture(ModelAdmin, request, queryset):

    for object in queryset:
        object.duplicate(object.quiz)

    duplicate_question_qcm.short_description = "Dupliquer l'enregistrement"

class QuestionChoixMultiplesAdmin(admin.ModelAdmin):
    list_display = ('quiz','num','texte', )
    list_filter = ()
#    fields = ('texte', 'figure', 'quiz', 'explication', 'answer_order')

    search_fields = ('question', 'explication')
    inlines = [PropositionInline]
    actions = [duplicate_question_qcm]

class QuestionPictureAdmin(admin.ModelAdmin):
    list_display = ('quiz','num','texte',)
    list_filter = ()
#    fields = ('texte', 'figure', 'quiz', 'explication', 'answer_order')

    search_fields = ('question', 'explication')
    actions = [duplicate_question_picture]

#class ProgressAdmin(admin.ModelAdmin):
#    """
#    to do:
#            create a user section
#    """
#    search_fields = ('user', 'score', )


#class TFQuestionAdmin(admin.ModelAdmin):
#    list_display = ('content', 'category', )
#    list_filter = ('category',)
#    fields = ('content', 'category', 'sub_category',
#              'figure', 'quiz', 'explanation', 'correct',)
#
#    search_fields = ('content', 'explanation')
#    filter_horizontal = ('quiz',)


class WorkPropositionInline(admin.TabularInline):
    model = Work_QCM_Proposition

class WorkChoixMultiplesAdmin(admin.ModelAdmin):
#    list_display = (, )
    list_filter = ()
#    fields = ('texte', 'figure', 'quiz', 'explication', 'answer_order')

    search_fields = ('question', 'explication')

    inlines = [WorkPropositionInline]


#class ProgressAdmin(admin.ModelAdmin):
#    """
#    to do:
#            create a user section
#    """
#    search_fields = ('user', 'score', )


#class TFQuestionAdmin(admin.ModelAdmin):
#    list_display = ('content', 'category', )
#    list_filter = ('category',)
#    fields = ('content', 'category', 'sub_category',
#              'figure', 'quiz', 'explanation', 'correct',)
#
#    search_fields = ('content', 'explanation')
#    filter_horizontal = ('quiz',)


admin.site.register(Quiz, QuestionnaireAdmin)
admin.site.register(Question_Picture, QuestionPictureAdmin)
admin.site.register(Job)
admin.site.register(Question_QCM, QuestionChoixMultiplesAdmin)
admin.site.register(Work_QCM, WorkChoixMultiplesAdmin)
admin.site.register(Work_Picture)
