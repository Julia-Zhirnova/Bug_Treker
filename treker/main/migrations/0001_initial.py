# Generated by Django 3.1.2 on 2020-10-21 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Progs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Syntax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('err_text', models.CharField(max_length=1000)),
                ('score', models.CharField(max_length=200)),
                ('count', models.IntegerField()),
                ('prog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.progs')),
            ],
        ),
        migrations.CreateModel(
            name='Runtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('err_text', models.CharField(max_length=1000)),
                ('prog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.progs')),
            ],
        ),
    ]
