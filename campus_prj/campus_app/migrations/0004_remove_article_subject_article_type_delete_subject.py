# Generated by Django 5.0 on 2024-01-01 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_app', '0003_subject_article_subject'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='subject',
        ),
        migrations.AddField(
            model_name='article',
            name='type',
            field=models.CharField(choices=[('laba', 'Лабораторна робота'), ('kursova', 'Курсова робота'), ('bach_diplom', 'Бакалаврська робота'), ('mag_diplom', 'Магістерська робота')], default='laba', max_length=64),
        ),
        migrations.DeleteModel(
            name='Subject',
        ),
    ]
