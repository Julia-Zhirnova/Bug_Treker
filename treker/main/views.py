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
from .models import Progs, Syntax, Runtime
from django.db import connection


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
    context = {'prg_names': valids_progs(),
               'page_flag': '',
               'prg_data': '',
               'dataset': {},
               'status': ''}
    return render(request, 'main/index.html', context)


def syntax(request, p_name, time):
    cur_prg = Progs.objects.get(filename=p_name)
    p_id = cur_prg.id
    synt = Syntax.objects.get(prog_id=p_id, time=time)
    dataset = synt.get_dict()
    dataset['name'] = p_name
    dataset['time'] = time
    dataset['version'] = synt.version
    context = {'prg_names': valids_progs(),
               'title': p_name,
               'dat': dataset
               }
    return render(request, 'main/syntax.html', context)


def runtime(request, p_name, time):
    cur_prg = Progs.objects.get(filename=p_name)
    p_id = cur_prg.id
    run = Runtime.objects.get(prog_id=p_id, time=time)
    dataset = run.get_dict()
    dataset['name'] = p_name
    dataset['time'] = time
    dataset['version'] = run.version
    context = {'prg_names': valids_progs(),
               'title': p_name,
               'dat': dataset
               }
    return render(request, 'main/runtime.html', context)


@csrf_exempt
def prog(request, prg_name):
    if request.method == 'POST':
        cur_prg = Progs.objects.get(filename=prg_name)
        t = Tester(prg_name + '.py', cur_prg.get_version(), cur_prg.id)
        t.syntax_test()
        t.runtime_test()
        if t.report_items['runtime_errors'] != '':
            cur_prg.status = 'runtime_errors'
        elif t.report_items['runtime_errors'] == '' and int(t.report_items['syntax_count']) >= 2:
            cur_prg.status = 'syntax_errors'
        else:
            cur_prg.status = 'passed'
        cur_prg.save()
        del t
        return HttpResponseRedirect(f'''/prog/{prg_name.replace('.py', '')}''')
    else:
        cur_prg = Progs.objects.get(filename=prg_name)
        p_id = cur_prg.id
        status = cur_prg.get_status()
        version = cur_prg.get_version()
        color_dict = {'not_runned': 'darkgray', 'syntax_errors': 'yellow', 'passed': 'green', 'runtime_errors': 'red'}
        synt = Syntax.objects.filter(prog_id=p_id)
        dataset = []
        for s in synt:
            up_data = s.get_dict()
            r = Runtime.objects.get(time=s.time)
            for key, value in r.get_dict().items():
                up_data[key] = value
            up_data['time'] = s.time
            dataset.append(up_data)
        context = {'prg_names': valids_progs(),
                   'title': prg_name,
                   'status': status.replace('_', ' '),
                   'status_colour': color_dict[status],
                   'version': version,
                   'dataset': dataset
                   }
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
                os.remove(os.path.join(os.getcwd(), 'main', 'user_files', f_name.replace('.py', ''), f_name))
                prg = Progs.objects.get(filename=f_name.replace('.py', ''))
                prg.version += 1
                prg.save()
                f = request.FILES['file']
                write_file(f)
            else:
                os.mkdir(os.path.join(os.getcwd(), 'main', 'user_files', f_name.replace('.py', '')))
                f = request.FILES['file']
                write_file(f)
                new_p = Progs()
                new_p.filename = f_name.replace('.py', '')
                new_p.status = 'not_runned'
                new_p.save_base()
            # new_p.save()
            # with connection.cursor() as cursor:
            # cursor.execute("INSERT INTO main_progs VALUES (%s), (%s)",[f_name.replace('.py', ''),'no_runned'])
            return HttpResponseRedirect(f'''/prog/{f_name.replace('.py', '')}''')
    else:
        form = UploadFileForm()
        context = {'prg_names': valids_progs(),
                   'form': form
                   }
        return render(request, 'main/upload.html', context)


def download_file(request):
    can_download = []
    for i in valids_progs():
        for file in os.listdir(os.path.join(os.getcwd(), 'main', 'user_files', i)):
            if '.xlsx' in file:
                can_download.append(i)
    context = {'prg_names': valids_progs(),
               'can_download': can_download
               }
    return render(request, 'main/download.html', context=context)


def file_send(request, p_name):
    img = open(os.path.join(os.getcwd(), 'main', 'user_files', p_name, 'Report_' + p_name + '.xlsx'), 'rb')
    response = FileResponse(img)
    return response


def how_use(request):
    context = {'prg_names': valids_progs(),
               }
    return render(request, 'main/how_use.html', context)
