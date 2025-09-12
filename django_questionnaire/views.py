from django.shortcuts import render, redirect, HttpResponseRedirect
from django_questionnaire.forms import QuestionForm, QuestionPictureForm
from django_education.models import Etudiant, Utilisateur, Professeur
from django_education.views import rentree_scolaire
from django_questionnaire.models import Job,Question, Question_QCM, Quiz, Work, Job, Work_QCM, Work_QCM_Proposition,\
    Work_Picture
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from datetime import datetime, timedelta
from dateutil import tz

def decaler_heure(job_heure,heure,minute):
    to_zone = tz.tzutc()
    from_zone = tz.gettz('Europe/Paris')
    return job_heure.replace(hour=heure).replace(minute=minute).replace(tzinfo=from_zone).astimezone(to_zone)

class JobList(ListView):
    model = Job
    template_name = "questionnaire/questionnaires.html"
    def get_queryset(self):
        queryset = Job.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jobs_all=Job.objects.all().values('created_at__date').annotate(total=Count('id')).order_by('-created_at__date')
        date_1=rentree_scolaire().strftime("%Y-%m-%d")
        date_2=(rentree_scolaire()+timedelta(days=365)).strftime("%Y-%m-%d")
        print(date_1)
        jobs_all=Job.objects.filter(created_at__range=[date_1,date_2]).values('created_at__date').annotate(total=Count('id')).order_by('-created_at__date')
        print(jobs_all)
        all_jobs=[]
        for date in jobs_all:
            jobs_by_date=Job.objects.filter(created_at__date=date['created_at__date'])
            all_jobs.append([date['created_at__date'],{'8h':[],'10h30':[],'autre':[]}])
            for job in jobs_by_date:
                if job.created_at>decaler_heure(job.created_at,8,0) \
                        and job.created_at<decaler_heure(job.created_at,10,30) :
                    all_jobs[-1][1]['8h'].append(job)
                elif job.created_at>decaler_heure(job.created_at,10,30) \
                        and job.created_at<decaler_heure(job.created_at,13,0):
                    all_jobs[-1][1]['10h30'].append(job)
                else:
                    all_jobs[-1][1]['autre'].append(job)
        context["all_jobs"] = all_jobs
        return context

class JobCreate(CreateView):
    model = Job
    fields = ['quiz', 'user']
    success_url = reverse_lazy('job-list')
    template_name = "questionnaire/job_form.html"

    def get_form(self):
        form = super(JobCreate,self).get_form()
        form.fields['user'].queryset = Utilisateur.objects.filter(etudiant__annee='PTSI')
        return form

class JobUpdate(UpdateView):
    model = Job
    fields = ['user']
    template_name = "questionnaire/job_form.html"
    success_url = reverse_lazy("job-list")

class JobDelete(DeleteView):
    model = Job
    success_url = reverse_lazy("job-list")
    template_name = "questionnaire/job_delete_form.html"

class WorkDelete(DeleteView):
    model = Work
    success_url = reverse_lazy("questionnaire/"+str(Work.job_id))
    template_name = "questionnaire/work_delete_form.html"

def questionnaire(request,jobid):
    # if this is a POST request we need to process the form data
    job=Job.objects.get(id=jobid)
    quiz=job.quiz
    works=[]
    for question in quiz.get_questions():
        subclass=question.get_sub_class()
        current_work=subclass[1].objects.get_or_create(job=job,question=question)[0]
        if subclass[0]==Question_QCM: # c'est un QCM
            for prop in subclass[2]:
                current_work_prop=Work_QCM_Proposition.objects.get_or_create(work=current_work,proposition=prop)[0]
        works.append(current_work)
    return render(request, 'questionnaire/questionnaire.html', {'job': job,'works': works})

def work_update(request,jobid,workid):
    # if this is a POST request we need to process the form data
    job=Job.objects.get(id=jobid)
    work=Work.objects.get_subclass(id=workid)
    result=''
    if request.method == 'POST':
        result=dict(request.POST)
        if (isinstance(work,Work_QCM)):
            if 'answers' in result.keys():
                work.set_prop_answers_list(result['answers'])
        elif (isinstance(work,Work_Picture)):
            form = QuestionPictureForm(work,request.user, request.POST,request.FILES,instance=work)
            if form.is_valid():
                work = form.save(commit=False)
                work.job = job
                work.question=work.question
                work.save()
        work.status_eleve=request.POST['status_eleve']
        if request.user.is_student:
            work.eleve=request.user.etudiant
        if 'status_prof' in result.keys():
            work.status_prof=request.POST['status_prof']
            if request.user.is_teacher:
                work.prof=request.user.professeur
        work.save()
    if (isinstance(work,Work_QCM)):
        props_set=work.get_prop_answers_list()
        form = QuestionForm(work,request.user,initial={'answers':props_set,'status_eleve':work.status_eleve,'status_prof':work.status_prof})
    elif (isinstance(work,Work_Picture)):
            form = QuestionPictureForm(work, request.user,initial={'image':work.image,'commentaire':work.commentaire,'status_eleve':work.status_eleve,'status_prof':work.status_prof})
    if result!='':
        if 'button' in result.keys():
            if result['button'][0]=='Next':
                return HttpResponseRedirect('/'.join(['/questionnaires',str(work.job.id),str(work.next_work().id)]))
            elif result['button'][0]=='Previous':
                return HttpResponseRedirect('/'.join(['/questionnaires',str(work.job.id),str(work.previous_work().id)]))

    return render(request, 'questionnaire/question.html', {'job': job,'work': work, 'form': form,\
                                'previous_item': work.previous_work(), 'next_item': work.next_work()})
