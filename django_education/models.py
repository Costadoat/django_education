# -*- coding:utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

github='https://github.com/Costadoat/'

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class sequence(models.Model):
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return "%02d" % self.numero+' '+self.nom

    def str_numero(self):
        return "%02d" % self.numero

    class Meta:
        ordering = ['numero']


class sequence_info(models.Model):
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.numero)+' '+self.nom

    def str_numero(self):
        return "%02d" % self.numero

    class Meta:
        ordering = ['numero']


class filiere_prepa(models.Model):
    sigle=models.CharField(max_length=30)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return str(self.sigle)

    class Meta:
            ordering = ['id']


class ecole(models.Model):
    sigle=models.CharField(max_length=30)
    nom = models.CharField(max_length=100)


class concours(models.Model):
    filiere = models.ForeignKey('filiere_prepa', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.nom+' ('+str(self.filiere)+')'

    class Meta:
            ordering = ['nom']

class systeme(models.Model):
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    image = models.FileField(upload_to='systemes/')

    def __str__(self):
        return self.nom

    class Meta:
            ordering = ['nom']

class grandeur(models.Model):
    nom = models.CharField(max_length=100)
    unite = models.CharField(max_length=100)

    def __str__(self):
        return self.nom


class parametre(models.Model):
    grandeur = models.ForeignKey('grandeur', on_delete=models.CASCADE)
    valeur = models.FloatField()
    systeme = models.ForeignKey('systeme', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.systeme)+' ('+str(self.grandeur)+')'


class type_de_fichier(models.Model):
    nom = models.CharField(max_length=100)
    icone = models.CharField(max_length=100)
    extension = models.CharField(max_length=100)

    def __str__(self):
        return self.nom

class fichier_systeme(models.Model):
    type_de_fichier = models.ForeignKey('type_de_fichier', on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    nom_fichier = models.CharField(max_length=100)
    systeme = models.ForeignKey('systeme', on_delete=models.CASCADE)
    def __str__(self):
        return str(self.type_de_fichier)+': '+str(self.nom)
    def url_fichier(self):
        return github + 'Sciences-Ingenieur/raw/master/Systemes/' + self.systeme.nom + '/' + \
                  self.nom_fichier + '.' + self.type_de_fichier.extension


class sujet(models.Model):
    concours = models.ForeignKey('concours', on_delete=models.CASCADE)
    annee = models.IntegerField(('year'), validators=[MinValueValidator(1984), max_value_current_year])
    systeme = models.OneToOneField(systeme, on_delete=models.PROTECT, null=True, blank=True)
    SUJET_PT = [('SiA', 'SiA'),('SiB', 'SiB'),('SiC', 'SiC')]
    sujet_pt = models.CharField(max_length=3,choices=SUJET_PT,default='',null=True, blank=True)

    def __str__(self):
        return str(self.systeme)+' ('+str(self.concours)+' '+str(self.annee)+')'

    class Meta:
            ordering = ['systeme__nom']


class famille_competence(models.Model):
    reference = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return str(self.reference)+' '+self.nom

    def image(self):
        return self.nom.lower().replace('é','e')+'.jp2'

class competence(models.Model):
    famille=models.ForeignKey(famille_competence, on_delete=models.CASCADE)
    parent = models.ManyToManyField('self')
    reference = models.CharField(max_length=30)
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    semestre = models.IntegerField()
    active = models.BooleanField()

    def __str__(self):
        return str(self.reference)+' '+self.nom

    class Meta:
        ordering = ['id']


class competence_info(models.Model):
    reference = models.CharField(max_length=30)
    description = models.CharField(max_length=1000)
    active = models.BooleanField()

    def __str__(self):
        return str(self.reference)+' '+self.nom

    class Meta:
        ordering = ['id']


class ressource(models.Model):
    competence = models.ManyToManyField(competence)
    sequence = models.ForeignKey(sequence, on_delete=models.CASCADE)
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    systeme = models.ManyToManyField('systeme')

    def str_numero(self):
        return "%02d" % self.numero


def url(self,matiere,lien,type,ilot):
    if matiere=='si' and ilot==0:
        dossier = github + 'Sciences-Ingenieur/raw/master/' + str("S%02d" % self.sequence.numero) + ' ' + \
          self.sequence.nom + '/' + type + ("%02d" % self.numero) \
          + " " + self.nom + "/"
        if lien == 'git':
           return dossier
        elif lien == 'pdf':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + ".pdf"
        elif lien == 'prive':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + "_prive.pdf"
    elif matiere=='si' and ilot!=0:
        dossier = github + 'Sciences-Ingenieur/raw/master/' + str("S%02d" % self.sequence.numero) + ' ' + \
          self.sequence.nom + '/' + type + ("%02d" % self.numero) \
          + " " + self.nom + '/Ilot_' + ("%02d" % ilot) + " " + str(self.nom_ilot()) + '/'
        if lien == 'git':
           return dossier
        elif lien == 'pdf':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + '-I' + "%02d" % ilot + ".pdf"
        elif lien == 'prive':
            return dossier + str("%02d" % self.sequence.numero) + '-' + type + ("%02d" % self.numero) + '-I' + "%02d" % ilot + "_prive.pdf"
    else:
        if type == 'C':
            nom_type = 'Cours'
        else:
            nom_type = type
        dossier = github + 'Informatique/raw/master/' + nom_type + '/' + type + ("%02d" % self.numero) \
          + " " + self.nom + "/"
        if lien == 'git':
            return dossier
        elif lien == 'pdf':
            return dossier + 'I-' + type + ("%02d" % self.numero) + ".pdf"
        elif lien == 'prive':
            return dossier + 'I-' + type + ("%02d" % self.numero) + "_prive.pdf"
        elif lien == 'python':
            return dossier + 'Code/I-' + type + ("%02d" % self.numero) + ".py"

class cours(ressource):

    def __str__(self):
        return str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"si","pdf","C",0)

    def url_prive(self):
        return url(self,"si","prive","C",0)

    def url_git(self):
        return url(self,"si","git","C",0)



class td(ressource):

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"si","pdf","TD",0)

    def url_prive(self):
        return url(self,"si","prive","TD",0)

    def url_git(self):
        return url(self,"si","git","TD",0)


class tp(ressource):
    ilot = models.IntegerField()

    def nom_ilot(self):
        return self.systeme.all()[0]

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    def str_numero_ilot(self):
        return str("%02d" % self.ilot)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"si","pdf","TP",self.ilot)

    def url_prive(self):
        return url(self,"si","prive","TP",self.ilot)

    def url_git(self):
        return url(self,"si","git","TP",self.ilot)


class khole(ressource):

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"si","pdf","KH",0)

    def url_prive(self):
        return url(self,"si","prive","KH",0)

    def url_git(self):
        return url(self,"si","git","KH",0)


class ressource_info(models.Model):
    sequence = models.IntegerField()
    numero = models.IntegerField()
    nom = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)

    def str_numero(self):
        return "%02d" % self.numero


class cours_info(ressource_info):

    def __str__(self):
        return str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"info","pdf","C",0)

    def url_prive(self):
        return url(self,"info","prive","C",0)

    def url_git(self):
        return url(self,"info","git","C",0)

    def url_python(self):
        return url(self,"info","python","C",0)

class td_info(ressource_info):

    def __str__(self):
        return 'I-'+ self.type +'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"info","pdf","TD",0)

    def url_prive(self):
        return url(self,"info","prive","TD",0)

    def url_git(self):
        return url(self,"info","git","TD",0)

    def url_python(self):
        return url(self,"info","python","TD",0)


class tp_info(ressource_info):

    def __str__(self):
        return 'S'+str("%02d" % self.sequence.numero)+'-'+str("%02d" % self.numero)+' '+self.nom

    def str_numero(self):
        return str("%02d" % self.numero)

    class Meta:
        ordering = ['sequence', 'numero']

    def url_pdf(self):
        return url(self,"info","pdf","TP",0)

    def url_prive(self):
        return url(self,"info","prive","TP",0)

    def url_git(self):
        return url(self,"info","git","TP",0)

    def url_python(self):
        return url(self,"info","python","TP",0)


class matiere(models.Model):
    nom=models.CharField(max_length=100)

    def __str__(self):
        return self.nom

    class Meta:
        ordering = ['id']


class langue_vivante(matiere):
    langue=models.CharField(max_length=100)

    def __str__(self):
        return self.langue

    class Meta:
        ordering = ['id']


class Utilisateur(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.last_name+' '+self.first_name+' ('+self.username+')'


class Etudiant(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)
    ANNEE = [
        ('PTSI', 'PTSI'),
        ('PT', 'PT')
    ]
    annee = models.CharField(
        max_length=4,
        choices=ANNEE,
        default='PTSI',
    )
    lv1 = models.ForeignKey('langue_vivante', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.last_name+' '+self.user.first_name


class Professeur(models.Model):
    user = models.OneToOneField(Utilisateur, on_delete=models.CASCADE, primary_key=True)
    ANNEE = [
        ('PTSI', 'PTSI'),
        ('PTSI/PT', 'PTSI/PT'),
        ('PT', 'PT')
    ]
    annee = models.CharField(
        max_length=7,
        choices=ANNEE,
        default='PTSI',
    )
    matiere = models.ForeignKey('matiere', on_delete=models.PROTECT)

    def __str__(self):
        return self.user.last_name+' '+self.user.first_name


class DS(models.Model):
    TYPE_DE_DS = [
        ('DS', 'DS'),
        ('DM', 'DM'),
        ('Cours', 'Cours'),
        ('CB', 'CB')
    ]
    type_de_ds=models.CharField(
        max_length=5,
        choices=TYPE_DE_DS,
        default='DS',
    )
    numero = models.IntegerField()
    date = models.DateField()
    sujet_support=models.ManyToManyField('sujet', blank=True)
    nb_questions=models.IntegerField()
    nb_parties=models.IntegerField()
    coefficients=models.CharField(max_length=100)
    ajustement=models.FloatField()
    question_parties=models.CharField(max_length=100)
    points_parties=models.CharField(max_length=100)
    moyenne=models.FloatField()
    ecart_type=models.FloatField()

    def __str__(self):
        return str(self.date)+' DS'+str(self.numero)

    class Meta:
        ordering = ['-date']

class Note(models.Model):
    etudiant = models.ForeignKey('Etudiant', on_delete=models.CASCADE)
    numero=models.IntegerField()
    competence = models.ForeignKey('competence', on_delete=models.CASCADE)
    ds = models.ForeignKey('DS', on_delete=models.CASCADE)
    value = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)

    class Meta:
        ordering = ['competence']
