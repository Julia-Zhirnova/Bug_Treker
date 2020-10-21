from django.shortcuts import render
from .models import Progs, Syntax, Runtime

def index(request):
    for prog in Progs.objects.all():
        print(prog)

    context = {'prg_names': ['qwe','qwe'],
               'page_flag':'',
               'prg_data':'',
               'dataset':{},
               'status':''}
    return render(request, 'main/index.html', context)

def syntax(request):
    pass

def runtime(request):
    pass