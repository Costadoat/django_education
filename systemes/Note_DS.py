# -*- coding: utf-8 -*-
from time import gmtime, strftime
import datetime
from django.utils import timezone
import django
import sys
import os
sys.path.append(os.path.abspath("/home/renaud/Documents/Renaud/GitHub/django_education/"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'django_education.settings'
django.setup()
from django_education.models import Etudiant, DS, competence, Note, systeme

import os, sys

# Open a file
path = "."
dir = os.listdir( path )
fichiers=[]
exts=[]

for file in dir:
    fichiers.append(file.split('.')[0])
    exts.append(file.split('.')[1])

systemes = systeme.objects.all()

# This would print all the files and directories
for systeme in systemes:
    if systeme.nom!='E.P.A.S':
        nom=systeme.nom.replace(' ','_').replace(':','').replace("'","")
        ext=exts[fichiers.index(nom)]
        nom_image='static/systemes/'+nom+'.'+ext
        systeme.image=nom_image
        systeme.save()
