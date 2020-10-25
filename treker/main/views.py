import os
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .testing_worker import Tester
from .form import UploadFileForm
from django.views.decorators.csrf import csrf_exempt
from django.core.files import File
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import FileResponse
from .models import Progs


def valids_progs():
    progs_dir = os.listdir(os.path.join(os.getcwd(), 'main', 'user_files'))
    valid_prg = []
    for prg in progs_dir:
        if '.py' in prg or 'xlsx' in prg:
            continue
        else:
            valid_prg.append(prg)
    return valid_prg


def index(request):
    prg = Progs(filename='erors_file', status='no_run')
    prg.save()
    print(Progs.objects.all())
    context = {'prg_names': valids_progs(),
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
    t = Tester(prg_name + '.py')
    t.syntax_test()
    t.runtime_test()
    print(t.report_items)
    del t

    context = {'prg_names': valids_progs(),
               'title': prg_name,
               'report': []}
    return render(request, 'main/prog.html', context)


@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            f_name = request.FILES['file'].name

            def write_file(f):
                # with open(os.path.join(os.getcwd(), 'main', 'user_files', f_name.replace('.py', ''), f_name
                #                        ), 'wb') as destination:
                #     destination.write(f.read())
                path = default_storage.save(
                    os.path.join(os.getcwd(), 'main', 'user_files', f_name.replace('.py', ''), f_name
                                 ), ContentFile(f.read()))

            if f_name.replace('.py', '') in os.listdir(os.path.join(os.getcwd(), 'main', 'user_files')):
                f = request.FILES['file']
                write_file(f)
            else:
                os.mkdir(os.path.join(os.getcwd(), 'main', 'user_files', f_name.replace('.py', '')))
                f = request.FILES['file']
                write_file(f)
            return HttpResponseRedirect(f'''/prog/{f_name.replace('.py', '')}''')
    else:
        form = UploadFileForm()
        context = {'prg_names': valids_progs(),
                   'form': form
                   }
        return render(request, 'main/upload.html', context)


def download_file(request):
    context = {'prg_names': valids_progs(),
               }
    return render(request, 'main/download.html', context=context)


def file_send(request, p_name):
    img = open(os.path.join(os.getcwd(), 'main', 'user_files', p_name, 'Report_' + p_name + '.xlsx'), 'rb')
    response = FileResponse(img)
    return response
