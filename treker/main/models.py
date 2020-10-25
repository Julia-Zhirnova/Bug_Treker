from django.db import models


class Progs(models.Model):
    filename = models.CharField(max_length=200)
    status = models.CharField(max_length=200)

    def __str__(self):
        return self.filename


class Syntax(models.Model):
    prog = models.ForeignKey(Progs, on_delete=models.CASCADE)
    err_text = models.CharField(max_length=1000)
    score = models.CharField(max_length=200)
    count = models.IntegerField()

    def __str__(self):
        return self.prog, self.err_text


class Runtime(models.Model):
    prog = models.ForeignKey(Progs, on_delete=models.CASCADE)
    err_text = models.CharField(max_length=1000)
