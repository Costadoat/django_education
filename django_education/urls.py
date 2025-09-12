from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django_filters.views import FilterView
from .filters import SystemeFiltre
from django.contrib.sitemaps.views import sitemap
from .sitemaps import SequenceSitemap, SystemeSitemap, CompetenceSitemap

from .views import index, upload_eleves,\
    lister_ressources_si, afficher_sequence_si, lister_ressources_info, afficher_sequence_info, lister_competences,\
    afficher_famille_competence,  afficher_competence, relative_url_view, relative_url_view_systeme,\
    resultats, resultats_vierge, details, autoevaluationlistseq, autoevaluationsave, ds_eleve,\
    resultats_quizz, resultats_quizz_eleve,contact, thanks, afficher_systeme, lister_ds_si,\
    afficher_sysml, relative_url_sysml, relative_url_sysml_app, relative_url_image_sysml, afficher_sequence_videos,\
    afficher_ressource_videos, fiche_ressource_edit, fiche_ressource_display, generer_fiche_synthese_PDF,\
    liste_fiches_ressource, progression, fiche_suivi

from .applications import compute, interface_tp, app

sitemaps = {
    "sequences": SequenceSitemap,
    "systemes": SystemeSitemap,
    "competences": CompetenceSitemap,
}

app_name = 'registration'
urlpatterns = [
   path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('password-change-done/',
        auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
        name='password_change_done'
    ),
    path('password-change/',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'
    ),
    path('password-change/',
        auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
        name='password_change'
    ),
    path('si/<int:id_sequence>/', afficher_sequence_si),
    path('si/tp', interface_tp),
    path('compute/<int:id_app>/', compute, name="compute"),
    path('si/<int:id_sequence>/app/<int:id_app>/', app),
    path('si/<int:id_sequence>/<int:id_ressource>/fiche_ressource/edit', fiche_ressource_edit),
    path('si/<int:id_sequence>/<int:id_ressource>/fiche_ressource/pdf', generer_fiche_synthese_PDF),
    path('si/<int:id_sequence>/<int:id_ressource>/fiche_ressource/', fiche_ressource_display),
    path('si/<int:id_etudiant>/<int:id_sequence>/<int:id_ressource>/fiche_ressource/edit', fiche_ressource_edit),
    path('si/<int:id_etudiant>/<int:id_sequence>/<int:id_ressource>/fiche_ressource/pdf', generer_fiche_synthese_PDF, name='totot'),
    path('si/<int:id_etudiant>/<int:id_sequence>/<int:id_ressource>/fiche_ressource/', fiche_ressource_display),
    path('mes_fiches_ressource/', liste_fiches_ressource),
    path('si/<int:id_sequence>/videos/', afficher_sequence_videos),
    path('si/<int:id_sequence>/r<int:id_ressource>/videos/', afficher_ressource_videos),
#    path('info/<int:id_sequence>/', afficher_sequence_info),
    path('info/', afficher_sequence_info),
    path('si/ds/', lister_ds_si),
    path('si/progression/', progression),
    path('si/', lister_ressources_si),
#    path('info/', lister_ressources_info),
    path('competences', lister_competences),
    path('systemes/', FilterView.as_view(filterset_class=SystemeFiltre,
            template_name='systemes.html'), name='lister_systemes'),
    path('systeme/<int:id_systeme>/', afficher_systeme),
    path('systeme/<int:id_systeme>/sysml', afficher_sysml),
    path('systeme/<int:id_systeme>/images/<str:data>', relative_url_image_sysml),
    path('systeme/<int:id_systeme>/app/view/<str:fichier>', relative_url_sysml_app),
    path('systeme/<int:id_systeme>/<str:dossier>/<str:data>', relative_url_sysml),
    path('competence/<int:id_famille>/', afficher_famille_competence),
    path('competence/<int:id_famille>/<int:id_competence>/', afficher_competence),
    path('uploads/<str:year>/<str:month>/<str:day>/<str:nom>.<str:ext>', relative_url_view),
    path('admin/django_education/systeme/<str:id_systeme>/<str:action>/systemes/<str:nom>.<str:ext>', relative_url_view_systeme),
    path('admin/multichoice/mcquestion/<str:nomquiz>/<str:action>/uploads/<str:year>/<str:month>/<str:day>/<str:nom>.<str:ext>', relative_url_view),
    path('resultats/<int:id_etudiant>/ds/', ds_eleve),
    path('resultats/<int:id_etudiant>/details/', details),
    path('resultats/<int:id_etudiant>/autoevaluation/<int:id_sequence>/', autoevaluationlistseq),
    path('resultats/<int:id_etudiant>/autoevaluation/<int:id_sequence>/save/', autoevaluationsave),
    path('resultats/details/', details),
    path('resultats/<int:id_etudiant>/', resultats),
    path('resultats/', resultats_vierge),
    path('resultats_quizz/', resultats_quizz),
    path('mes_resultats_quizz/', resultats_quizz_eleve),
    path('q/', include('django_quiz.quiz.urls')),
    path('questionnaires/', include('django_questionnaire.urls')),
    path('upload_eleves/', upload_eleves),
    path('fiche_suivi/<int:id_etudiant>/', fiche_suivi),
    path('fiche_suivi/', fiche_suivi),
    path('contact/', contact),
    path('', index),
    path('thanks/', thanks),
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
