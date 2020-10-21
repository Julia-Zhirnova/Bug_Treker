from django.shortcuts import render
import os
import sys
from .models import Progs, Syntax, Runtime

TESTER_PATH = sys.path.insert(0, '\\'.join(os.getcwd().split('\\')[0:-2]))
import testing_worker


def index(request):
    progs_dir = os.listdir('user_files')
    valid_prg = []
    for prg in progs_dir:
        print(prg)
        if '.py' in prg or 'xlsx' in prg:
            continue
        else:
            valid_prg.append(prg)
    context = {'prg_names': valid_prg,
               'page_flag': '',
               'prg_data': '',
               'dataset': {},
               'status': ''}
    return render(request, 'main/index.html', context)


def syntax(request):
    pass


def runtime(request):
    pass


def prog(request, prg_name):
    test_obj = testing_worker.Tester('erors_file.py')
    test_obj.syntax_test()
    test_obj.runtime_test()
    del test_obj
    # lst=os.path.join(os.getcwd()).split('\\')
    # stri='\\'.join(os.getcwd().split('\\')[0:-1])+'\\testing_worker.py'
    # print(stri)

    progs_dir = os.listdir('user_files')
    valid_prg=[]
    for prg in progs_dir:
        if '.py' in prg or 'xlsx' in prg:
            continue
        else:
            valid_prg.append(prg)
    context = {'prg_names': valid_prg,
               'title': prg_name,
               's_count': 2,
               'r_count': 2}
    return render(request, 'main/prog.html', context)
