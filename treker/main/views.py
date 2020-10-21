from django.shortcuts import render

def index(request):
    context = {'prg_names': [1,2,3,4,4],
               'page_flag':'',
               'prg_data':'',
               'dataset':{},
               'status':''}
    return render(request, 'main/index.html', context)

def app(request):
    pass