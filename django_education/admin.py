from django.contrib import admin
from .models import sequence, filiere_prepa, ecole, concours, sujet, systeme, cours, td, tp, ilot, matiere, langue_vivante,\
    Etudiant, Professeur, Utilisateur, cours_info, td_info, tp_info, khole, DS, Note, parametre,\
    grandeur, type_de_fichier, type_image_systeme, fichier_systeme, image_systeme, video, videoyoutube, fiche_synthese, item_synthese,\
    reponse_item_synthese, seance, reglage_date, application, sequence_info, note_suivi, tp_data, AutoEvaluation

from django_quiz.multichoice.models import MCQuestion, Answer
from django_quiz.quiz.models import Question
from django_quiz.quiz.admin import AnswerInline
from django import forms

class ParametreInline(admin.TabularInline):
    model=parametre

class FichierInline(admin.TabularInline):
    model=fichier_systeme

class ImageInline(admin.TabularInline):
    model=image_systeme


class SystemeAdmin(admin.ModelAdmin):
    inlines=[
        ParametreInline,
        FichierInline,
        ImageInline
    ]

def duplicate_mcquestion(ModelAdmin, request, queryset):
    for object in queryset:
        ordre=object.answer_order
        reponses=Answer.objects.filter(question_id=object.question_ptr_id)
        new_question=Question.objects.get(id=object.question_ptr_id)
        quizzes=new_question.quiz.all()
        new_question.id=None
        new_question.save()
        new_question.quiz.set(quizzes)
        new_mcquestion=MCQuestion.objects.get(question_ptr_id=object.question_ptr_id)
        new_mcquestion.id=None
        new_mcquestion.question_ptr_id=new_question.id
        new_mcquestion.answer_order=ordre
        new_mcquestion.save()
        for reponse in reponses:
            reponse.id=None
            reponse.question_id=new_question.id
            reponse.save()
duplicate_mcquestion.short_description = "Dupliquer l'enregistrement"

class MCQuestionAdmin(admin.ModelAdmin):
    list_display = ('content', 'category', )
    list_filter = ('category',)
    fields = ('content', 'category', 'sub_category',
              'figure', 'quiz', 'explanation', 'answer_order')

    search_fields = ('content', 'explanation')
    filter_horizontal = ('quiz',)

    inlines = [AnswerInline]

    actions = [duplicate_mcquestion]

def duplicate_video(ModelAdmin, request, queryset):
    for object in queryset:
        comps=[]
        for comp in object.competence.all():
            comps.append(comp)
        object.id=None
        object.save()
        for comp in comps:
            object.competence.add(comp)
        object.save()
duplicate_video.short_description = "Dupliquer l'enregistrement"

class VideoAdmin(admin.ModelAdmin):
    actions = [duplicate_video]

class ItemSyntheseAdmin(admin.ModelAdmin):
    model = item_synthese
    list_display = ['get_question']

    def get_question(self, obj):
        return str(obj.short_name())+' '+str(obj.question)
    get_question.short_description = 'Question'

admin.site.register(sequence)
admin.site.register(sequence_info)
admin.site.register(filiere_prepa)
admin.site.register(ecole)
admin.site.register(concours)
admin.site.register(sujet)
admin.site.register(fiche_synthese)
admin.site.register(item_synthese, ItemSyntheseAdmin)
admin.site.register(reponse_item_synthese)
admin.site.register(grandeur)
admin.site.register(type_de_fichier)
admin.site.register(type_image_systeme)
admin.site.register(systeme, SystemeAdmin)
admin.site.unregister(MCQuestion)
admin.site.register(MCQuestion, MCQuestionAdmin)
admin.site.register(td)
admin.site.register(tp)
admin.site.register(tp_data)
admin.site.register(ilot)
admin.site.register(cours_info)
admin.site.register(td_info)
admin.site.register(tp_info)
admin.site.register(matiere)
admin.site.register(seance)
admin.site.register(reglage_date)
admin.site.register(langue_vivante)
admin.site.register(Utilisateur)
admin.site.register(Etudiant)
admin.site.register(AutoEvaluation)
admin.site.register(Professeur)
admin.site.register(cours)
admin.site.register(khole)
admin.site.register(DS)
admin.site.register(Note)
admin.site.register(note_suivi)
admin.site.register(video, VideoAdmin)
admin.site.register(videoyoutube)
admin.site.register(application)

