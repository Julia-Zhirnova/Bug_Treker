from django.contrib import admin
from .models import Progs, Syntax, Runtime
# Register your models here.

admin.site.register(Progs)
admin.site.register(Syntax)
admin.site.register(Runtime)