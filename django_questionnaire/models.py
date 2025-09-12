from __future__ import unicode_literals

import datetime
import re
import json

from django.db import models
from django.utils.timezone import now as nowtz
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.core.validators import (
    MaxValueValidator, validate_comma_separated_integer_list,
)
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now
from six import python_2_unicode_compatible
from django.conf import settings

from django_education.models import sequence, competence, ressource, systeme, Etudiant, Professeur, Utilisateur

from model_utils.managers import InheritanceManager

list_status_eleve = (
    ('NVALI','Non validé'),
    ('BASSI',"Besoin d'assistance"),
    ('VALID','Validé')
)

class Quiz(models.Model):
    title = models.CharField(verbose_name="Titre",max_length=60, blank=False)
    description = models.TextField(verbose_name="Description",blank=True, help_text="Description du questionnaire")
    url = models.SlugField(max_length=60, blank=False,help_text="a user friendly url",verbose_name="user friendly url")
    sequence = models.ForeignKey(sequence, null=True, blank=True,verbose_name="Sequence", on_delete=models.CASCADE)
    competences = models.ManyToManyField(competence, blank=True,verbose_name="Competences")
    ressources = models.ManyToManyField(ressource, blank=True,verbose_name="Ressources")
    systeme = models.ForeignKey(systeme, null=True, blank=True,verbose_name="Systeme", on_delete=models.CASCADE)

#    class Meta:
#        verbose_name = "Questionnaire"
#        verbose_name_plural = "Questionnaires"

    def toutes_ressources(self):
        return ', '.join([str(el) for el in self.ressources.all()])

    def __str__(self):
        return '('+self.toutes_ressources()+') ('+self.systeme.nom+')'

    def get_questions(self):
        return self.question_set.all().select_subclasses()

    def get_orders(self):
        return [question.num for question  in self.get_questions()]

    def get_question(self,num):
        return self.question_set.get(num=num)

    def duplicate(self):
        new_quiz=Quiz.objects.create(title=self.title,description=self.description,url=self.url,\
                                                sequence=self.sequence,systeme=self.systeme)
        for competence in self.competences.all():
            new_quiz.competences.add(competence)
        for ressource in self.ressources.all():
            new_quiz.ressources.add(ressource)

        questions_qcm=Question_QCM.objects.filter(quiz=self.id)
        for question in questions_qcm:
            question.duplicate(quiz=new_quiz)
        questions_picture=Question_Picture.objects.filter(quiz=self.id)
        for question in questions_picture:
            question.duplicate(quiz=new_quiz)

class Question(models.Model):

    quiz = models.ForeignKey(Quiz,verbose_name="Questionnaire", on_delete=models.CASCADE)
    num = models.IntegerField(verbose_name="Numero", help_text="numero de la question")
    figure = models.ImageField(upload_to='uploads/%Y/%m/%d',blank=True,null=True,verbose_name="Figure")
    texte = models.TextField(max_length=1000,blank=False,help_text="Enter the question text",verbose_name='Question')
    explication = models.TextField(max_length=2000,blank=True,help_text="Explanation to be shown ",verbose_name='Explanation')
    objects = InheritanceManager()

    list_status_eleve=list_status_eleve

    class Meta:
#        verbose_name = "Question"
#        verbose_name_plural = "Questions"
        ordering = ['quiz','num']

    def get_sub_class(self):
        if hasattr(self, 'question_qcm'):
            props=Question_QCM_Proposition.objects.filter(question=self.question_qcm)
            return Question_QCM,Work_QCM,props
        elif hasattr(self, 'question_picture'):
            return Question_Picture,Work_Picture

    def __str__(self):
        return self.quiz.title+' '+str(self.num)+' '+self.texte

    def next_question(self):
        if self.quiz.get_orders().index(self.num)<len(self.quiz.get_orders())-1:
            next_num=self.quiz.get_orders()[self.quiz.get_orders().index(self.num)+1]
            return Question.objects.get(quiz=self.quiz,num=next_num)
        else:
            return None

    def previous_question(self):
        if self.quiz.get_orders().index(self.num)>0:
            previous_num=self.quiz.get_orders()[self.quiz.get_orders().index(self.num)-1]
            return Question.objects.get(quiz=self.quiz,num=previous_num)
        else:
            return None

class Job(models.Model):
    quiz = models.ForeignKey(Quiz, verbose_name="Questionnaire", on_delete=models.CASCADE)
    user = models.ManyToManyField(Utilisateur,blank=False,verbose_name="Etudiant")
    created_at = models.DateTimeField(default=nowtz)

    def tous_eleves(self):
        return ', '.join([str(el.name_short()) for el in self.user.all()])

    def __str__(self):
        return self.quiz.title+' ('+self.tous_eleves()+')'

class Work(models.Model):
    job = models.ForeignKey(Job, verbose_name="Activité", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, verbose_name="Question", on_delete=models.CASCADE)
    objects = InheritanceManager()

    list_status_eleve=list_status_eleve

    status_eleve = models.CharField(
        max_length=10,
        choices=list_status_eleve,
        default='NVALI',
    )
    list_status_prof = (
        ('NVALI','Non validé'),
        ('VALID','Validé')
    )

    status_prof = models.CharField(
        max_length=10,
        choices=list_status_prof,
        default='NVALI',
    )
    prof = models.ForeignKey(Professeur, verbose_name="Prof", on_delete=models.CASCADE,blank=True,null=True)
    eleve = models.ForeignKey(Etudiant, verbose_name="Eleve", on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.job.id)+'.'+str(self.id)+' - '+self.question.texte

    def previous_work(self):
        try :
            result=Work.objects.get(question=self.question.previous_question(),job=self.job)
        except:
            result=None
        return result

    def next_work(self):
        try :
            result=Work.objects.get(question=self.question.next_question(),job=self.job)
        except:
            result=None
        return result

class Question_Picture(Question):



    def duplicate(self,quiz):
        new_question=Question_Picture.objects.create(quiz=quiz,num=self.num,figure=self.figure,\
                                                texte=self.texte,explication=self.explication)

class Question_QCM(Question):

#    def check_if_correct(self, guess):
#        answer = Answer_MC.objects.get(id=guess)
#
#        if answer.correct is True:
#            return True
#        else:
#            return False

#    def order_answers(self, queryset):
#        if self.answer_order == 'content':
#            return queryset.order_by('content')
#        if self.answer_order == 'random':
#            return queryset.order_by('?')
#        if self.answer_order == 'none':
#            return queryset.order_by()
#        return queryset

#    def get_answers(self):
#        return self.order_answers(Answer_MC.objects.filter(question=self))

    def get_answers_list(self):
        return [(answer.id, answer.content) for answer in Question_QCM_Proposition.objects.filter(question=self)]

#    def answer_choice_to_string(self, guess):
#        return Answer_MC.objects.get(id=guess).content

#    class Meta:
#        verbose_name = "Question à choix multiples"
#        verbose_name_plural = "Questions à choix multiples"

    def duplicate(self,quiz):
        new_question=Question_QCM.objects.create(quiz=quiz,num=self.num,figure=self.figure,\
                                                texte=self.texte,explication=self.explication)
        reponses=Question_QCM_Proposition.objects.filter(question__id=self.id)
        for reponse in reponses:
            reponse.id=None
            reponse.question=new_question
            reponse.save()

class Question_QCM_Proposition(models.Model):

    question = models.ForeignKey(Question_QCM, verbose_name="Question", on_delete=models.CASCADE)
    content = models.CharField(max_length=1000,blank=False,help_text="Enter the answer text",verbose_name="Content")
    correct = models.BooleanField(blank=False,default=False,help_text="Is this a correct answer?",verbose_name="Correct")

    def __str__(self):
        return self.content

class Work_QCM(Work):

    def __str__(self):
        return self.question.texte

    def get_answers_list(self):
        return [(answer.id, answer.proposition) for answer in Work_QCM_Proposition.objects.filter(work=self)]

    def get_prop_answers_list(self):
        list_idx=[]
        for answer in Work_QCM_Proposition.objects.filter(work=self):
            if answer.answer==True:
                list_idx.append(str(answer.id))
        return list_idx

    def set_prop_answers_list(self,liste):
        for elt in Work_QCM_Proposition.objects.filter(work=self):
            if str(elt.id) in liste:
                elt.answer=True
            else:
                elt.answer=False
            elt.save()

    def clear_prop_answers_list(self,):
        for elt in Work_QCM_Proposition.objects.filter(work=self):
            elt.answer=False
            elt.save()


class Work_QCM_Proposition(models.Model):

    work = models.ForeignKey(Work_QCM, verbose_name="Travail", on_delete=models.CASCADE)
    proposition = models.ForeignKey(Question_QCM_Proposition, verbose_name="Proposition", on_delete=models.CASCADE)
    answer = models.BooleanField(blank=False,default=False,help_text="Réponse de l'élève",verbose_name="Réponse")

    def __str__(self):
        return self.proposition.content

def work_picture_url(instance, filename):
    return '/'.join(['uploads/travail_eleve', str(instance.job.id),str(instance.id), filename])

class Work_Picture(Work):
    image=models.ImageField(upload_to=work_picture_url,blank=True)
    commentaire = models.TextField(verbose_name="Commentaire",blank=True)

    def __str__(self):
        return self.question.texte
