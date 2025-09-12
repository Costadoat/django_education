from django.urls import path
from django.contrib.auth.decorators import login_required

from .views import JobList, JobCreate, JobDelete, JobUpdate, questionnaire, work_update, WorkDelete

urlpatterns = [
    path('', login_required(JobList.as_view()), name='job-list'),
    path('new', login_required(JobCreate.as_view())),
    path('<str:jobid>/',  login_required(questionnaire)),
    path('<str:pk>/edit',  login_required(JobUpdate.as_view())),
    path('<str:pk>/delete',  login_required(JobDelete.as_view())),
    path('<str:jobid>/<str:workid>',  login_required(work_update)),
    path('<str:pk>/<str:questionid>/delete',  login_required(WorkDelete.as_view())),
]
