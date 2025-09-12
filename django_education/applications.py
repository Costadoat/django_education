from numpy import arange, linspace, square, sqrt, angle, cos, sin, arccos, arcsin, exp, log10, arange, absolute
from django.shortcuts import render, redirect, HttpResponseRedirect
from cmath import phase
from .forms import TraceBodeForm, TraceBodeForm1erordre, TraceBodeForm2ndordre1,\
    TraceBodeForm2ndordre2, TraceBodeFormGenerale, TraceBodeRandom
from jchart import Chart
from random import randrange
from jchart.config import Axes, DataSet, rgba
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse

# Get the uploaded files
def uploadFiles():
      # get the uploaded file
      uploaded_file = request.files['file']
      if uploaded_file.filename != '':
          print(uploaded_file)
          # save the file
      return redirect(url_for('index'))

def interface_tp(request):
    sliders=[
        {'name':'K','label':'K (?)','target': '#K','val': [i/10 for i in range(1,101)],'set': [1]},
        {'name':'xi','label':'xi','target': '#xi','val': [i/20 for i in range(1,21)]+[i/20 for i in range(21,200)],'set': [1]},
        {'name':'w0','label':'w0 (rad/s)','target': '#w0','val': [10*i for i in range(1,100)], 'set': [500]},
        {'name':'tau','label':'tau (ms)','target': '#tau','val': [5*i for i in range(1,100)],'set': [100]},
    ]
    return render(request, 'interface_tp.html', {'sliders':sliders})

def const_conv(val):
    return float(val.replace(',','.'))

@csrf_exempt
def calcul_temporel(request):
    E0=1
    ordre1 = request.POST.get("sourceordre_premier_ordre")
    ordre2 = request.POST.get("sourceordre_second_ordre")
    identification = request.POST.get("sourceordre_identification")
    duree = request.POST.get("duree")
    duree=float(duree)
    t=linspace(0,duree,1000)
    if ordre1=='true':
        K = request.POST.get("K")
        tau = request.POST.get("tau")
        K=float(K)
        tau=float(tau)
        y=K*E0*(1-exp(-t*1000/tau))
    elif ordre2=='true':
        K = request.POST.get("K")
        w0 = request.POST.get("w0")
        xi = request.POST.get("xi")
        K=float(K)
        xi=float(xi)
        w0=float(w0)
        if xi<1:
            y=K*E0*(1-exp(-w0*xi*t)/sqrt(1-xi**2)*sin(w0*sqrt(1-xi**2)*t+arccos(xi)))
        elif xi>1:
            p1=-xi*w0-w0*sqrt(xi**2-1)
            p2=-xi*w0+w0*sqrt(xi**2-1)
            y=K*E0*(1-1/(2*sqrt(xi**2-1))*(exp(p1*t)/p1-exp(p2*t)/p2))
        else:
            y=K*E0*(1-(1 + t*w0)*exp(-t*w0))
    elif identification=='true':
        ordre = float(request.POST.get("def_ordre"))
        K = const_conv(request.POST.get("def_K"))
        xi = const_conv(request.POST.get("def_xi"))
        w0 = const_conv(request.POST.get("def_w0"))
        tau = const_conv(request.POST.get("def_tau"))
        if ordre==1:
            y=K*E0*(1-exp(-t*1000/tau))
        elif ordre==2:
            if xi<1:
                y=K*E0*(1-exp(-w0*xi*t)/sqrt(1-xi**2)*sin(w0*sqrt(1-xi**2)*t+arccos(xi)))
            elif xi>1:
                p1=-xi*w0-w0*sqrt(xi**2-1)
                p2=-xi*w0+w0*sqrt(xi**2-1)
                y=K*E0*(1-1/(2*sqrt(xi**2-1))*(exp(p1*t)/p1-exp(p2*t)/p2))
            else:
                y=K*E0*(1-(1 + t*w0)*exp(-t*w0))
    keys_list=['x','y']
    result=[dict(zip(keys_list, [t[i],y[i]])) for i in range(len(t))]
    return JsonResponse({"operation_result": result})

@csrf_exempt
def calcul_bode(request):
    ordre1 = request.POST.get("sourceordre_premier_ordre")
    ordre2 = request.POST.get("sourceordre_second_ordre")
    identification = request.POST.get("sourceordre_identification")
    if ordre1=='true':
        K = request.POST.get("K")
        tau = request.POST.get("tau")
        K=float(K)
        tau=float(tau)
        w0=1/tau
        puissances_w=arange(log10(w0)-3,log10(w0)+3,0.01)
        W=10**puissances_w
        def H(w,tau,K):
            return K/(1+tau*1j*w)
        module = 20*log10(absolute(H(W,tau,K)))
        # La phase en degré
        phase = angle(H(W,tau,K),'deg')
    elif ordre2=='true':
        K = request.POST.get("K")
        w0 = request.POST.get("w0")
        xi = request.POST.get("xi")
        K=float(K)
        xi=float(xi)
        w0=float(w0)
        puissances_w=arange(log10(w0)-3,log10(w0)+3,0.01)
        W=10**puissances_w
        def H(w,w0,xi,K):
            return K/(1+2*xi*1j*w/w0-w**2/w0**2)
            # Le module en dB
        module = 20*log10(absolute(H(W,w0,xi,K)))
        # La phase en degré
        phase = angle(H(W,w0,xi,K),'deg')
    elif identification=='true':
        ordre = const_conv(request.POST.get("def_ordre"))
        K = const_conv(request.POST.get("def_K"))
        xi = const_conv(request.POST.get("def_xi"))
        w0 = const_conv(request.POST.get("def_w0"))
        tau = const_conv(request.POST.get("def_tau"))
        if ordre==1:
            w0=1/tau
            puissances_w=arange(log10(w0)-3,log10(w0)+3,0.01)
            W=10**puissances_w
            def H(w,tau,K):
                return K/(1+tau*1j*w)
            module = 20*log10(absolute(H(W,tau,K)))
            # La phase en degré
            phase = angle(H(W,tau,K),'deg')
        elif ordre==2:
            puissances_w=arange(log10(w0)-3,log10(w0)+3,0.01)
            W=10**puissances_w
            def H(w,w0,xi,K):
                return K/(1+2*xi*1j*w/w0-w**2/w0**2)
                # Le module en dB
            module = 20*log10(absolute(H(W,w0,xi,K)))
            # La phase en degré
            phase = angle(H(W,w0,xi,K),'deg')
    keys_list=['x','y']
    resultmodule=[dict(zip(keys_list, [puissances_w[i],module[i]])) for i in range(len(puissances_w))]
    resultphase=[dict(zip(keys_list, [puissances_w[i],phase[i]])) for i in range(len(puissances_w))]
    return JsonResponse({"module": resultmodule,"phase": resultphase})

@csrf_exempt
def compute(request,id_app):
    if id_app==1:
        return calcul_temporel(request)
    elif id_app==2:
        return calcul_bode(request)

@csrf_exempt
def bode_param():
    tous=['ordre_premier_ordre','ordre_second_ordre','identification']
    sliders=[
        {'name':'K','label':'K (?)','target': '#K','val': [i/10 for i in range(1,101)]+[i/2 for i in range(21,201)],'set': [1],'active_with':tous[0:2]},
        {'name':'xi','label':'xi','target': '#xi','val': [i/20 for i in range(1,21)]+[i/20 for i in range(21,200)],'set': [1],'active_with':['ordre_second_ordre']},
        {'name':'w0','label':'w0 (rad/s)','target': '#w0','val': [5*i for i in range(1,100)], 'set': [50],'active_with':['ordre_second_ordre']},
        {'name':'tau','label':'tau (ms)','target': '#tau','val': [50*i for i in range(1,100)],'set': [50],'active_with':['ordre_premier_ordre']},
    ]
    defaults_param = [{'name':'Ordre','id':'def_ordre','val': (randrange(1,2))},
                      {'name':'K','id':'def_K','val': (randrange(1,100))/10},
                      {'name':'tau','id':'def_tau','val':(randrange(1,100))*10},
                      {'name':'w0','id':'def_w0','val':(randrange(1,100))/10},
                      {'name':'xi','id':'def_xi','val':(randrange(1,100))/10}]
    checkboxes=[
        {'name':'Montrer la réponse','id':'show','active_with':['ordre_identification'],'texte_checked':'Réponse','texte_unchecked':''},
    ]

    radios=[
        {'name':'Ordre','id':'ordre','choices':[{'name':'Premier ordre','id':'premier_ordre'},{'name':'Second ordre','id':'second_ordre'},{'name':'Identification','id':'identification'}]},
    ]
    labels=[
        {'name':'Résultats','id':'resultat','active_with':tous[0:2]},
    ]
    templates=['tracer_bode.html']
    return templates,sliders,radios,checkboxes,labels,defaults_param

@csrf_exempt
def temporel_param():
    tous=['ordre_premier_ordre','ordre_second_ordre','ordre_identification']
    sliders=[
        {'name':'duree','label':'Durée (s)','target': '#duree','val': [i/10 for i in range(50)],'set': [1],'active_with':tous},
        {'name':'K','label':'K (?)','target': '#K','val': [i/10 for i in range(1,101)]+[i/2 for i in range(21,201)],'set': [1],'active_with':tous[0:2]},
        {'name':'xi','label':'xi','target': '#xi','val': [i/20 for i in range(1,21)]+[i/20 for i in range(21,200)],'set': [1],'active_with':['ordre_second_ordre']},
        {'name':'w0','label':'w0 (rad/s)','target': '#w0','val': [5*i for i in range(1,100)], 'set': [50],'active_with':['ordre_second_ordre']},
        {'name':'tau','label':'tau (ms)','target': '#tau','val': [50*i for i in range(1,100)],'set': [50],'active_with':['ordre_premier_ordre']},
    ]
    defaults_param = [{'name':'Ordre','id':'def_ordre','val': (randrange(1,2))},
                      {'name':'K','id':'def_K','val': (randrange(1,100))/10},
                      {'name':'tau','id':'def_tau','val':(randrange(1,100))*10},
                      {'name':'w0','id':'def_w0','val':(randrange(1,100))/10},
                      {'name':'xi','id':'def_xi','val':(randrange(1,100))/10}]
    checkboxes=[
        {'name':'Montrer la réponse','id':'show','active_with':['ordre_identification'],'texte_checked':'Réponse','texte_unchecked':''},
    ]
    radios=[
        {'name':'Ordre','id':'ordre','choices':[{'name':'Premier ordre','id':'premier_ordre'},{'name':'Second ordre','id':'second_ordre'},{'name':'Identification','id':'identification'}]},
    ]
    labels=[
        {'name':'Résultats','id':'resultat','active_with':tous[0:2]},
    ]
    templates=['tracer_temporel.html']
    return templates,sliders,radios,checkboxes,labels,defaults_param

def app(request,id_sequence,id_app):
    if id_app==1:
        templates,sliders,radios,checkboxes,labels,defaults_param=temporel_param()
    elif id_app==2:
        templates,sliders,radios,checkboxes,labels,defaults_param=bode_param()
    return render(request,templates, {'app':id_app,'sliders':sliders,'radios':radios,'checkboxes':checkboxes,'labels':labels,'defaults_param':defaults_param})
