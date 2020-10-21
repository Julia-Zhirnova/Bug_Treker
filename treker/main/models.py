from django.db import models


class Progs(models.Model):
    filename = models.CharField(max_length=200)


class Syntax(models.Model):
    prog = models.ForeignKey(Progs, on_delete=models.CASCADE)
    err_text = models.CharField(max_length=1000)
    score = models.CharField(max_length=200)
    count = models.IntegerField()


class Runtime(models.Model):
    prog = models.ForeignKey(Progs, on_delete=models.CASCADE)
    err_text = models.CharField(max_length=1000)
