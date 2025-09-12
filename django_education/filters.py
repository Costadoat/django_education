from .models import systeme, type_de_fichier
from django.db import models
import django_filters

class SystemeFiltre(django_filters.FilterSet):
    nom = django_filters.CharFilter(label='Nom du système',lookup_expr='icontains')

    STATUS_CHOICES = []

    liste_fichier=type_de_fichier.objects.all().order_by('nom')
    for fichier in liste_fichier:
        STATUS_CHOICES.append((fichier.id,fichier.nom))
    fichier_systeme__type_de_fichier__id=django_filters.ChoiceFilter(choices=tuple(STATUS_CHOICES),label='Type de ressource', distinct=True)
    
    class Meta:
        model = systeme
        fields = ['nom']
 

       
       
       
